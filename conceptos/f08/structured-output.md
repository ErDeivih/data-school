---
id: structured-output
titulo: Salida estructurada
fase: 8
nivel: intermedio
rutas: [ds, de]
prerequisitos: [prompting, como-funciona-un-llm, tipos-y-estructuras-python]
tags: [llm, json, validacion, esquemas]
resumen: Pedir al modelo un objeto con campos y tipos, validarlo contra un esquema y reintentar con el error: por qué parsear texto libre con expresiones regulares acaba roto.
fuentes: ["Beurer-Kellner et al. (2023), 'Prompting Is Programming: A Query Language for Large Language Models'"]
---

## En una frase

Salida estructurada es pedirle al modelo datos con forma (un objeto con campos, tipos y
valores permitidos) en lugar de prosa, y tratar esa respuesta como una entrada de usuario:
validarla contra un esquema y rechazarla si no encaja.

## La idea

Supón que quieres extraer de un correo el importe, la moneda y la fecha de vencimiento. Con
prosa obtienes algo como «El importe es de 1.250 euros y vence el 15 de marzo de 2026». Para
usarlo en un programa hay que convertirlo a datos, y ahí empieza el sufrimiento: cada vez que
escribes un `split` o una expresión regular para sacar el importe, aparece una variante nueva
que la rompe.

La solución es no dejar al modelo elegir el formato. Se le da un **esquema**: qué campos hay,
de qué tipo y qué valores se aceptan. El modelo devuelve entonces algo así:

```text
{"importe": 1250.0, "moneda": "EUR", "vencimiento": "2026-03-15"}
```

Y aquí llega la parte que de verdad importa, y que casi todo el mundo se salta: **la respuesta
del modelo es una entrada no confiable**. Aunque el formato sea correcto, los valores pueden
estar mal, faltar un campo o venir el importe como texto. Comparar contra un esquema no es un
trámite: es lo que convierte una generación probabilística en un dato con garantías.

Un esquema tiene cuatro piezas útiles:

- **Campos obligatorios y opcionales.** Si el correo no tiene vencimiento, el campo debe poder
  faltar en lugar de inventarse una fecha.
- **Tipos.** `importe` es un número, no una cadena; `moneda` es un código de tres letras.
- **Restricciones.** El importe no puede ser negativo; la fecha tiene que tener el formato
  ISO `AAAA-MM-DD`; la moneda tiene que estar en una lista cerrada.
- **Campos anidados y listas.** Un pedido con una lista de líneas, cada una con su producto y
  su cantidad.

El fallo en el que cae todo el mundo no es de tipos, es de **reintentos**. Cuando la validación
falla, volver a pedir lo mismo da otra respuesta parecida e igual de inválida. Lo que funciona
es devolver el error concreto al modelo, como si fuera una observación: «el campo `importe`
debe ser un número, y llegó el texto "1.250,00"». Con esa información el modelo corrige. Si el
segundo intento también falla, se para y **falla el proceso**: reintentar sin límite es un
bucle que consume dinero y no mejora nada.

La última pieza es no escribir el validador a mano. Hay bibliotecas que declaran el esquema una
vez y hacen las tres cosas: generar la definición que se le pasa al modelo, validar la
respuesta y producir el error con la ruta exacta del campo que falla. Aquí, para que se vea el
mecanismo, el validador está escrito a mano con lo mínimo.

## Definición formal

Un esquema es una tupla `S = (campos, tipos, restricciones, requeridos)`:

- `campos` — el conjunto de nombres de campo admitidos.
- `tipos` — una función que asigna a cada campo su tipo: `entero`, `numero`, `cadena`,
  `booleano`, `lista`, `objeto`.
- `restricciones` — predicados adicionales sobre el valor: rango, longitud, pertenencia a un
  conjunto cerrado, expresión de formato.
- `requeridos ⊆ campos` — los campos que deben aparecer siempre.

Una respuesta `ŷ` es válida si y solo si se cumplen las cuatro condiciones:

:::formula
valido(ŷ, S) ⇔ requeridos ⊆ claves(ŷ) ∧ claves(ŷ) ⊆ campos ∧ tipos(ŷ) ok ∧ restricciones(ŷ) ok
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `ŷ` | La respuesta del modelo ya convertida a objeto | — | No es una variable que se mueva: o cumple el esquema o se rechaza entera |
| `S` | El esquema: campos, tipos, restricciones y campos requeridos | — | Cuanto más estricto, menos respuestas válidas al primer intento y más reintentos |
| `campos` | El conjunto de nombres de campo admitidos | nombres | Añadir un campo al esquema relaja el rechazo por «campo desconocido» si el modelo lo inventa |
| `tipos` | Función que asigna a cada campo su tipo | — | Endurecer un tipo (`str` a `float`) convierte respuestas que antes pasaban en reintentos |
| `restricciones` | Predicados sobre el valor: rango, longitud, pertenencia a una lista | — | Cada restricción nueva recorta el conjunto de respuestas aceptadas y añade un motivo de error distinto |
| `requeridos` | Subconjunto de `campos` que no puede faltar | nombres | Si crece, más respuestas se rechazan por falta de campo; si encoges, más huecos que rellenar en el código |
:::

Es decir: no falta ningún campo obligatorio, no sobra ningún campo desconocido, cada valor
tiene el tipo declarado y cumple sus restricciones. Las cuatro se comprueban por separado,
porque producen errores distintos y se corrigen de forma distinta.

La función de reintento se define con un límite `n_max`, y lo importante es **qué** se le
devuelve al modelo:

:::formula
error = (campo, motivo)      intento_(j+1) = modelo(prompt, error_j)
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `campo` | La ruta del campo que ha fallado, no un mensaje genérico | — | Cuanto más precisa la ruta (`lineas[2].cantidad`), menos intentos necesita el modelo para acertar |
| `motivo` | Por qué falla y qué se esperaba | — | Un motivo vago («respuesta inválida») deja al modelo repitiendo el mismo error; uno concreto lo corrige |
| `j` | El número de intento, empezando en 1 | intentos | Cada intento es una llamada completa: el coste crece linealmente con `j` |
| `error_j` | El error del intento anterior, que se añade al prompt | — | Es lo único que cambia entre intentos; si no se añade, el reintento es una tirada nueva a la lotería |
| `n_max` | Número máximo de intentos, típicamente 2 o 3 | intentos | Subirlo encarece sin mejorar: agotado el límite hay que fallar de forma explícita |
:::

- `campo` — la ruta del campo que ha fallado (`lineas[2].cantidad`), no un mensaje genérico.
- `motivo` — por qué falla y qué se esperaba («se esperaba un entero mayor que cero»).
- `n_max` — el número máximo de intentos, típicamente 2 o 3. Agotado el límite, el sistema
  debe fallar de forma explícita, no devolver un dato a medias.

Dos advertencias sobre la validación de tipos que ahorran disgustos:

- **Coerción silenciosa.** Muchas bibliotecas convierten `"1250"` en `1250` automáticamente. Es
  cómodo, pero también convierte `"12,50"` en un fallo confuso o en un valor equivocado. Decide
  si admites coerción y, si la admites, sé consciente de que estás aceptando datos que el
  modelo no produjo con el tipo correcto.
- **Validar el esquema no es validar la verdad.** Un importe de 1.250 € con el tipo correcto
  puede ser un importe inventado. La validación garantiza la forma; el contenido se contrasta
  con la fuente, como en [[alucinaciones-y-limites|la comprobación de anclaje]].

## Ejemplo

Esquema de una línea de factura extraída de un correo:

- `concepto`: cadena, obligatorio, entre 1 y 80 caracteres.
- `importe`: número, obligatorio, mayor o igual que cero.
- `moneda`: cadena, obligatoria, en `{EUR, USD, GBP}`.
- `notas`: cadena, opcional.

Tres respuestas del modelo:

| Respuesta | Veredicto | Motivo del rechazo |
| --- | --- | --- |
| `{"concepto": "Licencia anual", "importe": 1250.0, "moneda": "EUR"}` | válida | — |
| `{"concepto": "Licencia anual", "importe": "1250,00", "moneda": "EUR"}` | inválida | `importe` es una cadena, no un número |
| `{"concepto": "Licencia anual", "importe": -10.0, "moneda": "euros"}` | inválida | importe negativo y moneda fuera de la lista |

En el segundo caso, el mensaje que se devuelve al modelo es «el campo `importe` debe ser un
número; llegó la cadena "1250,00"», y no «respuesta inválida». La diferencia de resultado entre
esos dos mensajes es la diferencia entre corregir al primer reintento y no corregir nunca.

Y por qué no vale partir el texto con expresiones regulares: el mismo campo `importe` puede
llegar como `1250.0`, `"1250,00"`, `1.250,00 EUR`, `1250 euros`, `null` o con el campo
renombrado a `total`. Una expresión regular que acierte en los seis casos es más frágil que el
propio modelo, y se rompe en silencio: no falla, devuelve un número equivocado.

## Código

```python verificable
# Validador minimo: sin librerias, para que se vea que comprobar es barato.
ESQUEMA = {
    # el tipo se declara con la CLASE (str, float), no con su nombre entre comillas
    "concepto": {"tipo": str, "requerido": True, "long_min": 1, "long_max": 80},
    "importe": {"tipo": float, "requerido": True, "minimo": 0.0},
    "moneda": {"tipo": str, "requerido": True, "enum": ["EUR", "USD", "GBP"]},   # enum: lista cerrada
    "notas": {"tipo": str, "requerido": False},     # False explicito: este campo puede faltar
}

def validar(dato, esquema=ESQUEMA):
    errores = []
    for campo, regla in esquema.items():        # recorre el ESQUEMA: busca lo que falta y lo que esta mal
        if campo not in dato:
            # .get devuelve None si la clave no existe, y None es falso: sin "requerido" el campo es opcional
            if regla.get("requerido"):
                errores.append((campo, "falta un campo obligatorio"))
            continue                            # sin valor no hay nada mas que comprobar en este campo
        valor = dato[campo]
        if not isinstance(valor, regla["tipo"]):
            # __name__ da el nombre de la clase para el mensaje: "float", no <class 'float'>
            errores.append((campo, "se esperaba " + regla["tipo"].__name__))
        elif "enum" in regla and valor not in regla["enum"]:
            # los elif encadenados: este solo se comprueba si el tipo ya era correcto
            errores.append((campo, "valor fuera de la lista permitida"))
        elif "minimo" in regla and valor < regla["minimo"]:
            errores.append((campo, "valor por debajo del minimo"))
        elif "long_min" in regla and len(valor) < regla["long_min"]:
            # len() aqui es seguro porque el tipo str ya se ha comprobado antes
            errores.append((campo, "texto demasiado corto"))
    for campo in dato:                          # recorre la RESPUESTA: caza los campos que sobran
        if campo not in esquema:
            errores.append((campo, "campo desconocido"))
    return errores                              # lista de tuplas (campo, motivo); vacia = respuesta valida

respuestas = [
    {"concepto": "Licencia anual", "importe": 1250.0, "moneda": "EUR"},
    {"concepto": "Licencia anual", "importe": "1250,00", "moneda": "EUR"},
    {"concepto": "Licencia anual", "importe": -10.0, "moneda": "euros"},
]

for r in respuestas:
    errores = validar(r)
    print(("valida  " if not errores else "rechaza ") + str(errores))
# valida  []
# rechaza [('importe', 'se esperaba float')]
# rechaza [('importe', 'valor por debajo del minimo'), ('moneda', 'valor fuera de la lista permitida')]
```

:::claves
- El esquema guarda la **clase** del tipo (`str`, `float`), no su nombre: `isinstance` la compara directamente. Si escribieras `"tipo": "float"` con comillas, el validador compararía el valor contra la cadena `"float"` y rechazaría **todas** las respuestas.
- `isinstance(1250, float)` es `False`: un importe que llega como `1250` (sin decimales) es un `int` para Python y el esquema que pide `float` lo rechaza. Y al revés, `isinstance(True, int)` es `True`, así que un booleano pasa el control de un campo declarado `int`.
- `validar` **no lanza excepciones**: devuelve una lista de tuplas `(campo, motivo)`. Una lista vacía es falsa, y por eso `if not errores` sirve para decidir si la respuesta vale; la lista es también el mensaje exacto que se le devuelve al modelo en el reintento.
- La cadena `if / elif / elif` informa del **primer** problema de cada campo y se calla el resto: en la tercera respuesta, `importe` solo se queja del mínimo y nunca llega a comprobar la longitud. Si un valor incumple dos reglas, el modelo corrige de una en una.
- `regla.get("requerido")` devuelve `None` cuando la clave no está, y `None` es falso: por eso no poner nada equivale a «opcional». Con `regla["requerido"]` a secas, un campo sin esa clave daría `KeyError` y el validador se caería.
- El segundo bucle recorre `dato`, no `esquema`: iterar un diccionario devuelve sus **claves**, así que ahí se detectan los campos que el modelo se ha inventado. Rechazarlos es una decisión de diseño: ignorarlos también es posible, pero entonces pasan datos que nadie pidió. Y `esquema=ESQUEMA` se evalúa **una sola vez**, al definir la función: mutar ese diccionario por dentro afectaría a todas las llamadas futuras.
:::

```python verificable
import json
import re

# Por que no se parsea texto libre: la misma peticion, cinco variantes del mismo dato.
crudo = [
    '{"importe": 1250.0, "moneda": "EUR"}',
    '{"importe": 1250.0, "moneda": "EUR",}',
    'El resultado es {"importe": 1250.0, "moneda": "EUR"} y nada mas.',
    "```json\n{\"importe\": 1250.0, \"moneda\": \"EUR\"}\n```",
    "Aqui lo tienes: {'importe': 1250.0, 'moneda': 'EUR'}",
]

patron = re.compile(r'"importe"\s*:\s*([0-9.]+)')   # los parentesis capturan el numero como TEXTO

for texto in crudo:
    # quita las vallas de codigo, pero solo las de los extremos: el ^ y el $ lo limitan
    limpio = re.sub(r"^```(?:json)?\s*|\s*```$", "", texto.strip())
    try:
        dato = json.loads(limpio)
        print("json.loads ok     ", dato)
    except json.JSONDecodeError as error:
        # error.pos es la posicion del caracter donde el parser se ha atascado
        print("json.loads falla  ", error.msg, "en la posicion", error.pos)

    coincidencia = patron.search(texto)             # search devuelve un Match, o None si no hay nada
    print("   regex ve         ", coincidencia.group(1) if coincidencia else "nada")
# la regex acierta cuatro veces y falla en la ultima: comillas simples y sin comillas dobles
```

:::figura
fichero: structured-output-validar-o-raspar
pie: A la izquierda, cuántas de las cinco variantes del mismo dato acepta cada estrategia: `json.loads` a pelo acepta 1, quitar antes las vallas de código sube a 2, y la expresión regular encuentra el importe en 4. La tentación es quedarse con la regex, y es justo la decisión equivocada: lo que cuenta no es cuántas variantes acepta, sino qué garantiza cuando acepta. A la derecha se ve dónde falla cada una: la coma final tumba al parser, el texto alrededor solo lo salva la regex, y las comillas simples tumban a las tres. La regex no valida nada —devuelve el número como texto, ignora la moneda y los campos que faltan—, así que con `1.250,00` no falla: devuelve 1,25 y el error llega tres pantallas más tarde.
fuente: figuras/structured-output-1.py
:::

## Errores típicos

- **Parsear la salida con expresiones regulares.** Funciona en los tres ejemplos que pruebas y
  falla en producción con la primera variante que no habías visto: una coma final, comillas
  simples, un bloque de código alrededor o un campo con otro nombre. Cada parche añade una
  regla más a un parser que no debería existir.
- **Validar el JSON pero no el esquema.** `json.loads` solo comprueba que el texto es JSON
  válido. Un objeto sin el campo `importe` es JSON perfectamente válido y arruina el proceso
  que viene después.
- **Reintentar sin cambiar el prompt.** Repetir la misma petición esperando otro resultado
  produce otra respuesta parecida y falla igual. Cada reintento tiene que incluir el error
  concreto del intento anterior.
- **Reintentar sin límite.** Un bucle de validación y reintento sin `n_max` es un bucle
  infinito que gasta dinero. Dos o tres intentos y, si no, fallo explícito.
- **Aceptar campos de más.** Si el esquema declara cuatro campos y llegan siete, los tres
  desconocidos suelen ser invenciones del modelo. Rechazar los campos de más es más seguro que
  ignorarlos en silencio.
- **Confundir el esquema con la verdad.** Que el formato sea correcto no significa que el dato
  sea correcto. El esquema protege tu programa, no a tu usuario: el contenido va contra la
  fuente.
- **Pedir el formato solo con instrucciones y no con el modo estructurado.** Si la API admite
  esquemas o llamada a funciones, úsala: reduce mucho la tasa de respuestas inválidas. Las
  instrucciones en el prompt siguen siendo necesarias, pero son el complemento, no el
  mecanismo.

:::nota
Los esquemas también sirven para el **contrato entre servicios**. Si defines el objeto que
devuelve el extractor, puedes versionarlo, probarlo con casos fijos y detectar cuándo el
proveedor del modelo cambia el comportamiento. Un extractor sin esquema no se puede probar.
:::

## Comprueba que lo sabes

:::quiz
p: El modelo devuelve {"importe": "1250,00", "moneda": "EUR"} y tu esquema espera un número. ¿Cuál es la mejor respuesta del sistema?
o: Convertir la cadena a número con una expresión regular y continuar
o: Rechazar la respuesta y reintentar devolviendo al modelo el campo y el motivo del fallo
o: Reintentar la misma petición sin más, a ver si esta vez sale un número
a: 2
e: Rechazar y reintentar con el error concreto es lo que corrige el problema, porque el modelo puede reaccionar a «importe debe ser un número». Convertir por tu cuenta adivina el valor —y con separadores de miles europeos puede equivocarse—, y repetir la petición sin información nueva suele devolver otra respuesta igual de inválida.
:::

:::quiz
p: ¿Por qué no basta con json.loads para aceptar la respuesta del modelo?
o: Porque es lento con objetos grandes
o: Porque solo comprueba que el texto es JSON válido, no que estén los campos obligatorios, que los tipos sean los correctos ni que los valores estén en rango
o: Porque no admite caracteres acentuados
a: 2
e: Un objeto al que le falta el campo importe, o que lo trae como cadena, es JSON válido y romperá el proceso siguiente. La validación contra el esquema comprueba presencia, tipos, campos desconocidos y restricciones: cuatro cosas que json.loads no mira.
:::

:::quiz
p: Un campo opcional del esquema no aparece en la respuesta del modelo. ¿Qué haces?
o: Es correcto: el campo es opcional y puede faltar
o: Es un error grave y hay que reintentar hasta que aparezca
o: Hay que rellenarlo con una cadena vacía para que el objeto tenga siempre las mismas claves
a: 1
e: Si el campo está declarado como opcional, su ausencia es una respuesta válida y no hay nada que corregir. Reintentar por un campo opcional gasta intentos sin motivo, y rellenarlo con un valor inventado mete datos falsos en el sistema: mejor distinguir «no viene» de «viene vacío».
:::
