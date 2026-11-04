---
id: funciones-y-modulos
titulo: Funciones, módulos y paquetes
fase: 3
nivel: básico
rutas: [core, de, ds]
prerequisitos: [entorno-python, tipos-y-estructuras-python]
tags: [python, funciones, modulos, organizacion]
resumen: Una función le pone nombre y argumentos a un cálculo; un módulo lo guarda en un fichero y un paquete agrupa módulos para reutilizarlos sin copiar.
fuentes: ["Ramalho (2022), 'Fluent Python', 2.ª edición", "Python Software Foundation, 'The Python Tutorial', secciones 4 y 6"]
---

## En una frase

Una función es un cálculo con nombre, sus argumentos son los datos que recibe y su valor de
retorno es lo que devuelve; un módulo es un fichero `.py` que agrupa funciones y un paquete es una
carpeta de módulos, de modo que puedes reutilizar el trabajo en lugar de copiarlo.

## La idea

Imagina un recetario. La receta de la bechamel no se reescribe en cada plato: se escribe una vez,
tiene un nombre, pide unos ingredientes y unas cantidades y produce una salsa. Cuando la necesitas,
dices «haz bechamel con un litro de leche». Eso es una **función**: has empaquetado un
procedimiento, le has puesto nombre, le has declarado qué necesita y sabes qué devuelve.

Los **parámetros** son los huecos de la receta («un litro de leche») y los **argumentos** son los
valores que pasas al llamarla («0,75 litros»). El **valor de retorno** es lo que sale: la salsa.
La diferencia entre argumento y parámetro es solo de punto de vista, pero conviene no mezclarla:
el parámetro vive en la definición y el argumento vive en la llamada.

Los **argumentos por defecto** son los huecos con un valor ya puesto: `def interes(capital,
tasa=0.03)`. Si no pasas `tasa`, vale 0,03. Y aquí está la trampa que se lleva por delante a todo
el mundo: ese valor por defecto se calcula **una sola vez**, cuando Python lee la línea `def`, no en
cada llamada. Si el defecto es un número o una cadena da igual, porque no se pueden cambiar; si es
una lista o un diccionario, todas las llamadas comparten el mismo objeto y una llamada ensucia la
siguiente. La página de [[tipos-y-estructuras-python]] ya enseñó el síntoma; aquí ves el porqué.

El segundo escalón es el **módulo**. Cuando un fichero tiene veinte funciones, no quieres
copiarlas a otro script: quieres importarlas. `import` hace dos cosas, en este orden: ejecuta el
fichero entero de arriba abajo y guarda el resultado en `sys.modules` con su nombre. A partir de
ahí, cualquier `import` del mismo módulo reutiliza lo que ya está cargado y **no lo vuelve a
ejecutar**. Por eso un `print` en la primera línea de un módulo aparece una sola vez aunque lo
importes en cinco sitios.

De ahí sale la línea más rara del Python principiante, `if __name__ == "__main__":`. Cuando
ejecutas un fichero directamente, Python le pone el nombre `"__main__"`; cuando lo importas desde
otro, le pone su nombre de módulo. La condición pregunta «¿me están ejecutando o me están
importando?» y sirve para dejar las pruebas y el arranque fuera del camino cuando el fichero se usa
como biblioteca. Sin ella, importar tu módulo dispara su código.

El tercer escalón es el **paquete**: una carpeta con un `__init__.py`. `analisis/limpieza.py` e
`import analisis.limpieza` convierten una carpeta en una jerarquía de nombres. La consecuencia
práctica es que dos módulos pueden llamarse igual si están en paquetes distintos, y que un
proyecto grande se ordena por responsabilidad: `datos/`, `modelos/`, `informes/`.

Dos detalles que se aprenden a golpes. Primero: **`return` corta la función en seco**, así que
todo lo que escribas después no se ejecuta nunca; y una función sin `return` devuelve `None`, no
un error, lo cual produce el clásico `TypeError: unsupported operand type(s) for +: 'NoneType'`.
Segundo: **importar ejecuta el módulo, no lo copia**. Si dentro del módulo modificas una variable,
estás modificando el objeto que vive en `sys.modules` y todo el que lo importe verá el cambio.

## Definición formal

Las piezas de una función, con nombre para cada una:

:::formula
def nombre(parámetro, otro=valor_por_defecto) -> tipo:   …   return resultado
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `def` | La palabra que abre la definición; el cuerpo va indentado debajo | — | — |
| `nombre` | El nombre con el que llamas a la función | — | Un nombre peor hace el código más difícil de leer, no más lento |
| `parámetro` | El hueco obligatorio: si no le pasas argumento, `TypeError` | las del dato | Más parámetros obligatorios, más rígida es la llamada |
| `otro` | Parámetro con valor por defecto: se puede omitir | las del dato | Un defecto mutable (`[]`) se comparte entre llamadas y crece |
| `valor_por_defecto` | Lo que vale el parámetro si no lo pasas; se evalúa una vez, al definir | las del dato | Si es un objeto mutable, cada llamada ve lo que dejó la anterior |
| `*` | Separa los parámetros que solo se pueden pasar por nombre | — | Obliga a escribir `periodos=4`, que es más legible en llamadas largas |
| `->` | Anotación del tipo que devuelve; Python no la comprueba | — | Sirve a las herramientas de [[tipado-y-linters]], no al intérprete |
| `return` | Devuelve el resultado y sale; sin él la función devuelve `None` | las del resultado | Varios `return` permiten salidas tempranas, pero no deben solaparse |
| `__name__` | El nombre con el que se está ejecutando el módulo | texto | Vale `"__main__"` solo si ejecutas el fichero directamente |
| `sys.modules` | El diccionario de módulos ya importados | — | Si un módulo está dentro, `import` no lo vuelve a ejecutar |
:::

Y el contrato que hace que un módulo sea importable sin efectos secundarios:

:::formula
if __name__ == "__main__":   →   solo se ejecuta al lanzar el fichero
:::

:::figura
fichero: funciones-y-modulos-defecto-mutable
pie: La línea roja es la función con `caja=[]`: cada llamada devuelve un elemento más, porque todas comparten la lista que se creó al definir la función. La verde es la versión con `None`: siempre devuelve un elemento, porque la lista se crea dentro. Si tu función devuelve una lista que crece sola entre llamadas, este es el motivo.
fuente: figuras/funciones-y-modulos-1.py
:::

## Ejemplo

Una función de interés compuesto, con el número de periodos por defecto:

```
interes_compuesto(1000, 0.06)              -> 1061.68   (12 periodos)
interes_compuesto(1000, 0.06, periodos=4)  -> 1061.36   (4 periodos)
interes_compuesto(1000, 0.06, periodos=1)  -> 1060.00   (1 periodo)
```

El factor es `(1 + 0,06 / 12)^12 = 1,061678` con doce periodos y `(1 + 0,06 / 4)^4 = 1,061364` con
cuatro. Con un solo periodo, `1 + 0,06 = 1,06` exacto y el capital final son 1.060,00. Fíjate en que
más periodos **sube** el resultado sin tocar la tasa: es el efecto de capitalizar antes los
intereses.

Y el caso del defecto mutable, con las tres primeras llamadas:

```
acumula(1)  -> [1]
acumula(2)  -> [1, 2]
acumula(3)  -> [1, 2, 3]
```

La segunda llamada no empieza de cero: recibe la misma lista que dejó la primera. Con `caja=None`
y creando la lista dentro, las tres devuelven `[1]`.

## Código

```python verificable
def interes_compuesto(capital, tasa, *, periodos=12):
    """Devuelve (capital final, interes ganado). El asterisco obliga a nombrar periodos."""
    factor = (1 + tasa / periodos) ** periodos
    return capital * factor, capital * (factor - 1)

final, ganado = interes_compuesto(1000, 0.06)
print("doce periodos:", round(final, 2), round(ganado, 2))        # -> 1061.68 61.68
print("cuatro periodos:", round(interes_compuesto(1000, 0.06, periodos=4)[0], 2))  # -> 1061.36

# return corta en seco: lo que venga despues no se ejecuta
def clasifica(x):
    if x < 0:
        return "negativo"
    return "positivo o cero"

print("clasifica:", clasifica(-3), clasifica(0))                 # -> negativo positivo o cero
```

:::claves
- La función devuelve **una tupla**, no dos valores. `final, ganado = ...` la desempaqueta por
  posiciones, así que si cambias el orden del `return` cambias lo que recibe cada nombre sin que
  Python se queje.
- El `*` de la firma hace que `periodos` sea **keyword-only**: `interes_compuesto(1000, 0.06, 4)`
  lanza `TypeError`. Sirve para que una llamada con tres números seguidos no se lea de forma
  ambigua.
- El docstring va justo debajo de `def` y es lo que verás con `help(interes_compuesto)`. No es un
  comentario: es un atributo del objeto función (`interes_compuesto.__doc__`).
- `**` es la potencia aritmética, no la multiplicación repetida por un bucle: `(1 + 0.06) ** 12`
  se calcula con logaritmos y exponenciales en C, no doce veces a mano.
- `round(x, 2)` redondea **solo para imprimir**: no cambia `final` ni `ganado`, que siguen con
  todos sus decimales. Si redondeas y luego reutilizas el valor, arrastras el error.
:::

```python verificable
# El argumento por defecto se evalua UNA vez, cuando se define la funcion
def acumula(x, caja=[]):
    caja.append(x)
    return caja

print("defecto mutable:", acumula(1), acumula(2), acumula(3))   # -> [1, 2, 3] [1, 2, 3] [1, 2, 3]

# La forma correcta: None por defecto y el contenedor se crea en cada llamada
def acumula_bien(x, caja=None):
    if caja is None:
        caja = []
    caja.append(x)
    return caja

print("con None:", acumula_bien(1), acumula_bien(2), acumula_bien(3))   # -> [1] [2] [3]
```

```text
# proyecto/
#   pyproject.toml        dependencias y metadatos (lo escribe [[entorno-python]])
#   src/facturas/         el paquete: una carpeta con __init__.py
#       __init__.py       deja vacio o exporta lo publico
#       iva.py            def calcular(base): ...
#       totales.py        from facturas.iva import calcular
#   tests/test_iva.py     pruebas con [[testing-con-pytest]]
#   scripts/informe.py    script de arranque: from facturas.iva import calcular; calcular(100)
#
# quien ejecuta que:
#   python -m scripts.informe   ->  informe es "__main__", facturas se importa
#   python -m pytest            ->  los tests importan facturas, nada se ejecuta de mas
#   python src/facturas/iva.py  ->  iva es "__main__" y su bloque de pruebas se lanza
```

## Errores típicos

- **Poner una lista o un diccionario como valor por defecto.** `def f(x, caja=[])` comparte la
  misma caja entre todas las llamadas, como has visto arriba. Usa `None` y créala dentro.
- **Llamar a una función antes de que devuelva algo.** Si la función no tiene `return`, devuelve
  `None` y el error aparece en la línea siguiente, no dentro de la función: `TypeError: unsupported
  operand type(s) for +: 'NoneType' and 'int'`. Es el mismo despiste que contar con que una función
  «modifique» una variable de fuera.
- **Pensar que `return` y `print` son lo mismo.** `print` escribe en pantalla y devuelve `None`;
  `return` entrega el valor a quien llamó. Una función llena de `print` sin `return` no se puede
  reutilizar ni probar.
- **Creer que importar dos veces ejecuta dos veces.** No: el módulo se ejecuta la primera vez y
  queda en `sys.modules`. Si tu módulo imprime al importarlo, es que te falta el
  `if __name__ == "__main__":`.
- **Poner código suelto en un módulo pensado para importarse.** Un `print` o un cálculo pesado a
  nivel de módulo se dispara en cada `import`, incluso desde un test.
- **Modificar argumentos mutables que te pasan.** `def limpia(filas): filas.sort()` reordena la
  lista del que llamó. Si no quieres ese efecto, trabaja sobre `sorted(filas)` o `filas.copy()`:
  el quién-copia-a-quién está en [[vistas-y-copias]].
- **Olvidar que los nombres importados son globales del módulo.** Si `iva.py` define `tipos = 0.21`
  y otro módulo hace `from iva import tipos`, reasignar `iva.tipos` **no** cambia la copia local
  del que importó. Importa el módulo (`import iva`) y accede con `iva.tipos`.

:::practica
enunciado: Escribe una función `resumen(importes, *, iva=0.21)` que devuelva la base imponible (la suma), el total con IVA y el IVA en euros, con los tres redondeados a dos decimales. Llámala con `[100, 250, 50]` y con un IVA del 10 %, y explica por qué el total no es exactamente la base más el IVA redondeado.
pista: Suma primero, aplica el IVA después y redondea solo al final; devolver una tupla te permite sacar los tres números en una línea.
solucion: Con `base = sum(importes)`, la función devuelve `round(base, 2)`, `round(base * (1 + iva), 2)` y `round(base * iva, 2)`. Para `[100, 250, 50]` sale base 400.00, total 484.00 e IVA 84.00; con IVA del 10 %, base 400.00, total 440.00 e IVA 40.00. El total no es la suma de los otros dos redondeados porque cada uno se redondea por separado: 400 · 0,21 = 84,00 exacto aquí, pero con importes como 33,33 la diferencia de un céntimo aparece y hay que decidir qué cifra manda.
:::

## Comprueba que lo sabes

:::quiz
p: Llamas tres veces a `def apunta(x, registro=[]): registro.append(x); return registro` sin pasar `registro`. ¿Qué devuelve la tercera llamada?
o: `[3]`, porque el defecto se recrea en cada llamada
o: `[1, 2, 3]`, porque el defecto es el mismo objeto en las tres llamadas
o: Un `TypeError` porque el defecto no se puede modificar
a: 2
e: El valor por defecto se evalúa una sola vez, al definir la función, así que las tres llamadas comparten la misma lista. La solución es `registro=None` y crear la lista dentro de la función.
:::

:::quiz
p: ¿Para qué sirve `if __name__ == "__main__":` en un módulo?
o: Para que el módulo se importe más rápido
o: Para que su código de arranque y sus pruebas no se ejecuten cuando otro fichero lo importa
o: Para declarar que ese fichero es el único ejecutable del proyecto
a: 2
e: Python pone `__name__` a `"__main__"` solo cuando ejecutas el fichero directamente; al importarlo vale el nombre del módulo. Con el `if`, las pruebas y los ejemplos se quedan fuera del camino al importarlo. No afecta a la velocidad de importación ni prohíbe ejecutar otros ficheros.
:::

:::practica
enunciado: Tienes `import math`, luego `import math as m` y más tarde `from math import pi`. Di cuántas veces se ejecuta el módulo `math`, si `math.pi` y `m.pi` son el mismo objeto y qué pasa si otro fichero del proyecto asigna `math.pi = 3`.
pista: `import` ejecuta el módulo la primera vez y lo guarda en `sys.modules`; las demás formas solo crean nombres nuevos que apuntan a lo mismo.
solucion: Se ejecuta una sola vez, en el primer `import`. `math is m` es `True` y `math.pi` y `m.pi` son exactamente el mismo objeto; `from math import pi` crea además un nombre local `pi` ligado a ese objeto. Si alguien hace `math.pi = 3`, todos los que accedan por `math.pi` o `m.pi` verán 3, pero un módulo que ya hizo `from math import pi` conserva su copia del valor original: por eso se importa el módulo y no los valores sueltos.
:::
