---
id: rag-arquitectura
titulo: 'RAG: arquitectura'
fase: 8
nivel: avanzado
rutas: [ds]
prerequisitos: [como-funciona-un-llm, ventanas-de-contexto]
tags: [llm, rag, recuperacion, arquitectura]
resumen: Recuperar, aumentar y generar: el patron completo de RAG, sus seis etapas y los puntos donde se rompe la cadena antes de llegar al modelo.
fuentes: ["Lewis et al. (2020), 'Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks'", "Cormack, Clarke y Buettcher (2009), 'Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods'"]
---

## En una frase

RAG consiste en buscar en tu propia colección los fragmentos que responden a la pregunta,
meterlos en el contexto y pedirle al modelo que responda **solo** con ellos y citando de dónde
sale cada cosa.

## La idea

Un modelo de lenguaje tiene dos problemas cuando le preguntas por el catálogo de tu empresa: no
lo sabe, y no puede admitir que no lo sabe. Recuperar la información y dársela en el contexto
resuelve los dos a la vez, porque ahora la respuesta está delante de él, y además puedes pedirle
que diga de qué documento la ha sacado.

El patrón completo tiene seis etapas, y la regla que hay que interiorizar es que **la cadena se
rompe por el eslabón más débil, y el más débil casi nunca es el modelo**:

1. **Ingesta y extracción de texto.** PDFs con dos columnas, tablas, escaneos, HTML con menús,
   hojas de cálculo con celdas combinadas. Si el texto extraído está desordenado, ninguna etapa
   posterior lo arregla. Esta es la fase más aburrida y la que más proyectos hunde.
2. **Troceado.** El texto se parte en fragmentos de tamaño manejable, con solapamiento y
   respetando la estructura (títulos, secciones, apartados). Cada fragmento se guarda con
   metadatos: documento de origen, fecha, versión, y **permisos de acceso**. Un fragmento sin su
   título pierde el contexto y se vuelve ambiguo ([[chunking-y-embeddings|troceado y
   embeddings]]).
3. **Indexación.** Cada fragmento se convierte en un vector con un modelo de embeddings y se
   guarda en un índice ([[bases-de-datos-vectoriales|base de datos vectorial]]). En paralelo se
   mantiene un índice léxico tipo BM25, porque los dos fallan en cosas distintas.
4. **Recuperación.** Se busca con los dos índices y se fusionan los resultados. La búsqueda
   vectorial entiende paráfrasis pero se pierde con identificadores exactos y términos raros; la
   léxica hace lo contrario. Se recupera **generosamente**: 20, 50 o 100 candidatos.
5. **Reordenación.** Un modelo cruzado puntúa cada par (pregunta, fragmento) leyéndolos juntos,
   que es mucho más preciso que comparar vectores calculados por separado. De los 50 candidatos
   se quedan 3 a 8. Es la mejora con mejor relación coste-beneficio de toda la arquitectura
   ([[reranking|reordenación]]).
6. **Generación con citas.** Se monta el prompt con los fragmentos numerados, la pregunta
   **después** de los fragmentos, la instrucción de citar y la de responder «no está en los
   documentos» cuando no haya base. Sin esa última instrucción, el modelo rellenará el hueco.

Dos principios que ordenan todo el trabajo:

**La recuperación se evalúa por separado.** Si el fragmento que contiene la respuesta no está
entre los recuperados, el generador no puede hacer nada: su techo está fijado antes de que
escriba una palabra. Por eso se mide el **recall de recuperación** y se arregla la recuperación
antes de tocar el prompt de generación.

**Un índice es un producto, no un fichero.** Los documentos cambian, se corrigen y se borran. Si
el índice no se reconstruye, el sistema responde con citas a versiones antiguas, y eso es peor
que no responder: da apariencia de fundamento a un dato caducado.

Y una decisión de diseño que no es técnica: **el filtrado por permisos va antes de recuperar**,
no después de generar. Si el índice devuelve un fragmento que el usuario no puede ver y el
modelo lo resume, tienes una fuga de datos con la firma del sistema.

## Definición formal

**Recuperación.** Con una consulta `q` y un fragmento `d`, representados por sus vectores
`e_q` y `e_d`:

:::formula
similitud(q, d) = (e_q · e_d) / (‖e_q‖ · ‖e_d‖) = cos(θ)
:::

- `e_q`, `e_d` — vectores de la consulta y del fragmento, del **mismo** modelo de embeddings.
- `·` — producto escalar; `‖·‖` — norma euclídea.
- `cos(θ)` — el coseno del ángulo entre los dos vectores: 1 si apuntan igual, 0 si son
  ortogonales. Con vectores normalizados, el orden por producto escalar y por coseno es el
  mismo.

**Fusión de rangos recíprocos (RRF).** Para combinar el ranking denso y el léxico sin tener que
comparar puntuaciones de escalas distintas:

:::formula
RRF(d) = Σᵢ 1 / (k + rᵢ(d))
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `q`, `d` | La consulta y un fragmento del índice | texto (tokens) | No se comparan como texto: antes se convierten en vectores con el mismo modelo |
| `e_q`, `e_d` | Los vectores de la consulta y del fragmento | vector de dimensión fija | Si vienen de modelos distintos, la comparación no significa nada |
| `similitud(q, d)` | Coseno del ángulo entre los dos vectores | entre −1 y 1 | Cerca de 1 son parecidos; cerca de 0, sin relación. El orden por producto escalar y por coseno coincide solo si los vectores están normalizados |
| `rᵢ(d)` | Posición del fragmento en el ranking `i`, empezando en 1 | posición | Al bajar puestos, su aportación `1/(k + r)` se hace más pequeña, así que la fusión premia la cabeza de cada lista |
| `k` | Constante de suavizado de la RRF | adimensional (60 es lo habitual) | Con `k` grande, la diferencia entre el puesto 1 y el 3 se aplana: todos los puestos altos pesan parecido |
| `recall@k` | Proporción de consultas con un fragmento relevante entre los `k` primeros | entre 0 y 1 | Fija el **techo** del sistema: ninguna mejora del prompt lo supera |
| **Precisión de contexto** | Fragmentos enviados al modelo que resultan relevantes | entre 0 y 1 | Mide el ruido que pagas; subirla es recortar lo que envías, no recuperar más |
| **Fidelidad** | Afirmaciones de la respuesta sostenidas en los fragmentos | entre 0 y 1 | Una respuesta puede ser cierta y no estar apoyada en el contexto: eso también cuenta como fallo |
:::

- `rᵢ(d)` — la posición del fragmento `d` en el ranking `i` (1 = primero).
- `k` — una constante de suavizado; un valor habitual es 60. Cuanto mayor es `k`, más se
  reparte el peso entre las posiciones altas.
- La suma recorre todos los rankings que quieras fusionar.
- La gracia es que **solo usa posiciones**, no puntuaciones: no hay que normalizar nada entre
  un coseno y una puntuación BM25.

:::figura
fichero: rag-fusion-de-ranks-y-consenso
pie: Los dos paneles de la izquierda son la fusión de rankings del ejemplo. En el primero, cada buscador con sus posiciones: el fragmento D es el caso que justifica la fusión, porque la búsqueda vectorial lo dejaba tercero y la léxica lo pone primero. En el segundo, lo que aporta cada ranking a la puntuación final: A gana porque los dos la respaldan (denso 1, léxico 2), C se hunde porque el buscador léxico la manda al cuarto puesto y B pierde en los dos. Las puntuaciones son casi idénticas —0,03252 frente a 0,03150, un 3 % de diferencia— y sin embargo el orden final cambia por completo: la RRF no mide cuánto de buena es cada lista, solo dónde coloca a cada fragmento. El panel derecho es otra lección: el techo del sistema completo es el producto de los eslabones (0,92 · 0,85 = 0,78) y ninguna mejora del prompt de generación pasa de ahí. Mover la curva entera hacia arriba exige arreglar la recuperación o la reordenación, no el texto que le mandas al modelo.
fuente: figuras/rag-arquitectura-1.py
:::

**Métricas que hay que medir por separado.**

- `recall@k` — proporción de consultas en las que al menos un fragmento relevante aparece entre
  los `k` primeros. Es el techo del sistema.
- **Precisión de contexto** — proporción de fragmentos enviados al modelo que resultan
  relevantes. Mide cuánto ruido pagas.
- **Fidelidad** (*faithfulness*) — proporción de afirmaciones de la respuesta que se sostienen
  en los fragmentos recuperados. Una respuesta puede ser cierta y no estar apoyada en el
  contexto, y eso también es un fallo del sistema.

## Ejemplo

**Fusión de dos rankings.** Cuatro fragmentos, una búsqueda vectorial y una léxica que no
coinciden:

```
A: denso 1  lexico 2  RRF 0.03252
D: denso 3  lexico 1  RRF 0.03227
C: denso 2  lexico 4  RRF 0.03175
B: denso 4  lexico 3  RRF 0.03150
```

`A` gana porque los dos rankings la ponen arriba. `D` sube al segundo puesto aunque la búsqueda
vectorial la dejaba tercera, y `C` baja al tercero aunque era segunda en la densa: al buscador
léxico no le gusta nada. Eso es exactamente lo que aporta la fusión: un fragmento que un solo
ranking habría enterrado aparece arriba porque el otro lo respalda.

**El techo de la cadena.** Supón que el recuperador trae el fragmento correcto entre los 20
primeros en el 92 % de las consultas, y que el reordenador lo mantiene en el top-5 en el 85 % de
esos casos. El techo del sistema completo es `0,92 · 0,85 = 0,78`: ninguna mejora del prompt de
generación va a pasar de ahí. Los dos números son supuestos del ejemplo, pero la aritmética es la
lección: **los eslabones se multiplican, no se suman**.

**El coste de recuperar de más.** Recuperar 20 fragmentos de 400 tokens son 8.000 tokens de
prompt; enviar 5 son 2.000. Recuperar mucho es barato (comparar vectores es rápido), pero
**generar** con todo ese contexto cuesta dinero, tiempo y precisión, porque el modelo tiene que
atender a 8.000 tokens para producir 200. De ahí el reparto: recuperar mucho, reordenar y enviar
poco.

## Código

```python verificable
import numpy as np

# Similitud coseno entre la consulta y cuatro fragmentos (vectores escritos a mano)
consulta = np.array([1.0, 0.0, 0.5])
fragmentos = {
    "A": np.array([1.0, 0.1, 0.4]),
    "B": np.array([0.2, 1.0, 0.1]),
    "C": np.array([0.9, 0.2, 0.6]),
    "D": np.array([0.0, 0.3, 0.9]),
}

def coseno(a, b):
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))   # @ es el producto escalar; float() saca un escalar de Python

denso = sorted(fragmentos, key=lambda k: -coseno(consulta, fragmentos[k]))   # de mas parecido a menos: por eso el menos
lexico = ["D", "A", "B", "C"]          # orden que daria un buscador por palabras

# Fusion de rangos reciprocos (RRF): cada lista aporta 1 / (k + posicion)
k = 60
rrf = {c: 1 / (k + denso.index(c) + 1) + 1 / (k + lexico.index(c) + 1) for c in fragmentos}
for c in sorted(rrf, key=lambda x: -rrf[x]):     # ordena las claves del diccionario por su valor RRF
    print(f"{c}: denso {denso.index(c) + 1}  lexico {lexico.index(c) + 1}  RRF {rrf[c]:.5f}")
# -> A 0.03252, D 0.03227, C 0.03175, B 0.03150
```

:::claves
- `sorted(fragmentos, ...)` sobre un **diccionario** devuelve una lista de **claves** («A», «B», …), no de vectores. El vector sale después con `fragmentos[k]`: confundir los dos es el error que rompe este bloque.
- `denso.index(c)` devuelve la posición **empezando en 0**, y por eso la fórmula le suma 1. Sin ese `+ 1`, el primer puesto aportaría `1/(60+0)` y el ranking entero se desplazaría un puesto sin que se note a simple vista.
- `a @ b` es el producto escalar, no una multiplicación de listas. `np.linalg.norm` calcula la longitud del vector: si divides entre las dos normas, el resultado ya no depende de cuánto midan los vectores, solo de su dirección.
- La comprensión de diccionario `{c: ... for c in fragmentos}` recorre las claves en orden de inserción, así que `rrf` conserva el orden A, B, C, D del diccionario original. El orden final de la salida lo decide el `sorted` de la línea siguiente, no la inserción.
- `sorted(rrf, key=lambda x: -rrf[x])` ordena las **claves** por su valor, con el signo cambiado. `reverse=True` daría lo mismo y es más legible, pero con `-` queda explícito que lo que se invierte es el criterio.
- Los dos rankings tienen los **mismos cuatro fragmentos**: si uno de ellos no apareciera en la otra lista, `index()` lanzaría `ValueError`. En un sistema real hay que decidir qué hacer con los que solo salen en un ranking (penalizarlos o ignorarlos), y esa decisión cambia el resultado.
:::

```python verificable
# Techo de un pipeline de RAG: la generacion no puede arreglar lo que no se recupero.
# Los dos porcentajes son supuestos del ejemplo, no resultados medidos.
recall_20 = 0.92      # el fragmento correcto esta entre los 20 recuperados
rerank_5 = 0.85       # el reordenador lo mantiene en el top-5
print(f"techo del sistema {recall_20 * rerank_5:.2f}")     # -> 0.78

# Coste en prompt segun cuantos fragmentos se envian al modelo
por_fragmento = 400   # tokens medios por fragmento
print(f"20 fragmentos -> {20 * por_fragmento} tokens")     # -> 8000 tokens
print(f" 5 fragmentos -> {5 * por_fragmento} tokens")      # -> 2000 tokens
```

:::claves
- Los dos porcentajes se **multiplican**, no se suman: `0,92 · 0,85 = 0,78`. Es la lección del bloque, y también su trampa: si el reordenador fallara solo en el 5 % de los casos, el techo subiría a `0,92 · 0,95 = 0,874`, pero nunca por encima del `recall`.
- `0.92` y `0.85` son **supuestos escritos a mano**, no resultados medidos, y así lo dice el comentario. Si los cambiaras por los de tu sistema, el número que sale no sería una predicción: sería una multiplicación.
- `f"...{20 * por_fragmento} tokens"` hace la cuenta dentro de la cadena, así que el `print` no depende de ninguna variable intermedia. Si `por_fragmento` fuese un texto, la multiplicación daría una cadena repetida 20 veces en vez de un error.
- El coste se calcula en **tokens de prompt**, que es la unidad que se paga y la que ocupa ventana. Pasar de 20 fragmentos a 5 no reduce el tiempo de recuperación (comparar vectores es rápido): reduce el coste y el ruido de la generación.
:::

```python ilustrativo
# Prompt de generacion con citas: los fragmentos van primero y la pregunta al final.
# Necesita un modelo real, por eso no se ejecuta aqui.
PLANTILLA = """Responde a la pregunta usando UNICAMENTE los fragmentos numerados.
Cita el numero del fragmento entre corchetes despues de cada afirmacion.
Si la respuesta no esta en los fragmentos, escribe exactamente: NO_ESTA_EN_LOS_DOCUMENTOS.

[1] {fragmento_1}
[2] {fragmento_2}
[3] {fragmento_3}

Pregunta: {pregunta}
Respuesta:"""

respuesta = cliente.generar(entrada=PLANTILLA.format(**datos), temperatura=0.0, max_tokens=400)

# Sin la instruccion de abstenerse, el modelo rellena el hueco con lo mas plausible
if "NO_ESTA_EN_LOS_DOCUMENTOS" in respuesta.texto:   # la abstención se detecta por texto exacto
    registrar_sin_respuesta(pregunta)                # queda constancia de la consulta sin base
else:
    exigir_citas(respuesta.texto)      # cada afirmacion debe llevar su [n]
```

:::claves
- `PLANTILLA.format(**datos)` sustituye las llaves por los valores del diccionario: `**datos` desempaqueta las claves como argumentos con nombre, así que la clave `fragmento_1` tiene que existir o el `format` falla con `KeyError`. Si un fragmento contuviera llaves (`{`), `format` las interpretaría como huecos.
- La abstención se comprueba con `in` sobre el **texto literal**, no con una interpretación del modelo: es una comprobación barata y frágil a la vez. Si el modelo escribe «NO_ESTA_EN_LOS_DOCUMENTOS.» con punto o en minúsculas, la condición no se cumple.
- `temperatura=0.0` hace que la misma entrada dé la misma salida. Sin eso, la comprobación de citas fallaría de forma intermitente y no sabrías si el fallo es del modelo o del azar.
- `exigir_citas(...)` no devuelve nada que se use: está llamada por su **efecto** (registrar, lanzar un error o marcar la respuesta). Una función que se llama y se ignora es legítima aquí, pero conviene que su nombre lo deje claro.
:::

## Errores típicos

- **Evaluar solo la respuesta final.** Si la métrica es «¿la respuesta es buena?», no sabes si el
  problema está en el recuperador o en el generador. Mide `recall@k` por un lado y fidelidad por
  otro: son dos sistemas distintos con dos conjuntos de fallos distintos.
- **Subir `k` en vez de reordenar.** Meter 50 fragmentos en el prompt no mejora la respuesta:
  añade ruido, encarece la llamada y entierra la información buena en el medio del contexto. El
  orden correcto es recuperar mucho (barato) y **reordenar** antes de enviar poco.
- **Fragmentos sin contexto.** Un trozo de tabla o un párrafo que empieza con «por lo tanto» no
  se entiende solo. Hay que anteponer el título de la sección, el nombre del documento y la
  fecha al texto del fragmento: los metadatos también son contexto y son casi gratis.
- **Mezclar embeddings de modelos distintos en el mismo índice.** Dos vectores solo son
  comparables si salen del mismo modelo y de la misma versión. Si cambias de modelo de
  embeddings, hay que **reindexar todo**; los vectores viejos y los nuevos en el mismo índice dan
  resultados sin sentido.
- **No filtrar permisos antes de recuperar.** Recuperar primero y filtrar después significa que
  el fragmento prohibido ya entró en el prompt. El control de acceso va en la consulta al índice,
  nunca en la generación.
- **No dar salida a la abstención.** Si el prompt no contempla «no lo sé», el modelo tiene que
  producir algo y lo producirá con el mismo tono seguro que cuando acierta
  ([[alucinaciones-y-limites|alucinaciones]]). Una instrucción de abstención explícita y una
  comprobación de que las citas existen son la defensa mínima.
- **Confundir RAG con ajuste fino.** RAG aporta información que cambia; el ajuste fino cambia el
  comportamiento y el formato. Casi siempre se empieza por RAG porque se actualiza sin reentrenar
  ([[fine-tuning-vs-rag|ajuste fino frente a RAG]]).

## Comprueba que lo sabes

:::quiz
p: La recuperación trae el fragmento correcto en el 95 % de las consultas, pero el reordenador lo tira en la mitad de esos casos. ¿Dónde está el problema?
o: En el prompt de generación, que no aprovecha bien el contexto
o: En la etapa de reordenación, que está reduciendo por debajo del techo que fija la recuperación
o: En el modelo de embeddings, que no distingue bien los fragmentos
a: 2
e: Si el fragmento bueno se recupera pero no llega al prompt, el generador nunca lo verá. Los eslabones se multiplican: `recall` alto por reordenación mala da un sistema mediocre. Se arregla midiendo la reordenación por separado, no cambiando el prompt.
:::

:::quiz
p: ¿Qué ventaja tiene fusionar un ranking vectorial con uno léxico tipo BM25?
o: Que se suman las puntuaciones de los dos y el resultado es siempre mejor
o: Que cubren fallos distintos: la búsqueda vectorial entiende paráfrasis y la léxica acierta con identificadores y términos exactos
o: Que el índice ocupa la mitad de espacio
a: 2
e: Los dos recuperadores fallan en cosas complementarias: los vectores capturan significado pero se pierden con códigos y nombres raros, y la búsqueda por palabras hace lo contrario. La fusión por rangos combina posiciones sin tener que normalizar puntuaciones de escalas diferentes.
:::

:::quiz
p: ¿Por qué conviene recuperar 50 fragmentos y enviar solo 5 al modelo?
o: Porque el modelo solo puede leer cinco fragmentos
o: Porque recuperar es barato y generar con mucho contexto es caro, más lento y menos preciso
o: Porque los fragmentos sobrantes se cobran dos veces
a: 2
e: Comparar vectores cuesta muy poco y ampliar el conjunto de candidatos sube el recall. Pero cada fragmento enviado ocupa ventana, cuesta dinero y compite por la atención del modelo, que además atiende peor lo que queda en el medio. Se recupera generosamente y se reordena antes de enviar.
:::

:::aviso
Un índice desactualizado produce respuestas incorrectas **con citas**. Es más peligroso que un
sistema que no sabe: la cita da apariencia de rigor a un dato caducado. Versiona los documentos,
reconstruye el índice cuando cambien y muestra la fecha del documento en la respuesta.
:::
