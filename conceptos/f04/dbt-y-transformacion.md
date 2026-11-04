---
id: dbt-y-transformacion
titulo: dbt y transformación
fase: 4
nivel: intermedio
rutas: [de]
prerequisitos: [sql-select-y-filtros, sql-joins, sql-subconsultas-y-cte, etl-vs-elt]
tags: [sql, transformacion, linaje, testing]
resumen: dbt convierte tus consultas SQL en un proyecto con dependencias, materializaciones, pruebas y documentación; el grafo lo deduce él a partir de ref().
fuentes: ["Reis & Housley (2022), 'Fundamentals of Data Engineering'", "Kimball & Ross (2013), 'The Data Warehouse Toolkit'"]
---

## En una frase

dbt es una herramienta que coge tus consultas `SELECT`, las versiona en Git, deduce el orden en
que hay que ejecutarlas a partir de las referencias entre ellas, las materializa como vistas o
tablas según le digas y ejecuta pruebas sobre el resultado.

## La idea

Antes de dbt, la transformación de un almacén solía ser un cajón de scripts: `carga_diaria.sql`,
`carga_diaria_v2.sql`, `carga_diaria_v2_bueno.sql`. El orden de ejecución vivía en la cabeza de
una persona y en un documento que nadie actualizaba. Cuando esa persona se iba de vacaciones, el
pipeline se paraba.

dbt pone tres cosas encima de SQL normal, sin cambiar el motor (el que ejecuta sigue siendo tu
almacén: [[duckdb-y-analitica-local|DuckDB]], Postgres, Snowflake, BigQuery, Spark):

1. **Un grafo de dependencias explícito.** En lugar de escribir el nombre de la tabla, escribes
   `{{ ref('stg_pedidos') }}`. dbt lee todas las referencias, construye un DAG y calcula el
   orden. Ese mismo grafo es el [[catalogo-y-linaje|linaje]] y no hay que documentarlo aparte.
2. **Materializaciones.** El mismo `SELECT` se puede publicar de cuatro maneras distintas, y
   elegir bien es la mitad del rendimiento:
   - `view`: no se guarda nada, se recalcula en cada consulta. Barato de escribir, caro de leer.
   - `table`: se reconstruye entera en cada ejecución. Caro de escribir, barato de leer.
   - `incremental`: sólo procesa las filas nuevas y las fusiona con lo que ya había. Es la
     opción para tablas de hechos grandes.
   - `ephemeral`: no se materializa; se inyecta como CTE en los modelos que lo usan.
3. **Pruebas y documentación como código.** Los tests (`not_null`, `unique`,
   `accepted_values`, `relationships`) se declaran en YAML junto al modelo y se ejecutan en el
   mismo pipeline y en integración continua.

La convención que hace que un proyecto de dbt se entienda es separar capas. `stg_` para
limpiar y castear (una vista por tabla de origen, sin lógica de negocio). `int_` para los pasos
intermedios. `fact_` y `dim_` para lo que consume el negocio, siguiendo
[[modelado-dimensional|el modelado dimensional]]. Si mezclas las tres capas en un solo modelo,
el grafo se vuelve inmanejable en cuanto hay veinte modelos.

:::nota
dbt no ejecuta SQL mágico: **compila** plantillas Jinja a SQL y luego lo lanza. Casi todo lo que
hace un modelo se puede escribir a mano en SQL; lo que aporta dbt es el orden, la reutilización,
las pruebas y el linaje, no una capacidad nueva del motor.
:::

## Definición formal

Un proyecto de dbt es un grafo dirigido acíclico `G = (V, E)` donde:

- `V` — los modelos. Cada modelo `m` es una consulta `SELECT` con un nombre y una
  materialización `mat(m) ∈ {view, table, incremental, ephemeral}`.
- `E` — las aristas. Hay una arista `u → v` si el modelo `v` contiene `ref('u')`. dbt garantiza
  que `G` no tiene ciclos; si detecta uno, falla la compilación. Un linaje con ciclos es
  siempre un error.

El orden de ejecución es una ordenación topológica de `G`. Y la propiedad que hace que el
conjunto sea útil:

:::formula
si u → v entonces v se ejecuta después de u
:::

En un modelo `incremental`, la condición que decide qué filas se procesan es:

:::formula
filas nuevas = origen donde marca_tiempo > max(marca_tiempo) ya presente en el destino
:::

Símbolos:

- `marca_tiempo` — la columna que ordena los datos (fecha del evento, `updated_at` del origen).
- `max(...)` — el máximo ya materializado en el destino; en dbt se consulta con
  `{% if is_incremental() %}`, que es verdadero sólo cuando la tabla ya existe y no se ha pedido
  un `--full-refresh`.
- `unique_key` — la clave por la que se fusiona. Si falta y hay filas repetidas, el incremental
  **duplica** en cada ejecución, que es el fallo clásico de esta materialización.

## Ejemplo

Una tabla de origen con 500 días de historia y 12.000 pedidos por día: 6.000.000 de filas en
total.

- Con materialización `table`, cada ejecución diaria lee y agrega las 6.000.000 de filas para
  producir el mismo resultado más un día. Procesa 500 veces más de lo necesario.
- Con `incremental` y corte por `fecha`, cada ejecución lee los 12.000 pedidos del día anterior y
  fusiona por `fecha`. La proporción de trabajo entre los dos enfoques es 500 a 1.
- El precio de `incremental` es que el modelo deja de ser una función pura del origen: si el
  origen **corrige** un pedido de hace tres semanas, el incremental no lo ve. Para eso existe el
  reproceso de una partición concreta ([[backfill-y-reproceso]]) o un `--full-refresh` puntual.

Y los dos tests que evitan la mayoría de los incidentes, declarados en el `schema.yml` del
modelo: `unique` y `not_null` sobre la columna que define el grano (`fecha` en una tabla diaria,
`pedido_id` en una tabla de detalle). Un cambio de granularidad sin avisar rompe a los
consumidores de una forma que ningún test de esquema detecta.

## Código

```sql ilustrativo
-- models/marts/fact_ventas_diarias.sql  (dbt; las llaves dobles son Jinja, no SQL)
{{ config(materialized='incremental', unique_key='fecha', on_schema_change='append_new_columns') }}

select
    fecha,
    count(*)            as pedidos,
    sum(importe)        as total
from {{ ref('int_pedidos') }}
{% if is_incremental() %}
where fecha >= (select max(fecha) from {{ this }}) - interval '3 days'
{% endif %}
group by fecha
```

```yaml
# models/marts/schema.yml — las pruebas viajan con el modelo, en el mismo repositorio
models:
  - name: fact_ventas_diarias
    description: Ventas agregadas por dia. Grano: una fila por fecha.
    columns:
      - name: fecha
        description: Dia natural en UTC, no la fecha de carga.
        tests:
          - unique
          - not_null
      - name: total
        tests:
          - not_null
```

```sql verificable
-- El mismo incremental, en SQL puro, para ver por que es idempotente.
CREATE TABLE raw_pedidos AS
SELECT * FROM (VALUES
    (DATE '2024-03-01', 'P1', 100.0, 'ok'),
    (DATE '2024-03-01', 'P2', 250.0, 'cancelado'),
    (DATE '2024-03-02', 'P3', 80.0,  'ok'),
    (DATE '2024-03-02', 'P4', 120.0, 'ok')
) AS t(fecha, pedido_id, importe, estado);

-- Primera ejecucion: la tabla entera (equivale a un --full-refresh)
CREATE TABLE fact_ventas_diarias AS
SELECT fecha, sum(importe) AS total, count(*) AS pedidos
FROM raw_pedidos WHERE estado = 'ok' GROUP BY fecha;

-- Siguiente ejecucion: solo la particion nueva, reconstruida y reemplazada
CREATE OR REPLACE TABLE nuevo AS
SELECT fecha, sum(importe) AS total, count(*) AS pedidos
FROM raw_pedidos WHERE estado = 'ok' AND fecha = DATE '2024-03-02' GROUP BY fecha;

DELETE FROM fact_ventas_diarias WHERE fecha IN (SELECT fecha FROM nuevo);
INSERT INTO fact_ventas_diarias SELECT * FROM nuevo;

SELECT * FROM fact_ventas_diarias ORDER BY fecha;
```

```text
fecha | total | pedidos
2024-03-01 | 100.0 | 1
2024-03-02 | 200.0 | 2
```

## Errores típicos

- **Poner `incremental` sin `unique_key` ni filtro de corte.** Si el `SELECT` no tiene un `where`
  que dependa de `is_incremental()`, el modelo reprocesa todo cada día y encima va acumulando
  duplicados porque no sabe qué reemplazar.
- **Elegir `view` o `table` por costumbre.** Una vista sobre una tabla de 2.000 millones de filas
  que se consulta 300 veces al día es peor que una tabla. Y una tabla que se reconstruye entera
  cada hora para algo que se consulta dos veces al día es peor que una vista. La decisión es
  cuestión de cuántas lecturas frente a cuántas escrituras.
- **Meter lógica de negocio en el `staging`.** El staging renombra, castea, filtra registros
  técnicos y normaliza. Si ahí decides qué es un cliente activo, esa regla acabará duplicada en
  tres modelos con tres definiciones ligeramente distintas.
- **Confiar en `dbt run`.** `dbt run` no ejecuta las pruebas; `dbt build` construye los modelos y
  ejecuta los tests en orden de dependencias, y detiene el grafo cuando un test falla. Si tus
  tests sólo corren en la máquina de alguien, no existen.
- **Cambiar el grano de un modelo sin avisar.** Un consumidor que hacía `sum(total)` sobre una
  tabla diaria suma el doble si el modelo pasa a ser por pedido. Cambiar el grano es un cambio
  incompatible: va con [[contratos-de-datos|contrato]] y con aviso.
- **Documentar en una herramienta aparte.** Si la descripción del modelo no vive junto al SQL, se
  queda obsoleta. La documentación que se genera del propio proyecto es la única que se mantiene.

## Comprueba que lo sabes

:::quiz
p: ¿Qué aporta `{{ ref('stg_pedidos') }}` frente a escribir el nombre de la tabla a mano?
o: Ejecuta la consulta más rápido porque reutiliza la caché
o: Declara una dependencia que dbt usa para ordenar la ejecución y para construir el linaje
o: Comprueba que la tabla existe antes de consultarla
a: 2
e: `ref()` es la arista del grafo: dbt compila el proyecto, ve quién depende de quién y ordena las ejecuciones. Además, ese mismo grafo es el linaje que se consulta después para saber el impacto de un cambio. No cambia el rendimiento ni valida datos: sólo declara la dependencia.
:::

:::quiz
p: Un modelo `incremental` lleva seis meses funcionando y hoy el origen corrige un pedido de hace tres semanas. ¿Qué pasa?
o: El incremental lo detecta solo porque compara con el origen
o: El pedido corregido no entra: el filtro de corte sólo mira las filas posteriores al máximo ya cargado
o: La ejecución falla con un error de clave duplicada
a: 2
e: Por construcción, el incremental sólo lee lo que es más nuevo que el máximo del destino. Una corrección retroactiva queda fuera. Se arregla con un rango de solape de unos días en el filtro, con un reproceso de esa partición o con un `--full-refresh` puntual.
:::

:::truco
Empieza todos los modelos nuevos como `view`, y cámbialos a `table` o `incremental` cuando tengas
una queja de rendimiento concreta. Al revés —empezar por `incremental`— te obliga a razonar sobre
claves y filtros de corte antes de saber siquiera si el modelo sirve.
:::
