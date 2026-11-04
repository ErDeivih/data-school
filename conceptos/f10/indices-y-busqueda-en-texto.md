---
id: indices-y-busqueda-en-texto
titulo: Índices y búsqueda en texto
fase: 10
nivel: avanzado
rutas: [alg, de]
prerequisitos: [tablas-hash, tries, procesamiento-de-texto-clasico, ordenacion]
tags: [busqueda, recuperacion, tf-idf, bm25]
resumen: Índice invertido, análisis de texto, TF-IDF y BM25: cómo un motor encuentra los documentos relevantes sin leerlos todos en cada consulta.
fuentes: ["Manning, Raghavan y Schütze (2008), 'Introduction to Information Retrieval'", "Robertson y Zaragoza (2009), 'The Probabilistic Relevance Framework: BM25 and Beyond'", "Witten, Moffat y Bell (1999), 'Managing Gigabytes'"]
---

## En una frase

Un índice invertido guarda, para cada término, la lista de documentos donde aparece, y una
función de puntuación como BM25 convierte esas listas en un orden: primero los documentos donde
los términos de la consulta son frecuentes **y** raros en el resto de la colección.

## La idea

Un libro de texto lleva un índice alfabético al final: en lugar de leer las 600 páginas buscando
«entropía», vas a la `E` y lees la lista de páginas. Un motor de búsqueda hace lo mismo, pero al
revés: en lugar de construir el índice para que lo lea una persona, lo construye para que lo lea
una máquina, y por eso puede permitirse una entrada por cada palabra que existe en la colección.

La pieza central es el **índice invertido**: un diccionario que va de término a **lista de
postings**, es decir, a los identificadores de los documentos que contienen ese término. La
diferencia con no tener índice es abismal: buscar una palabra en 10 millones de documentos sin
índice es leerlo todo; con índice es leer una lista que, para una palabra corriente, tiene unos
pocos millones de entradas, y para una rara, unas decenas.

Alrededor del índice hay cuatro decisiones que determinan la calidad del resultado:

1. **El análisis.** Antes de indexar, el texto se tokeniza (se parte en palabras), se pasa a
   minúsculas, a veces se le quitan las **stopwords** (palabras vacías como `de`, `la`, `y`,
   que aparecen en todos los documentos y no discriminan) y a veces se le aplica **stemming**
   (reducir cada palabra a su raíz: `corriendo` y `correr` comparten raíz).
2. **Las listas de postings.** Se guardan ordenadas por identificador de documento, lo que
   permite resolver una consulta de varios términos con una **intersección lineal** del tipo
   `merge`, sin ordenar nada.
3. **La puntuación.** No basta con saber qué documentos contienen los términos: hay que
   ordenarlos. Un documento donde `gato` aparece 8 veces es más relevante que uno donde aparece
   una vez, pero no ocho veces más. Y un término que aparece en el 90 % de los documentos no
   aporta nada, mientras que uno que aparece en 3 documentos es casi una huella dactilar.
4. **La consulta.** Un `AND` de términos corrientes puede devolver millones de documentos; lo
   que hace útil a un buscador no es filtrar, es **ordenar** bien los primeros veinte.

La puntuación pasó por dos etapas. **TF-IDF** combina la frecuencia del término en el documento
(`tf`) con su rareza en la colección (`idf`), y funciona, pero su parte de frecuencia crece sin
límite: un documento que repite la palabra 200 veces gana a uno que la explica mejor con 20.
**BM25** corrige eso con dos ideas que hoy son el estándar de facto:

- **Saturación de la frecuencia.** La contribución de `tf` crece rápido al principio y se aplana
  después. Pasar de 1 a 2 apariciones importa mucho; de 20 a 21, casi nada.
- **Normalización por longitud.** Un documento largo tiene más probabilidad de contener cualquier
  término por puro tamaño. BM25 lo penaliza, pero de forma suave y ajustable con el parámetro
  `b`: con `b = 0` no se normaliza nada y con `b = 1` se normaliza del todo.

## Definición formal

**Índice invertido.** Para cada término `t` del vocabulario, la lista de postings `P(t)` es la
lista ordenada de los identificadores de documentos que contienen `t`. Si además se guarda, por
cada aparición, la posición dentro del documento, el índice es **posicional** y permite resolver
consultas de frase («gato come», en ese orden y contiguos). El precio es que las listas pasan de
unos pocos bytes por documento a uno por cada aparición.

**TF-IDF.** Con `N` documentos en la colección, `df(t)` el número de documentos que contienen el
término `t` y `tf(t, d)` el número de veces que `t` aparece en el documento `d`:

:::formula
tf-idf(t, d) = tf(t, d) · log(N / df(t))
:::

- `N` — número total de documentos de la colección.
- `df(t)` — frecuencia de documento: en cuántos documentos distintos aparece `t`.
- `log(N / df(t))` — el factor `idf`; vale 0 si el término está en todos los documentos y crece
  al hacerse más raro. En la práctica se usa `log(1 + N / df(t))` para que no se anule.

**BM25.** La puntuación de un documento `d` para una consulta `q` formada por los términos `t`:

:::formula
BM25(q, d) = Σ_t IDF(t) · f(t,d) · (k₁ + 1) / (f(t,d) + k₁ · (1 − b + b · L_d / L_media))
:::

:::formula
IDF(t) = ln(1 + (N − df(t) + 0,5) / (df(t) + 0,5))
:::

- `f(t, d)` — número de apariciones del término `t` en el documento `d`.
- `L_d` — longitud del documento `d` en tokens.
- `L_media` — longitud media de los documentos de la colección.
- `k₁` — controla la saturación de la frecuencia; valores típicos entre 1,2 y 2,0. Con `k₁ = 0`
  la frecuencia deja de importar.
- `b` — controla la normalización por longitud, entre 0 y 1; el valor habitual es 0,75.
- `ln` — logaritmo natural; `e` es su base, aproximadamente 2,71828.
- `Σ_t` — suma sobre los términos de la consulta que aparecen en el documento.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `N` | Número total de documentos de la colección | documentos | El `IDF` de todos los términos sube un poco por igual, así que el orden entre documentos apenas cambia. Una colección más grande ayuda a discriminar: lo que era raro en 1.000 documentos es rarísimo en un millón |
| `df(t)` | Frecuencia de documento: en cuántos documentos distintos aparece `t` | documentos | El término discrimina menos y su `IDF` baja. Cuando `df(t) = N` (aparece en todos) el peso se queda casi en cero, y ese es el motivo de que las palabras vacías se eliminen |
| `tf(t, d)` y `f(t, d)` | Veces que aparece el término en un documento concreto; la página usa los dos nombres para la misma cantidad | apariciones | En TF-IDF la puntuación crece en proporción; en BM25 se satura y tiende a multiplicar por `k₁ + 1` como mucho. Es toda la diferencia entre los dos órdenes |
| `L_d` | Longitud del documento `d`, en tokens | tokens | El denominador crece y el documento se penaliza: un documento largo tiene más ocasiones de contener cualquier término por puro tamaño, no por ser más relevante |
| `L_media` | Longitud media de los documentos de la colección | tokens | Con la misma `L_d`, un documento se ve relativamente más largo y se penaliza más. Solo entra en el cociente `L_d / L_media`, así que lo que importa es la desviación respecto a la media, no el valor absoluto |
| `k₁` | Controla la saturación de la frecuencia: cuánto puede llegar a pesar repetir el término | adimensional, típicamente entre 1,2 y 2,0 | El techo `k₁ + 1` sube: con `k₁ = 1,2` el máximo es 2,2 veces y con `k₁ = 5` es 6. Con `k₁ = 0` la frecuencia deja de importar y la puntuación solo mira si el término está o no está |
| `b` | Controla la normalización por longitud | adimensional, entre 0 y 1 | El castigo por ser largo crece: con `b = 0` no se normaliza nada y con `b = 1` se normaliza del todo. El valor habitual es 0,75 |
| `IDF(t)` | Peso del término por su rareza: `ln(1 + (N − df(t) + 0,5) / (df(t) + 0,5))` | adimensional | El término pesa más en la suma, y con él todos los documentos que lo contienen. Es un factor común a todos ellos, así que subirlo no reordena nada por sí solo |
:::

El límite de saturación se ve bien: cuando `f(t, d)` se hace muy grande, el factor
`f · (k₁+1) / (f + k₁·…)` tiende a `k₁ + 1`, un techo. Con `k₁ = 1,2` ese techo es 2,2: por muchas
veces que repitas la palabra, no puedes multiplicar su contribución más allá de 2,2 veces el
`IDF`.

**Coste y compresión.** Las listas de postings se guardan como **diferencias** entre
identificadores consecutivos (delta encoding) y cada diferencia con **varint**, que usa 7 bits por
byte y reserva el bit alto para indicar si sigue. Los identificadores crecen, las diferencias no,
y por eso se codifican en uno o dos bytes. Además, para acelerar la intersección se añaden
**skip pointers** cada `√|P|` posiciones, que permiten saltar tramos enteros de una lista.

## Ejemplo

Tres documentos:

- `d1`: «el gato come pescado y el gato duerme» (8 tokens)
- `d2`: «el perro come pienso» (4 tokens)
- `d3`: «el gato y el perro duermen» (6 tokens)

**Postings.** `gato` está en `d1` y `d3`; `come` en `d1` y `d2`. Una consulta `gato AND perro`
interseca `{d1, d3}` con `{d2, d3}` y devuelve `d3`.

**Puntuación BM25 de `gato`** con `k₁ = 1,2`, `b = 0,75`, longitud media 6 y `df(gato) = 2` de 3
documentos:

- `IDF(gato) = ln(1 + (3 − 2 + 0,5) / (2 + 0,5)) = ln(1,6) = 0,4700`.
- En `d1`: `f = 2`, `L_d = 8`. Denominador: `2 + 1,2·(1 − 0,75 + 0,75·8/6) = 2 + 1,2·1,25 = 3,5`.
  Numerador: `2 · 2,2 = 4,4`. Puntuación: `0,4700 · 4,4/3,5 = **0,5909**`.
- En `d3`: `f = 1`, `L_d = 6`. Denominador: `1 + 1,2·(0,25 + 0,75·1) = 2,2`. Numerador: `2,2`.
  Puntuación: `0,4700 · 1 = **0,4700**`.
- En `d2`: `f = 0`, puntuación `0`.

`d1` gana por repetir el término (`f = 2`), y la normalización por longitud no llega a compensar
esa ventaja. Pero si `d1` tuviera 20 tokens en lugar de 8, el denominador sería
`2 + 1,2·(0,25 + 0,75·20/6) = 5,3`, la puntuación bajaría a `0,4700 · 4,4/5,3 = 0,390` y **`d3`
pasaría por delante** pese a mencionar el gato una sola vez. Eso es exactamente lo que hace `b`:
castigar la verbosidad.

**Compresión de las listas.** Una lista de postings `[1, 3, 4, 7, 11, 12, 800, 801]` ocupa 32
bytes como enteros de 4 bytes. Guardada como diferencias `[1, 2, 1, 3, 4, 1, 788, 1]` y con
varint ocupa 9 bytes: el 788 necesita dos bytes y los demás, uno. Un ahorro del 72 % que se paga
solo una vez, al construir el índice, y se cobra en cada consulta.

:::figura
fichero: bm25-saturacion-y-longitud
pie: Izquierda: lo que aporta repetir el término, con el IDF aparte. La curva sube de golpe al principio y se aplana: con k₁ = 1,2 el techo es 2,2, así que pasar de 1 a 2 apariciones sube la puntuación un 38 % y pasar de 20 a 21 solo un 0,3 %. Ese es el motivo de que BM25 ordene mejor que contar apariciones, y las líneas de puntos marcan el techo de cada k₁. Derecha: el ejemplo de la página, con la puntuación de «gato» en función de la longitud del documento. El documento que repite el término dos veces gana mientras es corto (0,591 con 8 tokens frente al 0,470 del breve), pero el castigo por longitud lo hunde: a partir de 14 tokens el documento breve, que solo menciona el gato una vez, pasa por delante. Eso es lo que hace b: en igualdad de término, gana el que lo dice sin rellenar.
fuente: figuras/indices-y-busqueda-en-texto-1.py
:::

## Código

```python verificable
import re
from collections import defaultdict

documentos = {
    "d1": "el gato come pescado y el gato duerme",
    "d2": "el perro come pienso",
    "d3": "el gato y el perro duermen",
}


def analizar(texto):
    """Tokeniza a minusculas. Aqui no se quitan stopwords, a proposito."""
    return re.findall(r"[a-z]+", texto.lower())


indice = defaultdict(set)
for doc, texto in documentos.items():
    for termino in analizar(texto):
        indice[termino].add(doc)

print("postings de 'gato':", sorted(indice["gato"]))   # -> ['d1', 'd3']
print("postings de 'come':", sorted(indice["come"]))   # -> ['d1', 'd2']
print("terminos distintos:", len(indice))              # -> 9

# Una consulta AND es la interseccion de las listas de postings.
consulta = ["gato", "perro"]
resultado = set.intersection(*(indice[t] for t in consulta))
print("documentos con", consulta, ":", sorted(resultado))   # -> ['d3']
```

:::claves
- `analizar` devuelve una **lista de tokens** (cadenas), no el texto ni un conjunto, y pasa a minúsculas **antes** de buscar: con `texto.split()` el término saldría como `gato,` y `indice["gato"]` no encontraría nada. El análisis decide qué es un término, y cambiarlo cambia el índice entero.
- `indice` es un `defaultdict(set)`, así que preguntar por una clave que no existe la **crea**: después de `indice["zarzuela"]`, `len(indice)` cuenta un término que no está en ningún documento. Lo mismo pasa al recorrer el diccionario para depurarlo.
- `sorted(indice["gato"])` devuelve una lista nueva y ordenada, pero el `set` original sigue sin orden: `print(indice["gato"])` puede salir de cualquier manera y ese orden no dice nada sobre los documentos.
- Con una consulta vacía, `set.intersection(*(...))` no devuelve el conjunto vacío: lanza `TypeError: unbound method set.intersection() needs an argument`. Y si un término no está en el índice, el `defaultdict` lo crea vacío y la intersección sale vacía en silencio, que es peor que un error.
- Los `set` de este ejemplo guardan **documentos**, no posiciones: con esta estructura se resuelve `gato AND perro`, pero no la frase «gato come». Para eso hace falta un índice posicional y guardar cada aparición.
- En el bloque siguiente, `math.log` es el logaritmo **natural** (`ln`), no `log₂`: la fórmula del `IDF(t)` de la página lleva `ln` a propósito. Cambiarlo por `math.log2` multiplica todas las puntuaciones por `1/ln(2) ≈ 1,4427`, así que el orden de los documentos no cambia pero los números dejan de coincidir con los del ejemplo.
- El `+ 0.5` del IDF no es decorativo: con `df = N` (el término está en todos los documentos) la fórmula clásica `log(N/df)` valdría cero y ese término no puntuaría nada, mientras que la suavizada le deja `ln(1,143) = 0,133`.
:::

```python verificable
import math

# BM25 de "gato" en tres documentos. k1 controla la saturacion; b, la longitud.
documentos = {
    "d1": "el gato come pescado y el gato duerme",
    "d2": "el perro come pienso",
    "d3": "el gato y el perro duermen",
}
termino, k1, b = "gato", 1.2, 0.75

largos = {doc: len(texto.split()) for doc, texto in documentos.items()}
medio = sum(largos.values()) / len(largos)
N = len(documentos)
df = sum(1 for texto in documentos.values() if termino in texto.split())
idf = math.log(1 + (N - df + 0.5) / (df + 0.5))       # version suavizada del IDF

print("largo medio: {:.2f}  df: {}  idf: {:.4f}".format(medio, df, idf))
for doc, texto in documentos.items():
    f = texto.split().count(termino)
    score = idf * (f * (k1 + 1)) / (f + k1 * (1 - b + b * largos[doc] / medio))
    print("{:<3} f={} largo={}  BM25={:.4f}".format(doc, f, largos[doc], score))
# idf = 0.4700; d1 f=2 largo=8 BM25=0.5909; d2 BM25=0.0000; d3 f=1 BM25=0.4700
```

```python verificable
# Postings comprimidos: diferencias entre identificadores consecutivos + varint.
def varint(n):
    """Entero no negativo en 7 bits por byte; el bit alto indica que hay continuacion."""
    salida = bytearray()
    while True:
        byte = n & 0x7F
        n >>= 7
        if n:
            salida.append(byte | 0x80)
        else:
            salida.append(byte)
            return bytes(salida)


postings = [1, 3, 4, 7, 11, 12, 800, 801]
deltas = [postings[0]] + [b - a for a, b in zip(postings, postings[1:])]
comprimido = b"".join(varint(d) for d in deltas)

print("postings:", postings)
print("deltas:", deltas)                                # -> [1, 2, 1, 3, 4, 1, 788, 1]
print("bytes sin comprimir (4 por doc):", 4 * len(postings))   # -> 32
print("bytes con delta + varint:", len(comprimido))            # -> 9
```

```json ilustrativo
{
  "query": {
    "bool": {
      "must": [
        { "match": { "titulo": { "query": "gato perro", "operator": "and" } } }
      ],
      "filter": [
        { "term": { "idioma": "es" } },
        { "range": { "fecha": { "gte": "2024-01-01" } } }
      ]
    }
  },
  "size": 10
}
```

## Errores típicos

- **No normalizar por la longitud del documento.** Sin el factor `b`, un documento que repite
  todas las palabras del vocabulario acaba siempre arriba. `b = 0,75` es el punto de partida
  razonable; súbelo si tus documentos tienen longitudes muy dispares y bájalo si son uniformes.
- **Confundir TF-IDF con BM25 y llamarlos equivalentes.** El `tf` de TF-IDF crece de forma
  lineal (o logarítmica en las variantes habituales); el de BM25 se satura en `k₁ + 1`. En
  documentos donde una palabra se repite mucho, los dos órdenes difieren, y BM25 suele ordenar
  mejor.
- **Analizar mal el texto: stopwords de más o stemming agresivo.** Si eliminas `de`, `la` e `y`
  de la consulta «el gato y el perro», ya no puedes distinguirla de «el perro y el gato». Y un
  stemmer demasiado agresivo confunde términos distintos: el de Porter reduce `university` y
  `universe` a la misma raíz `univers`. Quita las stopwords del índice de puntuación y revisa los
  conflictos del stemmer en tu dominio.
- **Esperar del índice invertido cosas que no hace.** No resuelve búsquedas por prefijo (para eso
  están los [[tries]] o un índice de n-gramas), ni errores de escritura (distancia de edición o
  n-gramas), ni sinónimos (hay que expandir la consulta).
- **Evaluar el motor con los ojos.** «Los resultados se ven bien» no es una métrica. Mide
  **precisión** (de los devueltos, cuántos son relevantes) y **exhaustividad** (de los relevantes,
  cuántos devuelve) sobre un conjunto de consultas con relevancia etiquetada, y compara los
  cambios con esos números.
- **Ordenar los postings solo al final.** La intersección lineal exige que las dos listas estén
  ordenadas; si se construyen desordenadas y se ordenan en cada consulta, pagas `O(n log n)` por
  consulta en lugar de `O(n)` en la unión de dos listas ya ordenadas.

:::practica
enunciado: Dos listas de postings ordenadas: gato = [2, 5, 9, 14, 20, 31] y perro = [1, 5, 8, 9, 15, 20, 40]. Haz la intersección con un merge lineal, di qué documentos salen y cuántas comparaciones haces entre elementos. ¿Y si hubiera que ordenar las listas en cada consulta?
pista: Avanza siempre el puntero de la lista que tiene el valor menor; cada paso de ese puntero es una comparación.
solucion: Coinciden en 5, 9 y 20, así que el resultado es {5, 9, 20}. El merge avanza los 6 elementos de la primera lista y los 7 de la segunda: 13 comparaciones, es decir O(|A| + |B|). Ordenar en cada consulta costaría 6·log₂6 + 7·log₂7 ≈ 15,5 + 19,7 = 35 comparaciones, casi el triple, y se pagaría en cada consulta.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué mide el IDF de un término y por qué importa?
o: Cuantas veces aparece el término dentro de un documento concreto
o: En cuántos documentos distintos aparece: cuanto más raro es, más discrimina y más pesa en la puntuación
o: La longitud media de los documentos que contienen el término
a: 2
e: La frecuencia de documento df(t) cuenta documentos, no apariciones. Un término que está en todos los documentos no ayuda a elegir; uno que está en 3 de un millón es casi un identificador. El IDF convierte esa rareza en un peso, y es la razón de que las palabras vacías se eliminen del índice.
:::

:::quiz
p: Un documento repite la palabra buscada 50 veces. ¿Cuánto sube su puntuación BM25 respecto a un documento donde aparece una vez, en igualdad de longitud?
o: Cincuenta veces, proporcional al número de apariciones
o: Como mucho un factor de k₁ + 1, porque la contribución de la frecuencia se satura
o: Nada, porque BM25 ignora la frecuencia del término
a: 2
e: El factor f·(k₁+1)/(f + k₁·...) tiende a k₁+1 cuando f crece. Con k₁ = 1,2 el techo es 2,2, así que repetir en exceso no sirve para escalar posiciones. Si BM25 ignorara la frecuencia, el factor sería constante y no habría saturación.
:::

:::aviso
Un índice invertido no es gratis: hay que construirlo, ocupa espacio y hay que mantenerlo al día
cuando los documentos cambian. En un sistema con escrituras continuas, el coste dominante no es
la consulta, es la indexación y la reindexación. Antes de montar un motor de búsqueda, pregúntate
si un `LIKE`, una tabla de agregados o un [[tries]] de prefijos no resuelven tu caso con una
fracción del coste.
:::
