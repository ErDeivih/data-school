---
id: datos-que-no-caben-en-memoria
titulo: Datos que no caben en memoria
fase: 3
nivel: intermedio
rutas: [de, ds]
prerequisitos: [pandas-fundamentos, arrow-y-formatos-columnares, ficheros-y-encoding]
tags: [memoria, chunks, parquet, pereza]
resumen: Si la tabla no cabe en RAM se lee por bloques y se agrega sobre la marcha; el resultado de una agregación es diminuto aunque el fichero tenga 50 GB.
fuentes: ["McKinney (2017), 'Python for Data Analysis'", "Reis y Housley (2022), 'Fundamentals of Data Engineering'"]
---

## En una frase

Un fichero de 50 GB no cabe en tu portátil, pero **su suma por ciudad sí**: lee el fichero por
trozos, calcula el parcial de cada trozo y quédate solo con los parciales.

## La idea

Imagina que tienes que contar los ladrillos de un camión y el garaje es demasiado bajo para
descargarlo entero. No hay truco: bajas un palé, cuentas los ladrillos de ese palé, apuntas el
número en una libreta y devuelves el palé. Al final la libreta tiene una línea por palé. El camión
nunca estuvo dentro del garaje y el total es exacto.
Ese es todo el concepto, y tiene una consecuencia que se pasa por alto: **hay que decidir qué
apuntas en la libreta antes de mirar el primer palé**. Si apuntas el total y el número de ladrillos,
puedes calcular la media con exactitud. Si apuntas solo la media de cada palé, cuando los palés no
tienen el mismo tamaño la media final sale mal y no te enteras.

Hay dos formas de arruinarlo, y las dos son frecuentes:

1. **Leer el fichero entero.** `pd.read_csv("datos.csv")` pide memoria para todas las filas a la
   vez (ver [[pandas-fundamentos]]). Cuando no la hay, el proceso muere (en Linux lo mata el sistema
   por falta de memoria) o empieza a usar el disco como si fuera RAM y todo se vuelve lentísimo.
   Pandas solo lanza `MemoryError` si falla la reserva; muchas veces falla más tarde, al hacer una
   copia.
2. **Leer por bloques y guardarlos todos en una lista.** El código *parece* que va por bloques,
   pero la lista tiene todas las filas y el `pd.concat` final construye una segunda copia de la
   tabla completa: el pico es el doble que leyendo de golpe.

La segunda mitad del oficio es saber que **no todas las preguntas se pueden contestar por
bloques**. Sumas, cuentas, mínimos, máximos y medias (llevando suma y cuenta) son *agregables*:
basta con combinar los parciales. La mediana y los cuantiles exactos **no** lo son: no existe
ningún parcial de tamaño fijo que los reconstruya, así que o guardas todos los datos o aceptas un
resumen aproximado (t-digest, *sketches* de cuantiles). El número de valores distintos sí sale
exacto: se guarda el conjunto de distintos de cada bloque y se unen al final, y el coste es el
número de valores distintos, no el de filas.

Los motores perezosos (Polars, DuckDB, Spark) aplican la misma idea con mejor cara: tú describes la
consulta, el motor la ejecuta por lotes y nunca materializa la tabla entera. La decisión de qué
calcular antes de leer sigue siendo tuya.

## Definición formal

Para una tabla de `n` filas y `m` columnas numéricas de `b` bytes por valor (`b = 8` para `int64`
y `float64`), la memoria de los datos es `n · m · b`. Leer por bloques de `n_b` filas cambia el
pico de la lectura:

:::formula
pico_completo ≈ n · m · b          pico_por_bloques ≈ n_b · m · b
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `n` | Filas del fichero | filas | El pico de la lectura completa sube igual; el de la lectura por bloques no se entera |
| `m` | Columnas que lees de verdad | columnas | El pico sube en las dos formas: leer 40 columnas cuando usas 3 es pagar 13 veces más memoria |
| `b` | Bytes por valor | bytes | Un `float64` ocupa 8; el texto ocupa muchísimo más, porque se guarda aparte de la tabla |
| `n_b` | Filas de cada bloque (`chunksize`) | filas | El pico por bloques sube proporcionalmente; bajarlo reduce memoria y aumenta el número de lecturas |
:::

La forma correcta de combinar parciales. Si el bloque `i` tiene `c_i` valores no nulos y suma `s_i`:

:::formula
media = Σ s_i / Σ c_i          nunca          media = (1/k) · Σ media_i
:::

Y el resultado de una agregación también ocupa memoria: si agrupas por una clave con 20 millones de
valores distintos, la tabla de salida tiene 20 millones de filas y no cabe, por mucho que hayas
leído por bloques. La regla práctica es que **el resultado tiene que caber**; si no cabe, hay que
agregar en dos pasos (primero por bloques y luego sobre los parciales).

Las tres herramientas que vas a usar:

- **Pandas**: `pd.read_csv(ruta, chunksize=n_b)` devuelve un iterador que entrega `DataFrame`s de
  `n_b` filas. No es un `DataFrame`.
- **PyArrow**: `pyarrow.dataset` abre un directorio de Parquet como un solo conjunto, empuja el
  filtro al lector y entrega lotes con `to_batches()`.
- **Polars**: `pl.scan_parquet(patrón)` construye un plan (`LazyFrame`) sin leer nada y
  `collect(engine="streaming")` lo ejecuta por lotes.

## Ejemplo

Un CSV de 200.000 filas y 3 columnas numéricas (`int64`, `float64`, `int64`) ocupa en memoria
`200.000 · 3 · 8 = 4.800.000` bytes, es decir **4,8 MB**. Un bloque de 10.000 filas ocupa
`10.000 · 3 · 8 = 240.000` bytes, **0,24 MB**: la vigésima parte, y ese tamaño no depende del
fichero. Con 200 millones de filas la tabla completa serían 4,8 GB (demasiado para un portátil de
8 GB) y el bloque seguiría ocupando 0,24 MB.

El error silencioso, con números. 20.000 importes: los 19.000 primeros valen 10 y los 1.000
últimos valen 100.

- La media verdadera es `(19.000 · 10 + 1.000 · 100) / 20.000 = 290.000 / 20.000 = 14,5`.
- Leyendo en bloques de 7.500 salen tres bloques con medias **10,0**, **10,0** y **28,0** (el
  tercero mezcla 4.000 del primer grupo con 1.000 del segundo).
- La media de esas tres medias es `(10 + 10 + 28) / 3 = 16,0`: un **10,3 % más alta** que la real.
- Con suma y cuenta: `(75.000 + 75.000 + 40.000 + 100.000) / 20.000 = 14,5`. Exacta.

Y la suma sí se puede repartir sin miedo: la suma de las sumas de los bloques es la suma total,
porque la suma es asociativa. Ese es el criterio para saber si una métrica es agregable.

:::figura
fichero: datos-que-no-caben-en-memoria-bloques
pie: Arriba, la memoria que pide cada forma de leer el mismo fichero: la lectura completa crece en línea recta con las filas y cruza la línea de los 8 GB de un portátil corriente a los 333 millones de filas, mientras que leer por bloques de 100.000 filas se queda en 2,4 MB pase lo que pase. Abajo, el error que no avisa: con bloques de 7.500 filas las medias son 10, 10 y 28, y la media de esas tres medias (16,0, línea de puntos) queda 1,5 por encima de la media real (14,5, línea discontinua), porque el tercer bloque mezcla dos regímenes distintos y pesa lo mismo que los otros.
fuente: figuras/datos-que-no-caben-en-memoria-1.py
:::

## Código

```python verificable
import io

import pandas as pd

# 20.000 importes: 19.000 con valor 10 y 1.000 con valor 100
valores = [10.0] * 19_000 + [100.0] * 1_000
texto = "importe\n" + "\n".join(str(v) for v in valores)

# En cada bloque se guardan la suma y la cuenta, no las filas
suma, cuenta, medias = 0.0, 0, []
for bloque in pd.read_csv(io.StringIO(texto), chunksize=7_500):
    suma += float(bloque["importe"].sum())
    cuenta += len(bloque)
    medias.append(float(bloque["importe"].mean()))

print(medias)                                # -> [10.0, 10.0, 28.0]
print(suma, cuenta, suma / cuenta)           # -> 290000.0 20000 14.5
print(round(sum(medias) / len(medias), 1))   # -> 16.0  la media de medias no es la media
```

```python verificable
import io
import tracemalloc

import numpy as np
import pandas as pd

# Un CSV de 200.000 filas y 3 columnas numericas, construido en memoria
rng = np.random.default_rng(0)
partes = ["a,b,c"]
for i in range(200_000):
    partes.append(f"{i},{rng.random():.6f},{i % 7}")
texto = "\n".join(partes) + "\n"

# tracemalloc mide lo que pide Python, no lo que ocupa el fichero en disco
tracemalloc.start()
completo = pd.read_csv(io.StringIO(texto))
pico_completo, _ = tracemalloc.get_traced_memory()
tracemalloc.stop()

tracemalloc.start()
suma = 0.0
for bloque in pd.read_csv(io.StringIO(texto), chunksize=10_000):
    suma += float(bloque["b"].sum())
    memoria_bloque = bloque.memory_usage(deep=True).sum()
pico_bloques, _ = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(len(completo), round(completo.memory_usage(deep=True).sum() / 1e6, 1))  # -> 200000 4.8
print(round(memoria_bloque / 1e6, 2))          # -> 0.24  un bloque, siempre igual
print(pico_completo > 10 * pico_bloques)       # -> True  el pico del bloque es minimo
```

```python verificable
import os
import tempfile

import polars as pl
import pyarrow as pa
import pyarrow.dataset as ds
import pyarrow.parquet as pq

with tempfile.TemporaryDirectory() as carpeta:
    # Dos ficheros Parquet, como los dejaria un proceso que escribe por lotes
    for i in range(2):
        tabla = pa.table({"ciudad": ["ES"] * 3 + ["FR"] * 2,
                          "importe": [1.0, 2.0, 3.0, 4.0, 5.0]})
        pq.write_table(tabla, os.path.join(carpeta, f"parte-{i}.parquet"))

    # pyarrow.dataset: el filtro se evalua en el lector y los lotes se piden de uno en uno
    conjunto = ds.dataset(carpeta, format="parquet")
    print(conjunto.count_rows(filter=ds.field("importe") > 2))   # -> 6
    print([l.num_rows for l in conjunto.scanner(batch_size=3).to_batches()])
    # -> [3, 2, 3, 2]  el tamano de lote se aplica a cada fichero por separado

    # Polars: scan_parquet no lee nada hasta que se pide el resultado
    perezoso = pl.scan_parquet(os.path.join(carpeta, "*.parquet"))
    print(type(perezoso).__name__)                              # -> LazyFrame
    print(perezoso.group_by("ciudad").agg(pl.col("importe").sum()).sort("ciudad")
          .collect(engine="streaming").to_dict(as_series=False))
    # -> {'ciudad': ['ES', 'FR'], 'importe': [12.0, 18.0]}
    try:
        perezoso.collect(streaming=True)                        # en Polars 2.x ya no existe
    except Exception as e:
        print(type(e).__name__)                                 # -> ArgumentRemovedError
```

:::claves
- `pd.read_csv(..., chunksize=)` **no devuelve un `DataFrame`**: devuelve un `TextFileReader`, que
  es un iterador. Se agota: si lo recorres dos veces, la segunda no da nada.
- El fichero sigue **abierto** mientras queden bloques por leer: en Windows eso impide borrarlo o
  moverlo, y el descriptor no se libera solo por abandonar el bucle. Ciérralo con `lector.close()`
  o, mejor, dentro de un `with`.
- `memory_usage(deep=True)` da el tamaño real. Con una columna de texto guardada como `object`,
  `deep=False` mide solo los punteros y se queda muy corto: en una columna de 2.000 cadenas da
  16 KB frente a los 175 KB reales. Con el dtype `str` de Pandas 3 las dos opciones coinciden,
  porque el texto vive en un búfer de Arrow y no como objetos de Python sueltos. Y la cuenta
  incluye el índice salvo que pases `index=False`: un `RangeIndex` no cuesta nada (132 bytes), pero
  `set_index` materializa 8 bytes por fila, 8.000 bytes por 1.000 filas que hay que sumar.
- `usecols=["a", "b"]` recorta el pico de forma proporcional: leer 3 de 40 columnas cuesta 13 veces
  menos memoria, y `dtype={"a": "int32"}` lo vuelve a reducir a la mitad.
- `ds.dataset(carpeta)` trata un directorio de Parquet como una sola tabla y `count_rows(filter=…)`
  empuja el filtro al lector. `scanner(batch_size=…)` entrega lotes **bajo demanda**, con ese
  tamaño aplicado **a cada fichero** y no al conjunto: en el ejemplo salen `[3, 2, 3, 2]` porque
  cada uno de los dos ficheros de 5 filas se parte en un lote de 3 y otro de 2. `to_table()` los
  juntaría todos y perderías la ventaja.
- `collect(engine="streaming")` no cambia el resultado, cambia el plan: agrega bloque a bloque en
  vez de materializar. El resultado final tiene que caber igualmente en memoria.
:::

## Errores típicos

- **Leer el fichero entero «para ver qué tiene».** Es la operación que mata el proceso. Para mirar,
  usa `nrows=5` y `usecols` con las columnas que te interesan; para el análisis de verdad, bloques.
- **Guardar los bloques en una lista y concatenar al final.** `pd.concat(trozos)` construye la
  tabla completa: has leído por bloques para acabar con el pico doble. Agrega dentro del bucle y
  deja fuera de la lista solo el resultado pequeño.
- **Calcular la media como media de medias.** Con bloques de distinto tamaño el resultado se
  desvía (10,3 % en el ejemplo) y no hay ningún aviso. Guarda `sum` y `count`, y divide al final.
- **Suponer que todo se puede agregar por bloques.** La mediana y los cuantiles exactos no se
  reconstruyen a partir de parciales. Si te los piden, o guardas los datos, o usas un resumen
  aproximado y lo dices en el informe.
- **Confundir bytes en disco con bytes en RAM.** Un Parquet comprimido de 500 MB puede ocupar 3 GB
  en memoria si lleva columnas de texto; y un CSV de 2 GB se convierte en un `DataFrame` de 5 GB.
  Mide con `memory_usage(deep=True)` antes de prometer nada (ver [[arrow-y-formatos-columnares]]).
- **Creer que `pl.scan_parquet` ya lee por lotes.** Devuelve un `LazyFrame`: no se ha leído ni un
  byte. Y en Polars 2.x `collect(streaming=True)` está eliminado (`ArgumentRemovedError`): ahora se
  escribe `collect(engine="streaming")`.

:::trampa
`pd.read_csv(ruta, chunksize=10_000)` seguido de `pd.concat(lista)` y luego un `groupby` es el
antipatrón clásico: parece procesamiento por bloques y es una lectura completa con una copia extra.
El `groupby` tiene que ir **dentro** del bucle, sobre cada bloque.
:::

:::practica
enunciado: Un CSV de 40 GB tiene las columnas `ciudad`, `fecha` e `importe`. Escribe el código que calcula el importe total por ciudad sin cargar el fichero entero y explica qué cambiarías si además te pidieran la mediana del importe por ciudad.
pista: La suma es agregable, así que puedes sumar los totales parciales de cada bloque; la mediana no lo es.
solucion: Se recorre con `pd.read_csv(ruta, chunksize=1_000_000, usecols=["ciudad", "importe"])`, se hace `bloque.groupby("ciudad")["importe"].sum()` en cada iteración y se guardan esas series parciales (una fila por ciudad, no por fila original). Al final se concatenan los parciales y se vuelve a agrupar con `sum()`: el resultado tiene una fila por ciudad. Para la mediana hay que cambiar de estrategia, porque no existe una combinación de medianas de bloques que dé la mediana global: o se guardan todos los importes (imposible aquí), o se calcula un cuantil aproximado con un resumen tipo t-digest o un sketch, y se informa de que es aproximado.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué devuelve `pd.read_csv("datos.csv", chunksize=100_000)`?
o: Un `DataFrame` con las primeras 100.000 filas
o: Un iterador que entrega `DataFrame`s de 100.000 filas y se agota al recorrerlo
o: Una lista con todos los `DataFrame`s de 100.000 filas ya cargados en memoria
a: 2
e: Devuelve un `TextFileReader`, que es un iterador: cada vuelta entrega un bloque y el fichero se lee a medida que avanzas. No es un `DataFrame` ni una lista; si lo recorres dos veces, la segunda no da nada.
:::

:::quiz
p: El bloque 1 tiene 1.000 filas con media 10 y el bloque 2 tiene 4.000 filas con media 20. ¿Cuál es la media real y qué da la media de las medias?
o: 18,0 real y 15,0 de media de medias
o: 15,0 las dos
o: 18,0 las dos
a: 1
e: La media real pondera por tamaño: (1.000 · 10 + 4.000 · 20) / 5.000 = 90.000 / 5.000 = 18,0. La media de las medias trata los bloques como si fueran iguales: (10 + 20) / 2 = 15,0. Solo coinciden si todos los bloques tienen el mismo número de filas.
:::

:::quiz
p: ¿Cuál de estas métricas NO se puede calcular exactamente agregando parciales de bloques?
o: La suma de una columna
o: El máximo de una columna
o: La mediana de una columna
a: 3
e: La suma y el máximo son agregables: el total es la suma de las sumas y el máximo global es el máximo de los máximos. La mediana necesita la posición central de todos los datos ordenados, y esa posición depende de valores que están repartidos entre bloques.
:::

:::quiz
p: `pl.scan_parquet("datos/*.parquet")` sobre un directorio de 20 GB, ¿cuánto tarda y cuánta memoria usa?
o: Lee los 20 GB y los deja listos en memoria
o: Casi nada y casi nada: construye un plan y no lee los datos hasta que se pide el resultado
o: Lanza un error si los ficheros no caben en memoria
a: 2
e: `scan_parquet` devuelve un `LazyFrame`: solo describe el plan. El trabajo ocurre en `collect()`, y con `collect(engine="streaming")` se agrega bloque a bloque. Aun así, el resultado de la agregación tiene que caber en memoria.
:::

:::nota
Este es el problema número uno del data engineer junior, y casi siempre se resuelve antes de
escribir código: elige la métrica, comprueba que es agregable y solo entonces decide cómo leer. Si
el volumen es de verdad grande, el siguiente escalón no es optimizar Pandas, es mover el cálculo a
un motor que lo haga por ti (ver [[duckdb-y-analitica-local]] y [[spark-fundamentos]]).
:::
