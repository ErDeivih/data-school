---
id: privacidad-y-datos-en-llms
titulo: Privacidad de datos en LLMs
fase: 8
nivel: avanzado
rutas: [ds]
prerequisitos: [bases-de-datos-vectoriales, coste-y-latencia]
tags: [privacidad, llm, rgpd, datos]
resumen: Cada prompt es una transferencia de datos a un tercero: que sale, quién lo recibe, cuánto se guarda y que no debería salir nunca de casa.
fuentes: ["Reglamento (UE) 2016/679 (RGPD), articulos 5, 6 y 28", "AEPD (2021), 'Adecuacion al RGPD de tratamientos que incorporan Inteligencia Artificial'"]
---

## En una frase

Usar un modelo alojado significa mandar tu texto a la maquina de otro: si ese texto lleva datos
de personas, tienes una cesion de datos con obligaciones legales, y hay categorias de
información que simplemente no deben salir de tu infraestructura.

## La idea

Piensa en la diferencia entre escribir un informe en tu portatil y dictarselo por telefono a una
empresa para que lo redacte. En el primer caso el texto no sale de casa. En el segundo, alguien
lo está oyendo, decidiendo si lo guarda, y quiza usandolo para mejorar su servicio. No es
irrelevante quien escucha: si el informe lleva nombres de clientes, diagnosticos o nominas,
acabas de hacer una cesion de datos personales sin haberlo decidido conscientemente.

Eso es exactamente lo que ocurre cada vez que llamas a un LLM alojado. Hay tres categorias de
exposición que conviene separar porque se arreglan de forma distinta:

1. **Lo que envias en el prompt.** La pregunta, el fragmento recuperado, el historial de la
   conversación y los ejemplos que uses. Todo eso viaja al proveedor en cada llamada.
2. **Lo que envias al indexar.** Menos evidente y más olvidado: si calculas los vectores con el
   *embedding* del proveedor, le estas enviando los documentos enteros, uno a uno. Mucha gente
   cree que «solo subo vectores» cuando en realidad ya subió el texto.
3. **Lo que el proveedor hace con ello.** Retención para abuso, registro de peticiones,
   entrenamiento con datos de clientes, subencargados y ubicación fisica del tratamiento. Esto
   no lo decides tu: lo decide el contrato.

Sobre el tercer punto hay una base legal concreta en Europa. Los datos personales se rigen por el
RGPD, y el proveedor que trata datos por tu cuenta es un **encargado del tratamiento**, lo que
exige un contrato de encargo con sus garantías. Además, si el tratamiento sale del Espacio
Economico Europeo, entran en juego las garantías de transferencia internacional. Y hay una
categoria que no admite matices: los datos de categorias especiales (salud, ideologia, religion,
orientación sexual, biometria) tienen un régimen mucho más estricto. Si tu caso de uso los toca,
el proveedor externo deja de ser una opcion razonable.

Un matiz que se confunde constantemente: **anonimizar no es lo mismo que seudonimizar**. Si
eliminas los identificadores de un texto, pero conservas una tabla que permite volver a
identificar a la persona, no has anonimizado: has seudonimizado, y el dato sigue siendo
personal. La prueba es sencilla: si con información adicional razonablemente disponible se puede
volver a la persona, no es anonimo.

:::aviso
El texto que se envia al calcular un embedding también es tu documento. Si indexas con el
servicio del proveedor, tu corpus completo pasa por sus servidores. Para corpus sensibles, el
primer paso es calcular los vectores en local con un modelo abierto; el detalle del índice está
en [[bases-de-datos-vectoriales|las bases de datos vectoriales]].
:::

Antes de elegir proveedor, cuatro preguntas concretas, con respuesta escrita y no de oidas:

- ¿Se usan mis datos para entrenar? Que la respuesta sea no, por contrato.
- ¿Cuánto tiempo se retienen las peticiones y los registros? Hay modalidades de retención cero.
- ¿Dónde se procesan y quienes son los subencargados?
- ¿Se pueden borrar mis datos y los de mis usuarios si lo pido? En que plazo.

Las técnicas que reducen el riesgo, de menos a más coste: **minimizar** (no mandar campos que no
hacen falta y quitar identificadores antes de enviar), **seudonimizar** (sustituir nombres por
referencias que se resuelven en tu sistema), **elegir la configuración sin retención ni
entrenamiento**, **desplegar modelos abiertos en tu propia infraestructura** y, si el dato es
especialmente sensible, **no usar el modelo para ese flujo en absoluto**. La última es una
opcion legitima y a veces la única correcta.

## Definición formal

Sea `T` el texto que se envia al proveedor en una llamada. Define la exposición como el conjunto
de información identificable que contiene:

:::formula
expuesto(T) = { c en T : c es dato personal }  más  los metadatos de la llamada
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `T` | El texto completo que sale en una llamada: instrucciones, pregunta, fragmentos e historial | tokens | Cada fragmento recuperado y cada turno arrastrado suman a la exposición, aunque no lleven nombres |
| `c` | Cada trozo de información que permite identificar a una persona, directa o indirectamente | — | Basta con que crezca uno: un número de pedido o un texto libre pueden identificar sin nombre |
| `metadatos` | IP, identificador de usuario, hora y traza de la petición | — | No los escribes tú y también son datos personales: se acumulan aunque el prompt esté limpio |
| `expuesto(T)` | El conjunto de información identificable que viaja al proveedor | — | Es lo que hay que reducir antes de enviar; no depende de la buena voluntad del proveedor |
:::

- `T` — el prompt completo: instrucciones, entrada del usuario, fragmentos recuperados e
  historial.
- `c` — cada fragmento de información que permite identificar a una persona, directa o
  indirectamente.
- **metadatos** — dirección IP, identificador de usuario, hora y traza de la petición; también
  son datos personales aunque no los escribas tu.

El principio de minimización se escribe entonces como una condición sobre esa exposición:

:::formula
expuesto(T) contenido en lo_necesario(objetivo)   y   retención <= plazo_justificado
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `lo_necesario(objetivo)` | El conjunto mínimo de datos para cumplir la finalidad declarada | campos o categorías | Cuanto más amplio lo declares, más justificas enviar; declararlo ancho para «por si acaso» es lo que rompe la minimización |
| `objetivo` | La finalidad concreta del tratamiento: clasificar tickets, resumir correos | — | Un objetivo vago justifica cualquier dato; uno concreto deja fuera lo que no aporta |
| `retención` | El tiempo que el proveedor guarda `T` y sus registros | días | Más retención es más exposición y más obligaciones que atender ante una petición de acceso o supresión |
| `plazo_justificado` | El plazo que puedes defender ante la autoridad de control | días | No lo fija el proveedor: si su retención por defecto es mayor, hay que pedir la modalidad sin retención y dejarla por escrito |
| `base jurídica` | Consentimiento, ejecución de contrato, interés legítimo u obligación legal | — | Sin base jurídica, minimizar no arregla nada: la condición previa es que exista y que el titular esté informado |
:::

- `lo_necesario(objetivo)` — el conjunto mínimo de datos para cumplir la finalidad declarada.
- `retencion` — el tiempo que el proveedor guarda `T` y sus registros.
- `plazo_justificado` — el plazo que puedes defender ante la autoridad de control.

Y una condición previa que suele olvidarse: tiene que existir base juridica para ese tratamiento
(consentimiento, ejecución de contrato, interes legitimo, obligación legal) y hay que informar
al titular de que sus datos se tratan así.

## Ejemplo

Una empresa de software quiere un asistente que clasifique tickets de soporte. Cada ticket lleva
el nombre del cliente, su correo, el número de pedido y, a veces, el texto libre donde el
usuario cuenta cosas personales.

Comparación de dos disenos sobre 1.000 tickets al día:

- **Diseno A: enviar el ticket tal cual.** Cada ticket son unos 300 tokens; 1.000 tickets al día
  son 300.000 tokens diarios de texto con identificadores directos enviados a un tercero, unos
  9 millones de tokens al mes. Coste de modelo: a 1 dolar por millon de tokens de entrada,
  unos **9 dolares al mes**, más el coste de cumplimiento: registros de tratamiento, contrato de
  encargo y respuesta a cualquier petición de acceso que incluya esos envios.
- **Diseno B: minimizar antes de enviar.** Sustituyes nombre y correo por un identificador
  interno (`cli-8823`), quitas el número de pedido y recortas el texto libre a los primeros 200
  caracteres. Cada ticket baja a unos 120 tokens: 3,6 millones al mes, unos **3,6 dolares**.
  Además el identificador se resuelve en tu base de datos, así que el proveedor no ve nunca a
  quien pertenece.
- **Diseno C: modelo local.** No se envia nada. Necesitas una maquina con GPU y asumir tu el
  mantenimiento; para una tarea de clasificación acotada suele ser viable, y el coste por
  ticket deja de depender de un proveedor externo.

El diseño B cuesta un tercio que el A y, más importante, reduce el alcance del tratamiento a lo
estrictamente necesario. El C elimina la cesion por completo. La elección depende de la
sensibilidad del texto y de si el flujo necesita un modelo grande: casi nunca la decisión se
decide por el precio.

:::figura
fichero: privacidad-y-datos-en-llms-lo-que-sale
pie: A la izquierda, lo que cruza la frontera cada mes con 1.000 tickets al día: el diseño A manda 9 millones de tokens con el nombre y el correo dentro; el B, con el ticket minimizado, manda 3,6 millones ya seudonimizados; el C, con modelo local, no manda nada. La bajada de A a B no es solo de volumen, es de naturaleza del dato: los 3,6 millones ya no identifican a nadie en el proveedor. A la derecha, el coste del modelo, que es la parte fácil de medir: baja de 9 $ a 3,6 $ al mes. Lo que no baja con el precio del token es el coste de cumplimiento (contrato de encargo, registro del tratamiento y respuesta a las peticiones de acceso), y por eso la decisión de diseño no se toma mirando solo la factura del modelo.
fuente: figuras/privacidad-y-datos-en-llms-1.py
:::

## Código

```python verificable
import re

# Minimizar antes de enviar: quitar identificadores directos del texto.
ticket = "Soy Ana Ruiz (ana.ruiz@ejemplo.es), pedido 4471, no me llega el pedido."

def minimizar(texto):
    # El correo se sustituye sin comerse los parentesis que lo rodean.
    # [^\s()] es "todo menos espacio o parentesis"; re.sub devuelve una cadena NUEVA, no toca texto
    sin_correo = re.sub(r"[^\s()]+@[^\s()]+", "[correo]", texto)
    # depende de tres cosas a la vez: la palabra "Soy", las mayusculas y un nombre de dos palabras
    sin_nombre = re.sub(r"Soy [A-Z][a-z]+ [A-Z][a-z]+", "Soy [cliente]", sin_correo)
    # \d+ es "uno o mas digitos": solo cae el numero que va detras de la palabra pedido
    return re.sub(r"pedido \d+", "pedido [ref]", sin_nombre)

limpio = minimizar(ticket)                       # el original sigue intacto: se trabaja sobre copias
print(limpio)
# -> Soy [cliente] ([correo]), pedido [ref], no me llega el pedido.
# len cuenta CARACTERES, no tokens: la rebaja de 71 a 62 no mide el riesgo que se quita
print("caracteres originales:", len(ticket))     # -> 71
print("caracteres enviados  :", len(limpio))     # -> 62
```

:::claves
- `re.sub` **no modifica** la cadena: devuelve una nueva. `ticket` sigue teniendo el nombre y el correo después de llamar a `minimizar`, y las tres sustituciones se encadenan porque cada una recibe la salida de la anterior. Si la tercera usara `texto` en vez de `sin_nombre`, se perderían las dos primeras.
- `[^\s()]+@[^\s()]+` se lee «todo lo que no sea espacio ni paréntesis, una arroba, y otra vez lo mismo»: por eso los paréntesis que rodean al correo sobreviven y el resultado no queda con un hueco raro.
- La regla del nombre depende de tres cosas a la vez: la palabra «Soy», las mayúsculas y un nombre de exactamente dos palabras. `Soy ana ruiz` en minúsculas, `Soy Ana` o `Soy Ana Ruiz García` pasan sin sustituir, y el nombre viaja al proveedor. Es el fallo clásico de la minimización con expresiones regulares.
- `\d+` significa «uno o más dígitos»: la tercera regla borra el número que sigue a la palabra `pedido`, pero deja intacta la palabra `pedido` sin número del final de la frase. Las reglas sustituyen lo que encaja con el patrón, no lo que tú querías decir.
- `len(ticket)` cuenta **caracteres**, no tokens: la rebaja de 71 a 62 caracteres es un 13 % menos de texto y no dice nada del riesgo que se quita. El objetivo de minimizar no es enviar menos letras, es no enviar identificadores.
- Lo que sale sigue siendo **seudonimización**, no anonimización: `[cliente]`, `[correo]` y `[ref]` se revierten con la tabla que los resuelve, así que el dato sigue siendo personal y el RGPD se sigue aplicando. Cambiar el nombre por una referencia reduce el riesgo; no lo elimina.
:::

```python ilustrativo
# Auditoria de lo que sale de casa: una lista corta que evita sustos.
FLUJOS = [
    {"nombre": "clasificador de tickets", "destino": "proveedor-externo",
     "campos": ["texto_anonimizado"]},
    {"nombre": "indice de manuales publicos", "destino": "proveedor-externo",
     "campos": ["pdf_publico"]},
    {"nombre": "informes medicos", "destino": "modelo-local",
     "campos": ["historia_clinica"]},
]

for f in FLUJOS:
    # une la lista de campos en una sola cadena para poder buscar dentro; el `in` de Python
    # es una busqueda de subcadena, por eso "clinica" encuentra "historia_clinica"
    sensible = "clinica" in " ".join(f["campos"])
    riesgo = "alto" if sensible else "bajo"          # expresion condicional: "alto" si sensible, si no "bajo"
    if riesgo == "alto":
        # el segundo argumento del assert es el mensaje que se ve si falla; con python -O los assert no se ejecutan
        assert f["destino"] == "modelo-local", f["nombre"]
    print(f["nombre"], f["destino"], riesgo)
```

## Errores típicos

- **Creer que no envias datos porque el prompt no lleva nombres.** Un historial de conversación,
  un número de pedido o el propio texto libre identifican a menudo a una persona concreta. Y los
  metadatos de la llamada (IP, identificador de sesión) ya son datos personales.
- **Confundir seudonimizar con anonimizar.** Cambiar el nombre por `cli-8823` no convierte el
  dato en anonimo si tu tienes la tabla que lo resuelve. Sigue siendo dato personal y sigue
  necesitando base juridica.
- **Olvidar el paso de indexación.** El corpus entero pasa por el proveedor cuando vectorizas
  con su modelo de embeddings. Si el corpus es sensible, la fuga ocurre antes de la primera
  consulta, no durante las respuestas.
- **No leer la política de retención y entrenamiento.** Es la diferencia entre «texto que se
  procesa y se olvida» y «texto que se guarda y puede acabar en un entrenamiento futuro». Hay
  modalidades de retención cero: se piden por escrito y quedan en el contrato.
- **Guardar la clave de API en el cliente.** En una aplicación web, la clave en el navegador
  permite a cualquiera usar tu cuenta; y si el proxy no filtra, también enviar lo que quiera.
  La clave vive en el servidor y el servidor decide que se reenvia.
- **Mandar datos de salud por comodidad.** Es la categoria que más rapido convierte un
  experimento en un incidente. Para eso, modelo local o nada.

## Comprueba que lo sabes

:::quiz
p: Sustituyes los nombres de tus clientes por identificadores internos antes de enviar el texto a un proveedor de LLM. ¿Que has hecho?
o: Anonimizar: el dato ya no es personal y no aplica el RGPD
o: Seudonimizar: el dato sigue siendo personal porque tu puedes revertir la sustitución
o: Nada relevante: el proveedor no conserva el texto
a: 2
e: La seudonimización reduce el riesgo pero no saca el dato del ambito del RGPD: mientras exista una tabla que permita volver a la persona, sigue siendo dato personal. Solo la anonimización real, irreversible con medios razonables, queda fuera.
:::

:::quiz
p: ¿Que exposición se pasa por alto con más frecuencia al montar un RAG con un proveedor externo?
o: Los documentos que se envian al calcular los embeddings durante la indexación
o: Las respuestas que devuelve el modelo
o: Las etiquetas de la interfaz de usuario
a: 1
e: La indexación envia el corpus completo, fragmento a fragmento, al servicio de embeddings. Es una transferencia de datos tan real como la consulta, y ocurre una sola vez, antes de que el sistema este en producción, por lo que nadie la revisa. Calcular los vectores en local con un modelo abierto lo evita.
:::

:::trampa
La frase «tranquilo, el proveedor no entrena con nuestros datos» no resuelve el problema por si
sola. Sigue habiendo comunicación de datos a un tercero, con su contrato de encargo, su
retención y su ubicación. La privacidad no es una casilla que se marca: es una lista de
decisiones sobre que sale, hacia donde y por cuanto tiempo.
:::
