---
id: reranking
titulo: Reordenación
fase: 8
nivel: avanzado
rutas: [ds]
prerequisitos: [rag-arquitectura, embeddings, bases-de-datos-vectoriales, metricas-de-ranking, chunking-y-embeddings]
tags: [rag, recuperacion, ranking, cross-encoder]
resumen: Recuperar cien candidatos rápido y barato, y reordenarlos con un modelo que lee consulta y documento juntos: la forma más rentable de mejorar la recuperación.
fuentes: ["Nogueira y Cho (2019), 'Passage Re-ranking with BERT'", "Manning, Raghavan y Schütze (2008), 'Introduction to Information Retrieval'"]
---

## En una frase

La reordenación es una segunda pasada sobre los candidatos que ya devolvió el buscador: un
modelo más caro y más preciso lee la consulta y cada fragmento **juntos** y vuelve a ordenar
la lista, de modo que el fragmento correcto suba al primer puesto sin tocar el índice.

## La idea

Un buscador vectorial tiene una limitación estructural que casi nadie menciona: para poder
precalcular el vector de cada documento, tiene que resumir el documento **sin saber cuál será
la pregunta**. El vector de un fragmento es el mismo tanto si preguntas por su fecha como si
preguntas por su importe. Eso se llama **bi-codificador** (dos codificadores independientes,
uno para la consulta y otro para el documento) y es lo que hace posible comparar millones de
vectores en milisegundos.

El precio de esa independencia es que el modelo no puede ver las coincidencias exactas entre
las palabras de la pregunta y las del documento. Si preguntas «cambiar la contraseña de
acceso», un bi-codificador puntúa alto el fragmento «cambiar la contraseña de la cuenta»
(habla del mismo tema) y bajo «acceso a la cuenta y cambio de contraseña» (dice exactamente
lo mismo, en otro orden). Y si un fragmento repite «contraseña» y «acceso» cinco veces sin
responder nada, también sube.

El **codificador cruzado** (*cross-encoder*) mete la consulta y el documento en el mismo
modelo, concatenados, y devuelve una única puntuación de relevancia. Como la atención del
transformador ve las dos partes a la vez, puede valorar la coincidencia exacta de la frase,
el orden de las palabras y la estructura de la pregunta. Es mucho más preciso.

El problema es que ese modelo no puede precalcular nada: la puntuación depende de la pareja
(consulta, documento), así que hay que ejecutarlo una vez por candidato y por consulta. Con
50 documentos es viable; con 10 millones, no. De ahí la arquitectura en dos etapas:

1. **Recuperación (recall).** El índice vectorial devuelve entre 50 y 200 candidatos en
   milisegundos. En esta etapa lo que importa es no dejar fuera nada relevante.
2. **Reordenación (precisión).** El codificador cruzado puntúa esos candidatos y los ordena
   de nuevo. Con 100 candidatos, son 100 ejecuciones del modelo: unos cientos de
   milisegundos en GPU, más en CPU.

La clave mental es que las dos etapas optimizan cosas distintas. La primera se juzga con
`recall@100`: ¿está el fragmento bueno entre los candidatos? La segunda se juzga con
`precision@3` o `NDCG@3`: ¿está arriba? Mejorar la reordenación no arregla una recuperación
que nunca trajo el fragmento correcto, y mejorar la recuperación no arregla una lista
desordenada.

## Definición formal

Sea una consulta `q` y un conjunto de candidatos `C = {c₁, …, c_m}` devuelto por el
recuperador, cada uno con su puntuación de primera etapa `s₁(c)`. El reordenador es una
función `g` que asigna a cada pareja una puntuación de relevancia:

:::formula
g : (q, c) ↦ ℝ      orden final = los c ordenados por g(q, c) de mayor a menor
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `q` | La consulta del usuario | texto | Nada por sí sola: el reordenador no la vectoriza, la lee junto a cada documento |
| `c` | Un fragmento candidato de la primera etapa | texto | El coste depende de cuántos `c` haya (`m`), no de lo largos que sean. Un fragmento de 2.000 tokens cuesta más por pareja que uno de 200 |
| `g(q, c)` | La puntuación del codificador cruzado para esa pareja | un número sin unidades ni escala | Ordena, pero **no es una probabilidad**: un 0,8 no es «80 % de ser relevante». El umbral de filtrado hay que calibrarlo con datos propios |
| `m` | Candidatos que pasan al reordenador | fragmentos | Es **la** palanca de coste: el tiempo crece de forma lineal con `m`, y también el techo, porque ningún reordenador puede subir lo que la etapa 1 no trajo |
| `s₁(c)` | Puntuación de la primera etapa (coseno, BM25 o una fusión) | depende de la métrica | Determina quién entra en la lista, no en qué orden queda: para eso está `g` |
| `pos` | Posición del primer documento relevante en el orden final | posición, empezando en 1 | `MRR = 1/pos`: bajar del segundo al tercer puesto cuesta 0,17, y del décimo al undécimo casi nada. El MRR solo mira el primero |
| `k` | Documentos que se conservan tras reordenar | fragmentos | Fija el `NDCG@k`: reordenar bien 100 candidatos y quedarte con 3 hace que solo importen los 3 primeros |
:::

- `g` — el codificador cruzado. Se aplica `m` veces, una por candidato, y **no** produce un
  vector reutilizable del documento: su salida es un número, no un embedding.
- `s₁(c)` — puntuación de la primera etapa (similitud del coseno, BM25, o una combinación).
- `m` — tamaño del conjunto de candidatos; es el parámetro que gobierna el coste, porque el
  tiempo de reordenación crece de forma lineal con `m`.

La calidad del orden se mide con métricas sensibles a la posición. Las dos más usadas:

- **MRR** (*Mean Reciprocal Rank*): con `pos` la posición del primer documento relevante,
  `MRR = 1 / pos`. Si el relevante está el primero, `1`; si está el segundo, `0,5`; si no
  aparece, `0`. Se promedia sobre todas las consultas.
- **NDCG@k** (*Normalized Discounted Cumulative Gain*): suma la relevancia de cada documento
  dividida por un descuento creciente con la posición (`log₂(pos + 1)`), y normaliza por el
  valor que se obtendría con el orden perfecto. A diferencia del MRR, tiene en cuenta el
  orden de **todos** los relevantes, no solo del primero.

Una variante útil y barata: en vez de reordenar, usar `g` solo como **filtro**. Se puntúan los
candidatos y se descartan los que no llegan a un umbral; el orden se conserva. Sirve cuando lo
que duele no es el orden sino el ruido que llega al generador, pero ojo: la escala de `g` no
está calibrada, así que el umbral hay que ajustarlo con datos propios, no copiarlo.

## Ejemplo

Consulta: «cambiar la contraseña de acceso». El recuperador devuelve 5 candidatos con sus
puntuaciones de primera etapa y su relevancia real:

| Candidato | Texto | Primera etapa | Relevancia real |
| --- | --- | --- | --- |
| A | cambiar la contraseña de la cuenta | 0,81 | 2 |
| B | donde veo mi contraseña guardada | 0,79 | 1 |
| C | acceso a la cuenta y cambio de contraseña | 0,74 | 3 |
| D | recuperar la contraseña olvidada del correo | 0,72 | 0 |
| E | acceso desde el móvil y datos personales | 0,70 | 2 |

La etapa 1 devuelve A, B, C, D, E y coloca el documento realmente relevante (C) en tercera
posición: `MRR = 1/3 = 0,333`.

El codificador cruzado, que ve las dos partes juntas, da estas puntuaciones: A 17, C 4, D 4,
B 1, E 1. El orden final es A, C, D, B, E: el relevante sube a la segunda posición y
`MRR = 0,5`, un 50 % mejor en una sola pasada y sin tocar el índice ni revectorizar nada.
El top-3 pasa de `[A, B, C]` a `[A, C, D]`.

Fíjate en el empate entre C y D: el reordenador de juguete puntúa igual un documento que
responde y otro que no. Es exactamente lo que hay que vigilar en un reordenador real: además
de subir el relevante, tiene que **separar** las puntuaciones. Un modelo entrenado con
negativos difíciles produce márgenes claros donde este ejemplo produce un empate.

## Código

```python verificable
consulta = "cambiar la contrasena de acceso"

# Etapa 1: el bi-codificador ya vectorizo todo el corpus. Guardamos su puntuacion y la
# relevancia real de cada documento (3 = responde del todo, 0 = no responde).
candidatos = [
    ("A", 0.81, 2, "cambiar la contrasena de la cuenta"),
    ("B", 0.79, 1, "donde veo mi contrasena guardada"),
    ("C", 0.74, 3, "acceso a la cuenta y cambio de contrasena"),
    ("D", 0.72, 0, "recuperar la contrasena olvidada del correo"),
    ("E", 0.70, 2, "acceso desde el movil y datos personales"),
]

def pares(secuencia, n):
    # conjuntos de n-gramas: set(), para que una repeticion no cuente dos veces
    return set(tuple(secuencia[i:i + n]) for i in range(len(secuencia) - n + 1))

def codificador_cruzado(q, doc):
    # El codificador cruzado lee consulta y documento juntos: puede premiar frases exactas.
    p = doc.split()
    # suma palabras sueltas (peso 1), bigramas (2) y trigramas (3): cuanto mas larga la
    # coincidencia, mas pesa. La interseccion & de dos set() es la parte comun.
    return (sum(p.count(w) for w in q.split())
            + 2 * len(pares(q.split(), 2) & pares(p, 2))
            + 3 * len(pares(q.split(), 3) & pares(p, 3)))

etapa1 = [i for i, _, _, _ in sorted(candidatos, key=lambda c: -c[1])]
puntuaciones = {i: codificador_cruzado(consulta, t) for i, _, _, t in candidatos}
# sorted sobre un diccionario recorre sus CLAVES, y la clave es la funcion del orden
etapa2 = sorted(puntuaciones, key=lambda i: -puntuaciones[i])
relevancia = {i: r for i, _, r, _ in candidatos}

def mrr(orden):
    # la lista tiene que venir ya ordenada: la posicion es la del recorrido
    for posicion, i in enumerate(orden, 1):
        if relevancia[i] == 3:
            return 1.0 / posicion

print("etapa 1 (bi-codificador)", etapa1, " MRR", round(mrr(etapa1), 3))
print("etapa 2 (reordenacion)  ", etapa2, " MRR", round(mrr(etapa2), 3))
print("puntuaciones cruzadas", {i: puntuaciones[i] for i in etapa2})
print("top-3 antes", etapa1[:3], "despues", etapa2[:3])
# el documento C sube de la tercera a la segunda posicion solo por reordenar
```

:::claves
- `pares()` devuelve un `set`, no una lista: por eso la intersección `&` funciona y la comparación es de **n-gramas exactos**. Con dos `set` de tuplas, `&` da los que están en los dos; con listas, `&` ni siquiera existe.
- El reordenador de juguete suma coincidencias de 1, 2 y 3 palabras con pesos 1, 2 y 3. Eso premia la coincidencia larga, que es lo que hace un codificador cruzado de verdad con la atención: **no produce un vector del documento**, produce un número por pareja. Su salida no se puede guardar para reutilizarla con otra consulta.
- `sorted(candidatos, key=lambda c: -c[1])` ordena por el **segundo campo de la tupla** y el menos delante lo pone de mayor a menor. `etapa1` es una lista de letras, no de tuplas.
- `sorted(puntuaciones, ...)` recorre las **claves** del diccionario (los documentos), no los valores; la clave del orden es `puntuaciones[i]`. Si inviertes el argumento y pones `puntuaciones.values()`, te quedas sin saber a qué documento corresponde cada número.
- `mrr(orden)` devuelve `1/posición` del primer documento con relevancia 3 y **no sigue buscando**. Con cinco candidatos, estar el segundo vale 0,5 y el tercero 0,333: por eso el MRR es tan sensible a la cabeza de la lista. Si el documento bueno no está, la función devuelve `None` y cualquier media con él falla.
- Las puntuaciones del codificador cruzado del ejemplo (17, 4, 4, 1, 1) **no están calibradas ni normalizadas**: solo sirven para ordenar. Un documento que responde y otro que no empatan a 4, y ese empate es lo que hay que vigilar en un reordenador real.
:::

```python verificable
# Tiempo de consulta segun el tamano del conjunto de candidatos. Los numeros por pareja
# son hipotesis de trabajo (0,5 ms en CPU), no una medida publicada: lo que importa es la forma.
candidatos = [50, 100, 200, 500]
ms_por_pareja = 0.5
ms_recuperacion = 25.0        # busqueda en el indice vectorial, constante con m

for m in candidatos:
    # el coste del reordenador es lineal en el numero de candidatos: m ejecuciones del modelo
    reorden = m * ms_por_pareja
    # el total se imprime con formato de anchura fija para que las columnas queden alineadas
    print(f"candidatos {m:>3}  reordenar {reorden:>6.1f} ms  "
          f"total {ms_recuperacion + reorden:>6.1f} ms  "
          f"coste relativo {(ms_recuperacion + reorden) / ms_recuperacion:.1f}x")
```

:::figura
fichero: reranking-puestos-y-coste
pie: A la izquierda, la lista del ejemplo antes y después de reordenar: cada línea es un candidato y su puesto en cada etapa. En rojo, el documento que responde de verdad (C), que pasa del tercer puesto al segundo; en naranja, el documento que no responde nada (D), que sube dos puestos. Es el aviso del ejemplo: un reordenador malo sube el bueno y también el que solo lo parece, mientras B baja del segundo al cuarto. A la derecha, lo que cuesta esa segunda pasada: la recuperación es un tiempo fijo (línea de puntos, 25 ms) y la reordenación se suma encima, linealmente, medio milisegundo por candidato. Con 200 candidatos son 125 ms por consulta, cinco veces el coste de buscar. Ese es el presupuesto que se paga antes del primer token, cuando la respuesta va en streaming.
fuente: figuras/reranking-1.py
:::

## Errores típicos

- **Reordenar el corpus entero.** El codificador cruzado cuesta una ejecución del modelo por
  pareja. Aplicarlo a 10 millones de documentos son 10 millones de pasadas y decenas de horas
  por consulta. Solo se reordena lo que ya pasó el filtro de la primera etapa.
- **Reordenar demasiado poco.** Con `m = 10` candidatos, si el fragmento bueno estaba en la
  posición 15 nunca llegará al reordenador, y ningún modelo puede arreglar lo que no ve. Si el
  `recall@100` de la etapa 1 es bajo, el problema está antes: sube `m` o mejora el troceado.
- **Usar la puntuación del reordenador como probabilidad.** Las salidas de un codificador
  cruzado no están calibradas: un 0,8 no significa «80 % de probabilidad de ser relevante».
  Si necesitas un umbral, ajústalo con datos etiquetados de tu dominio.
- **Entrenar con negativos aleatorios.** Un reordenador aprende a distinguir lo bueno de lo
  malo que le pongas delante. Con negativos fáciles (documentos de otro tema) aprende a
  separar temas, no a ordenar matices. Los negativos deben salir del propio recuperador: los
  candidatos que puntúa alto y no son relevantes.
- **Olvidar el coste en el presupuesto de latencia.** Doblar `m` dobla el tiempo de
  reordenación. En una interfaz con respuesta en streaming, los milisegundos del reordenador
  se suman **antes** del primer token, así que se notan más que los del generador.
- **Reordenar y no medir.** Sin un conjunto de consultas con relevancia etiquetada no hay
  forma de saber si el reordenador mejora o empeora. La comparación honesta es la misma lista
  de candidatos con y sin reordenación, midiendo MRR o NDCG@3.

:::truco
Empieza siempre por medir `recall@100` de la etapa 1. Si es 0,95, un reordenador barato te da
casi todo el beneficio. Si es 0,60, el reordenador solo puede ordenar mejor el 60 % de las
veces: el trabajo está en el troceado y en el modelo de embeddings.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué un codificador cruzado es más preciso que un bi-codificador?
o: Porque usa vectores de más dimensiones
o: Porque procesa la consulta y el documento juntos, así que puede valorar coincidencias exactas de frase y el orden de las palabras
o: Porque se entrena con más datos
a: 2
e: Esa es toda la diferencia: el bi-codificador vectoriza cada parte por separado, y para que eso sea posible el documento se resume sin conocer la pregunta. El cruzado ve las dos partes a la vez y puntúa la pareja. La dimensión del vector no es la causa, y el volumen de entrenamiento es independiente de la arquitectura.
:::

:::quiz
p: Tienes 200 candidatos de la etapa 1 y un presupuesto de latencia muy ajustado. ¿Qué haces primero?
o: Reducir el número de candidatos que pasan al reordenador y medir cuánto MRR se pierde
o: Eliminar la etapa de recuperación y reordenar todo el corpus
o: Cambiar la métrica de evaluación a exactitud
a: 1
e: El coste del reordenador crece de forma lineal con el número de candidatos, así que la palanca directa es bajarlo y comprobar cuánta calidad se pierde: muchas veces 50 candidatos dan casi el mismo MRR que 200. Reordenar el corpus entero es inviable, y cambiar de métrica no mejora nada, solo oculta el problema.
:::

:::quiz
p: El reordenador sube el documento relevante del puesto 5 al 4, pero el MRR apenas cambia. ¿Qué comprobación haces?
o: Si la primera etapa deja fuera documentos relevantes, porque entonces el problema no está en ordenar
o: Si el modelo de embeddings tiene demasiadas dimensiones
o: Si hay que reordenar dos veces seguidas
a: 1
e: Un reordenador solo puede reordenar lo que recibe. Si los relevantes no entran en el conjunto de candidatos, subir posiciones dentro de él no cambia el resultado. La comprobación correcta es el recall del recuperador. Repetir la reordenación no aporta nada nuevo y la dimensión del embedding no es la causa.
:::
