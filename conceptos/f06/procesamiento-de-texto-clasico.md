---
id: procesamiento-de-texto-clasico
titulo: Procesamiento de texto clásico
fase: 6
nivel: intermedio
rutas: [ds, de]
prerequisitos: [regex-y-limpieza-de-texto, naive-bayes]
tags: [nlp, tf-idf, bolsa-de-palabras, clasificacion]
resumen: Contar palabras y ponderarlas por lo raras que son sigue ganando en textos cortos, tabulares o con pocos datos; el truco está en saber qué se pierde al hacerlo.
fuentes: ["Manning, Raghavan y Schütze (2008), 'Introduction to Information Retrieval'", "Salton y Buckley (1988), 'Term-Weighting Approaches in Automatic Text Retrieval'"]
---

## En una frase

La bolsa de palabras convierte un texto en un vector de recuentos —ignorando el orden— y TF-IDF
pondera cada palabra por lo informativa que es, con lo que un clasificador sencillo resuelve
bien muchos problemas de texto sin necesidad de redes neuronales.

## La idea

Clasificar un correo como spam o no, etiquetar una reseña como positiva o negativa, separar
tickets de soporte por categoría: la mayoría de estos problemas tienen textos cortos, categorías
claras y un vocabulario repetitivo. En ese terreno, un modelo que solo cuenta palabras suele
igualar a un transformer, tarda milisegundos y se puede explicar línea a línea.

La trampa del «solo cuenta palabras» es evidente: si tiras el orden, `no es bueno` y `es no
bueno` son la misma bolsa, y también lo son `el perro muerde al hombre` y `el hombre muerde al
perro`. Pero, contra la intuición, eso no suele arruinar el resultado, por dos motivos:

1. **En clasificación bastan pocas señales fuertes.** Para separar quejas de felicitaciones,
   `devolucion`, `roto` y `tarde` pesan mucho más que el orden gramatical.
2. **TF-IDF compensa la frecuencia.** Si solo contaras palabras, las más comunes (`de`, `la`,
   `que`) dominarían todo. TF-IDF divide cada recuento por la frecuencia con la que la palabra
   aparece en el conjunto de documentos, así que una palabra que sale en todos los documentos
   vale casi cero y una que sale en pocos vale mucho.

Donde se queda corto, y conviene decirlo antes de invertir tiempo: cuando el significado depende
del contexto (ironía, negación matizada), cuando hay muchos sinónimos que el modelo trata como
palabras distintas, cuando el idioma tiene morfología rica sin lematizar, y cuando los textos
son largos y el orden importa. Ahí es donde entran los [[embeddings]] y los [[transformers]].

## Definición formal

Con un vocabulario `V` de `|V|` términos extraído del corpus y un documento `d`:

**Frecuencia de término** (la forma más simple, presencia o recuento):

:::formula
tf(t, d) = número de veces que el término t aparece en d
:::

**Frecuencia inversa de documento**, en la versión suavizada que usa scikit-learn:

:::formula
idf(t) = ln( (1 + n) / (1 + df(t)) ) + 1
:::

- `n` — número de documentos del corpus.
- `df(t)` — número de documentos que contienen `t` al menos una vez.
- El `+1` del numerador, el del denominador y el `+1` final evitan divisiones por cero y que un
  término presente en todos los documentos tenga `idf = 0` (todavía valdría 1, no 0).
- La `idf` **se calcula sobre el corpus de entrenamiento**, y ese es el origen de una fuga de
  datos muy común: si la calculas con todo el conjunto, el vocabulario y los pesos ya saben algo
  del conjunto de prueba.

**Ponderación y normalización:**

:::formula
tfidf(t, d) = tf(t, d) · idf(t)        w(t, d) = tfidf(t, d) / √( Σ_{t'} tfidf(t', d)² )
:::

- `w(t, d)` — el peso final, tras normalizar el vector a longitud 1 (norma L2).
- La normalización es lo que permite comparar documentos largos con cortos: sin ella, un
  documento el doble de largo tendría todos los pesos el doble de grandes.

**Similitud entre dos documentos** es el coseno de sus vectores normalizados, que con vectores
de norma 1 es simplemente su producto escalar: `cos(d₁, d₂) = Σ_t w(t, d₁) · w(t, d₂)`.

**BM25**, el estándar en recuperación, mejora TF-IDF con dos correcciones: satura el recuento
(la décima aparición de una palabra aporta mucho menos que la segunda) y normaliza por la
longitud del documento:

:::formula
BM25(q, d) = Σ_{t ∈ q} idf(t) · f(t, d)·(k₁ + 1) / ( f(t, d) + k₁·(1 − b + b·len(d)/avg_len) )
:::

- `f(t, d)` — frecuencia del término en el documento; `len(d)` su longitud en palabras.
- `avg_len` — longitud media de los documentos del corpus.
- `k₁` — controla la saturación, típicamente entre 1,2 y 2,0.
- `b` — peso de la normalización por longitud, 0,75 por convenio; `b = 0` la desactiva.

**Clasificador de referencia.** Con [[naive-bayes]] multinomial y suavizado de Laplace `α`:

:::formula
log P(c | d) ∝ log P(c) + Σ_t f(t, d) · log( (N_tc + α) / (N_c + α·|V|) )
:::

- `N_tc` — veces que el término `t` aparece en documentos de la clase `c`.
- `N_c` — total de términos de la clase `c`; `α = 1` es el suavizado habitual.
- Se elige la clase con mayor valor. Es un modelo lineal, así que se entrena en segundos y se
  inspeccionan sus coeficientes.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `tf(t, d)` | Veces que el término `t` aparece en el documento `d` | apariciones | El término pesa más en ese documento, pero de forma lineal: la décima aparición cuenta igual que la segunda, y ahí es donde BM25 mejora a TF-IDF |
| `df(t)` | Número de documentos del corpus que contienen `t` al menos una vez | documentos | La `idf` baja: la palabra es menos informativa porque está por todas partes. Es el contrapeso del recuento |
| `n` | Número de documentos del corpus | documentos | Con más documentos, la `idf` de un término raro crece (hay más donde destacar) y la de uno común apenas cambia: el suelo lo pone el suavizado |
| `idf(t)` | Peso inverso a la frecuencia de documento: `ln((1 + n)/(1 + df)) + 1` | adimensional | Con `df` alto baja hasta 1 (nunca a 0); con `df = 1` llega a su máximo. Es el factor que decide qué palabras mandan |
| `w(t, d)` | Peso final del término en el documento, ya normalizado a norma L2 | adimensional | Cuanto mayor, más pesa ese término al comparar dos documentos; pero al normalizar, subir un peso baja todos los demás del mismo vector |
| `len(d)` y `avg_len` | Longitud del documento y longitud media del corpus | palabras | En BM25, un documento más largo que la media penaliza: sube `len(d)/avg_len` y el denominador, así que el término vale menos |
| `k₁` (BM25) | Cuánto satura el recuento de apariciones | adimensional | Con `k₁` alto, la décima aparición sigue sumando casi como la segunda; el valor habitual está entre 1,2 y 2,0 |
| `b` (BM25) | Cuánto se corrige por la longitud del documento | adimensional (0 a 1) | `b = 0` desactiva la corrección y favorece los documentos largos; `b = 1` la aplica entera. El convenio es 0,75 |
| `α` (Naive Bayes) | Suavizado de Laplace del clasificador de texto | adimensional | Con `α` mayor, las probabilidades se acercan entre sí y el modelo se vuelve más conservador: menos sobreajuste y menos señal en vocabularios grandes |
:::

## Ejemplo

Tres documentos diminutos:

```
d1: el gato duerme
d2: el perro duerme
d3: el gato come
```

El vocabulario es `{come, duerme, el, gato, perro}`. Las frecuencias de documento son
`df(el) = 3`, `df(gato) = 2`, `df(duerme) = 2`, `df(perro) = 1`, `df(come) = 1`. Con `n = 3`,
aplicando la fórmula suavizada:

- `idf(el) = ln(4/4) + 1 = 1,000`.
- `idf(gato) = ln(4/3) + 1 = 1,288`, igual que `idf(duerme)`.
- `idf(perro) = ln(4/2) + 1 = 1,693`, igual que `idf(come)`.

El documento `d1` tiene `tf = 1` en `el`, `gato` y `duerme`, así que sus pesos sin normalizar son
`1,000`, `1,288` y `1,288`. La norma del vector es `√(1,000² + 1,288² + 1,288²) = 2,078`, y al
dividir quedan `0,481`, `0,620` y `0,620`. Ahora las similitudes por coseno:

- `cos(d1, d2) = 0,5443`. Comparten `el` y `duerme`.
- `cos(d1, d3) = 0,5443`. Comparten `el` y `gato`.
- `cos(d2, d3) = 0,1810`. Solo comparten `el`.

El resultado incómodo está en las dos primeras: el modelo considera **exactamente igual de
parecidos** los pares que comparten «duerme» y los que comparten «gato», porque ambas palabras
tienen la misma `idf`. No sabe que un gato y un perro son más parecidos entre sí que un gato y
la acción de dormir. Una bolsa de palabras no tiene semántica: solo tiene coincidencias.

:::figura
fichero: texto-idf-y-pesos
pie: El panel izquierdo es la fórmula de la idf dibujada: cae muy rápido al principio y solo se aplana al final. Lo que hay que retener es dónde acaba. Una palabra que aparece en un solo documento de los 1 000 vale 7,22; una que aparece en todos sigue valiendo 1, no 0, gracias a los dos +1 del suavizado. Ese factor, y no el recuento, es el que decide qué palabras mandan. El panel derecho lo lleva al caso práctico: en un documento con cinco «el», dos «devolución», un «roto» y un «tarde», contar palabras deja a «el» como lo más importante (0,56) y no distingue nada; con tf-idf normalizado, «el» baja a 0,48 y «devolución» sube a 0,80, porque es la que separa una queja de una felicitación. La conclusión operativa es que puedes leer las palabras con más peso de cada clase y decidir si el modelo está usando la señal del problema o un atajo del corpus; es la comprobación más barata que hay en texto y la que más veces salva un proyecto.
fuente: figuras/procesamiento-de-texto-clasico-1.py
:::

## Código

```python verificable
import math
from collections import Counter

documentos = ["el gato duerme", "el perro duerme", "el gato come"]
cestas = [d.split() for d in documentos]
n = len(cestas)

# Frecuencia inversa de documento, con el suavizado habitual.
df = Counter(t for c in cestas for t in set(c))     # set(c): cuenta documentos, no repeticiones
idf = {t: math.log((1 + n) / (1 + df[t])) + 1 for t in df}    # math.log es neperiano
print("idf:", {t: round(v, 4) for t, v in sorted(idf.items())})
# -> {'come': 1.6931, 'duerme': 1.2877, 'el': 1.0, 'gato': 1.2877, 'perro': 1.6931}

def vector(documento):
    """Pesos tf-idf del documento, normalizados a norma 1."""
    cuenta = Counter(documento.split())
    v = {t: cuenta[t] * idf[t] for t in cuenta}     # solo las palabras que estan: vector disperso
    norma = math.sqrt(sum(x ** 2 for x in v.values()))   # norma L2, para comparar largos y cortos
    return {t: round(x / norma, 4) for t, x in v.items()}

def coseno(a, b):
    """Con vectores de norma 1, el coseno es el producto escalar."""
    return sum(v * b.get(t, 0.0) for t, v in a.items())   # get: la palabra ausente vale 0

print("tf-idf doc1:", vector(documentos[0]))
# -> {'el': 0.4813, 'gato': 0.6198, 'duerme': 0.6198}

d1, d2, d3 = (vector(d) for d in documentos)
print("coseno doc1-doc2:", round(coseno(d1, d2), 4),
      "doc1-doc3:", round(coseno(d1, d3), 4),
      "doc2-doc3:", round(coseno(d2, d3), 4))
# -> coseno doc1-doc2: 0.5443 doc1-doc3: 0.5443 doc2-doc3: 0.181
```

:::claves
- `df = Counter(t for c in cestas for t in set(c))` cuenta en cuántos **documentos** aparece cada
  término: el `set(c)` elimina las repeticiones dentro del mismo documento. Sin ese `set`, `df`
  contaría apariciones totales y la `idf` saldría mal: sería una frecuencia de colección con el
  nombre de otra cosa.
- `math.log` es el logaritmo **neperiano**, que es lo que dice la fórmula. Cambiar a `math.log10` o
  a `np.log2` no rompe nada, pero todos los pesos cambian de escala a la vez: el orden se mantiene
  y los números no, así que dos resultados calculados con bases distintas no son comparables.
- `v = {t: cuenta[t] * idf[t] for t in cuenta}` recorre las palabras **del documento**, no el
  vocabulario entero: el vector es disperso y las ausentes valen 0 sin ocupar sitio. Por eso
  `coseno()` usa `b.get(t, 0.0)`: una palabra que no está no da `KeyError`, aporta cero. Con un
  vocabulario de 50.000 términos y documentos de 200 palabras, esa diferencia es la que hace que
  todo funcione en memoria.
- `norma = math.sqrt(sum(x ** 2 for x in v.values()))` es la norma L2 y dividir por ella deja el
  vector de longitud 1. Sin esa división, un documento el doble de largo tiene todos los pesos el
  doble de grandes y gana todas las similitudes: el coseno se convierte en una medida de longitud.
- `round(x / norma, 4)` redondea **dentro del diccionario que se devuelve**, no solo al imprimir:
  las similitudes de la última línea se calculan con los pesos ya redondeados. Es un redondeo que
  afecta al resultado (0,5443 en lugar de 0,54427…); si necesitas precisión, redondea al imprimir y
  no al construir el vector.
- `vocabulario(documentos, 2)` genera unigramas **y** bigramas por el `range(1, tam + 1)`, y con dos
  frases pasa de 5 variables a 10. Es la primera señal de por qué los n-gramas encarecen el modelo:
  cada palabra nueva se multiplica por las que pueden seguirla, y con 50.000 términos el bigrama
  posible es una cifra de nueve dígitos.
:::

```python verificable
# Dos frases que significan lo contrario y solo se diferencian en un "no".
documentos = ["la pelicula es buena", "la pelicula no es buena"]

def vocabulario(documentos, tam):
    """tam=1 devuelve unigramas; tam=2, unigramas y bigramas."""
    terminos = set()
    for d in documentos:
        palabras = d.split()
        for t in range(1, tam + 1):
            terminos.update(tuple(palabras[i:i + t]) for i in range(len(palabras) - t + 1))
    return sorted(" ".join(t) for t in terminos)     # la tupla se une con espacios: "pelicula no"

unigramas = vocabulario(documentos, 1)
print("unigramas:", unigramas)
# -> unigramas: ['buena', 'es', 'la', 'no', 'pelicula']
print("recuento de cada frase:", [[d.split().count(t) for t in unigramas] for d in documentos])
# -> recuento de cada frase: [[1, 1, 1, 0, 1], [1, 1, 1, 1, 1]]

con_bigramas = vocabulario(documentos, 2)
print("variables con bigramas:", len(con_bigramas))       # -> 10
print("aparece 'pelicula no':", "pelicula no" in con_bigramas)   # -> True
```

Los dos vectores de unigramas son idénticos salvo por la posición del `no`: para el modelo, la
segunda frase es la primera **más** una palabra, y si esa palabra no está en la lista de
términos que discriminan, las dos se clasifican igual. Con bigramas aparece la variable
`pelicula no`, que sí distingue. El precio es que el vocabulario crece: aquí pasa de 5 variables
a 10 con solo dos frases, y en un corpus real cada palabra nueva se multiplica por las que
pueden seguirla.

## Errores típicos

- **Eliminar las negaciones con la lista de palabras vacías.** Algunas listas de *stopwords* en
  español incluyen `no` y `sin`. Borrarlas hace que `no recomiendo` y `recomiendo` sean lo
  mismo. Revisa la lista antes de usarla y quita esas palabras.
- **Ajustar el vectorizador con todos los datos antes de dividir.** Si calculas el vocabulario y
  la `idf` con el conjunto completo y luego separas en entrenamiento y prueba, ya has filtrado
  información del test. El vectorizador va **dentro** del [[pipelines-de-ml|pipeline]], ajustado
  solo con el entrenamiento.
- **Meter texto crudo sin limpiar.** Etiquetas HTML, firmas de correo, números de ticket y
  cabeceras repetidas generan variables que el modelo usa como atajos y que no existirán en
  producción. Limpia antes y revisa las variables con más peso.
- **Confundir stemming con lematización.** Un *stemmer* corta sufijos y produce raíces que no son
  palabras (`corriendo` y `correr` pueden acabar igual, pero también `caso` y `casa`); un
  lematizador necesita diccionario y etiquetas gramaticales. En español, con textos cortos,
  muchas veces compensa no hacer ninguna de las dos cosas.
- **Usar exactitud con clases desbalanceadas.** Con un 2 % de quejas, un modelo que siempre dice
  «no es queja» acierta el 98 %. Mira [[precision-recall-y-pr]] y elige el umbral por coste.
- **Suponer que la bolsa de palabras entiende el orden.** `no me gusta nada` y `me gusta todo`
  comparten `me` y `gusta`, y sin normalizar los vectores el documento más largo gana en todas
  las similitudes. Si el orden importa, usa n-gramas (que capturan un poco de contexto local) o
  directamente un modelo secuencial.

:::practica
enunciado: 8 documentos y un vocabulario de 6.000 términos. El término `devolucion` aparece en 4 documentos. Calcula su idf suavizada y su peso final en un documento donde aparece 2 veces y cuyo vector, antes de normalizar, tiene norma 4,472.
pista: idf(t) = ln((1 + n) / (1 + df(t))) + 1. Para normalizar, divide el tf-idf entre la norma del vector del documento, que ya te dan.
solucion: idf = ln(9/5) + 1 = 0,588 + 1 = 1,588. tf-idf = 2 · 1,588 = 3,176. Peso normalizado = 3,176 / 4,472 = 0,710. La mitad del vector es ese término; si apareciera en un solo documento, su idf sería ln(9/2) + 1 = 2,504 y su peso subiría a 1,120 antes de normalizar, lo que confirma que la ponderación premia los términos raros.
:::

## Comprueba que lo sabes

:::quiz
p: En el corpus con `df(el) = 3` sobre 3 documentos, ¿por qué la idf de `el` es 1,000 y no 0?
o: Porque el término aparece muchas veces
o: Porque la fórmula suavizada suma 1 al final, y así un término presente en todos los documentos todavía conserva un peso mínimo
o: Porque la idf nunca puede valer 0
a: 2
e: Con la fórmula sin suavizar, `ln(3/3) = 0` y la palabra desaparecería del vector. La versión suavizada, `ln((1+n)/(1+df)) + 1`, da `ln(4/4) + 1 = 1`. Ese 1 es el que mantiene la palabra en el modelo con un peso bajo, en lugar de eliminarla.
:::

:::quiz
p: ¿Qué capturan los n-gramas que no captura la bolsa de palabras?
o: El significado de las palabras, porque agrupa sinónimos
o: Un poco de orden local, como que `no` va justo antes de `buena`
o: La longitud del documento
a: 2
e: Un bigrama es una pareja de palabras consecutivas, así que conserva algo de contexto inmediato y distingue `pelicula no` de `no pelicula`. Los sinónimos siguen siendo palabras distintas para el modelo, y la longitud se controla normalizando, no con n-gramas.
:::

:::quiz
p: Tienes 50.000 reseñas y quieres clasificarlas en positiva o negativa. ¿Cuándo NO bastaría TF-IDF con regresión logística?
o: Cuando las reseñas son cortas y el vocabulario se repite
o: Cuando la etiqueta depende de la ironía, del contexto de la frase o de sinónimos que nunca has visto en el entrenamiento
o: Cuando hay más de 10.000 documentos
a: 2
e: El tamaño del corpus no es el problema: TF-IDF escala bien, incluso mejor que un modelo grande. Falla cuando la señal está en el orden, el contexto o el significado y no en la presencia de palabras concretas. Ahí hacen falta embeddings contextuales o un transformer.
:::

:::truco
Antes de entrenar nada, mira las 20 variables con mayor peso del modelo para cada clase. Si
aparecen números de ticket, nombres de empleados o meses concretos, tienes fuga de datos o un
atajo que no sobrevivirá en producción. Es la comprobación más barata que existe en texto.
:::
