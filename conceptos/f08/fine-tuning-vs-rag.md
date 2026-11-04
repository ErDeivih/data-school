---
id: fine-tuning-vs-rag
titulo: Ajuste fino frente a RAG
fase: 8
nivel: avanzado
rutas: [ds]
prerequisitos: [rag-arquitectura, prompting, alucinaciones-y-limites, fine-tuning-y-lora]
tags: [llm, rag, fine-tuning, coste]
resumen: RAG cambia lo que el modelo lee; el ajuste fino cambia cómo se comporta. Casi siempre se empieza por RAG, y aquí se explica por qué.
fuentes: ["Lewis et al. (2020), 'Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks'", "Hu et al. (2021), 'LoRA: Low-Rank Adaptation of Large Language Models'"]
---

## En una frase

La recuperación (RAG) le da al modelo los documentos correctos en el momento de responder; el
ajuste fino cambia los pesos del modelo para que escriba o decida de otra forma. Si el problema
es que le falta un dato, búscalo; si es que no se comporta como quieres, entrénalo.

## La idea

Imagina que contratas a un becario muy listo que ha leido medio internet. Le pides que atienda
el telefono de tu tienda. Sabe redactar perfectamente, pero no se sabe las politicas de tu
empresa: cuando le preguntan por el plazo de devolución, improvisa, y acierta la mitad de las
veces.

Tienes dos formas de arreglarlo. La primera es darle una carpeta con las politicas y una regla:
«antes de contestar, busca en la carpeta y cita el parrafo». La segunda es mandarlo tres meses a
una academia donde le enseñan a hablar como tu empresa. La carpeta resuelve el problema hoy y se
actualiza cambiando una hoja; la academia cuesta meses, se queda obsoleta y no le permite citar
nada. La carpeta es RAG (*Retrieval-Augmented Generation*: recuperar, aumentar el prompt,
generar). La academia es el ajuste fino.

La razón técnica de fondo es esta: en un LLM, **el conocimiento factual vive en los pesos y es
caro de cambiar, mientras que la forma de responder también vive en los pesos pero se puede
moldear con relativamente pocos ejemplos**. Lo primero que quieres (que sepa el precio de hoy)
es lo que el ajuste fino hace peor.

Lo segundo (que conteste en tres líneas con el tono de
la marca) es lo que el ajuste fino hace mejor.

RAG, en concreto, monta una tuberia: partes los documentos en fragmentos, calculas un vector por
fragmento, guardas esos vectores en un índice, y en cada consulta buscas los fragmentos más
parecidos, los pegas en el prompt y dejas que el modelo responda apoyandose en ellos. Tres
consecuencias prácticas: actualizar el conocimiento es reindexar un documento, puedes citar la
fuente y puedes medir por separado si el fallo está en la búsqueda o en la redacción. Nada de
eso lo da el ajuste fino.

El ajuste fino entrena el modelo con pares de entrada y salida para fijar un formato, un tono o
una decisión. Sirve, por ejemplo, para que un modelo pequeño clasifique tickets en 12 categorias
con la misma exactitud que uno grande, a una decima parte del coste por consulta. Lo que no hace
es meter hechos nuevos de forma fiable: el modelo puede repetir con total seguridad un dato que
solo vio de refilón, y no hay manera de citar de donde lo sacó.

:::truco
Antes de decidir, hazte una sola pregunta: ¿el problema es que le falta información o que no se
comporta como quieres? Si falta información, es recuperación. Si se comporta mal (formato, tono,
idioma, decisiones), es ajuste fino. Y si son las dos cosas, se combinan: el ajuste fino fija el
formato y RAG aporta el contenido.
:::

Combinar los dos tiene sentido cuando necesitas una salida muy rígida sobre datos que cambian.
El modelo pequeño ajustado para rellenar un JSON concreto no se inventa las claves, y el
fragmento recuperado le da los valores frescos.

## Definición formal

Un sistema RAG se describe como dos funciones encadenadas más una generación:

:::formula
respuesta = LLM( prompt(q, top_k( Retriever(q), I ) ) )
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `q` | La consulta del usuario: el texto que hay que responder | — | Es lo único que cambia en cada llamada; el índice y el modelo se quedan igual |
| `I` | El índice de fragmentos ya vectorizados | fragmentos | Más documentos dan más cobertura y más ruido: el fragmento bueno compite con más candidatos |
| `Retriever(q)` | Puntúa cada fragmento de `I` según su similitud con `q` | puntuaciones | Con un recuperador flojo, el fragmento correcto no llega al prompt y ningún modelo lo arregla |
| `top_k` | Se queda con los `k` fragmentos de mayor puntuación | fragmentos | Subirlo mete más contexto, más tokens y más coste, y baja la precisión: lo típico es entre 3 y 20 |
| `k` | Cuántos fragmentos se recuperan | fragmentos | Con `k = 1` cualquier fallo de la búsqueda es un fallo de la respuesta; con `k` enorme, el dato se diluye |
| `prompt(q, …)` | La plantilla que pega la consulta y los fragmentos en el contexto | — | Es la única pieza de RAG que se cambia sin reindexar nada |
| `LLM(…)` | El modelo, que no ha cambiado | — | El mismo modelo con mejores fragmentos responde mejor: RAG no toca los pesos |
:::

- `q` — la consulta del usuario, el texto que hay que responder.
- `I` — el índice de fragmentos ya vectorizados; se construye a partir de los documentos.
- `Retriever(q)` — función que puntua cada fragmento de `I` segun su similitud con `q`.
- `top_k` — devuelve los `k` fragmentos con mayor puntuación (`k` suele estar entre 3 y 20).
- `prompt(q, ...)` — plantilla que inserta la consulta y los fragmentos en el contexto.
- `LLM(...)` — el modelo, que no ha cambiado: solo ha leído más cosas en esta llamada.

El ajuste fino, en su versión más común hoy, actualiza una parte pequeña de los parámetros.
Con LoRA, para una matriz de pesos `W` de dimensiones `d x k` no se toca `W`, sino que se
aprende una corrección de bajo rango:

:::formula
W' = W + (alpha / r) · B · A     con B de d x r y A de r x k, y r mucho menor que d y k
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `W` | La matriz de pesos original del modelo, congelada durante el entrenamiento | d × k números | No se toca nunca: el ajuste no reescribe el modelo, le suma una corrección |
| `W'` | La matriz que se usa al inferir, ya con el adaptador aplicado | d × k números | Es lo único que cambia respecto al modelo original, y el cambio es de bajo rango |
| `A` | Primera matriz del adaptador, de rango r | r × k números | Se inicializa con ruido; junto a `B` es lo que de verdad se entrena |
| `B` | Segunda matriz del adaptador | d × r números | Se inicializa a **cero**, y por eso al empezar el entrenamiento `W' = W`: no se rompe el modelo antes de aprender nada |
| `r` | Rango del adaptador: cuántos parámetros nuevos hay | entero, típico 8, 16 o 32 | Más capacidad de adaptación y más riesgo de sobreajustar; necesita más datos |
| `alpha` | Factor de escala de la corrección | entero, en la práctica `2r` | Subirlo da más peso al adaptador; como se divide entre `r`, cambiar `r` sin tocar `alpha` ya cambia el efecto |
:::

- `W` — matriz de pesos original del modelo, congelada durante el entrenamiento.
- `A`, `B` — matrices pequeñas que si se entrenan; `A` se inicializa con ruido y `B` a cero.
- `r` — rango del adaptador: controla cuántos parámetros nuevos hay. Valores típicos: 8, 16, 32.
- `alpha` — factor de escala; en la práctica se usa `alpha = 2r` como punto de partida.

`r` pequeño significa pocos parámetros entrenables y menos riesgo de sobreajustar; `r` grande
da más capacidad de adaptación y necesita más datos.

Una tabla para decidir, con el criterio que de verdad pesa en cada caso:

| Criterio | RAG | Ajuste fino |
| --- | --- | --- |
| Que cambia | el contexto de cada llamada | los pesos del modelo |
| Actualizar un dato | reindexar el documento | volver a entrenar |
| Trazabilidad | citas el fragmento que lo dice | no hay fuente |
| Datos necesarios | los documentos, ya los tienes | cientos o miles de ejemplos etiquetados |
| Coste de arranque | bajo: un índice y un prompt | alto: preparar datos, entrenar, evaluar |
| Coste por consulta | más tokens de entrada | puede bajar si usas un modelo menor |
| Ideal para | hechos, politicas, catalogos que cambian | formato, tono, clasificación acotada |

:::figura
fichero: fine-tuning-vs-rag-recuperar-o-entrenar
pie: A la izquierda, la similitud real de los tres fragmentos del manual con la pregunta «cuánto tarda un envío a Canarias»: 0,206 para el de los envíos, 0,074 para el de las devoluciones y 0,000 para el de la garantía. El recuperador elige el correcto, y esa es toda la diferencia entre una respuesta y una invención: si el fragmento bueno no entrara en el `top_k`, el modelo respondería igual pero sin el dato. A la derecha, lo que cuesta poner al día un dato que ha cambiado (escala logarítmica): reindexar un documento son céntimos y la fuente sigue citándose, mientras que reentrenar son 4,5 $ por experimento —y hay varios— sin garantía de que el modelo aprenda el dato nuevo. La primera palanca es buscar mejor; la segunda solo se paga cuando el problema es de comportamiento, no de información.
fuente: figuras/fine-tuning-vs-rag-1.py
:::

## Ejemplo

Un asistente de soporte para una tienda. Hay 400 documentos de política (unas 500.000 palabras
en total) y 2.000 consultas al mes. El equipo maneja 2.000 ejemplos etiquetados de respuestas
correctas.

- **RAG.** Indexar 500.000 palabras cuesta, a 0,02 dolares por millon de tokens de embedding y
  unos 700.000 tokens, 0,014 dolares, una sola vez. Cada consulta envia unos 2.500 tokens de
  fragmentos y 200 de pregunta, y recibe 150 de respuesta: con un modelo a 3 dolares por millon
  de tokens de entrada y 15 por millon de salida, cada consulta sale a
  (2.700 / 1.000.000) · 3 + (150 / 1.000.000) · 15 = 0,0081 + 0,00225 = **0,0104 dolares**, es
  decir unos **20,7 dolares al mes**. Cambiar una política es reindexar un fichero.
- **Ajuste fino.** Entrenar con 2.000 ejemplos, en un modelo abierto de 7.000 millones de
  parámetros y 2 epocas, son unas 3 horas de GPU; a 1,5 dolares por hora, unos **4,5 dolares**
  por experimento. Pero haras varios: preparar datos, entrenar, evaluar, corregir. Y cuando la
  política cambie, el modelo no lo sabra: seguira respondiendo con la versión vieja.

La conclusión práctica no es que el ajuste fino sea caro, sino que **resuelve otro problema**.
Gastar 4,5 dolares en entrenar para meter hechos es tirar el dinero; gastarlos para que un
modelo pequeño devuelva siempre el JSON de tu API puede ahorrar miles al mes.

## Código

```python verificable
import re
import numpy as np

# Tres fragmentos de un manual interno: lo que un RAG pondria en el prompt.
fragmentos = [
    "El plazo de devolucion de un pedido es de 30 dias desde la entrega.",
    "Los envios a Canarias tardan entre 5 y 7 dias laborables.",
    "La garantia de los productos electronicos cubre 2 anos.",
]
consulta = "cuanto tarda un envio a Canarias"
documentos = fragmentos + [consulta]     # lista nueva: la consulta entra como un documento mas

# TF-IDF calculado a mano: frecuencia de termino por el logaritmo de la
# frecuencia inversa, y luego cada fila normalizada para comparar por coseno.
def vectorizar(docs):
    # un set quita repetidos y sorted fija el orden: la columna de cada palabra no cambia entre ejecuciones
    vocabulario = sorted({p for d in docs for p in re.findall(r"[a-z]+", d.lower())})
    indice = {p: i for i, p in enumerate(vocabulario)}      # palabra -> numero de columna
    tf = np.zeros((len(docs), len(vocabulario)))            # una fila por documento, en float
    for f, d in enumerate(docs):
        for p in re.findall(r"[a-z]+", d.lower()):
            tf[f, indice[p]] += 1                           # cuenta cuantas veces sale cada palabra
    df = (tf > 0).sum(axis=0)                               # axis=0 suma por columnas: en cuantos documentos sale
    idf = np.log((1 + len(docs)) / (1 + df)) + 1            # el +1 evita dividir entre cero
    # keepdims deja la norma con forma (n, 1) para poder dividir fila a fila
    return (tf * idf) / np.linalg.norm(tf * idf, axis=1, keepdims=True)

matriz = vectorizar(documentos)
similitud = matriz[:-1] @ matriz[-1]     # producto matriz-vector: un numero por fragmento (la consulta es la ultima fila)

# El fragmento util tiene que estar arriba: si no, el prompt no salva la respuesta.
for i in np.argsort(-similitud):         # el menos ordena de mayor a menor: argsort ordena ascendente
    print(f"{similitud[i]:.3f}  fragmento {i}")
# -> 0.206  fragmento 1
# -> 0.074  fragmento 0
# -> 0.000  fragmento 2
print("mejor fragmento:", int(np.argmax(similitud)))    # -> 1
```

:::claves
- `documentos = fragmentos + [consulta]` crea una lista **nueva**: `fragmentos` queda intacto. La consulta se mete como un documento más para poder vectorizarla con la misma función, y por eso después se separa con `matriz[-1]`.
- El vocabulario sale de `sorted({...})` sobre `re.findall(r"[a-z]+", d.lower())`: el conjunto elimina las palabras repetidas, `sorted` fija el orden alfabético —sin él, la columna de cada palabra cambiaría entre ejecuciones— y el `d.lower()` hace que «Canarias» cuente como «canarias». Los números y los signos se descartan: es un TF-IDF de juguete, y uno de verdad trocea de otra forma ([[chunking-y-embeddings|troceado y embeddings]]).
- `df = (tf > 0).sum(axis=0)`: `tf > 0` es una matriz de booleanos y `axis=0` suma **hacia abajo**, así que devuelve un número por palabra (en cuántos documentos aparece). Con `axis=1` sumaría por documento y el IDF saldría del revés.
- `np.linalg.norm(..., axis=1, keepdims=True)` calcula la norma de cada fila y la deja con forma `(n, 1)`. Sin `keepdims` tendría forma `(n,)` y la división contra la matriz `(n, m)` no se repartiría por filas. El resultado son vectores de longitud 1, y por eso el producto `@` mide el coseno.
- `matriz[:-1] @ matriz[-1]` es un producto matriz-vector: devuelve **un número por fragmento**, no una matriz, y la consulta no aparece en el resultado. `np.argsort(-similitud)` ordena de mayor a menor porque `argsort` ordena de menor a mayor: el signo menos invierte el orden, no los valores.
- `idf = np.log((1 + len(docs)) / (1 + df)) + 1`: los `+1` son suavizado. Sin ellos, una palabra que aparezca en todos los documentos daría `log(1) = 0` y su columna se anularía; y una palabra ausente daría división entre cero.
:::

```python ilustrativo
# Los dos enfoques vistos como datos: mismo objetivo, artefactos distintos.
# RAG necesita un indice que se puede rehacer en caliente.
indice = [{"id": "pol-014", "texto": "El plazo de devolucion es de 30 dias.",
           "vector": [0.12, -0.04, 0.88]}]

# Ajuste fino necesita ejemplos de comportamiento, no de conocimiento:
# el par guarda la SALIDA ESPERADA (la intencion y el pedido), no el dato en si.
ejemplo_ajuste = {
    "entrada": "El cliente pregunta por su pedido 4471.",
    "salida_esperada": '{"intencion": "estado_pedido", "pedido": "4471"}',
}

# Lo que NO cambia: el prompt de sistema sigue haciendo falta en ambos casos.
print(indice[0]["id"], ejemplo_ajuste["salida_esperada"][:24])   # [:24] corta la CADENA, no la lista
```

## Errores típicos

- **Ajustar antes de haber intentado recuperar.** Es el error más caro y el más común. Si el
  modelo falla porque no conoce tus documentos, el ajuste fino no le da ese conocimiento de
  forma fiable: lo que hace es ensenarle a sonar seguro. Prueba RAG primero; es más barato y
  se mide mejor.
- **Creer que el ajuste fino elimina las alucinaciones.** Las reduce en el dominio de los
  ejemplos y las puede aumentar fuera de el, porque el modelo ajustado responde con su estilo
  aprendido aunque no tenga el dato. Para acotar la invención se combinan recuperación,
  instrucciones de citar y verificación de la salida.
- **Usar el ajuste fino para meter conocimiento que caduca.** Precios, stock, politicas y
  plantillas cambian. Todo eso es material de recuperación, no de pesos.
- **Dar por hecho que RAG ya evita inventarse cosas.** Si el fragmento correcto no entra en el
  `top_k`, el modelo responde igual, con o sin contexto. Mide la recuperación por separado:
  si el fragmento bueno no aparece en el top 5, ningun prompt lo arregla. El detalle está en
  [[chunking-y-embeddings|troceado y embeddings]] y en [[reranking|la reordenacion]].
- **Trocear por caracteres.** Un fragmento que corta una tabla de precios por la mitad produce
  respuestas incompletas. Trocea por secciones o parrafos con sentido, y solapa un poco.
- **Comparar RAG contra ajuste fino con conjuntos distintos.** Si mides uno con 40 preguntas
  faciles que tu mismo elegiste y el otro con el trafico real, no has comparado nada. Usa el
  mismo conjunto, las mismas preguntas y la misma rúbrica de corrección; el detalle está en
  [[evaluacion-de-llms|la evaluación]].

## Comprueba que lo sabes

:::quiz
p: Un equipo necesita que su asistente conozca el catalogo de productos, que cambia cada semana. ¿Que enfoque es el correcto?
o: Ajuste fino semanal del modelo con el catalogo nuevo
o: Recuperación: indexar el catalogo y pegar los fragmentos relevantes en cada consulta
o: Subir el catalogo entero en el prompt en cada llamada, sin buscar
a: 2
e: El catalogo es conocimiento que caduca, justo lo que el ajuste fino hace mal: habria que reentrenar cada semana y el modelo no podría citar el dato. Meter el catalogo entero no escala: supera la ventana de contexto y dispara el coste. Recuperar los fragmentos relevantes es lo único que se actualiza reindexando.
:::

:::quiz
p: ¿Para que sirve de verdad el ajuste fino en un sistema con RAG?
o: Para que el modelo memorice los documentos y no haga falta recuperar nada
o: Para fijar comportamiento: formato de salida, tono, idioma o una clasificación concreta
o: Para reducir el número de tokens del contexto eliminando el prompt de sistema
a: 2
e: El ajuste fino moldea la conducta del modelo con ejemplos de entrada y salida. Memorizar documentos no es fiable ni citable, y el prompt de sistema sigue siendo necesario: el ajuste no sustituye las instrucciones que cambian por consulta.
:::

:::trampa
Cuando alguien dice «vamos a hacer fine-tuning para que el modelo sepa de nuestro negocio»,
casi siempre lo que necesita es un buscador decente. Empieza midiendo la recuperación: si el
fragmento correcto aparece en el top 5 en el 90 % de las preguntas, el problema es de
redacción y se arregla con prompt. Si aparece en el 50 %, ningun entrenamiento te salva.
:::
