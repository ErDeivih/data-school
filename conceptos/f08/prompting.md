---
id: prompting
titulo: Ingeniería de prompts
fase: 8
nivel: básico
rutas: [ds]
prerequisitos: [como-funciona-un-llm, tokenizacion]
tags: [llm, prompts, practicas, evaluacion]
resumen: Un prompt es el enunciado de la tarea: rol, contexto, ejemplos, formato y criterio de exito, y se mejora midiendo, no buscando palabras magicas.
fuentes: ["Wei et al. (2022), 'Chain-of-Thought Prompting Elicits Reasoning in Large Language Models'", "Jurafsky y Martin (2025), 'Speech and Language Processing'"]
---

## En una frase

Un prompt es la especificación de lo que quieres: quién debe ser el modelo, qué información
tiene, qué formato debe devolver y qué cuenta como respuesta correcta; escribirlo bien es
escribir un buen enunciado, no encontrar la fórmula mágica.

## La idea

Imagina que contratas a alguien brillante y rapidísimo, pero con tres particularidades
incómodas: **no recuerda nada de ayer**, **no pregunta nunca** y **toma todo al pie de la
letra**. Si le pides «hazme un resumen», elegirá la longitud y el enfoque por su cuenta y
seguirá adelante.

Eso es lo que hace un modelo: su tarea es continuar el texto que le das de la forma más
probable, así que el prompt no es una orden que se interpreta, sino el contexto que determina
la distribución de la que sale la respuesta.

Hay dos formas de equivocarse, y son opuestas:

- **Quedarse corto.** «Resume esto». El modelo elegirá el resumen medio de todo lo que ha visto:
  ni el enfoque, ni la longitud, ni el nivel de detalle que necesitas.
- **Pasarse de largo.** Veinte reglas, cinco ejemplos contradictorios, tres formatos distintos y
  una instrucción que dice «sé conciso pero no omitas nada». Cuando dos reglas se contradicen, el
  modelo elige una y el resultado es impredecible.

La anatomía de un prompt que funciona tiene seis piezas, y no todas son obligatorias:

1. **Rol y objetivo** — «Eres un revisor de contratos; tu tarea es señalar cláusulas de riesgo».
   El rol no da superpoderes, pero acota el registro y el vocabulario.
2. **Contexto y datos** — el texto sobre el que trabajar, delimitado y separado de las
   instrucciones.
3. **La tarea, en un verbo concreto** — «clasifica», «extrae», «reescribe», «compara». No
   «ayúdame con».
4. **El formato de salida** — exacto y comprobable: «devuelve un JSON con las claves
   `riesgo`, `clausula` y `gravedad`».
5. **El criterio de éxito** — qué cuenta como correcto y qué hacer con los casos dudosos. «Si el
   contrato no menciona el plazo, escribe `null`, no lo inventes».
6. **Ejemplos** — de cero a cinco, elegidos para fijar el formato y los casos límite. Los
   ejemplos enseñan más que las descripciones: si quieres que una fecha salga en formato
   `AAAA-MM-DD`, pon un ejemplo. Es lo que se llama **aprendizaje con pocos ejemplos**
   (*few-shot*).

Sobre la **cadena de pensamiento**: pedir al modelo que razone los pasos antes de dar la
respuesta mejora los resultados en tareas de varios pasos (aritmética, lógica, comparaciones
encadenadas). Lo que **no** hace es darte una explicación fiable de cómo llegó a la respuesta: el
texto que escribe es otra generación plausible, no la traza de su cálculo interno. Sirve como
técnica para acertar más; no sirve como auditoría.

Y una regla que ahorra semanas: **un prompt es código**. Se versiona, se revisa y se prueba
contra un conjunto fijo de casos antes de cambiarlo. Sin esos casos, cada «mejora» es una
impresión.

## Definición formal

Un prompt `p` es una secuencia de tokens que se concatena con la entrada del usuario `u` y se le
pasa al modelo. La respuesta es una muestra de:

:::formula
y ~ P( · | p, u ; θ )
:::

- `p` — el prompt: sistema, contexto, ejemplos e instrucción.
- `u` — el contenido variable de la petición (el texto del usuario, el documento, la pregunta).
- `θ` — los pesos del modelo, que no cambian con el prompt.
- `~` — indica que `y` se **muestrea** de esa distribución, no que sea su valor más probable;
  con temperatura mayor que cero, dos ejecuciones pueden dar respuestas distintas.

El reparto del presupuesto de tokens es una restricción dura:

:::formula
tokens(p) + tokens(u) + tokens(y) ≤ ventana de contexto
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `p` | El prompt fijo: rol, contexto, ejemplos e instrucción | tokens | Come presupuesto a la entrada y a la respuesta: lo que ocupa el prompt no lo ocupa la salida |
| `u` | La parte variable: el texto del usuario o el documento | tokens | Es lo que suele descontrolarse: doce documentos de 500 tokens ya son 6.000 |
| `y` | La respuesta que genera el modelo | tokens | Hay que reservarla **antes** de escribir el prompt, o la generación se corta a mitad |
| `θ` | Los pesos del modelo | número de escalares | No cambia con el prompt: el mismo modelo con dos prompts distintos es el mismo modelo |
| `~` | Muestreo, no valor más probable | — | Con temperatura mayor que cero, dos ejecuciones dan respuestas distintas |
| `T` | Temperatura del muestreo | positiva | Más variedad y menos reproducibilidad; para extraer datos se usa 0 |
| `top-p` | Cola de la distribución que se descarta | entre 0 y 1 | Recorta los tokens improbables antes de muestrear: evita salidas absurdas |
:::

- `tokens(·)` — número de tokens de cada parte, que da el tokenizador del modelo
  ([[ventanas-de-contexto|ventana de contexto]]).
- `tokens(y)` — la respuesta, que hay que reservar **antes** de escribir el prompt.
- Si el prompt más la entrada se acercan al límite, lo que sobra se recorta: y lo que se recorta
  suele ser el contexto, justo lo que hacía falta.

Tres parámetros de muestreo se eligen junto al prompt: **temperatura** (0 para extraer datos de
forma estable, valores altos para generar ideas), **top-p** (recorta la cola de la distribución)
y **semilla**, cuando la API la admite. Ni con temperatura 0 hay reproducibilidad garantizada:
el orden de las operaciones en la GPU altera el último decimal del resultado.

:::figura
fichero: prompting-presupuesto-de-la-ventana
pie: A la izquierda, tres formas de montar el mismo prompt contra una ventana de 4.096 tokens. En la primera, los doce documentos dejan 6.350 tokens de prompt: no cabe nada y hay que recortar contexto. En la segunda, el prompt se ha ajustado a 3.996 y quedan 100 tokens para la respuesta, que es el margen que evita que la generación se corte a mitad. En la tercera, el mismo texto medido con la regla de 2 caracteres por token se pasa de largo: el prompt no cambió, cambió la regla con la que lo mediste. A la derecha se ve esa trampa: la misma entrada cabe o no cabe según cuántos caracteres por token supongas, y la regla cómoda de 4 se queda corta con código, cifras e identificadores.
fuente: figuras/prompting-1.py
:::

## Ejemplo

**Malo** (pide un resumen sin decir para quién):

```
Resume el siguiente contrato.
<contrato>
```

**Bueno** (rol, criterio, formato y caso dudoso):

```
Eres un analista que revisa contratos para el departamento de compras.
Extrae tres datos del contrato: partes, duracion en meses y preaviso de cancelacion en dias.
Devuelve solo un JSON con las claves "partes", "meses" y "preaviso_dias".
Si un dato no aparece en el texto, pon null. No lo deduzcas ni lo inventes.
<contrato>
```

**Cuentas de tokens.** El prompt del primer bloque de código tiene 421 caracteres: unos 105
tokens con la regla de 4 caracteres por token, o 210 en el peor caso (código, cifras,
identificadores). Con doce documentos de 500 tokens y un sistema de 350, el prompt son
`350 + 12 · 500 = 6.350` tokens: no cabe en una ventana de 4.096, y ese cálculo evita
descubrirlo en producción. Un prompt más largo no es un prompt mejor: cada token de más compite
por la atención con el resto.

## Código

```python verificable
# Montar un prompt y comprobar que cabe: contar caracteres es una aproximacion,
# el numero real de tokens lo da el tokenizador del modelo.
sistema = "Eres un asistente que responde en espanol de Espana, breve y sin relleno."
documentos = [
    "El contrato se renueva automaticamente cada 12 meses salvo aviso con 30 dias.",
    "La facturacion se emite el primer dia laborable de cada mes.",
    "El soporte responde en un maximo de 8 horas laborables.",
]
pregunta = "Cuando puedo cancelar sin penalizacion?"

partes = [f"[SISTEMA] {sistema}"]
for i, d in enumerate(documentos, 1):        # enumerate empieza en 1: los documentos se numeran [DOC 1], [DOC 2]...
    partes.append(f"[DOC {i}] {d}")
partes.append(f"[PREGUNTA] {pregunta}")
partes.append("[FORMATO] Responde solo con la fecha o el plazo, sin explicaciones.")

prompt = "\n".join(partes)                   # une las piezas con salto de linea: los delimitadores van dentro
caracteres = len(prompt)                     # cuenta caracteres, NO tokens: es la aproximacion que se critica
print(f"caracteres {caracteres}  tokens aproximados {caracteres // 4}")     # -> 421  105
print(f"peor caso (2 caracteres por token) {caracteres // 2} tokens")      # -> 210
```

:::claves
- `len(prompt)` cuenta **caracteres**, no tokens. El número real lo da el tokenizador del modelo: aquí se usa `// 4` como regla de andar por casa y `// 2` como peor caso. Es una estimación, y por eso el bloque imprime las dos cifras.
- `" ".join(...)` devuelve una **cadena nueva** y no toca la lista `partes`; `"\n".join(partes)` hace lo mismo pero separando con saltos de línea. El separador es el que va delante del punto, no detrás.
- `prompt` es una `str` **inmutable**: si quisieras quitar un documento tendrías que construir otra cadena. Modificar `partes` después de la unión no cambia `prompt` en absoluto.
- `enumerate(documentos, 1)` empieza a contar en 1, no en 0. Sin ese segundo argumento, el primer documento se etiquetaría `[DOC 0]`, que es un error silencioso y difícil de ver en la salida.
- En el bloque ilustrativo, `temperatura=0.0` es lo que hace reproducible la extracción, y `formato="json"` delega el esquema en el proveedor. Si el modelo no admite ese parámetro, lo devuelve como texto libre y `json.loads` revienta con `JSONDecodeError`.
- El `assert set(datos) == {...}` comprueba el **esquema**, no el contenido: si el modelo añade una clave extra, el `assert` falla aunque los tres datos pedidos estén bien. Los `assert` se desactivan con `python -O`, así que en producción van como comprobación explícita con `raise`.
:::

```python ilustrativo
# Esquema de una llamada real: la plantilla de arriba y una temperatura de 0 para extraer datos.
# Necesita red y una clave de API, por eso no se ejecuta aqui.
respuesta = cliente.generar(
    instrucciones=SISTEMA,
    entrada=prompt,
    temperatura=0.0,          # extraccion de datos: la misma entrada debe dar la misma salida
    max_tokens=300,
    formato="json",           # si el proveedor lo admite, evita parsear texto libre
)

datos = json.loads(respuesta.texto)     # si el modelo no devuelve JSON valido, esto revienta
assert set(datos) == {"partes", "meses", "preaviso_dias"}, "el modelo cambio el esquema"
```

## Errores típicos

- **Pedir precisión sin definir el criterio.** «Sé preciso», «piensa bien», «hazlo perfecto» no
  cambian la distribución de forma útil porque no dicen qué es correcto. Cambia eso por un
  criterio comprobable: «cita el párrafo exacto», «si no está en el texto, responde `null`».
- **Acumular reglas contradictorias.** «Responde en una sola frase, con todo el detalle y sin
  omitir ningún matiz». Cuando dos reglas chocan, el modelo elige una de forma impredecible. Si
  una regla no se puede cumplir a la vez que otra, quita una.
- **Confiar en la cadena de pensamiento como explicación.** Pedir los pasos mejora el acierto en
  tareas de varios pasos, pero el razonamiento escrito es otra generación plausible. Si necesitas
  auditar una decisión, verifica la respuesta por separado; no leas la justificación como si
  fuera un registro.
- **Usar temperatura alta para extraer datos.** Con `T = 1` dos ejecuciones dan respuestas
  distintas para la misma entrada, y tu validación posterior falla de forma intermitente. Para
  extracción, clasificación y cualquier tarea con respuesta única: temperatura 0.
- **Pedir JSON y luego parsearlo con expresiones regulares.** Si el proveedor admite esquemas,
  úsalos ([[structured-output|salida estructurada]]): valida la respuesta contra el esquema y
  reintenta cuando no encaje. Analizar texto libre con patrones es frágil y falla justo en los
  casos raros.
- **No separar las instrucciones del contenido del usuario.** Si pegas el texto del usuario sin
  delimitadores, ese texto puede contener frases que parezcan instrucciones y cambiar el
  comportamiento del modelo ([[seguridad-y-prompt-injection|inyección de prompts]]). Delimita,
  etiqueta el origen del contenido y no le des permisos que no necesite.

## Comprueba que lo sabes

:::quiz
p: ¿Qué le falta a un prompt que solo dice «resume este informe»?
o: Nada: el modelo ya sabe resumir y elegirá lo mejor para cada caso
o: El destinatario, la longitud, el enfoque y el formato, que son lo que determina qué resumen quieres
o: Subir la temperatura para que el resumen sea más creativo
a: 2
e: Sin esos datos, cada ejecución elegirá un resumen distinto y la mayoría no servirá. El prompt es la especificación de la tarea; lo que no especifiques lo decidirá el muestreo del modelo, no tú. Subir la temperatura aumenta la variabilidad, que es justo lo contrario de lo que falta aquí.
:::

:::quiz
p: ¿Para qué sirve pedir al modelo que razone paso a paso antes de responder?
o: Para mejorar el acierto en tareas de varios pasos y para obtener una explicación fiable de su cálculo interno
o: Para mejorar el acierto en tareas de varios pasos, aunque el texto del razonamiento no sea una explicación fiable de su cálculo
o: Para reducir el número de tokens de la respuesta
a: 2
e: La cadena de pensamiento da al modelo espacio para hacer operaciones intermedias y suele mejorar el resultado en tareas encadenadas. Pero el texto que escribe es otra generación plausible: no es un registro interno auditable, y puede justificar una respuesta que ya había elegido.
:::

:::quiz
p: Estas extrayendo datos estructurados y la misma entrada da resultados distintos entre ejecuciones. ¿Qué miras primero?
o: La temperatura de muestreo, que debería ser 0 para extracción
o: El número de ejemplos del prompt, que debería ser al menos diez
o: El tamaño del modelo, que debería ser el mayor disponible
a: 1
e: Con temperatura mayor que cero, la respuesta se muestrea y cambia entre llamadas. Para tareas con una única respuesta correcta se usa temperatura 0 y, si el proveedor lo permite, un esquema de salida validado; los ejemplos y el tamaño influyen en la calidad, no en la variabilidad entre llamadas idénticas.
:::

:::truco
Antes de tocar el prompt, reúne entre 20 y 50 casos con su respuesta esperada y mide el acierto
actual. Sin esa línea base no puedes saber si el cambio de esta tarde ha mejorado algo o solo ha
arreglado el caso que estabas mirando.
:::
