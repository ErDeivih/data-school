---
id: duckdb-y-analitica-local
titulo: DuckDB y analítica local
fase: 4
nivel: intermedio
rutas: [de, ds]
prerequisitos: [pandas-fundamentos, sql-agregaciones-y-group-by, parquet-avro-orc]
tags: [duckdb, parquet, sql, olap, analitica]
resumen: Un motor SQL analítico dentro de tu propio proceso: consulta Parquet y CSV de varios gigabytes sin servidor, sin clúster y sin cargarlo todo en memoria.
fuentes: ["Raasveldt & Muehleisen (2019), 'DuckDB: an Embeddable Analytical Database'", "DuckDB documentation, 'Why DuckDB'"]
---

## En una frase

DuckDB es un motor de SQL analítico que se ejecuta dentro de tu propio programa: lee los ficheros
Parquet o CSV que ya tienes en disco, no necesita servidor ni clúster y responde agregaciones
sobre millones de filas usando solo la memoria que le hace falta.

## La idea

SQLite es a las aplicaciones transaccionales lo que DuckDB es al análisis: un motor embebido, sin
servidor, que vive dentro de tu proceso y guarda su estado en un fichero. La diferencia es el
trabajo para el que está construido: SQLite está pensado para leer y escribir filas sueltas con
muchas conexiones a la vez; DuckDB, para leer columnas enteras y agregarlas.

El problema concreto que resuelve aparece el primer día que trabajas con datos de verdad. Tienes
40 ficheros Parquet en un disco externo con 300 millones de filas y quieres el total de ventas
por provincia del último trimestre. Tus opciones, sin DuckDB:

- **pandas:** habría que leerlo todo en memoria. No cabe, y aunque cupiera tardaría.
- **Spark:** montas un clúster, esperas a que arranque y pagas por veinte segundos de consulta.
- **Una base de datos:** importas los datos primero, lo que significa copiar cientos de gigabytes
  para hacer una pregunta.

Con DuckDB es una consulta SQL sobre los ficheros, sin importar nada. El motor lee por bloques,
toca solo las columnas que nombras y aprovecha las estadísticas que Parquet ya guarda por bloque
para saltarse los que no contienen las fechas que pides.

¿Por qué va rápido sin trucos?

1. **Columnar.** Solo lee las columnas que aparecen en el `SELECT`. De un Parquet con 40 columnas
   del que usas 3, se lee una fracción pequeña del fichero.
2. **Vectorizado.** Ejecuta cada operación sobre lotes de valores (unos 2.048 por defecto) en vez
   de ir fila a fila, lo que permite aprovechar las instrucciones SIMD del procesador.
3. **Pushdown.** El filtro del `WHERE` se aplica durante la lectura, no después. Y un grupo de
   filas cuyas estadísticas de mínimo y máximo no cumplen el filtro ni se descomprime.
4. **Trabaja con datos mayores que la memoria.** Si una operación no cabe, escribe temporalmente
   a disco en vez de morir con un error de memoria.
5. **Sin copias con Arrow.** Puede consultar un `DataFrame` de pandas o un `Table` de Polars sin
   serializar ni duplicar nada ([[arrow-y-formatos-columnares]]).

Y hay un caso en el que no debes usarlo. DuckDB escribe su base de datos en un único fichero y
admite un solo proceso escritor: no es un motor para servir la aplicación de la empresa con
cientos de usuarios escribiendo a la vez. Eso es un sistema transaccional ([[oltp-vs-olap]]).

## Definición formal

No hay una fórmula única, pero conviene fijar el vocabulario, porque explica por qué unas
consultas vuelan y otras no:

- **Grupo de filas (row group):** bloque de un fichero Parquet —típicamente de 128 MB— que lleva
  estadísticas por columna: valor mínimo, valor máximo y número de nulos. Es la unidad mínima que
  el motor puede saltarse entera.
- **Pushdown de proyección:** leer del disco únicamente las columnas que la consulta nombra.
- **Pushdown de predicado:** aplicar el `WHERE` durante la lectura y descartar los grupos de
  filas que las estadísticas permiten excluir.
- **Vectorización:** ejecutar cada operador sobre lotes de `V` valores en vez de sobre una fila.
  `V` es el tamaño de lote, 2.048 por defecto en DuckDB.

El coste de una consulta se aproxima por los bytes que hay que mover:

:::formula
Bytes leídos ≈ filas examinadas × Σ (anchura de cada columna usada)
:::

donde `filas examinadas` son las que el motor no ha podido descartar antes de leerlas y `Σ`
recorre las columnas que la consulta necesita. La proporción que sobrevive al filtro se llama
**selectividad**:

:::formula
selectividad = filas devueltas / filas totales
:::

Una selectividad de 0,01 significa que el filtro deja el 1 % de las filas. Cuanto menor sea, más
importa el pushdown: si el motor puede saltarse grupos de filas, `filas examinadas` baja y con
ella los bytes leídos. Un índice en una base transaccional y un grupo de filas en Parquet
persiguen lo mismo: reducir `filas examinadas`.

## Ejemplo

Un fichero `ventas.parquet` con **4.000.000 de filas** y 9 columnas (5 numéricas de 8 bytes y 4 de
texto), comprimido con Zstd: unos 310 MB en disco. Está ordenado por fecha y tiene 40 grupos de
filas de 100.000 filas cada uno.

La consulta:

```text
SELECT region, SUM(importe)
FROM 'ventas.parquet'
WHERE fecha >= DATE '2024-03-01'
GROUP BY region
```

- Columnas que usa la consulta: 3 de 9 (`fecha`, `region`, `importe`).
- Si hubiera que materializar las 9 columnas como números de 8 bytes:
  4.000.000 × 9 × 8 = **288 MB**.
- Solo con las 3 columnas: 4.000.000 × 3 × 8 = **96 MB**, y eso antes del filtro.
- El filtro deja el 2,3 % de las filas: 92.000. Con 3 columnas: 92.000 × 3 × 8 = **2,2 MB**.
- Y como las filas están ordenadas por fecha, los meses pedidos viven en 1 o 2 de los 40 grupos:
  el resto de grupos ni se descomprime.

La diferencia entre 288 MB y un par de megabytes es toda la razón de ser de DuckDB. No es «SQL
dentro de Python»: es **leer menos**.

## Código

```python verificable
import duckdb
import pandas as pd

ventas = pd.DataFrame({
    "region": ["norte", "sur", "norte", "sur", "norte"],
    "fecha": pd.to_datetime(["2024-03-01", "2024-03-05", "2024-04-02",
                             "2024-04-02", "2024-05-03"]),
    "importe": [120.0, 80.0, 200.0, 50.0, 30.0],
})

con = duckdb.connect()          # en memoria: ni servidor ni fichero
con.register("ventas", ventas)  # consulta el DataFrame sin copiarlo

filas = con.sql("""
    SELECT region, SUM(importe) AS total
    FROM ventas
    WHERE fecha >= DATE '2024-04-01'
    GROUP BY region
    ORDER BY total DESC
""").fetchall()

print("grupos devueltos:", len(filas))       # -> grupos devueltos: 2
print("primera region:", filas[0][0])        # -> primera region: norte
print("total de la primera:", filas[0][1])   # -> total de la primera: 230.0
print("total de la segunda:", filas[1][1])   # -> total de la segunda: 50.0
```

```sql verificable
-- Analitica local: SQL con funciones de ventana sobre datos que crea el propio bloque.
CREATE TABLE pedidos AS
SELECT * FROM (VALUES
    ('2024-01-05', 'ana',  120.0),
    ('2024-01-19', 'ana',   80.0),
    ('2024-02-15', 'ana',   40.0),
    ('2024-02-02', 'luis', 200.0),
    ('2024-03-01', 'luis', 100.0)
) AS t(fecha, cliente, importe);

SELECT cliente,
       fecha,
       importe,
       SUM(importe) OVER (PARTITION BY cliente ORDER BY fecha) AS acumulado
FROM pedidos
ORDER BY cliente, fecha;
```

La consulta devuelve cinco filas. Para `ana`, el acumulado va 120.0, 200.0 y 240.0; para `luis`,
200.0 y 300.0.

```text
# Leer Parquet directamente desde la consola, sin importar nada a una base de datos
duckdb -c "SELECT region, count(*) FROM 'datos/ventas/*.parquet' GROUP BY region ORDER BY 2 DESC"
```

## Errores típicos

- **Usar DuckDB como base de datos de la aplicación.** Tiene un solo escritor por fichero, no
  gestiona usuarios ni conexiones concurrentes y no está pensado para eso. Si tu web necesita
  escribir filas mientras otros leen, necesitas un motor transaccional.
- **Importar los Parquet antes de consultarlos.** Si vas a leer el dato y no a modificarlo,
  `CREATE TABLE AS SELECT * FROM 'x.parquet'` solo consigue duplicar el disco y perder el
  pushdown. Consulta los ficheros directamente.
- **Volver a pandas en cuanto sale el resultado.** El patrón correcto es hacer la agregación,
  las uniones y los filtros en SQL y traer a pandas únicamente la tabla pequeña que vas a
  dibujar. Si traes 300 millones de filas para agruparlas en pandas, has tirado la ventaja.
- **Dejar los datos en CSV «porque es lo que hay».** Sobre CSV no hay columnas ni estadísticas:
  leer una columna obliga a recorrer todo el fichero. Convertir una vez a Parquet cambia el
  orden de magnitud de las consultas siguientes ([[compresion-y-codificacion]]).
- **Suponer que «sin servidor» significa «sin límites».** Una unión sin filtros sobre cientos de
  gigabytes puede llenar el disco temporal. Vigila dónde escribe DuckDB sus ficheros temporales
  cuando trabajas con volúmenes grandes.
- **Esperar milagros con un Parquet mal ordenado.** El pushdown por estadísticas solo descarta
  grupos de filas si la columna del filtro está correlacionada con el orden físico del fichero.
  Si las fechas están repartidas al azar, se leen todos los grupos ([[particionado-y-clustering]]).

## Comprueba que lo sabes

:::quiz
p: Un Parquet tiene 40 columnas y tu consulta usa 3. ¿Qué hace DuckDB?
o: Lee las 40 columnas y descarta 37 al final
o: Lee del disco solo las 3 columnas que nombra la consulta
o: Convierte el fichero a CSV antes de consultarlo
a: 2
e: Es el pushdown de proyección: en un formato columnar cada columna se guarda por separado, así que se puede leer solo lo que hace falta. Leer las 40 y descartar después es lo que ocurre en un formato orientado a fila como CSV, y es justo lo que DuckDB evita.
:::

:::quiz
p: ¿Por qué DuckDB puede responder una consulta sobre un fichero mayor que la memoria disponible?
o: Porque comprime los datos en memoria
o: Porque procesa por bloques y puede derramar a disco lo que no cabe, en lugar de cargarlo todo
o: Porque usa la tarjeta gráfica
a: 2
e: El motor nunca necesita el conjunto completo en memoria: lee por bloques, agrega lo que puede y escribe a disco los estados intermedios que no caben. Comprimir en memoria ayuda pero no cambia el orden de magnitud, y DuckDB no usa la GPU.
:::

:::aviso
DuckDB guarda su base de datos en un único fichero y admite un solo proceso escritor. Si varias
personas tienen que consultar a la vez, deja los datos en Parquet y abre conexiones de solo
lectura. Si además necesitas escritura concurrente, gobierno y usuarios, eso ya es un almacén con
servidor ([[data-warehouse]]).
:::
