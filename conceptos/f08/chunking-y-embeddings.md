---
id: chunking-y-embeddings
titulo: Troceado y embeddings
fase: 8
nivel: avanzado
rutas: [ds]
prerequisitos: [rag-arquitectura, embeddings, tokenizacion, producto-punto-y-similitud, norma-y-distancias]
tags: [rag, embeddings, recuperacion, texto]
resumen: Como se corta el texto antes de vectorizarlo: tamaño de fragmento, solapamiento y por qué la frontera elegida decide lo que el buscador no encontrará.
fuentes: ["Manning, Raghavan y Schütze (2008), 'Introduction to Information Retrieval'"]
---

## En una frase

Trocear es decidir en qué pedazos se parte un documento para convertirlos en vectores, y esa
decisión decide la recuperación: un fragmento demasiado grande diluye el tema entre diez
asuntos, uno demasiado pequeño pierde el contexto, y una frontera mal puesta parte en dos la
única frase que respondía a la pregunta.

## La idea

Piensa en una enciclopedia de 200 páginas. Alguien te pregunta por el procedimiento de
devolución. Si le entregas el tomo entero, el resumen que haga de él hablará de todo un poco
y de devoluciones casi nada. Si le entregas frases sueltas, ninguna dirá «el plazo es de 30
días» porque esa frase se apoya en la anterior. Lo útil es entregarle la sección: un trozo
que trata de una cosa y se entiende solo.

Un **fragmento** (en inglés, *chunk*) es exactamente eso, y el **embedding** de ese fragmento
es un vector de números que lo representa, de forma que dos textos que hablan de lo mismo
acaban cerca. Cuando llega una pregunta, se vectoriza con el mismo modelo y se buscan los
fragmentos cuyo vector está más cerca del de la pregunta. Toda la maquinaria de
[[producto-punto-y-similitud|similitud del coseno]] y [[norma-y-distancias|distancias]] que
ya conoces se aplica aquí tal cual.

El problema es que un documento no viene troceado. Y tú no puedes partir 40 páginas en
fragmentos sin decidir tres cosas: **cuánto mide cada fragmento**, **cuánto se solapan** y
**dónde cortas exactamente**. Las tres tienen consecuencias medibles.

El tamaño es un compromiso. Un fragmento de 1.500 tokens habla de cuatro o cinco cosas, y su
embedding es el promedio borroso de todas: sirve para «temas generales», falla para preguntas
concretas. Un fragmento de 50 tokens («el plazo es de 30 días») es preciso pero huérfano: no
dice de qué plazo ni de qué producto. En la práctica se trabaja entre 200 y 800 tokens, y se
elige midiendo, no por gusto.

El solapamiento resuelve un fallo muy concreto: si partes el texto cada 300 tokens a ciegas,
tarde o temprano cortas una frase por la mitad. Las dos mitades quedan en fragmentos
distintos y ninguna de las dos contiene la frase completa. Si repites los últimos 50 tokens
al principio del fragmento siguiente, la frase vuelve a estar entera en algún sitio. El
precio es obvio: más fragmentos, más vectores, más almacenamiento y más candidatos repetidos
en los resultados.

Y la frontera importa tanto como el tamaño. Cortar por párrafos, por secciones o por filas de
una tabla respeta la estructura del documento; cortar cada 300 caracteres la destruye. Una
tabla partida en dos fragmentos ya no dice nada: la cabecera con los nombres de columna se
queda en un trozo y los números en otro.

Esto no es un detalle de implementación, es el punto donde fallan la mayoría de los sistemas
de [[rag-arquitectura|RAG]] que funcionan «regular»: si el fragmento correcto nunca entra en
la lista de candidatos, ningún modelo generador puede arreglarlo después.

## Definición formal

Un documento `D` es una secuencia de `N` [[tokenizacion|tokens]] `t₁, t₂, …, t_N`. Un troceado
queda definido por tres parámetros:

:::formula
ventana w (tokens) · salto s (tokens) · solapamiento r = w − s
:::

- `w` — número de tokens de cada fragmento.
- `s` — desplazamiento entre el inicio de un fragmento y el del siguiente, `1 ≤ s ≤ w`.
- `r = w − s` — tokens que comparten dos fragmentos consecutivos. Con `s = w` no hay
  solapamiento.

El fragmento `k`-ésimo (empezando en `k = 0`) es:

:::formula
C_k = ( t_(k·s + 1), …, t_(min(k·s + w, N)) )
:::

y el número total de fragmentos es `⌈N / s⌉`, que con solapamiento es siempre mayor que
`⌈N / w⌉`. Ese cociente es el **factor de duplicación**: si `w = 300` y `s = 240`, produces un
25 % más de vectores que sin solapamiento.

Un modelo de embeddings `f` es una función que lleva texto a un vector:
`v = f(C) ∈ ℝ^d`, con `d` la dimensión (típicamente entre 384 y 3.072). La relevancia entre
una consulta `q` y un fragmento `C` se mide con la similitud del coseno:

:::formula
sim(q, C) = ( f(q) · f(C) ) / ( ‖f(q)‖ · ‖f(C)‖ )
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `w` | Tokens de cada fragmento (la ventana) | tokens | Cada vector promedia más asuntos: gana en preguntas generales y pierde en las concretas. El límite duro es el máximo de tokens de entrada del modelo |
| `s` | Desplazamiento entre el inicio de un fragmento y el del siguiente | tokens | Con `s` grande produces menos vectores y más baratos, pero más frases cortadas por la mitad. `s = w` es «sin solapamiento» |
| `r = w − s` | Tokens que comparten dos fragmentos consecutivos | tokens | Repara las fronteras y multiplica el almacenamiento. Pasar del 10 % al 50 % de `w` duplica los vectores y devuelve el mismo párrafo dos veces en los candidatos |
| `N` | Longitud del documento en tokens | tokens | El número de fragmentos es `⌈N/s⌉`, no `⌈N/w⌉`: dividir `s` entre dos casi duplica los vectores |
| `k` | Cuántos fragmentos devuelve la búsqueda | fragmentos | Ensancha el techo (`recall@k`) y también el ruido que llega al generador; se elige con presupuesto de contexto |
| `recall@k` | Fracción de fragmentos relevantes que aparecen entre los `k` primeros | entre 0 y 1 | Es el techo del sistema. Un troceado que parte la respuesta en dos lo baja aunque el modelo de embeddings sea excelente |
:::

donde `·` es el producto escalar y `‖·‖` la norma euclídea. La recuperación devuelve los `k`
fragmentos con mayor `sim`, y la calidad de ese ranking se mide con `recall@k`: la fracción de
fragmentos verdaderamente relevantes que aparecen entre los `k` devueltos. Si el troceado
parte en dos el fragmento relevante, `recall@k` baja aunque el modelo de embeddings sea
excelente, porque la información ya no está entera en ningún vector.

## Ejemplo

Documento de 137 caracteres: «La factura se emite el dia 1. El plazo de pago es de 30 dias
desde la fecha de emisión. Los pagos tardios devengan un interes del 3,75 %.» Con un corte
ciego cada `w = 34` caracteres y sin solapamiento salen 5 fragmentos:

```
"La factura se emite el dia 1. El p"   "lazo de pago es de 30 dias desde l"
"a fecha de emision. Los pagos tard"   "ios devengan un interes del 3,75 %"
"."
```

Cada palabra que cae justo en una frontera queda partida: «plazo» aparece como `p` + `lazo`,
«los» como `l` + `os`. Y la frase que importa («interes del 3,75 %») queda con «interes» en el
cuarto fragmento y «del 3,75 %» en el mismo, sí, pero cualquier consulta que use las dos
palabras cortadas no encuentra nada: **ninguno de los cinco fragmentos contiene «plazo» ni
«los» como palabra completa**.

Con `w = 34` y `s = 24` (solapamiento `r = 10`) salen 6 fragmentos en vez de 5, y ahora:

- El segundo fragmento es `"ia 1. El plazo de pago es de 30 di"`: recupera «plazo» entero.
- El cuarto es `"cha de emision. Los pagos tardios "`: recupera «Los» y «pagos tardios».
- El quinto es `"s tardios devengan un interes del "`: recupera «interes» y su contexto.
- La similitud de la consulta «interes por pagos tardios» con el mejor fragmento pasa de
  **0,105 a 0,342**, más del triple, sin haber tocado el modelo de embeddings. Y el fragmento
  ganador cambia de identidad: sin solapar gana «a fecha de emisión. Los pagos tard» —que no
  contiene «pagos tardios» completo— y con solape gana el que sí la lleva entera.

Es decir: el solapamiento no mejora el modelo, mejora las *fronteras*. Y se paga en vectores.

## Código

El bloque siguiente reproduce el ejemplo con un embedding por dispersión (*hashing trick*):
cada palabra y cada bigrama se asigna de forma determinista a una posición de un vector de
256 dimensiones. No es un modelo semántico —no entiende sinónimos—, pero sirve para medir el
efecto del troceado sin descargar nada.

```python verificable
import numpy as np

DIM = 256

def posicion(pieza, dim=DIM):
    """Hash propio y determinista: el mismo numero en cada ejecucion y en cada maquina.
    El hash() de Python no sirve aqui porque cambia de un proceso a otro."""
    valor = 0
    for letra in pieza:
        valor = (valor * 31 + ord(letra)) % dim   # el modulo deja el resultado dentro del vector
    return valor

def embedding(texto):
    """Embedding disperso determinista: suma un 1 por palabra y por bigrama."""
    # .lower() borra las mayusculas: "El" y "el" acaban en el mismo vector
    palabras = texto.lower().split()
    # bigramas con guion bajo: "pagos tardios" -> "pagos_tardios", asi se conserva algo de orden
    piezas = list(palabras) + [a + "_" + b for a, b in zip(palabras, palabras[1:])]
    v = np.zeros(DIM)
    for p in piezas:
        v[posicion(p)] += 1.0            # dos palabras distintas pueden caer en la misma casilla
    return v

def similitud(a, b):
    # norm() es la raiz de la suma de cuadrados: el denominador del coseno
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    # si un vector es todo ceros la division daria nan, y nan contamina cualquier max()
    return float(a @ b / (na * nb)) if na and nb else 0.0

def trocear(texto, w, s):
    # el rango avanza de s en s: el tamano de cada trozo es w y el salto es s, no son lo mismo
    return [texto[i:i + w] for i in range(0, len(texto), s)]

doc = ("La factura se emite el dia 1. El plazo de pago es de 30 dias "
       "desde la fecha de emision. Los pagos tardios devengan un interes del 3,75 %.")
consulta = embedding("interes por pagos tardios")

for nombre, s in (("sin solape", 34), ("con solape", 24)):
    trozos = trocear(doc, 34, s)
    # max() recorre los trozos y se queda con el mas parecido: asi se simula el top-1
    mejor = max(similitud(consulta, embedding(t)) for t in trozos)
    print(f"{nombre:12s} fragmentos {len(trozos):>2}  mejor similitud {mejor:.3f}")
```

:::claves
- `posicion()` comprime cualquier palabra a una de las 256 posiciones: es la *hashing trick*. Con 256 huecos y decenas de términos hay **colisiones** (dos palabras distintas en la misma posición suman sus cuentas), y por eso los modelos reales usan 384-3.072 dimensiones.
- `posicion()` es un hash **propio**, no el `hash()` de Python: el de Python cambia en cada ejecución (por seguridad, para que nadie pueda forzar colisiones), y un programa con él imprimiría un número distinto cada vez. Fíjate en que aquí no se usa `hash()` en ninguna línea.
- `texto.lower().split()` tira la puntuación y el orden de las palabras: **no entiende sinónimos ni niega nada**. «pagos tardíos» y «pagos no tardíos» dan vectores casi idénticos. Es un truco para medir el troceado sin descargar un modelo, no un buscador semántico.
- `trocear(texto, w, s)` **no recorta al final**: el último trozo puede salir más corto que `w`, y con `range(0, len(texto), s)` el número de trozos es `⌈N/s⌉`, no `⌈N/w⌉`. Copiar `w` en el sitio de `s` da un rendimiento distinto sin dar ningún error.
- Los trozos son **solapamientos del mismo texto**, así que el mismo párrafo se vectoriza y se almacena dos veces. Con `w = 34` y `s = 24` pasas de 5 a 6 fragmentos: un 20 % más de vectores y de almacenamiento, a cambio de que la frase clave quede entera.
- `similitud()` devuelve un `float` de Python, no un array de NumPy: `a @ b` da un escalar 0-d y `float()` lo convierte. Sin esa conversión, comparar dos resultados con `==` funciona igual, pero imprimirlos o meterlos en un JSON falla.
- `max(... for t in trozos)` compara las similitudes y devuelve **la mayor**, no el fragmento ganador. Si necesitas citar la fuente, hay que quedarse con el trozo: `max(trozos, key=lambda t: similitud(consulta, embedding(t)))`.
:::

```python verificable
# La frontera, medida: cuantos fragmentos contienen la frase clave entera.
doc = ("La factura se emite el dia 1. El plazo de pago es de 30 dias "
       "desde la fecha de emision. Los pagos tardios devengan un interes del 3,75 %.")
frase_clave = "pagos tardios"

def trocear(texto, w, s):
    return [texto[i:i + w] for i in range(0, len(texto), s)]

def integros(trozos, frase):
    # sum() sobre booleanos cuenta los True: asi se cuenta en cuantos trozos aparece la frase
    return sum(frase in t for t in trozos)

print("documento con", len(doc), "caracteres")
for s in (34, 24):
    trozos = trocear(doc, 34, s)
    print(f"salto {s}: {len(trozos)} fragmentos, "
          f"{integros(trozos, frase_clave)} conservan la frase entera")
# salto 24 (solapamiento 10) recupera la frase; salto 34 la parte entre dos fragmentos
```

:::figura
fichero: chunking-frontera-y-tamano
pie: A la izquierda, cuántos fragmentos conservan entera la frase clave «pagos tardíos» con un salto de 34 caracteres (solapamiento 0) y con uno de 24 (solapamiento 10): sin solapar, ninguno de los 5 fragmentos la contiene completa, y ninguna consulta que use esas dos palabras puede recuperarla. A la derecha, el otro extremo del compromiso, medido con la frase «interes del 3,75 %»: al crecer la ventana la similitud con la consulta sube —el fragmento incluye por fin la palabra que responde—, llega a un máximo y vuelve a bajar, porque un trozo grande reparte su vector entre varios asuntos. Por debajo de 20 caracteres el mejor fragmento ni siquiera contiene el término buscado. El tamaño bueno no es el mayor ni el menor: es el que se mide.
fuente: figuras/chunking-y-embeddings-1.py
:::

## Errores típicos

- **Elegir el tamaño de fragmento por costumbre (512, 1000, «lo que salga»).** El tamaño
  correcto depende del corpus y de las preguntas: en un manual de procedimientos, preguntas
  concretas piden fragmentos de 200-400 tokens; en actas de reuniones, de 800. Se decide
  midiendo `recall@k` sobre un conjunto de preguntas con respuesta conocida, no copiando un
  número de un tutorial.
- **Solapar mucho «por seguridad».** Un solapamiento del 50 % duplica el almacenamiento y
  devuelve el mismo párrafo dos veces en la lista de candidatos, gastando cupo de contexto en
  información repetida. Entre el 10 % y el 20 % de `w` cubre la mayoría de los casos.
- **Cortar a ciegas cada N caracteres en documentos con estructura.** Una tabla, un bloque de
  código o una lista numerada partidos por la mitad quedan inservibles. Corta por párrafos,
  secciones o encabezados, y usa el tamaño solo como límite máximo.
- **Vectorizar el documento entero y llamarlo fragmento.** Un embedding de 40 páginas es un
  promedio de todo: se parece un poco a todo y mucho a nada, y su similitud con cualquier
  consulta concreta es mediocre.
- **Guardar los vectores sin la procedencia.** Si el fragmento no lleva metadatos (documento,
  sección, fecha, página), no puedes citar la fuente ni filtrar por ella, y la respuesta del
  generador queda sin forma de verificarse.
- **Trocear primero y elegir el modelo después.** Cada modelo de [[embeddings|embeddings]]
  tiene su propio límite de tokens de entrada y su propio vocabulario. Un fragmento de 1.200
  tokens se trunca en silencio en un modelo que admite 512: has vectorizado solo la primera
  mitad sin enterarte.

:::trampa
Cambiar de modelo de embeddings obliga a revectorizar todo el corpus. Los vectores de dos
modelos distintos no son comparables entre sí, aunque tengan la misma dimensión: mezclarlos
en el mismo índice devuelve resultados sin ningún sentido.
:::

## Comprueba que lo sabes

:::quiz
p: Con fragmentos de 300 tokens y un salto de 240, ¿cuál es el solapamiento y cuántos vectores produces de media por cada 300 tokens de texto?
o: Solapamiento 0 y exactamente un vector por cada 300 tokens
o: Solapamiento 60 tokens y un 25 % más de vectores que sin solapar
o: Solapamiento 240 tokens y un 80 % más de vectores que sin solapar
a: 2
e: El solapamiento es w − s = 300 − 240 = 60 tokens. El salto es 240 en lugar de 300, así que el número de fragmentos crece en la proporción 300/240 = 1,25, es decir un 25 % más. El solapamiento no puede ser 240 porque entonces s = 60 y el crecimiento sería mucho mayor.
:::

:::quiz
p: El buscador devuelve fragmentos que hablan del tema general pero nunca la frase exacta que responde a la pregunta. ¿Qué es lo primero que revisas?
o: La temperatura del modelo generador
o: El tamaño de los fragmentos, porque uno muy grande promedia varios temas y diluye el concreto
o: El número de réplicas del índice vectorial
a: 2
e: Cuando se recupera el tema pero no el detalle, la causa habitual es que el fragmento es demasiado grande y su vector representa el promedio de varios asuntos. Reducir w y medir recall@k es el primer experimento. El muestreo del generador no cambia lo que entra en la lista de candidatos, y las réplicas del índice solo afectan a la disponibilidad.
:::

:::quiz
p: ¿Por qué no se pueden mezclar en un mismo índice los vectores de dos modelos de embeddings distintos?
o: Porque ocupan dimensiones distintas de memoria
o: Porque cada modelo define su propio espacio: un mismo vector no significa lo mismo en los dos, y las similitudes entre ellos no son comparables
o: Porque el índice solo admite vectores de modelos de la misma versión
a: 2
e: Aunque los dos den 768 dimensiones, cada modelo ha aprendido su propia geometría: la dirección que codifica «facturación» en uno no tiene por qué ser la misma en el otro, así que la distancia entre un vector de un modelo y otro del segundo no mide nada. Lo correcto es revectorizar todo el corpus con un único modelo.
:::
