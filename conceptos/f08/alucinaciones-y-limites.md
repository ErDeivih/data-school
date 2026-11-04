---
id: alucinaciones-y-limites
titulo: Alucinaciones y límites
fase: 8
nivel: intermedio
rutas: [ds]
prerequisitos: [como-funciona-un-llm, prompting, ventanas-de-contexto, rag-arquitectura]
tags: [llm, fiabilidad, verificacion, limites]
resumen: Por qué un modelo inventa datos con total seguridad, cómo se detecta una respuesta sin apoyo en las fuentes y qué decisiones no se le deben delegar nunca.
fuentes: ["Ji et al. (2023), 'Survey of Hallucination in Natural Language Generation'"]
---

## En una frase

Una alucinación es una respuesta fluida, segura y falsa: el modelo no consulta ningún archivo
de hechos, genera la continuación más probable del texto, y cuando no sabe algo produce algo
que *suena* a lo que sabría.

## La idea

Pide a un modelo que te diga el número de teléfono del departamento de facturación de una
empresa inventada. Te dará un número con el prefijo correcto, el formato correcto y la
seguridad de quien lo ha leído en un directorio. No está mintiendo: no tiene forma de
distinguir «recuerdo este dato» de «este dato encaja aquí».

Eso es todo el fenómeno. Durante el entrenamiento, el modelo aprende a predecir el siguiente
[[tokenizacion|token]] de un texto, y esa tarea premia la fluidez, la coherencia y el ajuste al
contexto, no la verdad. Como consecuencia directa:

- **No hay una base de datos de hechos que consultar.** Lo que el modelo «sabe» está
  distribuido en sus parámetros, de forma difusa y no verificable. No puede citar de dónde lo
  sacó.
- **No sabe lo que no sabe.** Un modelo no tiene una señal interna de «aquí estoy
  improvisando». El mismo tono acompaña a una definición correcta y a una cita inventada.
- **Se ve arrastrado por el contexto.** Si el prompt contiene un dato falso, el modelo tiende a
  usarlo y a construir sobre él. Y si tú insinúas la respuesta en la pregunta, la confirmará.

Los fallos se agrupan en dos familias, y se arreglan de forma distinta:

1. **Fallo de conocimiento.** El dato no está en el contexto ni de forma fiable en los
   parámetros. La solución es [[rag-arquitectura|recuperación]]: traer el dato real y
   obligar al modelo a responder solo con él.
2. **Fallo de fidelidad.** El modelo tiene el dato delante y aun así lo cambia: redondea una
   cifra, invierte un plazo, atribuye una frase al documento equivocado. La solución es
   generar con citas obligatorias —cada afirmación acompañada del fragmento que la sostiene— y
   comprobar automáticamente que el fragmento existe y contiene lo afirmado.

La detección práctica no requiere otro modelo grande. Tres comprobaciones baratas atrapan
buena parte de los casos: **anclaje** (¿aparecen en las fuentes los números, nombres y fechas
de la respuesta?), **consistencia** (¿responde lo mismo si reformulas la pregunta tres veces?)
y **verificación de citas** (¿existe la cita y dice lo que se le atribuye?). Ninguna prueba
que la respuesta sea verdadera: todas prueban que está apoyada. Y eso, en la práctica, es lo
que puedes exigir.

Por último, la parte que no es técnica sino de producto: hay decisiones que no se delegan. Un
modelo puede redactar un borrador de reclamación, extraer los datos de una factura o resumir
un contrato. No debe aprobar un pago, cerrar un diagnóstico, firmar una valoración laboral ni
decidir a quién se concede un crédito. La regla es sencilla: si el coste de un error es alto e
irreversible, el modelo **propone** y una persona o una regla determinista decide.

## Definición formal

Dada una consulta `q`, un contexto recuperado `C = {c₁, …, c_m}` y una respuesta generada
`ŷ = (s₁, …, s_T)` descompuesta en afirmaciones `s_t`, la respuesta es **fiel al contexto** si
cada afirmación está implicada por `C`:

:::formula
fidelidad(ŷ, C) = ( nº de afirmaciones apoyadas por C ) / ( nº total de afirmaciones )
:::

- Una afirmación está **apoyada** si existe al menos un `c_j` que la implica; si no existe,
  es una alucinación por definición, aunque sea verdadera en el mundo real. El modelo no
  puede demostrarlo, y por eso no cuenta.
- Los elementos más fáciles de comprobar y los que más daño hacen son los **atómicos**:
  números, fechas, importes, nombres propios y referencias normativas. Una comprobación de
  anclaje cuenta la fracción de ellos que aparecen literalmente en `C`:

:::formula
anclaje(ŷ, C) = ( nº de números y nombres de ŷ presentes en C ) / ( nº total en ŷ )
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `q` | La consulta del usuario | texto | Si la pregunta insinúa la respuesta («creo que son 30, ¿me equivoco?»), el modelo tiende a confirmarla: la comprobación de consistencia mide justo eso |
| `C` | El contexto recuperado, las fuentes que el modelo tiene delante | fragmentos | Todo lo que no esté en `C` y aparezca en la respuesta cuenta como alucinación, **aunque sea verdad en el mundo real**. Si `C` viene truncado, el fallo es de ventana de contexto, no de invención |
| `ŷ` | La respuesta generada, descompuesta en afirmaciones | texto | Se mide afirmación a afirmación, no frase a frase: una frase con dos afirmaciones, una apoyada y otra no, baja la fidelidad |
| `s_t` | Una afirmación concreta de la respuesta | una frase con un dato | Es la unidad de medida. Cuantas más afirmaciones atómicas tenga la respuesta, más fácil es que alguna no esté apoyada |
| `fidelidad(ŷ, C)` | Fracción de afirmaciones implicadas por el contexto | entre 0 y 1 | Por debajo de 1 hay algo inventado o mal atribuido, y el número no distingue cuál de las dos cosas |
| `anclaje(ŷ, C)` | Fracción de números y nombres propios que aparecen literalmente en `C` | entre 0 y 1 | Sube cuando la respuesta se limita a repetir datos de la fuente. **No sube** por combinar bien los datos: los números pueden estar todos y el orden estar invertido |
:::

Dos advertencias sobre estas medidas:

- El anclaje es **condición necesaria, no suficiente**. Una respuesta puede usar solo números
  del contexto y aun así combinarlos al revés («el plazo es 30 y el interés 3,75» cuando el
  contexto dice lo contrario). Es un filtro barato, no una prueba.
- La fidelidad se mide sobre **afirmaciones**, no sobre frases. Partir la respuesta en frases
  es una aproximación: una frase con dos afirmaciones, una apoyada y otra no, cuenta como una
  sola unidad.

Distinción que conviene no perder: **alucinación** es afirmar algo sin apoyo;
**abstención** es responder «no consta en la documentación». Un sistema que se abstiene más a
menudo puede ser mejor que uno que responde siempre, aunque parezca menos útil.

## Ejemplo

Contexto recuperado (una única fuente):

```
"Las devoluciones se admiten dentro de los 14 dias naturales desde la entrega. Para
productos personalizados el plazo es de 7 dias. El reembolso se emite en un maximo de
5 dias laborables tras la recepcion."
```

Tres respuestas a la pregunta «¿cuántos días tengo para devolver un producto?»:

| Respuesta | Números usados | Anclaje | ¿Fiel? |
| --- | --- | --- | --- |
| «14 días naturales desde la entrega» | 14 | 1/1 | sí |
| «30 días naturales según la normativa europea» | 30 | 0/1 | no |
| «14 días, o 10 si es personalizado» | 14, 10 | 1/2 | no |

- La primera es correcta y está anclada.
- La segunda usa un número que **no aparece** en el contexto y añade una atribución normativa
  inventada. Es fluida, plausible y falsa en las dos cosas.
- La tercera es la trampa fina: el 14 es correcto, pero el 10 no está en ninguna parte. La
  respuesta parece medio buena y sería la más peligrosa de las tres, porque un lector que
  reconoce el 14 baja la guardia con el 10.

Un comprobador que exija que **todos** los números de la respuesta aparezcan en el contexto
rechaza la segunda y la tercera, y deja pasar la primera. Cuesta unas pocas líneas de código y
atrapa el error más frecuente y más caro.

## Código

```python verificable
import re

contexto = ("Las devoluciones se admiten dentro de los 14 dias naturales desde la entrega. "
            "Para productos personalizados el plazo es de 7 dias. El reembolso se emite "
            "en un maximo de 5 dias laborables tras la recepcion.")

respuestas = [
    "Tienes 14 dias naturales desde la entrega.",
    "Tienes 30 dias naturales segun la normativa europea.",
    "Tienes 14 dias, o 10 si el producto es personalizado.",
]

# set() de todos los numeros de la fuente: la comprobacion es por coincidencia exacta
numeros_contexto = set(re.findall(r"\d+", contexto))

for r in respuestas:
    # \d+ encuentra cada numero de la respuesta; findall devuelve texto, no enteros
    numeros = re.findall(r"\d+", r)
    # el anclaje se mide numero a numero: los que no estan en la fuente se cuentan aparte
    anclados = [n for n in numeros if n in numeros_contexto]
    # exigir TODOS anclados es lo que rechaza la respuesta 3, la mas peligrosa
    fiel = len(anclados) == len(numeros)
    print(f"anclaje {len(anclados)}/{len(numeros)}  fiel {fiel}  {r[:40]}")
# solo la primera usa exclusivamente numeros que estan en el contexto
```

:::claves
- `re.findall(r"\d+", texto)` devuelve una **lista de cadenas**, no de números: `"14"`, no `14`. Es lo correcto aquí, porque la comprobación es de coincidencia exacta contra el texto de la fuente; si convirtieras a `int` perderías los ceros a la izquierda y los decimales.
- `\d+` encuentra **cualquier** secuencia de dígitos, también la del «3,75 %» o la de un número de teléfono. No distingue un importe de una fecha: para eso haría falta un patrón por tipo, y ahí es donde esta comprobación barata empieza a fallar.
- `numeros_contexto` es un `set`, así que la pertenencia `n in numeros_contexto` es inmediata aunque la fuente tenga miles de números. Con una lista, cada comprobación recorrería la fuente entera.
- `fiel = len(anclados) == len(numeros)` exige que **todos** los números estén anclados. Es deliberadamente estricto: la respuesta 3 («14 días, o 10…») se marca como no fiel aunque el 14 sea correcto, y ese es el caso que interesa atrapar.
- La comprobación **no demuestra que la respuesta sea verdadera**, solo que sus números aparecen en la fuente. Una respuesta puede combinar números reales al revés («el plazo es 30 y el interés 3,75» cuando el contexto dice lo contrario) y pasar el filtro. Es condición necesaria, no suficiente.
- Si una respuesta **no usa ningún número**, `numeros` está vacío y `fiel` sale `True` por la igualdad `0 == 0`: el anclaje no dice nada de las respuestas cualitativas, ni buenas ni malas.
:::

```python verificable
# Consistencia: la misma pregunta formulada de tres maneras. Un dato estable se repite;
# un dato inventado cambia con la formulacion.
variantes = {
    "directa": "El plazo es de 14 dias naturales.",
    "con contexto": "Segun la documentacion, 14 dias naturales.",
    "reformulada": "14 dias.",
    "con presion": "Creo que son 30, corrigeme si me equivoco: el plazo es de 30 dias.",
}

def extraer_plazo(texto):
    # el import esta aqui dentro: la funcion es autonoma, sin depender del bloque de arriba
    import re
    m = re.search(r"\d+", texto)          # search devuelve None si no hay ningun numero
    return int(m.group()) if m else None  # .group() da el texto; int() lo convierte

# un diccionario por comprension: variante -> plazo extraido
plazos = {k: extraer_plazo(v) for k, v in variantes.items()}
for k, v in plazos.items():
    print(f"{k:>13}: {v} dias")

# set() elimina los repetidos: cuantos valores distintos aparecen en total
distintos = set(plazos.values())
print("respuestas distintas:", len(distintos), "->", sorted(distintos))
print("estable:", len(distintos) == 1)
# la variante 'con presion' demuestra que el modelo confirma la cifra que le sugiere el usuario
```

:::figura
fichero: alucinaciones-anclaje-y-consistencia
pie: A la izquierda, las tres respuestas del ejemplo descompuestas número a número: en verde los que aparecen en la fuente, en rojo —con un círculo— los que no aparecen en ninguna parte. La respuesta 1 tiene todo anclado (1/1); la 2 no tiene nada (0/1); la 3 tiene anclaje 1/2 porque el 14 es correcto y el 10 está inventado. Esa es la trampa fina: un lector que reconoce el 14 baja la guardia con el 10, y por eso la tercera es la más peligrosa de las tres. A la derecha, la comprobación de consistencia: la misma pregunta formulada de cuatro maneras responde siempre 14 días, hasta que la última variante insinúa el 30 en el enunciado y el modelo lo confirma. Un dato estable se repite; uno inventado cambia con la formulación.
fuente: figuras/alucinaciones-y-limites-1.py
:::

## Errores típicos

- **Pedir al modelo que revise su propia respuesta y confiar en el veredicto.** «¿Estás
  seguro?» produce una respuesta más segura, no más verdadera: el modelo no tiene acceso a
  ninguna fuente nueva entre las dos preguntas. La verificación tiene que ser externa, contra
  el contexto o contra una fuente de datos.
- **Usar la fluidez como señal de calidad.** El estilo seguro y bien estructurado es
  exactamente igual en las respuestas correctas y en las inventadas. Ninguna métrica de forma
  (longitud, tono, vocabulario) distingue unas de otras.
- **Creer que la temperatura 0 elimina el problema.** Bajar la temperatura reduce la variedad
  de las respuestas, no la invención. Un dato falso es igual de falso en la respuesta más
  probable.
- **Dejar números, fechas y nombres sin comprobar.** Son los elementos con consecuencias
  reales y los más fáciles de verificar por coincidencia exacta con la fuente. Revisar el
  estilo de un párrafo y no comprobar el importe es revisar lo que no importa.
- **No dar al modelo la opción de no responder.** Si el prompt exige una respuesta y el
  contexto no la contiene, el modelo improvisa. Añade una salida explícita: «si la respuesta
  no está en el contexto, responde que no consta».
- **Comprimir el contexto hasta que la respuesta desaparece.** El modelo alucina también
  cuando el dato existía y se truncó: es un fallo de
  [[ventanas-de-contexto|ventana de contexto]] presentado como alucinación.
- **Delegar decisiones irreversibles.** Aprobaciones de pago, diagnósticos, sanciones o
  valoraciones de personas necesitan una regla determinista y una persona responsable. La
  fidelidad al contexto no protege de un contexto sesgado o incompleto.

:::trampa
Un sistema que cita fuentes parece fiable y no lo es por defecto: si nadie comprueba que las
citas existen y dicen lo que se les atribuye, has añadido un formato convincente a una
respuesta igual de inventada. La cita es útil solo cuando su contenido se verifica.
:::

## Comprueba que lo sabes

:::quiz
p: Preguntas por el teléfono de un departamento que no existe en ninguna fuente y el modelo te da uno con el formato correcto. ¿Qué ha pasado?
o: El modelo ha consultado un directorio interno
o: Ha generado el texto más plausible, porque su objetivo es la continuación probable y no tiene forma de saber que ese dato no lo conoce
o: Ha alucinado a propósito para señalar que falta información
a: 2
e: No hay directorio ni intención: el modelo predice el siguiente token y un número de teléfono con el formato correcto es una continuación muy probable. Lo importante es la consecuencia práctica: no tiene ninguna señal interna que distinga «lo sé» de «encaja aquí».
:::

:::quiz
p: En un contexto que dice «14 días naturales, 7 si es personalizado», el modelo responde «14 días, o 10 si es personalizado». ¿Qué comprobación lo detecta?
o: Comparar la longitud de la respuesta con la de las anteriores
o: Verificar que todos los números de la respuesta aparecen en el contexto: el 10 no está
o: Preguntar al modelo si está seguro de esa cifra
a: 2
e: El 10 no aparece en ninguna fuente, y la comprobación de anclaje por coincidencia exacta lo detecta sin necesidad de otro modelo. La longitud no dice nada sobre la veracidad, y preguntar al modelo produce una confirmación más segura, no una comprobación.
:::

:::quiz
p: ¿Cuál de estas tareas es razonable delegar en un modelo de lenguaje sin revisión humana?
o: Aprobar una solicitud de crédito de 40.000 euros
o: Redactar un borrador de respuesta a una reclamación para que lo revise una persona
o: Emitir un diagnóstico a partir de unos síntomas
a: 2
e: La redacción de un borrador es reversible y verificable: si está mal, se corrige antes de enviarlo. Las otras dos tienen consecuencias altas e irreversibles sobre personas, y necesitan una regla determinista y un responsable identificable, aunque el modelo ayude a preparar el expediente.
:::
