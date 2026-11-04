---
id: compresion-y-codificacion
titulo: Compresión y codificación
fase: 4
nivel: intermedio
rutas: [de, ds]
prerequisitos: [ficheros-y-encoding, arrow-y-formatos-columnares]
tags: [formatos, compresion, rendimiento, coste]
resumen: Diccionarios, rachas y delta codifican los valores según su tipo; Snappy, Zstd y gzip comprimen los bytes resultantes. Menos bytes casi siempre es menos tiempo.
fuentes: ["Kleppmann (2017), 'Designing Data-Intensive Applications', cap. 3", "Reis y Housley (2022), 'Fundamentals of Data Engineering'"]
---

## En una frase

**Codificar** es representar los valores de una columna de una forma más compacta aprovechando
sus patrones (un diccionario para textos repetidos, una racha para valores iguales seguidos,
una diferencia para números que crecen de uno en uno) y **comprimir** es aplicar un algoritmo
genérico a los bytes que salen de ahí; se hacen en ese orden y por eso dos tablas con los mismos
datos pueden ocupar diez veces más o menos.

## La idea

Hay dos capas y conviene no mezclarlas:

1. **Codificación**, dentro del fichero, que **conoce los tipos y los datos**. Sabe que la
   columna `pais` solo tiene 12 valores distintos y que `importe` está ordenado. Es la que
   consigue los ahorros grandes.
2. **Compresión**, encima, que solo ve bytes y busca repeticiones. No sabe si son nombres o
   números: aplica el mismo algoritmo a todo.

La analogía es escribir apuntes. Si en una libreta de 5.000 líneas el 90 % de las líneas dicen
`Madrid`, lo inteligente es numerar las ciudades al principio y escribir `3` en lugar de
`Madrid` en cada línea: eso es un **diccionario**. Después, además, puedes comprimir la libreta
metiéndola en una bolsa de vacío: eso es el **códec**. La bolsa ayuda, pero el ahorro gordo vino
de no repetir la palabra.

Las codificaciones que verás en Parquet, ORC y Arrow:

- **Diccionario:** se guardan los valores distintos una vez y, por cada fila, un índice de
  `⌈log₂ k⌉` bits, con `k` el número de valores distintos. Brilla con cardinalidad baja: países,
  estados, categorías, códigos.
- **Longitud de racha (RLE):** los valores iguales seguidos se guardan como un par (valor,
  repeticiones). Brilla cuando los datos están **ordenados** o casi.
- **Delta:** se guarda el primer valor y las diferencias con el anterior. Un contador o una
  secuencia temporal se convierte en una lista de unos, que después comprime casi a cero.
- **Referencia común y empaquetado de bits:** se resta el mínimo y se guardan los valores con
  los bits justos. Una columna de valores entre 1.000 y 1.100 no necesita 8 bytes por fila.
- **Nulos:** se guardan como una máscara de bits aparte, no como un valor especial por fila.

Los códecs que verás en la práctica:

- **Snappy y LZ4:** rapidísimos, ratio moderado. Buen punto de partida para datos calientes, que
  se leen muchas veces y se escriben deprisa.
- **Zstd:** el equilibrio actual. Niveles de 1 a 19: el 3 es el compromiso habitual entre tamaño
  y CPU, y los niveles altos se reservan para datos fríos o de archivo.
- **gzip (deflate):** ratio bueno y velocidad baja. Sigue siendo el rey de la interoperabilidad y
  el formato de los ficheros que se envían fuera.
- **Ninguno:** válido si el dato ya está comprimido (imágenes, ZIP) o si el cuello de botella es
  la CPU.

La razón de fondo para comprimir no es ahorrar disco, que es barato: es que **leer menos bytes
casi siempre es más rápido**, aunque haya que gastar CPU en descomprimir. Un disco o una red que
entrega 200 MB por segundo tarda la mitad en entregar 100 MB, y ese tiempo no se recupera con
CPU. Cuando el sistema está limitado por entrada y salida —casi todos los trabajos de datos—,
comprimir acelera. Cuando ya está limitado por CPU, comprimir con un códec caro lo frena.

## Definición formal

Sea `B_crudo` el tamaño de los valores sin codificar y `B_final` el tamaño del fichero:

:::formula
ratio = B_crudo / B_final  ·  bits_por_valor = 8 · B_final / filas
:::

Para el caso del diccionario, con `k` valores distintos, longitud media `L` y `n` filas:

:::formula
B_diccionario ≈ k · L + n · ⌈log₂ k⌉ / 8
:::

De ahí se ve la condición para que el diccionario gane: `k · L` tiene que ser pequeño frente a
`n · L`, es decir, `k` mucho menor que `n`. Con 20 ciudades y un millón de filas es una
victoria aplastante; con identificadores únicos (`k = n`) el diccionario ocupa lo mismo que los
datos y solo añade índices, así que el motor deja de usarlo.

Para la longitud de racha, con `r` rachas de longitud media `h`, `B_RLE ≈ r · (L + c)`, donde
`c` son los bytes del contador de repeticiones. La condición es que las rachas sean largas:
`h` grande. Si los valores van alternando, `r ≈ n` y el RLE es peor que no hacer nada.

Dos consecuencias prácticas:

1. **Ordenar las filas antes de escribir es gratis y multiplica el efecto** de las dos
   codificaciones.
2. **El códec va después.** Comprimir primero y codificar después no existe: el códec no entiende
   la columna.

## Ejemplo

Un millón de filas con una columna `ciudad` de 20 valores distintos, 9 caracteres cada uno
(`ciudad_00` a `ciudad_19`):

- **Sin codificar:** `1.000.000 × 9 = 9.000.000` bytes (9 MB).
- **Con diccionario:** los 20 valores ocupan `20 × 9 = 180` bytes y cada fila necesita un índice
  de 5 bits (`2⁵ = 32 ≥ 20`), es decir `1.000.000 × 5 / 8 = 625.000` bytes. Total:
  `625.180` bytes, un ratio de **14,4×**.
- **Con RLE y las filas ordenadas por ciudad:** cada ciudad forma una racha de 50.000 filas, así
  que la columna entera son 20 pares de valor y contador: pasa de 9 MB a unos cientos de bytes.

Con los mismos valores pero en orden aleatorio, el RLE no encuentra rachas y el fichero vuelve a
crecer. Los datos son idénticos; el orden no. En el bloque de abajo se comprueba con un códec
genérico: el orden agrupado comprime mucho mejor que el mismo contenido mezclado.

## Código

```python verificable
# 1.000.000 de filas con 20 ciudades distintas de 9 caracteres cada una
n = 1_000_000
ciudades = [f"ciudad_{i:02d}" for i in range(20)]

crudo = len(ciudades[0]) * n                    # cada fila guarda el texto completo
bits_indice = 5                                 # 2**5 = 32, suficiente para 20 valores
diccionario = sum(len(c) for c in ciudades) + n * bits_indice // 8

print("bytes sin codificar:", crudo)                                # -> bytes sin codificar: 9000000
print("bytes con diccionario:", diccionario)                        # -> bytes con diccionario: 625180
print("ratio de la codificacion:", round(crudo / diccionario, 1))   # -> ratio de la codificacion: 14.4
print("bits por valor:", round(8 * diccionario / n, 3))             # -> bits por valor: 5.001
```

```python verificable
import random
import zlib

# Las mismas 20 ciudades con las mismas frecuencias, en dos ordenes distintos
ciudades = [f"ciudad_{i % 20:02d}" for i in range(20_000)]
mezcladas = ciudades[:]
random.Random(0).shuffle(mezcladas)          # semilla fija: el resultado es reproducible

en_ciclo = ",".join(ciudades).encode()       # ciudad_00, ciudad_01, ... y vuelta a empezar
al_azar = ",".join(mezcladas).encode()       # mismas frecuencias, orden aleatorio

print("bytes crudos iguales:", len(en_ciclo) == len(al_azar))    # -> bytes crudos iguales: True
print("comprime mejor el orden agrupado:", len(zlib.compress(en_ciclo, 6)) < len(zlib.compress(al_azar, 6)))  # -> comprime mejor el orden agrupado: True
print("zlib agrupado baja de 100 kB:", len(zlib.compress(en_ciclo, 6)) < 100_000)  # -> zlib agrupado baja de 100 kB: True
```

## Errores típicos

- **Comprimir algo ya comprimido o un fichero diminuto.** Guardar un JPEG, un ZIP o un Parquet
  con Snappy dentro de otro códec hace trabajar a la CPU para ahorrar casi nada, y el códec
  necesita ver repeticiones: en un fichero de 20 kB casi todo es cabecera.
- **Usar gzip o Zstd en nivel 19 para datos calientes.** El ratio mejora un poco y la CPU se
  dispara. Para datos que se leen muchas veces, Snappy, LZ4 o Zstd en nivel bajo; los niveles
  altos son para archivo.
- **Creer que comprimir siempre acelera y mirar solo el tamaño.** Si el trabajo está limitado por
  CPU, añadir un códec caro lo hace más lento, y un fichero un 30 % más pequeño que tarda el
  doble en descomprimirse es un mal negocio ([[coste-y-optimizacion]]). Mide el tiempo además del
  tamaño.
- **Codificar por diccionario una columna de alta cardinalidad.** Con identificadores únicos, el
  diccionario ocupa tanto como los datos y añade índices. Los motores lo detectan y lo
  desactivan, pero si tú eliges la codificación a mano, perderás.
- **Confundir codificación con compresión.** «Parquet comprime» es impreciso: primero codifica
  por columnas (diccionario, delta, rachas) y después comprime los bytes con el códec elegido.
  Cambiar el códec sin ordenar los datos deja la mayor parte del ahorro sobre la mesa.
- **Olvidar que el orden de las filas cambia el ratio.** Escribir filas ordenadas por la columna
  de baja cardinalidad puede reducir el fichero a la mitad con el mismo códec y los mismos
  datos ([[parquet-avro-orc]]).

## Comprueba que lo sabes

:::quiz
p: Una columna tiene 20 valores distintos y un millón de filas. ¿Por qué la codificación por diccionario reduce tanto el tamaño?
o: Porque elimina las filas repetidas de la tabla
o: Porque guarda los 20 valores una sola vez y un índice de 5 bits por fila en lugar del texto completo
o: Porque aplica compresión gzip a cada valor
a: 2
e: El diccionario separa los valores únicos (180 bytes) de los índices (5 bits por fila, unos 625.000 bytes). No se pierde ninguna fila: es una representación más compacta de los mismos valores. Con cardinalidad alta, en cambio, el diccionario deja de compensar.
:::

:::quiz
p: ¿Qué relación hay entre codificación y compresión en un fichero Parquet?
o: Son lo mismo con dos nombres comerciales
o: La codificación aprovecha los patrones de la columna y después el códec comprime los bytes resultantes
o: Primero se comprime con Snappy y luego se aplica el diccionario
a: 2
e: El orden es codificar y luego comprimir. La codificación entiende el tipo de dato (diccionario, delta, rachas); el códec solo ve bytes. Por eso ordenar las filas mejora las dos etapas a la vez y cambiar de códec sin ordenar apenas cambia el resultado.
:::

:::quiz
p: Cambias el códec de Snappy a gzip y el fichero baja un 15 %, pero las consultas tardan más. ¿Qué ha pasado?
o: Que gzip es un códec con mejor ratio y más coste de CPU, y el sistema estaba limitado por CPU y no por lectura
o: Que el fichero ahora está corrupto
o: Que gzip ocupa más memoria y el motor hace más copias
a: 1
e: Comprimir más siempre gasta más CPU. Si el trabajo ya estaba limitado por CPU, ese gasto no se compensa con los bytes ahorrados. En cargas limitadas por entrada y salida ocurre lo contrario: el ahorro de bytes gana.
:::

:::truco
Antes de tocar códecs, ordena las filas por la columna de baja cardinalidad que más se filtra.
En la mayoría de tablas analíticas ese cambio, que no cuesta CPU en la lectura, reduce el tamaño
más que subir el nivel de compresión, y además mejora la poda por estadísticas.
:::
