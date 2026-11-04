# Leer el código de los proyectos: qué pasa paso a paso

**Fecha:** 2026-11-02 · Para aprender leyendo código terminado, no solo escribiéndolo.

Los dos proyectos están en `proyectos/`. Cada uno se lee en el mismo orden: primero el README,
después el script de ingesta, después el de modelo, y al final el verificador.

---

## 1. PF-01 · El pulso de dos economías

### Paso 1 · `ingerir.py` (¿qué hace?)

1. Define países, años e indicadores como constantes. **Todo lo que cambia está arriba**, no
   enterrado en el código.
2. `descargar()` pide la URL con `urllib`, reintenta con espera creciente y devuelve bytes.
   Fíjate en que no usa `pip install requests`: menos dependencias, menos problemas.
3. Guarda el bruto en `data/raw/<indicador>-<fecha>.json` **antes** de transformar. Ese fichero es
   la prueba de lo que dijo la API ese día.
4. Recorre `datos[1]`, que es la lista de registros de la API, y construye filas largas
   (indicador, país, año, valor).
5. Ordena y escribe `data/poblacion.csv`.

**Lo que hay que mirar:** por qué el bruto se guarda con la fecha en el nombre y por qué la tabla
es larga y no ancha.

### Paso 2 · `modelar.py` (¿qué construye?)

1. Lee cada `.sql` de `models/`.
2. Sustituye `{{ ref('stg_poblacion') }}` por el nombre de la tabla. Eso es lo único que hace dbt
   por debajo con las referencias.
3. Crea las tablas en DuckDB: `stg_poblacion` (limpieza), `dim_pais` (dimensión) y `f_poblacion`
   (hecho).
4. Ejecuta **siete pruebas**: filas esperadas, nulos, unicidad de la dimensión, integridad
   referencial, unicidad del hecho, años cubiertos.

**Lo que hay que mirar:** la diferencia entre `staging` (limpiar) y `marts` (modelar). Y que las
pruebas están en el modelo, no en un script aparte.

### Paso 3 · `panel.py` (¿cómo se sirve?)

1. Abre el almacén en solo lectura.
2. Dos consultas con `case when anio = 2000` para pivotar sin salir de SQL.
3. Genera SVG a mano: una barra por valor, ancho proporcional al máximo.
4. Escribe un HTML autocontenido.

**Lo que hay que mirar:** el panel no necesita servidor ni librería; y el pie dice qué no se puede
concluir con dos indicadores.

### Paso 4 · `orquestar.py` (¿qué le falta a un script para ser un pipeline?)

1. Lista los pasos en orden.
2. Ejecuta cada uno con `subprocess`, comprueba el resultado y **reintenta** una vez.
3. Escribe un log con hora y motivo del fallo.
4. Devuelve código de salida distinto de cero si algo falla.

**Lo que hay que mirar:** el contrato es el mismo que el de Airflow o Dagster (orden, reintento,
log, fallo ruidoso). La diferencia con ellos es la interfaz, no la idea.

---

## 2. P17 · OpenF1

### Paso 1 · `ingerir.py`

1. Pide `sessions?year=2024&session_name=Race` y se queda con tres.
2. Por cada sesión pide `drivers` y `laps`, y guarda los tres brutos.
3. Convierte cada vuelta en una fila con clave `(sesión, piloto, vuelta)`.
4. **Deduplica por esa clave** antes de escribir: ahí está la idempotencia.
5. Escribe `data/vueltas.csv`.

**Lo que hay que mirar:** qué pasa si la API devuelve una vuelta repetida y por qué la clave no es
solo el número de vuelta.

### Paso 2 · `degradacion.py` (el paso que enseña de verdad)

1. Lee las vueltas y se queda con las que tienen duración.
2. Por sesión pide `stints` (tramos entre paradas) y guarda el bruto.
3. Para cada stint filtra las vueltas del piloto entre `lap_start` y `lap_end`.
4. Calcula la mediana y la pendiente por mínimos cuadrados.
5. Escribe `degradacion.csv`.

**El hallazgo:** las pendientes salen **negativas** (las vueltas mejoran). No es un error: el coche
se aligera de combustible más rápido de lo que el neumático se degrada. Para aislar la degradación
hay que corregir por combustible o comparar la misma vuelta de stint entre pilotos. Ese detalle es
exactamente lo que separa un análisis de un gráfico.

---

## 3. El vocabulario de empresa, con su página

| Término | Página |
| --- | --- |
| dbt | `dbt-y-transformacion` |
| DuckDB | `duckdb-y-analitica-local` |
| Parquet, Avro, ORC | `parquet-avro-orc` |
| Data warehouse | `data-warehouse` |
| Data lake | `data-lake` |
| Lakehouse y formatos de tabla | `lakehouse-y-table-formats` |
| Arquitectura medallion (bronze, silver, gold) | `arquitectura-medallion` |
| ETL frente a ELT | `etl-vs-elt` |
| OLTP frente a OLAP | `oltp-vs-olap` |
| Modelado dimensional y esquema estrella | `modelado-dimensional`, `esquema-estrella-y-copo` |
| Capa semántica y métricas | `capa-semantica-y-metricas` |
| Catálogo y linaje | `catalogo-y-linaje` |
| Orquestación y DAG | `orquestacion-y-dag` |
| Spark | `spark-fundamentos` |
| Kafka | `kafka-y-colas` |
| Flink | `flink-y-procesamiento-de-eventos` |
| Data mart | dentro de `modelado-dimensional`: es un subconjunto del almacén para un área |
| Iceberg y Delta | dentro de `lakehouse-y-table-formats` |
| Bronze, silver, gold | dentro de `arquitectura-medallion` |

Los tres últimos no tienen página propia a propósito: son un matiz de otra página y una página de
un párrafo no enseña nada.

---

## 4. Cómo leer un proyecto que no es tuyo (método de 20 minutos)

1. Lee el README y escribe en una línea qué problema resuelve.
2. Mira la estructura de carpetas: si no se entiende, el proyecto está mal organizado.
3. Abre el fichero de ingesta y busca dónde guarda el bruto.
4. Abre el de modelo y busca las claves y el grano.
5. Abre el verificador: **es lo que más enseña**, porque dice qué puede fallar.
6. Ejecútalo. Si no corre, el README miente y eso también es una lección.
