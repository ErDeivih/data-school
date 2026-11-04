---
id: arrow-y-formatos-columnares
titulo: Arrow y formatos columnares
fase: 3
nivel: intermedio
rutas: [de, ds]
prerequisitos: [numpy-fundamentos, pandas-fundamentos]
tags: [arrow, parquet, memoria, interoperabilidad]
resumen: Guardar los datos por columnas y no por filas: menos bytes leídos, mejor compresión y una misma representación en memoria que los motores comparten sin copiar.
fuentes: ["Kleppmann (2017), 'Designing Data-Intensive Applications'", "Reis y Housley (2022), 'Fundamentals of Data Engineering'"]
---

## En una frase

Un formato columnar guarda juntos los valores de cada columna en vez de guardar cada fila
completa, y Arrow es la especificación de esa memoria para que Pandas, Polars y DuckDB lean los
mismos bytes sin convertir ni copiar nada.

## La idea

Piensa en un almacén. En la primera organización, cada pedido está en una caja con su fecha, su
cliente, su importe y su ciudad: para calcular el importe total del mes hay que abrir todas las
cajas y sacar un papel de cada una. En la segunda, hay un cajón con todas las fechas, otro con
todos los clientes y otro con todos los importes: para el total, abres un cajón.

Eso es todo el concepto, y explica las dos ventajas:

1. **Lees menos.** Un análisis típico usa 3 de 40 columnas. En un formato por filas hay que
   recorrer los 40 campos de cada registro para descartarlos; en uno por columnas se leen
   exactamente los 3 bloques que necesitas.
2. **Comprime mejor.** La compresión funciona encontrando repeticiones en valores contiguos. Si
   en un bloque están todos los países, aparecen muchas veces `ES` seguido, y basta con guardar
   «ES repetido 4.000 veces» o un diccionario de dos entradas con códigos de 1 byte.

Arrow añade la segunda mitad de la historia: **la misma disposición en memoria**. Sin una
especificación común, cada herramienta guarda los datos como quiere y pasar de una a otra exige
serializar y volver a parsear (el clásico «convertir a Pandas, procesar, volver a convertir»).
Con Arrow, un `Table` es una descripción de búferes de memoria con un esquema; si dos motores
hablan Arrow, el segundo puede leer los búferes del primero sin copiarlos. Eso es lo que hace que
DuckDB consulte directamente un DataFrame, que Polars lea un `Table` sin convertirlo y que el
resultado de una consulta se pueda pasar a otra librería sin peaje.

:::nota
No confundas los tres nombres: **Arrow** es el formato en memoria (y su versión serializada,
Arrow IPC o Feather); **Parquet** es el formato en disco, columnar y comprimido; y un
**lakehouse** (Delta, Iceberg) es una capa de tablas encima de Parquet (ver
[[lakehouse-y-table-formats]]). Arrow es para procesar, Parquet para almacenar.
:::

## Definición formal

Un **array columnar** de `n` valores se describe con:

- **longitud** (`length`) — cuántos valores hay; puede ser menor que el espacio reservado.
- **máscara de validez** (*validity bitmap*) — `n` bits, uno por valor: 1 si el valor está
  presente y 0 si es nulo. Una columna sin nulos no necesita máscara.
- **recuento de nulos** (`null_count`) — guardado aparte, así que preguntar cuántos nulos hay es
  O(1) y no recorre la columna.
- **búferes de datos** — los valores. Para tipos de tamaño fijo (`int64`, `float64`, `bool`) es un
  único búfer contiguo de `n · itemsize` bytes.
- **desplazamientos** (*offsets*) — para tipos de longitud variable (texto, listas) se añade un
  búfer de `n + 1` enteros: el valor `i` ocupa los bytes `offsets[i]` a `offsets[i+1]`.

De ahí sale la cuenta que explica por qué el formato columnar premia leer poco. En una tabla de
`m` columnas numéricas con `n` filas, leer `k` columnas cuesta aproximadamente

:::formula
bytes_leídos ≈ k · n · itemsize      de un total de      m · n · itemsize
:::

es decir, la fracción `k / m` del fichero. Con 3 columnas de 40, alrededor del 7,5 % de los
bytes.

**Parquet** organiza el fichero en tres niveles y guarda metadatos en los dos útiles:

- **Row group** — un bloque de filas (por ejemplo, un millón) que se procesa como unidad.
- **Column chunk** — dentro de un row group, los datos de **una** columna. Aquí es donde vive la
  compresión, que por tanto es distinta para cada columna.
- **Página** — la unidad mínima de lectura dentro de un column chunk.
- **Estadísticas** — mínimo, máximo, número de nulos y distintos por column chunk. Son las que
  permiten **saltar** row groups enteros cuando el filtro no puede cumplirse allí (ver
  [[particionado-y-clustering]]).
- **Codificaciones** — diccionario (un código entero por valor distinto), *run-length* para
  valores repetidos seguidos, delta para series crecientes (ver [[compresion-y-codificacion]]).

## Ejemplo

Una tabla de 8 filas y 4 columnas, todas de `int64` (8 bytes por valor):

```
fila     id   anyo   importe   unidades
   0      1   2024     150,00          3
   1      2   2024      89,50          1
   2      3   2023     210,00          5
   3      4   2024      45,00          2
   4      5   2023     310,00          4
   5      6   2024      12,00          1
   6      7   2023     180,00          6
   7      8   2024     220,00          2
```

Guardado por columnas, cada columna ocupa `8 · 8 = 64` bytes y la tabla completa `4 · 64 = 256`
bytes. Si el análisis solo necesita `importe`:

- Formato por filas: hay que recorrer los 8 registros completos, 256 bytes, para descartar tres
  campos de cada uno.
- Formato por columnas: se leen los 64 bytes de `importe`, el **25 %** del total. Con 40 columnas
  en lugar de 4, la misma consulta leería el 2,5 %.

Y la columna `anyo` es el ejemplo de manual de la compresión: solo tiene dos valores distintos
(2023 y 2024). Con codificación por diccionario se guarda un diccionario de dos entradas y un
código de 1 bit por fila, así que las ocho filas ocupan ocho bits en vez de 64 bytes. Con
*run-length* el ahorro depende del orden: la secuencia «2024, 2024, 2023, 2024, 2023, 2024, 2023,
2024» tiene siete tramos y no comprime casi nada; esa misma columna ordenada por año tendría dos.
Por eso Parquet combina las dos: diccionario para columnas de baja cardinalidad, sin importar el
orden, y run-length para columnas que ya vienen ordenadas o agrupadas.

## Código

```python verificable
import pyarrow as pa

tabla = pa.table({"pais": ["ES", "FR", None], "importe": [1.5, 2.5, None]})

print([(c, str(tabla.schema.field(c).type)) for c in tabla.column_names])
# -> [('pais', 'string'), ('importe', 'double')]
print(tabla.num_rows, tabla.num_columns)            # -> 3 2
print(tabla.column("importe").to_pylist())          # -> [1.5, 2.5, None]
print(tabla.column("importe").null_count)           # -> 1  (la mascara de validez lo sabe sin recorrer)
```

```python verificable
import io

import pyarrow as pa
import pyarrow.parquet as pq

n = 20_000
tabla = pa.table({"pais": ["ES", "FR"] * (n // 2), "importe": list(range(n))})

memoria = io.BytesIO()
pq.write_table(tabla, memoria, compression="zstd")

# El fichero comprimido ocupa menos que los datos en memoria
print(memoria.getbuffer().nbytes < tabla.nbytes)     # -> True

# Se lee SOLO la columna pedida: el resto no se descomprime
leida = pq.read_table(io.BytesIO(memoria.getvalue()), columns=["importe"])
print(leida.column_names, leida.num_rows)            # -> ['importe'] 20000
print(leida.equals(tabla.select(["importe"])))       # -> True
```

```python verificable
import duckdb
import pyarrow as pa

tabla = pa.table({"x": [1, 2, 3], "y": [10.0, 20.0, 30.0]})

# DuckDB consulta el Table de Arrow directamente, sin cargarlo en su propio formato
print(duckdb.sql("SELECT sum(y) AS total FROM tabla").fetchone())   # -> (60.0,)
print(duckdb.sql("SELECT count(*) AS filas FROM tabla").fetchone()) # -> (3,)
```

El mismo puente existe con Polars, que lee los búferes de Arrow sin convertirlos:
`pl.from_arrow(tabla)` no copia nada si los tipos son compatibles, y `df.to_arrow()` devuelve un
`Table` equivalente (ver [[polars]]).

## Errores típicos

- **Convertir a Pandas en cada paso del pipeline.** Cada `to_pandas()` y `from_pandas()` puede
  copiar los búferes (sobre todo si hay columnas de texto de tipo `object`). Si vas a encadenar
  transformaciones, quédate en un solo motor y convierte al principio y al final.
- **Creer que Parquet es «un CSV comprimido».** Es inmutable: no se puede añadir una fila al
  final, hay que reescribir el fichero. Y no se puede leer una fila concreta sin leer al menos
  las columnas que la contienen. Para eso están los formatos de tabla con transacciones.
- **Generar millones de ficheros minúsculos.** Un Parquet por minuto y por sensor parece
  ordenado, pero el coste lo domina el sistema de ficheros, no los datos: abrir un fichero por
  consulta es mucho más caro que leer 100 MB de uno solo. Agrupa en ficheros de tamaño razonable.
- **Guardar las 40 columnas cuando el análisis usa 3.** El formato columnar premia leer poco,
  pero solo si el resto no se lee: si tu consulta hace `SELECT *`, la ventaja desaparece y el
  fichero sigue pagándose entero.
- **Suponer que guardar más columnas «no cuesta».** Cuesta almacenamiento y cuesta leer metadatos
  y estadísticas de cada column chunk. Modelar en estrella (pocas columnas por tabla, ver
  [[esquema-estrella-y-copo]]) suele salir más barato que una tabla ancha para todo.
- **Esperar que los tipos complejos sobrevivan a una ida y vuelta por CSV o Excel.** Listas,
  mapas, decimales exactos y marcas de tiempo con zona se pierden o cambian de tipo; el texto
  plano no lleva esquema (ver [[ficheros-y-encoding]]).

:::practica
enunciado: Un Parquet tiene 5.000.000 de filas y 30 columnas, todas de `int64` (8 bytes por valor). Tu consulta usa 4 de esas columnas. ¿Cuántos bytes recorre un formato por filas, cuántos el columnar y qué fracción del total es la segunda?
pista: Los bytes de una columna son filas por 8; el formato por filas paga las 30 columnas y el columnar solo las 4.
solucion: Total de la tabla: 5.000.000 · 30 · 8 = 1.200.000.000 bytes (1,2 GB). Formato por filas: recorre los 1.200.000.000. Columnar: 5.000.000 · 4 · 8 = 160.000.000 bytes (160 MB), porque solo se descomprimen esos cuatro column chunks. Fracción: 4 / 30 = 0,133, es decir el 13,3 % del fichero, y 1.200.000.000 / 160.000.000 = 7,5 veces menos bytes. Con las 30 columnas en el `SELECT`, la ventaja desaparece.
:::

## Comprueba que lo sabes

:::quiz
p: Una tabla tiene 40 columnas y tu consulta usa 2. ¿Cuánto se lee de un Parquet, aproximadamente?
o: Todo el fichero, porque Parquet lee registros completos
o: Alrededor del 5 % de los bytes, porque solo se descomprimen los column chunks de esas 2 columnas
o: La mitad, porque hay dos columnas
a: 2
e: En un formato columnar cada columna se guarda en su propio column chunk dentro de cada row group, así que una consulta que solo usa dos columnas lee y descomprime esos bloques y descarta el resto. En un formato por filas habría que leer entero.
:::

:::quiz
p: ¿Qué papel juega la máscara de validez de un array de Arrow?
o: Indica con un bit por valor si el valor es nulo, y permite saber cuántos nulos hay sin recorrer la columna
o: Comprime los valores repetidos
o: Guarda el orden de las filas
a: 1
e: La validez es un búfer de `n` bits y el recuento de nulos se almacena aparte, así que consultarlo es O(1). La compresión por diccionario o run-length es cosa de las codificaciones de Parquet, no de la máscara.
:::

:::quiz
p: ¿Por qué Arrow permite pasar datos entre motores «sin copiar»?
o: Porque usa compresión sin pérdida
o: Porque define una disposición concreta de los búferes en memoria y un esquema, así que el segundo motor puede leer los mismos bytes
o: Porque guarda los datos en disco en un formato propio
a: 2
e: La clave es que Arrow es una especificación de memoria: longitud, máscara de validez y búferes de datos con tipos definidos. Si el layout coincide, no hay que serializar ni reconstruir nada. La compresión es irrelevante aquí y el formato en disco es Parquet.
:::

:::trampa
Si tu pipeline va «Parquet → Pandas → Polars → DuckDB», estás pagando conversiones que el formato
columnar pretendía evitar. Cada salto puede copiar los búferes: mide dónde se va el tiempo antes
de añadir otro motor (ver [[rendimiento-y-perfilado]]).
:::
