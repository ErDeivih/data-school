---
id: errores-y-depuracion
titulo: Errores y depuración
fase: 3
nivel: básico
rutas: [core, de, ds]
prerequisitos: [entorno-python, funciones-y-modulos]
tags: [python, errores, depuracion, excepciones]
resumen: Un traceback se lee de abajo arriba: da el tipo de error y la línea exacta. try/except decide qué haces con él y el depurador te deja mirar las variables.
fuentes: ["Python Software Foundation, 'The Python Tutorial', sección 8: Errors and Exceptions"]
---

## En una frase

Un error no es un desastre, es información: el **traceback** te dice en qué línea, en qué función y
de qué tipo es el fallo, y `try`/`except` te deja decidir si lo arreglas, lo anotas o lo dejas subir.

## La idea

Cuando un programa revienta, Python imprime un bloque de texto que casi todo el mundo cierra sin
leer. Ese bloque es el **traceback** y está pensado para contestar tres preguntas en este orden: qué
tipo de error, dónde ocurrió la última línea y por qué camino llegaste hasta ahí.

Léelo **de abajo arriba**, que es como se construyó. La última línea trae el tipo de excepción y su
mensaje: `ZeroDivisionError: division by zero`. La línea de justo encima es el fichero, el número de
línea y la instrucción exacta que falló, y suele bastar para arreglarlo. Y todo lo que hay más
arriba es la **pila de llamadas**: la primera línea es la que arrancó el programa y cada bloque
siguiente es una función que llamó a la de debajo. Un traceback con quince bloques no significa
quince errores: significa que el fallo está quince llamadas por debajo del sitio donde empezaste.

Cuando el error no se puede arreglar en el sitio donde ocurre, Python lo **propaga**: sale de la
función y busca un `try` que lo recoja en la función que llamó, y si no lo encuentra, en la
siguiente. Si no hay ninguno en toda la pila, el programa termina y te enseña el traceback. Esa
propagación hacia arriba es una función, no un accidente: permite que el que sabe qué hacer con el
error sea quien llama, y que la función de dentro no tenga que saber nada de la política.

`try`/`except` es la herramienta para interceptarlo. Se lee así: intenta esto, y si sale esta
excepción concreta, haz esto otro. Tiene una cuarta parte que casi nadie usa y que merece la pena:
`else` se ejecuta si **no** hubo error, y `finally` se ejecuta siempre, haya error o no. `finally`
es el sitio de cerrar un fichero o una conexión.

La regla que separa el código robusto del frágil: **captura la excepción más concreta que sepas
manejar**. `except Exception` captura cualquier error de ejecución, incluidos los que son errores
de programación —un nombre mal escrito, un `None` donde esperabas un número—, y `except:` a secas
llega más lejos todavía: se traga también `KeyboardInterrupt`, así que Ctrl+C deja de funcionar.
Si capturas todo, un dato corrupto sigue circulando por el pipeline sin que nadie se entere; la
figura de abajo lo mide.

`raise` es lo contrario: sirve para **lanzar** un error cuando detectas algo que no debería pasar.
Su forma útil es `raise ValueError("...") from error`, que conserva la causa original y produce un
traceback con dos bloques («the above exception was the direct cause of…»). Y `assert` es un
hermano menor: comprueba una condición y lanza `AssertionError` si es falsa. Sirve para documentar
lo que tú das por supuesto mientras programas, no para validar datos de entrada (Python puede
desactivar los `assert` con la opción `-O`, y entonces desaparecen sin avisar).

Si el error es difícil de reproducir, `logging.exception` escribe el mensaje **y** el traceback con
una sola línea, y es lo que deberías usar en lugar de `print(error)` cuando esto pasa en producción.
Para mirar las variables en el momento exacto del fallo, el depurador de Python (`python -m pdb
script.py`, o `breakpoint()` dentro del código desde la versión 3.7) te deja inspeccionar, avanzar
línea a línea y repetir la ejecución sin sembrar el código de `print`; en [[notebooks-vs-scripts]] hay más sobre qué conviene depurar en una celda y qué en un script. Muchos editores integran un
depurador gráfico con los mismos comandos: `n` para la línea siguiente, `s` para entrar en la
función, `c` para continuar, `p variable` para ver su valor.

## Definición formal

La forma general del manejo de errores, y la propagación:

:::formula
try: … except Tipo as error: … else: … finally: …
:::

:::formula
fallo dentro de la función  →  sube por la pila  →  lo recoge el primer try que lo nombra
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube / cambia… |
| --- | --- | --- | --- |
| `try` | El bloque vigilado: solo el código que puede fallar de forma esperada | — | Cuanto más grande es el `try`, más errores ajenos acabas capturando sin querer |
| `except Tipo` | Qué excepción recoges y cómo la nombras. Debe ser lo más concreta posible | — | Un tipo más genérico captura más cosas, incluidas las que no sabes arreglar |
| `error` | El objeto de la excepción: `error.args` y `str(error)` dan el mensaje | texto | Un mensaje propio y con el dato que falló ahorra media hora de búsqueda |
| `else` | Se ejecuta solo si el `try` terminó **sin** error | — | Úsalo para el camino feliz: deja el `try` con la única línea que puede fallar |
| `finally` | Se ejecuta siempre: con error, sin él y también al salir con `return` | — | Es donde se liberan recursos; si lanza, tapa la excepción original |
| `raise` | Lanza una excepción nueva desde donde estás | — | `raise ... from error` conserva la causa; `raise` a secas relanza la actual |
| `assert condición` | Comprueba un supuesto del programador y lanza `AssertionError` | — | `python -O` desactiva todos los `assert`: no valides datos con ellos |
| `traceback.format_exc()` | El texto del traceback actual, como cadena | texto | Sirve para guardarlo en un log en vez de perderlo en la consola |
| `__cause__` | La excepción que originó la actual, cuando usas `raise ... from` | — | Si vale `None`, perdiste el rastro del error original |
:::

## Ejemplo

Esto es un traceback de verdad, con una función que divide entre un número que llegó a cero:

```text
Traceback (most recent call last):
  File "informe.py", line 6, in <module>
    print(precio_medio(importes, noches))
  File "informe.py", line 3, in precio_medio
    return sum(importes) / noches
ZeroDivisionError: division by zero
```

Se lee así: abajo del todo, el tipo (`ZeroDivisionError`) y el mensaje. La línea marcada con `File
"informe.py", line 3` es la que reventó: `return sum(importes) / noches`, y el motivo es que
`noches` valía 0. Y arriba está el camino: el programa llamó a `precio_medio` desde la línea 6. Aquí
el traceback tiene dos bloques (el módulo y `precio_medio`); si `precio_medio` llamase a otra
función que llamase a otra, verías un bloque por nivel.

Y un caso con números, midiendo lo que cuesta capturar de más. Sobre 20.000 filas de un informe,
2.400 traen texto donde debería haber un número:

```
except: sin tipo        -> 2400 rechazadas, 1 fallo de programacion OCULTO
except ValueError:      -> 2400 marcadas, el fallo de programacion sube y se ve
```

Las 2.400 son el mismo número en los dos casos: lo que cambia es la fila que no es un dato malo
sino un error tuyo. Con `except:` el programa sigue como si nada y esa fila viaja hasta el informe
final; con `except ValueError:` el `TypeError` sale a la luz y lo arreglas en cinco minutos en lugar
de en tres semanas, cuando alguien pregunte por qué faltan filas.

:::figura
fichero: errores-y-depuracion-except-sin-tipo
pie: Compara las dos barras. La verde (dato malo rechazado) mide lo mismo en las dos: eso no es lo que cambia. Lo que cambia es el hueco rojo, el fallo de programación que el `except:` sin tipo se traga y el `except ValueError:` deja subir. Toda la franja naranja son filas que pasan sin revisar: es el precio de no validar en la entrada.
fuente: figuras/errores-y-depuracion-1.py
:::

## Código

```python verificable
import traceback

def precio_medio(importes, noches):
    return sum(importes) / noches

try:
    precio_medio([100, 150], 0)
except ZeroDivisionError as error:
    lineas = traceback.format_exc().splitlines()
    print("tipo:", type(error).__name__)                    # -> tipo: ZeroDivisionError
    print("mensaje:", error)                                # -> mensaje: division by zero
    print("ultima linea:", lineas[-1].strip())              # -> ultima linea: ZeroDivisionError: division by zero
```

:::claves
- El traceback se construye mientras el error **sube**, no cuando ocurre: por eso la última línea
  del texto es la más profunda y la primera es el punto de arranque del programa.
- `except ZeroDivisionError as error` liga el objeto de la excepción al nombre `error` solo dentro
  del bloque. Se usa `as` y no una coma porque la coma se eliminó en Python 3.
- `str(error)` da el mensaje («división by zero»), pero el tipo no está en el mensaje: hay que
  sacarlo con `type(error).__name__`. Confundir ambos es lo que hace que los logs digan «algo
  falló» sin decir qué.
- `traceback.format_exc()` devuelve el traceback **como cadena** y solo funciona dentro de un
  `except`; para el texto de cualquier excepción, `traceback.format_exception(error)`.
- `sum(importes) / noches` con `importes` vacío no da error de división: da `0 / noches`. El error
  que buscas y el que salta no siempre coinciden.
:::

```python verificable
# Profundidad de la pila: cuantas funciones hay que atravesar hasta el fallo
def tercer_nivel(n):
    return 10 / n

def segundo_nivel(n):
    return tercer_nivel(n)

def primer_nivel(n):
    return segundo_nivel(n)

try:
    primer_nivel(0)
except ZeroDivisionError as error:
    import traceback
    profundidad = len(traceback.extract_tb(error.__traceback__))
    print("funciones en la pila:", profundidad)     # -> funciones en la pila: 4
    print("ultima funcion:", traceback.extract_tb(error.__traceback__)[-1].name)  # -> tercer_nivel
```

```python verificable
def leer_importe(texto):
    try:
        return float(texto)
    except ValueError as error:
        # raise ... from conserva la causa: el traceback muestra las dos
        raise ValueError("importe no numerico: " + texto) from error

try:
    leer_importe("doce")
except ValueError as error:
    print("mensaje:", error)                                  # -> mensaje: importe no numerico: doce
    print("causa:", type(error.__cause__).__name__)           # -> causa: ValueError

# assert documenta un supuesto del programador: si es falso, avisa en vez de seguir
def ratio(a, b):
    assert b != 0, "el denominador no puede ser cero"
    return a / b

print("ratio:", ratio(6, 3))                                  # -> ratio: 2.0
try:
    ratio(6, 0)
except AssertionError as error:
    print("assert:", error)                                   # -> assert: el denominador no puede ser cero
```

```text
# En produccion, en vez de print(error): el log se lleva el mensaje Y el traceback
import logging
logging.basicConfig(level=logging.INFO)

try:
    leer_factura(ruta)
except (FileNotFoundError, ValueError) as error:
    logging.exception("no se pudo leer %s", ruta)   # -> ERROR:root:no se pudo leer datos.csv
                                                    #    Traceback (most recent call last): ...
```

## Errores típicos

- **`except:` a secas.** Captura todo, incluidos `KeyboardInterrupt` (Ctrl+C deja de funcionar) y
  los errores de programación, que quedan invisibles. Escribe `except ValueError:` y solo lo que
  sepas manejar.
- **`except Exception` con un `pass` dentro.** Es la forma más rápida de perder un dato: el fallo
  se descarta en silencio y el informe sale con menos filas sin que nadie lo sepa. Si de verdad hay
  que descartar, cuenta las descartadas y registra el motivo.
- **Leer el traceback de arriba abajo.** La primera línea es `Traceback (most recent call last)`,
  o sea «el último es el más reciente». La información útil está abajo: tipo, mensaje y la línea
  concreta que falló.
- **Usar `assert` para validar datos de usuario.** Con `python -O` todos los `assert` desaparecen y
  la validación con ellos. Para datos que vienen de fuera, `if` y `raise ValueError(...)`.
- **Capturar el error y lanzar otro sin `from`.** `raise ValueError("falló")` dentro de un `except`
  cambia la causa por «During handling of the above exception…» y complica la lectura. `raise
  ValueError("...") from error` mantiene la cadena limpia.
- **Dejar el `try` demasiado grande.** Si dentro metes la lectura del fichero, el cálculo y el
  guardado, un `except ValueError` acabará capturando un error de la parte que no tocaba. Deja en
  el `try` solo la línea que puede fallar y pon el resto en el `else`.
- **Tapar con `print` lo que debería ser un log.** `print(error)` en un script que corre de noche
  se pierde. `logging.exception` guarda mensaje, traceback y hora en el fichero de log.

:::practica
enunciado: Escribe una función `media_limpia(valores)` que reciba una lista de textos, convierta cada uno a número y devuelva la media de los válidos, contando cuántos ha descartado. Debe distinguir un texto no numérico (dato malo, se descarta) de una lista vacía (error del que llama, debe subir). Llámala con `["10", "12", "ocho", "8"]` y con `[]`.
pista: Un `try` alrededor de `float(texto)` con `except ValueError`, y una comprobación al principio que lance `ValueError` con mensaje propio si la lista no tiene elementos válidos.
solucion: Se recorre la lista, se intenta `float(texto)` dentro de un `try` y se cuentan los `ValueError` en un contador. Con `["10", "12", "ocho", "8"]` la media de los válidos es (10+12+8)/3 = 10.0 y el descartado es 1. El caso `[]` sale con media `None` y descartados 0, así que la comprobación de lista vacía debe lanzar `raise ValueError("no hay valores que promediar")`: distinguir «no hay datos» de «los datos venían mal» evita que un cero silencioso se cuele en el informe.
:::

## Comprueba que lo sabes

:::quiz
p: Tienes un traceback con seis bloques y el programa se ha parado. ¿Dónde está el fallo?
o: En la primera línea del traceback, que es la que arrancó el programa
o: En la línea marcada justo encima del tipo de error, que está al final del traceback
o: En el bloque del medio, que es donde se pierde la pila de llamadas
a: 2
e: El traceback se escribe de arriba abajo según sube el error, así que el último bloque es el más profundo y el más cercano al fallo. La línea de encima del tipo de excepción trae el fichero y la instrucción exacta; lo de arriba es el camino de llamadas, no más errores.
:::

:::quiz
p: Un script con `except: pass` lleva meses funcionando y ahora el informe tiene menos filas de las esperadas. ¿Qué ha pasado?
o: El `except:` ha ido descartando también errores de programación y datos malos sin dejar rastro
o: Python ha optimizado el bucle y se ha saltado filas
o: El fichero de entrada estaba corrupto y el programa lo ha avisado por pantalla
a: 1
e: Un `except:` sin tipo captura cualquier excepción, incluidas las que indican un fallo tuyo, y `pass` la descarta sin registrarla. No hay aviso por pantalla ni optimización: simplemente faltan filas. La solución es capturar el tipo concreto y contar o registrar lo descartado.
:::

:::quiz
p: ¿Por qué no se debe validar la entrada del usuario con `assert`?
o: Porque `assert` solo funciona con números
o: Porque con `python -O` los `assert` se eliminan y la validación desaparece sin avisar
o: Porque `assert` no permite escribir un mensaje
a: 2
e: `assert` documenta supuestos del programador y Python lo puede desactivar con la opción `-O`. Para datos que vienen de fuera hay que usar un `if` y lanzar `ValueError` con el dato problemático en el mensaje. Sí admite mensaje, y no está limitado a números.
:::
