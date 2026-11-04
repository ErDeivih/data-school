---
id: parquet-avro-orc
titulo: Parquet, Avro y ORC
fase: 4
nivel: intermedio
rutas: [de, ds]
prerequisitos: [ficheros-y-encoding, arrow-y-formatos-columnares]
tags: [formatos, columnar, lectura, rendimiento]
resumen: Columnar frente a orientado a fila: por qué Parquet lee solo lo que necesitas, dónde encaja Avro y qué aporta ORC, con el orden de las filas como verdadero truco.
fuentes: ["Kleppmann (2017), 'Designing Data-Intensive Applications', cap. 3", "Reis y Housley (2022), 'Fundamentals of Data Engineering'"]
---

## En una frase

**Parquet** y **ORC** guardan los datos por columnas (leer tres columnas de cuarenta cuesta una
fracción de lo que costaría leerlo todo) y **Avro** los guarda por filas con su esquema
incorporado, que es lo que quieres cuando escribes mucho y lees registros completos, como en un
flujo de eventos.

## La idea

Imagina un archivador con las fichas de 1.000 empleados: nombre, apellidos, dirección, teléfono,
salario, departamento. Quieres la media de salario por departamento, es decir, dos campos de
seis.

- **Orientado a fila** (CSV, JSON, Avro): cada ficha está entera en una página. Para calcular la
  media tienes que pasar las 1.000 fichas y saltarte cuatro campos de cada una. Lees 6 datos
  para usar 2.
- **Orientado a columna** (Parquet, ORC): hay una lista con todos los nombres, otra con todos
  los teléfonos y otra con todos los salarios. Vas directo a las dos listas que necesitas y
  lees aproximadamente un tercio de la información. Además, todos los valores de una misma
  columna son parecidos entre sí, y eso los hace mucho más fáciles de comprimir.

Esa segunda ventaja —comprimir mejor porque los valores vecinos se parecen— es la que casi nadie
espera y la que más se nota. En una columna de `pais`, los valores son `ES`, `ES`, `ES`, `FR`…
y basta con un diccionario de 4 entradas; en una columna de identificadores aleatorios no hay
nada que comprimir.

**Parquet** organiza el fichero en *grupos de filas* (normalmente de 128 MB) y, dentro de cada
uno, un bloque por columna. El pie del fichero guarda el esquema y, por cada bloque de columna,
estadísticas: mínimo, máximo, número de nulos y, a veces, un histograma. Con eso un motor puede
**descartar grupos enteros** sin leerlos (*predicate pushdown*) y **leer solo las columnas
pedidas** (*projection*). Es el formato por defecto de la analítica, y con razón.

**Avro** es lo contrario en el eje de lectura, y eso lo hace insuperable en otro sitio: guarda el
esquema en la cabecera del fichero y los registros completos uno detrás de otro. Es lo natural
para escribir un flujo de eventos a mucha velocidad ([[kafka-y-colas]]) y para evolucionar
esquemas con reglas claras: el escritor y el lector negocian sus esquemas y los campos nuevos se
rellenan con su valor por defecto. Para analítica es mala elección: leer dos columnas obliga a
recorrer todos los registros completos.

**ORC** nació en el ecosistema Hive y hace lo mismo que Parquet con otra disposición: franjas
(*stripes*) con índices por columna. En la práctica, si usas Spark, Hive o Trino, cualquiera de
los dos funciona; elige el que soporte mejor tu motor y no cambies a mitad de camino.

Y hay una consecuencia que conviene entender bien: la poda de ficheros y de grupos **solo
funciona si los datos están ordenados** por la columna del filtro. Si un grupo de filas contiene
los 12 meses del año, el mínimo y el máximo de la columna `fecha` son enero y diciembre y el
motor no puede descartar nada. Si ordenas por fecha antes de escribir, cada grupo cubre un rango
estrecho y una consulta de un mes lee uno o dos grupos.

## Definición formal

Términos que aparecen en cualquier documentación y conviene tener claros:

- **Grupo de filas (row group):** el bloque de filas que se escribe de una vez. Es la unidad de
  paralelismo de lectura y la unidad de las estadísticas. Típico: 128 MB.
- **Bloque de columna (column chunk):** los valores de **una** columna dentro de un grupo de
  filas. Es la unidad de lectura cuando proyectas.
- **Página:** la unidad más pequeña dentro de un bloque de columna; se codifica y comprime por
  separado. Aquí actúan las codificaciones ([[compresion-y-codificacion]]): diccionario, longitud
  de racha, delta.
- **Estadísticas:** mínimo, máximo, nulos y, opcionalmente, número de valores distintos por
  bloque. Son lo que permite saltarse datos.
- **Proyección:** leer solo un subconjunto de columnas. El coste en bytes es aproximadamente
  proporcional a esas columnas, no al total.
- **Poda (pruning):** descartar grupos de filas y ficheros enteros usando las estadísticas y el
  particionado ([[particionado-y-clustering]]).

:::formula
bytes_leídos ≈ bytes_totales · (columnas_pedidas / columnas_totales)
:::

La fórmula vale como orden de magnitud, no como promesa: los bloques tienen un tamaño mínimo de
lectura, las columnas no miden lo mismo (una cadena larga ocupa más que un entero) y una columna
con cinco valores distintos puede ocupar una milésima parte del fichero. Además, las estadísticas
de una columna no sirven de nada si los datos no están ordenados por ella.

## Ejemplo

Una tabla de 200.000 filas con tres columnas: `cliente` (entero con 1.000 valores distintos),
`ciudad` (texto con 5 valores) e `importe` (decimal con prácticamente un valor distinto por
fila). En crudo son unos 5 MB.

- **Leer las tres columnas:** el motor recorre los tres bloques de cada grupo de filas.
- **Leer solo `ciudad`:** recorre únicamente el bloque de esa columna. Y como tiene 5 valores
  distintos, va codificada con diccionario y ocupa una fracción mínima del fichero. Cuidado con
  la cuenta fácil «una columna de tres es un tercio»: una columna de baja cardinalidad pesa
  mucho menos que su fracción y una de alta entropía pesa mucho más.
- **Filtrar `importe > 900` con el fichero desordenado:** el primer grupo de filas va de 1,0 a
  1.000,9, así que las estadísticas no permiten descartar nada y el filtro se comprueba fila a
  fila.
- **Lo mismo con el fichero ordenado por `importe`:** el primer grupo solo llega a 200,9 y los
  valores altos quedan agrupados al final, así que se descartan grupos enteros sin leerlos. Esa
  es la diferencia entre pagar por bytes leídos y no pagarlos.

Además, ordenar por `importe` reduce el tamaño del fichero más de un 20 % en este mismo ejemplo,
porque los valores parecidos quedan juntos y el códec encuentra repeticiones que antes no
existían. No es magia del formato: es la consecuencia de que los datos vecinos se parezcan.

## Código

```python verificable
import io

import pyarrow as pa
import pyarrow.parquet as pq

n = 200_000
ciudades = ["Madrid", "Barcelona", "Sevilla", "Bilbao", "Valencia"]

# Datos deterministas y desordenados: alta cardinalidad en cliente e importe
tabla = pa.table({
    "cliente": pa.array([(i * 7919) % 1000 for i in range(n)], pa.int64()),
    "ciudad": pa.array([ciudades[(i * 3) % 5] for i in range(n)], pa.string()),
    "importe": pa.array([round(((i * 104729) % 100_000) / 100, 2) for i in range(n)], pa.float64()),
})

def serializar(t):
    buffer = io.BytesIO()
    pq.write_table(t, buffer, compression="zstd", row_group_size=50_000)
    return buffer.getvalue()

bytes_sin_orden = serializar(tabla)
bytes_ordenada = serializar(tabla.sort_by("importe"))

print("ordenar por importe reduce el fichero:", len(bytes_ordenada) < len(bytes_sin_orden))  # -> ordenar por importe reduce el fichero: True
print("la mejora pasa del 20 %:", len(bytes_ordenada) < 0.8 * len(bytes_sin_orden))          # -> la mejora pasa del 20 %: True

f = pq.ParquetFile(io.BytesIO(bytes_sin_orden))
print("grupos de filas:", f.metadata.num_row_groups)             # -> grupos de filas: 4
print("columnas del fichero:", f.metadata.num_columns)           # -> columnas del fichero: 3
print("filas al leer solo una columna:", f.read(columns=["ciudad"]).num_rows)  # -> filas al leer solo una columna: 200000

tam_ciudad = sum(f.metadata.row_group(g).column(1).total_compressed_size
                 for g in range(f.metadata.num_row_groups))
tam_total = sum(f.metadata.row_group(g).column(c).total_compressed_size
                for g in range(f.metadata.num_row_groups) for c in range(f.metadata.num_columns))
print("una columna de tres ocupa menos de la mitad:", tam_ciudad < tam_total / 2)  # -> una columna de tres ocupa menos de la mitad: True
```

```python verificable
import io

import pyarrow as pa
import pyarrow.parquet as pq

# 40.000 importes entre 1,00 y 1.000,99 en orden arbitrario pero reproducible
n = 40_000
tabla = pa.table({"importe": pa.array(
    [round(1 + ((i * 7919) % 100_000) / 100, 2) for i in range(n)], pa.float64())})

def rango_primer_grupo(t):
    """Minimo y maximo del primer grupo de filas: lo que el motor usa para podar."""
    buffer = io.BytesIO()
    pq.write_table(t, buffer, compression="none", row_group_size=8_000)
    meta = pq.ParquetFile(io.BytesIO(buffer.getvalue())).metadata
    est = meta.row_group(0).column(0).statistics
    return f"{est.min:.1f} a {est.max:.1f} en {meta.num_row_groups} grupos"

print("sin ordenar:", rango_primer_grupo(tabla))                 # -> sin ordenar: 1.0 a 1000.9 en 5 grupos
print("ordenado por importe:", rango_primer_grupo(tabla.sort_by("importe")))  # -> ordenado por importe: 1.0 a 200.9 en 5 grupos
```

## Errores típicos

- **Creer que Parquet ordena los datos.** No ordena nada: los escribe en el orden en que llegan.
  Las estadísticas por grupo solo sirven para podar si el fichero ya está ordenado por la
  columna del filtro. Ordenar antes de escribir es la optimización más rentable y la más
  olvidada.
- **Leer todas las columnas cuando usas tres.** Un `SELECT *` sobre una tabla de 40 columnas en
  un motor que sí proyecta sigue leyendo solo lo pedido, pero si materializas todo en memoria
  pagas el coste completo. Pide las columnas que necesitas.
- **Escribir ficheros diminutos.** Mil ficheros de 200 kB no se pueden leer en paralelo de forma
  eficiente y la sobrecarga de abrir y cerrar domina el tiempo. Apunta a ficheros de 128 MB a 1
  GB en la capa depurada.
- **Usar Avro para analítica, Parquet para un flujo de eventos o cambiar de formato sin razón.**
  Avro gana cuando escribes registros completos a gran velocidad y el esquema evoluciona
  ([[kafka-y-colas]]); Parquet gana cuando lees unas pocas columnas de muchos millones de filas.
  Elegir mal se paga en cada consulta, y migrar de un formato a otro cuesta tiempo sin aportar
  nada: elige uno, documenta por qué y quédate ahí.
- **Tratarlo como un contenedor de texto.** Parquet no es editable ni legible a mano: los
  ficheros son inmutables y actualizar una fila implica reescribirlos. Y guardar un JSON enorme
  dentro de una columna es peor: pierdes la proyección y las estadísticas, porque el motor lee el
  objeto completo aunque solo quieras un campo. Extrae a columnas propias lo que se consulta.
- **Reordenar columnas esperando leer menos.** La proyección es por nombre: leer la columna 1 y
  la 7 cuesta lo mismo que leer la 1 y la 2. Lo que cambia los bytes leídos es el conjunto de
  columnas y el número de grupos de filas que se descartan.

## Comprueba que lo sabes

:::quiz
p: Una tabla Parquet de 40 columnas se consulta pidiendo 3. ¿Por qué se lee mucho menos de lo que parece?
o: Porque el motor adivina qué columnas hacen falta y las guarda en caché
o: Porque los valores de cada columna están en bloques separados y solo se leen los de las columnas pedidas
o: Porque Parquet guarda una copia reducida de cada tabla
a: 2
e: En un formato columnar cada columna vive en su propio bloque dentro de cada grupo de filas, así que la proyección descarta el resto en disco. No hay copia reducida ni caché mágica: el ahorro está en la disposición física de los datos.
:::

:::quiz
p: Filtras por `fecha` y la consulta tarda lo mismo con y sin filtro. El fichero tiene las fechas mezcladas de tres años. ¿Qué está pasando?
o: Que Parquet no soporta filtros por fecha
o: Que cada grupo de filas contiene todo el rango de fechas, así que las estadísticas de mínimo y máximo no permiten descartar ninguno
o: Que falta un índice B-tree en la columna fecha
a: 2
e: La poda se apoya en el mínimo y el máximo de cada grupo de filas. Si todos los grupos contienen los tres años, ningún grupo se puede descartar y el motor acaba comprobando fila a fila. La solución es ordenar por fecha (o particionar por fecha) antes de escribir.
:::

:::quiz
p: ¿En qué caso Avro es mejor elección que Parquet?
o: Cuando quieres leer dos columnas de mil millones de filas
o: Cuando escribes un flujo de eventos completos a gran velocidad y necesitas que el esquema evolucione de forma explícita
o: Cuando necesitas que el fichero se pueda abrir con un editor de texto
a: 2
e: Avro guarda el esquema y los registros completos, que es justo lo que necesita una cola de eventos; además define cómo resolver diferencias entre el esquema del escritor y el del lector. Para analítica columnar, Parquet u ORC. Que sea binario no lo hace editable.
:::

:::nota
«Orden de las columnas» y «orden de las filas» se confunden todo el tiempo. Reordenar las
columnas del esquema no cambia los bytes que lees: la proyección va por nombre. Lo que de
verdad cambia el coste es **qué columnas pides** y **cómo están ordenadas las filas** dentro de
cada grupo, porque de eso dependen la poda y la compresión.
:::
