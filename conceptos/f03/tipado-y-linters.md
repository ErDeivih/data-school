---
id: tipado-y-linters
titulo: Tipado y linters
fase: 3
nivel: intermedio
rutas: [de, alg, ds]
prerequisitos: [entorno-python, tipos-y-estructuras-python, testing-con-pytest]
tags: [tipos, mypy, ruff, pydantic, calidad]
resumen: Anotaciones de tipo, dataclasses y Pydantic: cómo detectar antes de ejecutar los errores que en un pipeline de datos cuestan una tarde de depuración.
fuentes: ["PEP 484, 'Type Hints'", "Pydantic documentation, 'Why use Pydantic'"]
---

## En una frase

Las anotaciones de tipo y los linters convierten en **error inmediato** lo que en Python sería
un fallo silencioso a las tres de la madrugada: pasar una columna de textos donde la función
esperaba números, o llamar a una función con los argumentos en el otro orden.

## La idea

En un pipeline de datos cada función recibe datos que no has escrito tú. Vienen de un CSV, de
una API o de la tabla que dejó otro equipo. Si esa función espera un número y recibe la cadena
`"12,50"`, Python no se queja: intenta la operación, falla donde menos lo esperas, y el
mensaje de error apunta a una línea que no tiene nada que ver con la causa.

Piensa en la revisión de un manuscrito. Un **linter** es el corrector ortográfico: no sabe si
la historia es buena, pero detecta repeticiones, comas mal puestas y palabras que no existen.
Un **comprobador de tipos** (`mypy`) es un lector que compara lo que prometes con lo que haces:
si declaras que esa función devuelve un número, y hay un camino en el que devuelve `None`, te lo
dice. Y **la validación en la frontera** (`Pydantic`) es el portero de la puerta: comprueba el
documento cuando entra, no cuando ya está dentro del archivo.

Lo importante es entender que son tres capas distintas y que ninguna sustituye a las otras:

1. **Anotaciones + mypy:** análisis estático. Encuentras el error **antes de ejecutar nada**.
   Coste cero en tiempo de ejecución, porque Python se salta las anotaciones por completo.
2. **Linters (ruff):** estilo, imports muertos, variables sin usar, comparaciones sospechosas,
   partes del código que huelen mal. Detectan cosas que los tipos no ven.
3. **Pydantic en la frontera:** validación y conversión en **tiempo de ejecución**, con el dato
   externo. Es la única capa que ve lo que de verdad llega.

El error clásico del principiante es pensar que basta con una. Escribir `precio: float` no
convierte nada: si llega la cadena `"12,50"`, sigue siendo una cadena y la anotación no la toca.

## Definición formal

Los conceptos, precisos:

- **Anotación de tipo:** la sintaxis `nombre: tipo` en los parámetros y `-> tipo` en el
  retorno. Python las guarda en `función.__annotations__` y **no las comprueba nunca** al
  ejecutar. Son documentación ejecutable solo para las herramientas.

:::formula
nombre: Tipo_entrada → Tipo_salida
:::

  La flecha se lee «va de … a …»: una función que recibe un texto y devuelve un número se
  anota `str → float`. Es una promesa sobre la forma del dato, no un mecanismo de conversión.
- **Tipado gradual:** el código anotado y el no anotado conviven. `mypy` deduce los tipos que
  puede y trata como `Any` lo que no sabe. `--strict` prohíbe el `Any` implícito y obliga a
  anotar todo lo que se comprueba.
- **`Any`:** el tipo que desactiva el análisis. Un valor `Any` se puede pasar a cualquier sitio
  sin protestar. Es la salida de emergencia, y abusar de ella convierte el tipado en decoración.
- **`Optional[T]` (o `T / None`):** el valor puede ser `T` o `None`. Obliga a quien lo usa a
  tratar el caso nulo, y por eso detecta los `AttributeError: 'NoneType'` antes de que ocurran.
- **`dataclass`:** decorador que genera `__init__`, `__repr__` y `__eq__` a partir de los campos
  anotados. Declara la forma de un objeto; **no valida** los valores.
- **`TypedDict`:** describe un diccionario con claves y tipos fijos. mypy lo comprueba; en
  ejecución sigue siendo un `dict` normal y una clave que falta es un `KeyError`.
- **Pydantic `BaseModel`:** valida y **convierte** en el momento de construir el objeto. La
  cadena `"12.50"` se convierte en el número `12.5`; la cadena `"doce"` lanza un
  `ValidationError` que nombra el campo.
- **Regla del linter:** un identificador de regla como `E501` (línea demasiado larga) o `F401`
  (import sin usar). Se activan y desactivan en la configuración, y permiten silenciar una línea
  concreta con un comentario en lugar de desactivar la regla entera.

Una frase que resume la diferencia entre las capas: **mypy comprueba lo que tu código dice de
sí mismo; Pydantic comprueba lo que el mundo le entrega a tu código.**

## Ejemplo

Llega esta fila de una API de clientes:

```text
{"id": 7, "nombre": "Ana", "saldo": "12.50", "activo": "true"}
```

Las tres capas, una por una:

- **Anotación sola:** `saldo: float` no toca el valor. `cliente["saldo"] + 10` revienta con un
  `TypeError` que menciona la suma, no el campo.
- **`dataclass`:** tampoco valida. `Cliente(id=7, nombre="Ana", saldo="12.50")` se construye sin
  rechistar y el error aparece más tarde.
- **Pydantic:** al construir el modelo, `saldo` vale el número `12.5` y `activo` vale el booleano
  `True`. Si llegara `"doce"`, el error aparecería en la puerta con el nombre del campo.

Otro caso donde el tipado se gana el sueldo. Esta función tiene un error que se comete cada
semana:

```text
def porcentaje(parte: float, total: float) -> float:
    return parte / total * 100

porcentaje(250, 50)     # 500.0: el 250 % de una base de 50
```

Los argumentos están invertidos y el resultado es un número perfectamente plausible. Con las
anotaciones no se detecta (los dos son `float`), y por eso en datos se usan nombres
**específicos** y, cuando la magnitud importa, tipos propios o validación de rangos: el
comprobador no adivina la semántica, solo la forma.

## Código

```python verificable
# 1) Anotar no valida: las anotaciones no se comprueban al ejecutar.
def dobla(precio: float) -> float:
    return precio * 2

print("con un numero  :", dobla(2.5))
print("con una cadena :", dobla("25"))     # "25" + "25": ni 50 ni error, otra cosa

# Comprobacion real, en la frontera: aqui es donde debe fallar.
def dobla_validando(precio):
    if not isinstance(precio, (int, float)) or isinstance(precio, bool):
        raise TypeError(f"precio debe ser numerico, llego {type(precio).__name__}")
    return precio * 2

try:
    dobla_validando("25")
except TypeError as exc:
    print("falla en la puerta:", exc)
```

```python verificable
from dataclasses import dataclass, field

# La dataclass declara la forma del dato y genera __init__ y __repr__.
# Lo que NO hace: validar tipos al construir.
@dataclass
class Pedido:
    id: int
    importe: float
    descuento: float = 0.0
    etiquetas: list[str] = field(default_factory=list)

    def total(self) -> float:
        return self.importe * (1 - self.descuento)

p = Pedido(id=7, importe=100.0, descuento=0.15)
print(p)
print("total:", p.total())

# Sin descuento, el valor por defecto es 0.0
print("total sin descuento:", Pedido(id=8, importe=50.0).total())

# Y aqui esta el peligro: la dataclass NO valida. Un importe en texto entra sin protestar.
raro = Pedido(id=9, importe="100.0")
print("acepta texto sin quejarse:", raro.importe)

# La conversion, cuando hace falta, es explicita:
print("convertido a numero:", float(raro.importe) + 1)
```

```text
$ mypy --strict pipeline/
pipeline/limpieza.py:42: error: Incompatible return value type (got "float | None",
    expected "float")  [return-value]
pipeline/limpieza.py:57: error: Item "None" of "DataFrame | None" has no attribute "dropna"
    [union-attr]
pipeline/limpieza.py:61: note: By default the bodies of untyped functions are not checked,
    consider using --check-untyped-defs  [annotation-unchecked]
Found 2 errors in 1 file (checked 14 source files)
```

```text
$ ruff check pipeline/
pipeline/limpieza.py:3:1: F401 [*] `os` imported but unused
pipeline/limpieza.py:18:5: F841 Local variable `tmp` is assigned to but never used
pipeline/limpieza.py:29:9: E711 Comparison to `None` should be `cond is None`
pipeline/limpieza.py:33:1: E501 Line too long (104 > 88)
Found 4 errors.
[*] 3 fixable with the `--fix` option.
```

```python verificable
# La frontera del pipeline: validar y convertir en la puerta, no al final.
from pydantic import BaseModel, Field, ValidationError

class Cliente(BaseModel):
    id: int = Field(ge=1)
    nombre: str
    saldo: float = Field(ge=0)
    activo: bool = True

crudo = {"id": 7, "nombre": "Ana", "saldo": "12.50", "activo": "true"}
c = Cliente(**crudo)
print("saldo convertido:", c.saldo, "activo:", c.activo)

malo = {"id": 7, "nombre": "Ana", "saldo": "doce"}
try:
    Cliente(**malo)
except ValidationError as exc:
    print("la puerta rechaza el lote:", exc.error_count(), "error")
    print(exc.errors()[0]["loc"], exc.errors()[0]["type"])
```

```text
saldo convertido: 12.5 activo: True
la puerta rechaza el lote: 1 error
('saldo',) float_parsing
```

## Errores típicos

- **Creer que la anotación valida.** `precio: float` no convierte ni comprueba nada: Python
  ignora las anotaciones al ejecutar. Si el dato viene de fuera, necesita validación explícita
  (Pydantic o un `isinstance` con mensaje claro) o la anotación es solo un deseo.
- **Usar `Any` para callar a mypy.** `def f(x: Any) -> Any` desactiva el análisis de todo lo que
  toca ese valor, y encima deja el código con aspecto de estar tipado. Si no sabes el tipo, usa
  un `Protocol`, un `TypedDict` o una unión; `Any` es la última opción.
- **Marcar como `Optional` lo que nunca es `None`.** Obliga a cada persona que use la función a
  comprobar un caso imposible, y esconde el caso en el que el valor sí puede faltar. Al revés es
  peor: declarar `float` algo que puede llegar `None` produce el `AttributeError` en producción.
- **Activar todas las reglas del linter de golpe.** En un proyecto que ya existe salen miles de
  avisos, nadie los lee y se acaba desactivando el linter. Empieza por las reglas de errores
  reales (imports sin usar, variables muertas, comparaciones con `is`) y ve añadiendo.
- **Validar en todas las funciones.** Si el dato ya se validó en la frontera, volver a validarlo
  en cada paso es lento y hace el código imposible de cambiar: dos sitios que comprueban lo
  mismo acaban discrepando. Valida una vez, en la puerta, y pasa el objeto ya validado.
- **Silenciar el aviso en vez de arreglarlo.** Un `# type: ignore` o un `# noqa` sin explicación
  tapa el problema y lo deja para el siguiente. Si de verdad hace falta, acompaña el comentario
  con el motivo: `# type: ignore[arg-type]  # la libreria devuelve Any` .

:::aviso
`mypy` y `ruff` comprueban cosas distintas y se solapan poco: `ruff` mira el estilo y los errores
evidentes sin saber de tipos; `mypy` sigue los tipos a través de las llamadas y detecta el
`None` que se cuela. Un proyecto con los dos configurados y ejecutándose en cada commit
([[git-para-datos|ganchos de git]]) evita la mayor parte de los errores tontos. No sustituyen a
[[testing-con-pytest|los tests]]: comprueban la forma del código, no que el resultado sea el
correcto.
:::

:::practica
enunciado: Un modelo Pydantic `Pedido` declara `id: int = Field(ge=1)`, `importe: float = Field(ge=0)` y `unidades: int = 1`. Llegan tres registros: `{"id": 3, "importe": "25.50"}`, `{"id": 0, "importe": 10}` y `{"id": 5, "importe": -2}`. ¿Cuántos se construyen, con qué valores, y qué error da cada rechazo?
pista: Pydantic convierte lo que puede convertir y solo rechaza lo que incumple una restricción; mira campo por campo, no el registro entero.
solucion: Solo se construye el primero: `Pedido(id=3, importe="25.50")` da `importe = 25.5`, porque la cadena se convierte, y `unidades = 1`, que es el valor por defecto. El segundo lanza `ValidationError` con un error en `loc` `('id',)` y tipo `greater_than_equal`, porque 0 no cumple `ge=1`. El tercero falla igual, en `('importe',)`, porque -2 no cumple `ge=0`. Conclusión: dos de los tres registros se rechazan en la puerta y solo el válido entra al pipeline.
:::

## Comprueba que lo sabes

:::quiz
p: Anotas `def total(precios: list[float]) -> float` y llamas con `["1.20", "3.40"]`. ¿Qué ocurre?
o: Python convierte las cadenas a números al entrar en la función
o: La función se ejecuta igual: las anotaciones no se comprueban en ejecución y el error aparecerá al operar con las cadenas
o: Se lanza `TypeError` en la línea de la anotación
a: 2
e: En Python las anotaciones son metadatos que se guardan en `__annotations__` y nadie las comprueba al llamar. El fallo real llega dentro del cuerpo, al intentar sumar cadenas con números, y el mensaje no menciona el tipo declarado. Un comprobador estático lo habría avisado antes de ejecutar y Pydantic lo habría rechazado en la frontera.
:::

:::quiz
p: ¿Cuál es la diferencia práctica entre una `dataclass` y un modelo de Pydantic?
o: La dataclass es más rápida y Pydantic solo sirve para JSON
o: La dataclass genera los métodos del objeto pero no valida los valores; Pydantic valida y convierte al construir el objeto
o: Son lo mismo, Pydantic es solo una dataclass con un decorador distinto
a: 2
e: La dataclass es azúcar sintáctico: crea `__init__`, `__repr__` y `__eq__` a partir de los campos anotados, y si le pasas una cadena donde esperabas un número la acepta. Pydantic comprueba y convierte al construir el modelo, y falla con el nombre del campo y el valor recibido. La elección depende de si el dato lo construyes tú (dataclass) o viene de fuera (Pydantic).
:::
