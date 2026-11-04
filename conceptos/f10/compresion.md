---
id: compresion
titulo: Compresión
fase: 10
nivel: avanzado
rutas: [alg, de]
prerequisitos: [entropia-e-informacion, arrays-y-listas, tablas-hash, complejidad-asintotica]
tags: [compresion, entropia, formatos, rendimiento]
resumen: Huffman, LZ y codificación por diccionario: cómo se quita redundancia a los datos, cuál es el límite teórico y por qué comprimir suele acelerar.
fuentes: ["Huffman (1952), 'A Method for the Construction of Minimum-Redundancy Codes'", "Ziv y Lempel (1977), 'A Universal Algorithm for Sequential Data Compression'", "Nelson y Gailly (1995), 'The Data Compression Book'"]
---

## En una frase

Comprimir es reescribir la misma información con menos bits aprovechando su redundancia —símbolos
frecuentes con códigos cortos, secuencias repetidas con referencias a lo ya visto— y el límite
de lo que se puede apretar sin perder nada lo marca la **entropía** de la fuente.

## La idea

Escribe la frase «el que algo quiere, algo le cuesta» como un telegrama pagando por letra. Lo
primero que haces es sustituir «que» por `q` y «algo» por `alg`: eso es un **diccionario**. Lo
segundo, darte cuenta de que la `e` aparece mucho y la `k` casi nunca, y asignar al que más
aparece la abreviatura más corta: eso es **Huffman**. Las dos ideas son las que sostienen toda la
compresión sin pérdida, y no ha aparecido nada mejor en setenta años, solo implementaciones más
listas.

De dónde sale la redundancia, que es lo que hay que buscar antes de elegir un algoritmo:

1. **Símbolos con frecuencias muy distintas.** En español la `e` es mucho más frecuente que la
   `k`. Si usas el mismo número de bits para todas, estás gastando de más en las raras. Lo
   explotan Huffman y la codificación aritmética.
2. **Secuencias que se repiten.** Un log repite `2024-03-11T10:00:` en cada línea; una tabla de
   pedidos repite la misma ciudad miles de veces. Lo explotan LZ77 y LZ78: en lugar de escribir
   la secuencia otra vez, escriben «copia los 27 bytes que empiezan 400 posiciones más atrás».
3. **Valores correlacionados o con cardinalidad baja.** Una columna `pais` con 40 valores
   distintos se guarda mejor como un entero de 6 bits que como una cadena de 12 caracteres. Y
   una columna ordenada se guarda mucho mejor como diferencias entre valores consecutivos
   (**delta encoding**) que como valores absolutos.

**Qué se puede y qué no.** Sin pérdida hay un suelo teórico: no existe ningún códec que, de media,
gaste menos de `H` bits por símbolo, siendo `H` la entropía de la fuente. Y al revés: los datos
que ya son aleatorios tienen entropía máxima y **no se pueden comprimir**; intentarlo solo añade
la cabecera. Con pérdida (JPEG, MP3, vídeo) se tira información que el ojo o el oído no notan, y
ahí las tasas son de otro orden.

**Por qué comprimir acelera.** Esto sorprende hasta que se mira dónde está el cuello de botella.
Un analizador de columnas casi nunca está limitado por la CPU: está limitado por leer bytes de
disco o de red. Si comprimes un 75 %, lees cuatro veces menos bytes y la CPU dedica un poco más
a descomprimir, mucho menos de lo que has ganado. Hay un efecto secundario aún mejor en los
formatos columnares: si una columna está codificada por diccionario, un filtro del tipo
`pais = 'ES'` puede evaluarse **sobre los códigos enteros** sin reconstruir las cadenas. Con
datos pequeños, en cambio, la cabecera y el bloque mínimo mandan, y comprimir puede incluso
hacer crecer el fichero.

## Definición formal

**Entropía de Shannon.** Para una fuente que emite símbolos con probabilidad `pᵢ`:

:::formula
H = − Σᵢ pᵢ · log₂(pᵢ)   bits por símbolo
:::

- `pᵢ` — probabilidad del símbolo `i`, estimada con su frecuencia relativa.
- `Σᵢ` — suma sobre todos los símbolos distintos del alfabeto.
- `log₂` — logaritmo en base 2; `log₂(1/pᵢ)` es la «sorpresa» de ver ese símbolo, en bits.

El **teorema de codificación de fuente** de Shannon dice que ninguna codificación sin pérdida
puede usar de media menos de `H` bits por símbolo. La entropía no es una recomendación: es un
suelo.

**Codificación de Huffman.** Se construye un árbol binario: se toman los dos símbolos de menor
frecuencia, se unen en un nodo cuya frecuencia es la suma, y se repite hasta quedarse con un solo
nodo. Recorrer el árbol da códigos **libres de prefijo**: ningún código es el principio de otro,
así que se puede decodificar de izquierda a derecha sin separadores. La longitud media es
`L = Σᵢ pᵢ · ℓᵢ`, con `ℓᵢ` la longitud en bits del código del símbolo `i`, y cumple:

:::formula
H ≤ L < H + 1
:::

Es decir, Huffman nunca se queda a más de un bit por símbolo del óptimo teórico, y con
frecuencias muy desiguales se queda muchísimo más cerca.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `H` | Entropía de la fuente: el mínimo teórico de bits por símbolo de cualquier código sin pérdida | bits por símbolo | El suelo sube con ella y queda menos que rascar. Con datos aleatorios vale 8 (el máximo de un byte) y no hay nada que comprimir |
| `pᵢ` | Probabilidad del símbolo `i`, estimada con su frecuencia relativa en el texto | adimensional, entre 0 y 1 | Baja su `log₂(1/pᵢ)`, así que ese símbolo recibe un código más corto y el reparto de longitudes se vuelve más desigual: es justo lo que aprovecha Huffman |
| `ℓᵢ` | Longitud en bits del código que le toca al símbolo `i` | bits | Ese símbolo cuesta más, y el total sube en proporción a su `pᵢ`. Ningún `ℓᵢ` puede quedar por debajo de su ideal `log₂(1/pᵢ)`: es la desigualdad de Kraft |
| `L` | Longitud media del código, `L = Σᵢ pᵢ · ℓᵢ` | bits por símbolo | El fichero comprimido crece. La cota `H ≤ L < H + 1` dice que se acerca al suelo, pero nunca lo cruza |
| `R` | Ratio de compresión: tamaño comprimido entre tamaño original | adimensional | Se ahorra menos. Con `R = 0,21` el ahorro es del 79 %; a partir de `R = 1` comprimir ha hecho el fichero más grande, que es lo que pasa con la cabecera en ficheros diminutos |
| `k` | Valores distintos de una columna codificada por diccionario | valores distintos | Cada fila necesita `⌈log₂ k⌉` bits en vez de la cadena entera, pero la tabla de valores crece con `k`: cuando `k` se acerca al número de filas, el diccionario deja de compensar |
:::

**Compresión por diccionario (familia LZ).** LZ77 emite tripletas `(desplazamiento, longitud,
siguiente)` que significan «copia `longitud` bytes empezando `desplazamiento` posiciones atrás y
añade `siguiente`». LZ78 y LZW construyen explícitamente un diccionario de secuencias vistas y
emiten índices a ese diccionario. No necesitan conocer las frecuencias de antemano, y por eso
dominan en formatos de propósito general (`gzip` es LZ77 más Huffman; `zstd` es LZ más
codificación por entropía con tablas entrenadas).

**Medidas.** El **ratio** de compresión es `R = tamaño_comprimido / tamaño_original`, y el
**ahorro** es `1 − R`. Un `R = 0,21` es un ahorro del 79 %. Comparar ratios de dos códecs exige
medir sobre los mismos bytes de entrada y contando la cabecera de cada uno, porque en ficheros
pequeños la cabecera decide el resultado.

**Codificación por diccionario de columnas.** Si una columna tiene `k` valores distintos, se
guarda una tabla de `k` valores y, por cada fila, un índice de `⌈log₂ k⌉` bits. El coste pasa de
`n · longitud_media` a `n · ⌈log₂ k⌉` bits más la tabla. En una columna con 10 millones de filas y
4 ciudades distintas, eso es pasar de 120 MB de texto a unos 2,5 MB de índices.

## Ejemplo

La palabra `ABRACADABRA`, con 11 símbolos: `A` aparece 5 veces, `B` 2, `R` 2, `C` 1 y `D` 1.

- Frecuencias relativas: `5/11 = 0,4545`, `2/11 = 0,1818` (dos veces) y `1/11 = 0,0909` (dos
  veces).
- Entropía: `H = 2,04` bits por símbolo.
- Huffman, empezando por unir los dos menos frecuentes (`C` y `D`, con 1 cada uno): produce
  `A = 0`, `B = 110`, `R = 111`, `C = 100`, `D = 101`.
- Coste total: `5·1 + 2·3 + 2·3 + 1·3 + 1·3 = 23` bits, es decir `23/11 = 2,09` bits por
  símbolo.
- Con un código fijo de 3 bits por símbolo (5 símbolos necesitan 3 bits) serían `33` bits. Con
  ASCII de 8 bits, `88` bits.

Comprobación de la cota: `2,04 ≤ 2,09 < 3,04`. Huffman está a cinco centésimas del suelo teórico,
y el código fijo está un 57 % por encima del óptimo. Ese es el premio por aprovechar las
frecuencias.

**Efecto del tipo de datos.** Un texto muy repetitivo de 1.000 bytes comprime a 21 bytes, un
ratio del 2 %. En cambio 2.048 bytes de ruido uniforme comprimen a 2.059: el ratio es del 101 %,
porque la cabecera de `zlib` y el bloque mínimo pesan más que la nada que se puede ahorrar. Ese
es el recordatorio de que la compresión explota estructura, y los datos aleatorios no tienen
ninguna.

:::figura
fichero: compresion-huffman-y-tope
pie: Izquierda: los 31 símbolos de un log de 15.300 bytes ordenados por frecuencia, con el ideal de cada uno (`log₂(1/p)`, en azul) y los bits que le da Huffman (en verde). Las dos curvas van pegadas —4,61 bits por símbolo frente al suelo de 4,60 que marca la entropía— y las que se despegan un poco son las últimas, las raras: Huffman nunca se aleja más de un bit del ideal, y el código fijo de 8 bits de ASCII costaría casi el doble. Derecha: el ratio de `zlib` frente al tamaño de la entrada. Por debajo de 100 bytes manda la cabecera y el texto llega a ocupar un 25 % más de lo que ocupaba; el log repetitivo baja al 0,1 %; y los datos aleatorios se quedan clavados en el 100 %, porque no hay estructura que quitar. Las dos lecciones de la página están ahí: comprimir quita redundancia, no información, y por eso se ahorra cuando el cuello de botella son los bytes leídos, nunca cuando ya hay entropía máxima.
fuente: figuras/compresion-1.py
:::

## Código

```python verificable
import heapq
import itertools
import math
from collections import Counter


def huffman(texto):
    """Codigo libre de prefijo optimo: une siempre los dos simbolos menos frecuentes."""
    contador = itertools.count()          # desempate estable entre frecuencias iguales
    monticulo = [(peso, next(contador), {simbolo: ""})
                 for simbolo, peso in Counter(texto).items()]
    heapq.heapify(monticulo)
    while len(monticulo) > 1:
        p1, _, n1 = heapq.heappop(monticulo)
        p2, _, n2 = heapq.heappop(monticulo)
        for simbolo in n1:
            n1[simbolo] = "0" + n1[simbolo]
        for simbolo in n2:
            n2[simbolo] = "1" + n2[simbolo]
        n1.update(n2)
        heapq.heappush(monticulo, (p1 + p2, next(contador), n1))
    return monticulo[0][2]


texto = "ABRACADABRA"
codigos = huffman(texto)
bits = sum(len(codigos[c]) for c in texto)
entropia = -sum((texto.count(c) / len(texto)) * math.log2(texto.count(c) / len(texto))
                for c in set(texto))

print("codigos:", dict(sorted(codigos.items())))
print("bits con Huffman:", bits)                          # -> 23
print("bits con 3 bits fijos:", 3 * len(texto))           # -> 33
print("entropia: {:.2f} bits/simbolo".format(entropia))   # -> 2.04
print("media Huffman: {:.2f} bits/simbolo".format(bits / len(texto)))  # -> 2.09
```

:::claves
- `huffman(texto)` devuelve un **diccionario** `{símbolo: "01011"}`, no la cadena comprimida ni el número de bits: para saber cuánto ocupa hay que sumar `sum(len(codigos[c]) for c in texto)`, que es lo que hace la línea siguiente. Con la cadena vacía el montículo queda vacío y `monticulo[0]` lanza `IndexError`.
- El `itertools.count()` no participa en el peso: es el **desempate**. Cuando dos nodos empatan a frecuencia, `heapq` compara el segundo campo de la tupla y, sin ese contador, acabaría comparando los diccionarios: `huffman("ABRACADABRA")` sin él lanza `TypeError: '<' not supported between instances of 'dict' and 'dict'`. Con el contador, el desempate decide qué código se lleva cada símbolo, pero no sus longitudes ni el total de bits.
- `heapq.heapify(monticulo)` reordena la lista **en el sitio** y devuelve `None`: escribir `monticulo = heapq.heapify(lista)` deja `monticulo` valiendo `None` y el bucle falla en la primera iteración.
- Cada unión añade un bit a todos los símbolos del subárbol, y los dos que se unen primero son los menos frecuentes: acaban con los códigos más largos. Como el código de cada símbolo depende del orden de las uniones, `dict(sorted(codigos.items()))` sale ordenado por símbolo y no por longitud.
- La entropía se calcula con `texto.count(c)` por cada símbolo distinto, así que recorre el texto entero una vez por símbolo (`O(k · n)`) en vez de reutilizar el `Counter` que ya está calculado.
- La cota del ejemplo se comprueba sobre `bits / len(texto)` y no sobre `bits`: comparar el total de bits con la entropía mezcla unidades (bits contra bits por símbolo) y en un texto largo la desigualdad parecería falsa por puro tamaño.
:::

```python verificable
import zlib
import numpy as np

# Comprimir ayuda cuando hay estructura; con alta entropia solo anade cabecera.
repetitivo = ("fila," * 200).encode()
alta_entropia = np.random.default_rng(0).integers(0, 256, 2048, dtype=np.uint8).tobytes()

for nombre, datos in [("repetitivo", repetitivo), ("alta entropia", alta_entropia)]:
    comprimido = zlib.compress(datos, level=6)
    print("{:<14} {:>6} -> {:>6} bytes  ({:.0%})".format(
        nombre, len(datos), len(comprimido), len(comprimido) / len(datos)))
# repetitivo:    1000 bytes de entrada,   21 comprimidos (2 %)
# alta entropia: 2048 bytes de entrada, 2059 comprimidos (101 %)
```

```python verificable
import io
import pyarrow as pa
import pyarrow.parquet as pq

# Una columna categorica: el diccionario sustituye cadenas por indices enteros.
ciudades = ["Madrid", "Barcelona", "Valencia", "Sevilla"] * 2500
tabla = pa.table({"ciudad": ciudades, "importe": list(range(10000))})

for nombre, dicc, codec in [("sin diccionario", False, "none"),
                            ("con diccionario", True, "none"),
                            ("diccionario + zstd", True, "zstd")]:
    buffer = io.BytesIO()
    pq.write_table(tabla, buffer, use_dictionary=dicc, compression=codec)
    print("{:<20} {:>7} bytes".format(nombre, buffer.tell()))
# sin diccionario:      195721 bytes
# con diccionario:      100861 bytes
# diccionario + zstd:    28759 bytes
```

## Errores típicos

- **Comprimir datos que ya están comprimidos.** Un JPEG, un PNG, un `.parquet` con `zstd` o un
  `.gz` no se pueden comprimir más: intentarlo suele **aumentar** el tamaño un 0,1 % o un 1 %.
  Antes de añadir un códec, comprueba si el formato ya trae uno.
- **Suponer que comprimir siempre acelera.** En un flujo de datos que cabe en memoria y ya está
  caliente, comprimir solo añade ciclos de CPU. El beneficio aparece cuando el cuello de botella
  es el disco o la red: si tu trabajo está al 100 % de CPU y al 20 % de disco, comprimir te hará
  más lento.
- **Elegir el códec por su ratio y no por el coste de descompresión.** El descomprimido se paga
  en cada lectura, y en consultas analíticas hay muchas. Subir el nivel de compresión da ficheros
  algo más pequeños a cambio de descomprimir más despacio; en analítica, donde cada consulta
  vuelve a leer las mismas páginas, casi siempre conviene un nivel bajo (`zstd -3`, `snappy`)
  antes que exprimir el último punto de ratio.
- **Ignorar que un fichero `gzip` no se puede dividir.** Para procesar 50 GB con `gzip` en
  Hadoop o Spark hace falta **un solo** hilo de lectura de principio a fin del fichero. Los
  formatos columnares con grupos de fila (Parquet, ORC) o `zstd` sobre bloques independientes sí
  se reparten. Es la razón real por la que Parquet desplazó a los CSV comprimidos.
- **Medir el ratio con datos distintos.** Comparar el 2 % de un log repetitivo con el 101 % de
  datos aleatorios no dice nada de los códecs: dice que los datos eran distintos. Mide siempre
  sobre los mismos bytes.
- **Creer que un códec encuentra el óptimo.** Huffman es óptimo **entre los códigos prefijo
  símbolo a símbolo**, con frecuencias conocidas y estáticas. La codificación aritmética y los
  códecs con contexto baten esa cota porque no están limitados a un número entero de bits por
  símbolo. Y si las frecuencias cambian a lo largo del fichero, Huffman estático se queda corto.

:::practica
enunciado: Codifica con Huffman la palabra MISSISSIPPI (M 1, I 4, S 4, P 2) y calcula el coste total en bits y por símbolo. Compáralo con un código fijo de 2 bits y comprueba la cota, con entropía 1,82 bits por símbolo.
pista: Une siempre los dos símbolos menos frecuentes, empezando por M y P, y asigna 0 y 1 a cada rama.
solucion: M+P = 3; con I da 7; y con S, la raíz. Códigos: S = 0, I = 10, M = 110, P = 111. Coste: 4·1 + 4·2 + 1·3 + 2·3 = 21 bits, es decir 1,91 por símbolo. Un código fijo de 2 bits daría 22, y la cota se cumple: 1,82 ≤ 1,91 < 2,82. La ganancia es pequeña porque las frecuencias son poco desiguales.
:::

## Comprueba que lo sabes

:::quiz
p: Tienes 500 MB de datos y el trabajo pasa el 90 % del tiempo leyendo de disco. ¿Qué esperas si los comprimes a la mitad con zstd?
o: Que tarde el doble, porque hay que descomprimir
o: Que tarde menos, porque el tiempo de CPU ahorrado en descomprimir es menor que el ahorrado en leer la mitad de bytes
o: Que tarde exactamente lo mismo, porque el trabajo total es el mismo
a: 2
e: Si el cuello de botella es la entrada/salida, reducir a la mitad los bytes que hay que leer acorta el trabajo, y el coste de descomprimir se solapa con esa lectura. Con el trabajo limitado por CPU el balance sería el contrario.
:::

:::quiz
p: ¿Por qué no se puede comprimir de forma ilimitada un fichero de texto?
o: Porque los códecs tienen un tamaño máximo de bloque
o: Porque la entropía de la fuente fija un suelo de bits por símbolo para cualquier codificación sin pérdida
o: Porque los sistemas de ficheros reservan la cabecera
a: 2
e: El teorema de codificación de fuente de Shannon establece que ninguna codificación sin pérdida baja de H bits por símbolo de media. Huffman se acerca a menos de un bit de ese suelo y los métodos con contexto lo rozan, pero ninguno lo cruza. Un fichero con entropía máxima, como los datos aleatorios, no se comprime en absoluto.
:::

:::trampa
Un ratio de compresión espectacular suele significar que los datos tienen mucha estructura, no que
el códec sea maravilloso. Y al revés: medir el ratio de un códec sobre un fichero de 1 kB mide
sobre todo su cabecera. Compara siempre con el mismo contenido, el mismo tamaño y contando la
cabecera.
:::
