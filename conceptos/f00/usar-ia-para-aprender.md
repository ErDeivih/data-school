---
id: usar-ia-para-aprender
titulo: Usar la IA para aprender sin engañarte
fase: 0
nivel: básico
rutas: [core]
prerequisitos: [como-estudiar, hacer-preguntas-buenas]
tags: [metodo, ia, estudio, verificar]
resumen: Un modelo puede ser tu tutor o tu atajo, y solo se distinguen al defender el resultado: pide explicaciones, comprueba cada afirmación y no pegues código que no entiendas.
fuentes: ["Bender et al. (2021), 'On the Dangers of Stochastic Parrots: Can Language Models Be Too Big?'", "Ji et al. (2023), 'Survey of Hallucination in Natural Language Generation'"]
---

## En una frase

Un modelo de lenguaje es un buen tutor y un atajo peligroso, y la diferencia no está en la
herramienta sino en lo que haces después: pedir que te explique, comprobar lo que afirma y no dar
por bueno nada que no puedas defender tú.

## La idea

Aprender con un modelo se parece a cocinar con alguien que te dicta la receta por teléfono mientras
tú no ves la cocina. Si te dice «dos cucharadas de sal» y las echas sin probar, el plato lo decide
él. Si pruebas, corriges y entiendes por qué hacía falta sal, el plato es tuyo.

El detalle que lo cambia todo: un modelo de lenguaje no consulta un archivo de verdades. Escribe la
continuación más probable de lo que le preguntas. Por eso acierta casi siempre en lo común y falla
con toda tranquilidad en lo raro: el nombre exacto de un argumento que cambió de versión, el
comportamiento de una función de la que hay veinte versiones, un número. No ejecuta tu código, no
ve tu dataset y no sabe cuál es tu versión de pandas. Cuando se equivoca no se queda callado:
rellena el hueco con algo plausible, que es justo lo que lo hace difícil de detectar.

De ahí salen dos usos que no tienen nada que ver:

1. **Pedir explicaciones.** «Explícame por qué aquí se divide entre n − 1», «hazme tres preguntas
   para ver si lo he entendido», «¿qué supuestos está dando por hechos este trozo?». Este uso te
   deja algo: sales sabiendo más de lo que entraste.
2. **Pedir la solución.** «Dame el código que rellena los nulos con la media». Si lo copias sin
   entenderlo, has cambiado el problema de sitio: funciona hoy y no lo puedes tocar mañana.

Y una comprobación que casi todo el mundo hace mal: preguntarle «¿estás seguro?». Eso no verifica
nada, es pedir una segunda opinión al mismo que te dio la primera. Verificar es ejecutar, medir o
leer la documentación de **tu** versión, que es la única fuente que no se inventa nada.

El filtro que separa los dos usos es incómodo y cabe en una pregunta: **¿puedo explicar cada línea
en voz alta y decir qué pasa si cambio un dato?** Si la respuesta es no, todavía no es tuyo. Es la
misma idea que sostiene [[como-estudiar]]: lo que consolida es recuperar y comprobar, no reconocer
algo como familiar.

:::figura
fichero: usar-ia-entender-frente-a-comprobar
pie: Las dos preguntas que hay que hacerse con una respuesta de un modelo. Solo la casilla de arriba a la derecha es código tuyo: lo entiendes y lo has comprobado. Las otras tres son deuda con distinto plazo: la hipótesis que suena bien y nadie ha probado, el fragmento que funciona y no sabes tocar, y el atajo que se paga en el primer cambio.
fuente: figuras/usar-ia-para-aprender-1.py
:::

## Definición formal

Una respuesta se puede usar cuando pasa tres pruebas, y en este orden:

1. **Explicarla.** Puedes contar qué hace cada línea, por qué está ahí y qué pasaría si la quitas.
2. **Reproducirla.** La has ejecutado o medido tú, con tus datos, y el resultado coincide con lo
   que la respuesta decía. Sin esta prueba, «me lo ha dicho» no es «lo he comprobado».
3. **Defenderla.** Si te preguntan «¿por qué así y no de otra forma?», tienes una respuesta que no
   empieza por «porque lo vi en internet».

Lo que te has saltado se puede medir en una cifra fea pero útil:

:::formula
deuda_de_comprensión = líneas_sin_defensa / líneas_pegadas
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `líneas_sin_defensa` | Líneas que has metido en tu proyecto y no sabrías explicar ni cambiar | ninguna (recuento) | Sube la deuda: el siguiente cambio se apoya en código que no controlas |
| `líneas_pegadas` | Todo el código que entra en el proyecto, lo hayas escrito tú o no | ninguna (recuento) | No baja el cociente por sí sola: pegar más deprisa sin entender lo empeora |
| `deuda_de_comprensión` | Qué parte del proyecto no puedes defender | entre 0 y 1, o en % | Cada punto que sube encarece el siguiente cambio, porque primero hay que entender lo que ya está |
:::

:::nota
Es una comprobación, no una métrica de equipo: se mide leyendo el código en voz alta, no contando
líneas con una herramienta. Si no puedes explicar una línea, no la defiendas en una entrevista.
:::

## Ejemplo

Le preguntas al modelo cómo sacar la desviación típica de una columna y contesta: «usa
`serie.std()`». La respuesta es correcta y, a la vez, incompleta. Con los ocho valores 2, 4, 4, 4,
5, 5, 7 y 9:

- `serie.std()` de pandas da **2,13809**.
- `np.std(serie)` de NumPy da **2,0**.

La misma palabra, dos números, porque pandas divide entre n − 1 y NumPy entre n. Si no lo
compruebas, escribes en el informe una cifra cuyo significado no conoces; si lo compruebas —tres
líneas, las del bloque de abajo—, acabas de aprender para qué sirve `ddof` y ya sabes defender cuál
de las dos usas.

Fíjate en la forma del fallo: no es un error de sintaxis que salta al ejecutar, es una respuesta
razonable que produce un número distinto del que crees. Ese es el tipo de error que solo detecta la
comprobación.

## Código

```python verificable
import numpy as np
import pandas as pd

# La respuesta del modelo: "usa .std() para la desviacion tipica". Es correcta y ambigua:
# pandas y NumPy no dividen entre lo mismo, y la diferencia se ve en la tercera cifra.
serie = pd.Series([2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0])

print(f"pandas .std()       {serie.std():.5f}")             # -> 2.13809
print(f"numpy  .std()       {np.std(serie):.5f}")           # -> 2.00000
print(f"numpy  .std(ddof=1) {np.std(serie, ddof=1):.5f}")   # -> 2.13809
print(f"se llevan           {serie.std() / np.std(serie) - 1:.1%}")   # -> 6.9%
```

```python verificable
# Antes de pegar codigo, tres preguntas de defensa: ¿y si la lista esta vacia?, ¿y si
# falta un dato?, ¿y si llega un texto? Lo que no sepas contestar, no lo pegues.
def ticket_medio(importes):
    return sum(importes) / len(importes)

casos = {
    "tres importes": [10.0, 20.0, 30.0],
    "un nulo":       [10.0, None, 30.0],
    "sin ventas":    [],
}
for nombre, datos in casos.items():
    try:
        print(f"{nombre:14s} -> {ticket_medio(datos)}")
    except Exception as error:
        print(f"{nombre:14s} -> {type(error).__name__}: {error}")
# -> tres importes -> 20.0
# -> un nulo       -> TypeError: unsupported operand type(s) for +: 'float' and 'NoneType'
# -> sin ventas    -> ZeroDivisionError: division by zero
```

```text
Así se pide una explicación (sales sabiendo más):

  "Explícame esta línea como si tuviera 12 años, dime qué pasaría si la lista
   estuviera vacía y no me des la solución del ejercicio: hazme preguntas."

Así se pide la solución (sales con código que no sabes defender):

  "Dame el código que rellena los nulos con la media."

Y la comprobación no es "¿estás seguro?": eso es preguntar dos veces al mismo.
Se comprueba ejecutando el ejemplo o leyendo la documentación de tu versión.
```

:::claves
- `serie.std()` en pandas divide entre n − 1 (`ddof=1`) y `np.std` entre n (`ddof=0`). No es un
  descuido de ninguno de los dos: son dos definiciones distintas de la misma palabra.
- `np.std(serie)` sobre una Serie de pandas devuelve un `np.float64`, no un `float` de Python. Con
  un formato como `{x:.5f}` no se nota, pero el tipo aparece en cuanto comparas o serializas.
- `sum([10.0, None, 30.0])` no ignora el hueco ni devuelve `None`: suma hasta que choca y lanza
  `TypeError`. La lista vacía no da 0, da `ZeroDivisionError` porque divides entre `len(...) = 0`.
- El bloque de los tres casos no comprueba tu código: comprueba tus supuestos. Cambiar `casos` por
  los que se te ocurran es la forma más rápida de encontrar la línea que no sabes defender.
- Un `print` de comprobación vale más que releer la respuesta tres veces: si el número que sale no
  es el que la explicación prometía, acabas de encontrar el error en un segundo.
- Un modelo describe lo que suele pasar; quien dice lo que pasa de verdad en tu máquina es el
  intérprete. Cuando las dos versiones se contradicen, gana siempre el intérprete.
:::

## Errores típicos

- **Pedir la solución antes de intentarlo.** El rato de atasco es donde se aprende. Si la respuesta
  llega en el primer minuto, no has practicado el problema: has practicado leer.
- **Pegar código que funciona y no entiendes.** No puedes depurar lo que no entiendes y no puedes
  cambiar lo que no puedes depurar. El día que cambian los datos, el fragmento deja de funcionar y
  no hay por dónde empezar.
- **Creer que una explicación fluida es una explicación correcta.** La seguridad con la que está
  escrita una respuesta no dice nada de si es verdad: los errores vienen redactados igual de bien
  que los aciertos.
- **Comprobar preguntando al propio modelo.** «¿Seguro?», «¿puedes verificarlo?» o «cítame la
  fuente» no verifican: añaden otra afirmación a la pila. Comprobar es ejecutar o ir a la
  documentación de tu versión.
- **Quedarte con la primera versión de la respuesta.** Muchas veces el modelo acierta en el
  concepto y falla en el detalle (el nombre del argumento, el valor por defecto). Si no ejecutas,
  no distingues cuál de las dos partes te está fallando.
- **Confundir «me lo ha dicho» con «lo he comprobado» al entregar.** En un informe o en una
  entrevista, cada número tiene que tener detrás una comprobación tuya. Si te preguntan de dónde
  sale y contestas «lo saqué de una respuesta», el trabajo entero queda en duda.

## Comprueba que lo sabes

:::quiz
p: El modelo te contesta que uses `serie.std()`. ¿Qué convierte esa respuesta en algo tuyo?
o: Preguntarle otra vez si está seguro del resultado
o: Ejecutarla con tus datos y poder explicar por qué divide entre n − 1
o: Copiarla en el proyecto con un comentario que diga de dónde viene
o: Leerla dos veces despacio antes de usarla
a: 2
e: Reproducirla y saber explicarla son las dos pruebas que la hacen tuya. Volver a preguntar al mismo modelo no verifica nada, el comentario solo documenta el origen y leerla despacio aumenta la familiaridad, no el conocimiento.
:::

:::quiz
p: Con los mismos ocho valores, pandas da 2,13809 y NumPy 2,0. ¿Qué está pasando?
o: NumPy redondea el resultado a dos cifras decimales
o: pandas divide entre n − 1 y NumPy entre n: son dos definiciones distintas de desviación típica
o: Cada librería recibe una copia distinta de los datos
a: 2
e: No hay ningún error ni ningún redondeo oculto: `ddof` decide el denominador. Si quieres el mismo número en las dos, escribe `np.std(serie, ddof=1)`. La diferencia relativa es del 6,9 %, más que suficiente para que un informe cambie de conclusión.
:::

:::practica
enunciado: El modelo te da este fragmento para quedarte con los diez clientes que más gastan, donde cada cliente es un diccionario con la clave 'gasto' que viene como texto desde la base de datos: `top = sorted(clientes, key=lambda c: c["gasto"], reverse=True)[:10]`. Escribe las comprobaciones que harías antes de pegarlo.
pista: Piensa en el tipo del dato (¿número o texto?), en lo que falta en algunos registros y en los valores repetidos.
solucion: Cuatro comprobaciones. Primera: si 'gasto' es texto, la comparación es alfabética y '100' queda por debajo de '20', así que el top-10 sale mal y sin ningún error a la vista; hay que convertirlo a float. Segunda: si algún diccionario no tiene la clave 'gasto', el `sorted` revienta con `KeyError`; decide si esos clientes van al final o se descartan. Tercera: `sorted` es estable, así que con gastos repetidos el orden depende del orden de entrada y el mismo top-10 cambia de un día para otro; si el corte cae en un empate, hay que fijar un segundo criterio (por ejemplo el identificador). Cuarta: comprobar con un caso de tres clientes cuyos importes escritos como texto den un orden distinto al numérico, y dejarlo escrito como prueba.
:::

:::trampa
El «¿estás seguro?» es la comprobación más inútil que existe: el mismo sistema que se inventó un
argumento se inventará también la seguridad con la que lo defiende. La única comprobación de verdad
es ejecutar el ejemplo, medir con tus datos o leer la documentación de la versión que tienes
instalada.
:::
