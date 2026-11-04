---
id: json-y-datos-anidados
titulo: JSON y datos anidados
fase: 3
nivel: básico
rutas: [core, de, ds]
prerequisitos: [ficheros-y-encoding, tipos-y-estructuras-python]
tags: [json, datos-anidados, pandas]
resumen: JSON guarda objetos y listas unas dentro de otras; leerlo es fácil, pero convertirlo en tabla obliga a aplanar y a decidir cuántas filas salen.
fuentes: ["Python Software Foundation (2024), 'json — JSON encoder and decoder'", "McKinney (2022), 'Python for Data Analysis', 3.ª edición"]
---

## En una frase

JSON es texto que representa objetos (pares de clave y valor) y listas anidadas unas dentro de
otras; se lee con `json.loads` y, para analizarlo, hay que **aplanarlo** hasta una tabla en la que
cada elemento de una lista se convierte en una fila.

## La idea

Piensa en una dirección postal escrita con cajas dentro de cajas. En el sobre exterior pone el
destinatario; dentro hay un sobre con la factura; dentro de la factura, una lista de líneas, y cada
línea tiene su producto, su cantidad y su precio. Nada de eso es una tabla: es una estructura con
niveles, y cada nivel tiene su propia forma.

JSON es exactamente eso, y es el formato en el que hablan casi todas las APIs ([[apis-y-peticiones-http]])
y casi todas las herramientas de configuración. Tiene solo seis tipos de valor y dos de ellos —el
objeto y la lista— se pueden meter dentro de otros, que es de donde viene toda la complicación:

- **Objeto** (`{ }`): un diccionario, claves con nombre y valores de cualquier tipo. En Python es un
  `dict`.
- **Lista** (`[ ]`): una secuencia ordenada de valores. En Python es una `list`.
- **Cadena**, **número**, **booleano** (`true` / `false`) y **null**. En Python son `str`, `int` o
  `float`, `bool` y `None`.

Leerlo es la parte fácil: `json.loads(texto)` devuelve diccionarios y listas normales, y a partir de
ahí navegas con corchetes, `datos[0]["lecturas"][1]["temp"]`. Cada corchete es un nivel. Si te
equivocas de nivel, el error es inmediato y claro: `KeyError` si la clave no existe, `IndexError` o
`TypeError` si intentas indexar algo que no es una lista.

La parte que cuesta es pasar de esa estructura a una **tabla**, porque una tabla es rectangular y
JSON no. Ahí está la decisión que hay que tomar conscientemente: cuando dentro de un registro hay
una lista, esa lista puede quedarse como una celda con texto, o puede **explotar en filas**. Si
explotas, el registro padre se repite en cada fila hija: es el precio de tener una fila por lectura,
y es también la causa del error de análisis más común con estos datos, porque al promediar una
columna cada registro pesa lo que pesa su lista, no lo que pesa el registro.

Y una advertencia sobre el formato: JSON no tiene fechas. Una fecha viaja como cadena de texto, casi
siempre en formato ISO 8601 (`2026-05-04T08:30:00Z`), y hasta que alguien la convierta con
[[fechas-y-horas|datetime]] es texto que no se puede restar ni ordenar bien. Tampoco distingue
enteros de decimales: `19` y `19.0` son el mismo tipo de valor, número, así que la columna puede
llegar como `float` sin que nadie lo haya pedido.

## Definición formal

Aplanar un JSON con listas dentro consiste en recorrer cada registro y sustituir cada lista por sus
elementos, repitiendo las claves del padre. Si el JSON es una lista de `n` registros y el registro
`i` tiene una lista con `n_i` elementos, la tabla resultante tiene:

:::formula
N_filas = Σ n_i      ·      N_columnas = 1 + máx(k_i)
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `n` | Registros de nivel superior (la lista exterior del JSON) | registros | Más registros, más filas base antes de aplanar |
| `n_i` | Elementos que tiene la lista anidada del registro `i` | elementos | Cada elemento añade una fila: una lista de 10 multiplica por 10 las filas de ese registro |
| `Σ n_i` | Suma de los elementos de todas las listas anidadas | filas | Es el número exacto de filas de la tabla aplanada |
| `k_i` | Campos escalares dentro de cada elemento anidado | columnas | Cada campo nuevo añade una columna, aunque falte en los demás |
| `N_filas` | Filas de la tabla final | filas | Sube con la lista más larga y con el número de registros |
| `N_columnas` | Columnas de la tabla final | columnas | La fija el elemento más rico; los que no lo tienen quedan vacíos |
| profundidad | Niveles de anidamiento que hay que recorrer | niveles | Cada nivel nuevo añade un prefijo al nombre de la columna |
| `ruta` | El camino hasta un valor, como `lecturas.temp` | texto | Es el nombre que acaba teniendo la columna aplanada |
:::

Dos reglas prácticas que salen de ahí:

- **Aplanar puede multiplicar las filas, nunca las reduce.** Si un registro tiene cuatro lecturas,
  ese registro aparece cuatro veces. Nunca al revés.
- **La fila deja de ser «un cliente» y pasa a ser «una lectura».** Antes de calcular medias o
  contar, decide cuál es el grano de la tabla y agrupa si hace falta.

## Ejemplo

Este JSON tiene dos registros y tres lecturas en total:

```text
[
  {"sensor": "S1", "lecturas": [{"hora": "08:00", "temp": 19.5}, {"hora": "09:00", "temp": 21.0}]},
  {"sensor": "S2", "lecturas": [{"hora": "08:00", "temp": 22.4}]}
]
```

- Navegando a mano: `datos[0]["sensor"]` es `"S1"`, `datos[0]["lecturas"][1]["temp"]` es `21.0`,
  `datos[1]["lecturas"][0]["hora"]` es `"08:00"`.
- Para aplanar: `n_1 = 2` (S1) y `n_2 = 1` (S2), así que `N_filas = 2 + 1 = 3`.
- Las temperaturas son 19,5, 21,0 y 22,4. La media de la **tabla aplanada** es
  `(19,5 + 21,0 + 22,4) / 3 = 20,97`.
- La media **por sensor** es `(19,5 + 21,0) / 2 = 20,25` para S1 y `22,4` para S2; la media de esos
  dos valores es `21,32`.

La diferencia entre 20,97 y 21,32 no es un redondeo: es que S1 aporta dos filas y S2 solo una, así
que S1 pesa el doble en la primera cuenta. Ese es el error que hay que ver antes de cometerlo.

:::figura
fichero: json-y-datos-anidados-arbol-y-tabla
pie: A la izquierda está la forma real del dato: un objeto con un campo suelto y una lista de dos elementos. A la derecha, el resultado de aplanar: tres filas, y el sensor del padre repetido en cada una de las dos filas de S1. Fíjate en que el número de filas no lo decide el número de registros (2) sino la suma de elementos de las listas (3), que es exactamente lo que hace que S1 pese el doble al promediar la columna de temperatura.
fuente: figuras/json-y-datos-anidados-1.py
:::

## Código

```python verificable
import json

crudo = """
[
  {"sensor": "S1", "lecturas": [{"hora": "08:00", "temp": 19.5}, {"hora": "09:00", "temp": 21.0}]},
  {"sensor": "S2", "lecturas": [{"hora": "08:00", "temp": 22.4}]}
]
"""
datos = json.loads(crudo)        # texto -> listas y diccionarios de Python
print(type(datos).__name__, len(datos))          # -> list 2
print(datos[0]["sensor"])                        # -> S1
print(datos[0]["lecturas"][1]["temp"])           # -> 21.0
print(datos[1]["lecturas"][0]["hora"])           # -> 08:00
print("total de lecturas:", sum(len(r["lecturas"]) for r in datos))   # -> 3
```

:::claves
- `json.loads` convierte el texto en diccionarios y listas **de Python**, no en un tipo especial: a partir de ahí valen todas las reglas de [[tipos-y-estructuras-python]], incluido que los corchetes anidados son la única forma de llegar al fondo.
- Cada corchete es un nivel y ninguno avisa: `datos[0]["lecturas"][1]["temp"]` significa «primer registro, su lista de lecturas, segundo elemento, clave temp». Si `"lecturas"` no existiera, salta `KeyError`; si intentas indexar un número, `TypeError`.
- Los objetos JSON llegan como `dict` (claves de texto) y las listas como `list` (posiciones desde 0). Un objeto `{ }` y una lista `[ ]` se navegan distinto: `["sensor"]` frente a `[0]`. Confundirlos es el fallo más habitual.
- `json.loads` no convierte fechas ni tipos raros: una fecha ISO llega como `str` y `null` llega como `None`. Con los números sí distingue: `19` llega como `int` y `19.0` como `float`, aunque JSON tenga un solo tipo «número» en la especificación; el que los junta en una columna `float64` es pandas, no el lector de JSON.
- `sum(len(r["lecturas"]) for r in datos)` cuenta los elementos anidados sin aplanar nada: es la comprobación previa que te dice cuántas filas va a tener la tabla antes de construirla.
:::

```python verificable
import json

import pandas as pd

crudo = """
[
  {"sensor": "S1", "lecturas": [{"hora": "08:00", "temp": 19.5}, {"hora": "09:00", "temp": 21.0}]},
  {"sensor": "S2", "lecturas": [{"hora": "08:00", "temp": 22.4}]}
]
"""
datos = json.loads(crudo)

# record_path baja a la lista: una fila por lectura, y meta repite el campo del padre
tabla = pd.json_normalize(datos, record_path="lecturas", meta="sensor")
print(tabla.to_string(index=False))          # tres filas, con el sensor repetido
print("columnas:", list(tabla.columns))      # -> ['hora', 'temp', 'sensor']

# La media de la tabla NO es la media por sensor: S1 aporta el doble de filas
print("media de la tabla:", round(tabla["temp"].mean(), 2))          # -> 20.97
por_sensor = tabla.groupby("sensor")["temp"].mean()
print("media por sensor:", round(por_sensor.mean(), 2))              # -> 21.32

# Sin record_path, la lista se queda entera dentro de una celda
sin_bajar = pd.json_normalize(datos)
print("sin record_path:", list(sin_bajar.columns))                   # -> ['sensor', 'lecturas']
```

```python ilustrativo
import json

# Escribir: json.dump convierte diccionarios y listas en texto.
# indent=2 lo hace legible, ensure_ascii=False conserva las tildes.
informe = {"sensor": "S1", "ciudad": "Málaga", "media": 20.97}
with open("informe.json", "w", encoding="utf-8") as f:
    json.dump(informe, f, indent=2, ensure_ascii=False)

# json.dumps no sabe serializar fechas: lanza TypeError a menos que se conviertan
# antes a texto con isoformat(). Ver [[fechas-y-horas]].
```

## Errores típicos

- **Creer que el JSON ya es una tabla.** `pd.DataFrame(datos)` con listas dentro deja columnas que
  contienen listas de diccionarios: la tabla existe, pero no se puede sumar, agrupar ni exportar
  bien. Hay que decidir el grano antes de construirla.
- **Aplanar sin mirar cuántas filas salen.** Un registro con 200 lecturas se convierte en 200 filas
  y las métricas de nivel de registro (clientes, pedidos, sesiones) dejan de ser contables. Comprueba
  `len(tabla)` contra el número de registros originales.
- **Promediar la tabla aplanada y llamarlo «media por sensor».** Es el error del ejemplo: 20,97 en
  lugar de 21,32. Si el grano es la lectura, la media es de lecturas; para la media por sensor hay
  que agrupar primero.
- **Usar corchetes en el nivel equivocado.** `datos["sensor"]` sobre una lista da
  `TypeError: list indices must be integers`, y `datos[0]["lecturas"]["temp"]` da el mismo error
  porque `lecturas` es una lista, no un diccionario. El mensaje dice exactamente qué nivel falla.
- **Leer un JSON con `json.load` cuando tienes texto.** `json.load` espera un fichero abierto y
  `json.loads` espera una cadena; intercambiarlos da un error que no explica nada:
  `AttributeError: 'str' object has no attribute 'read'` en un sentido y `TypeError: the JSON object
  must be str, bytes or bytearray` en el otro. Si viene de una API, normalmente ya tienes texto y
  toca `loads`.
- **Escribir JSON con fechas u objetos de pandas dentro.** `json.dump` lanza
  `TypeError: Object of type datetime is not JSON serializable`. Se convierten antes a texto
  (`isoformat()`) o a tipos nativos (`int`, `float`, `str`).

:::practica
enunciado: Un JSON con dos pedidos tiene esta forma: el pedido A con 3 líneas y el pedido B con 1. Escribe el código que aplana las líneas a una tabla, imprime cuántas filas tiene, y calcula el importe total de dos maneras: sumando la columna de la tabla aplanada y sumando primero por pedido. Explica por qué coinciden o no.
pista: Con record_path="líneas" y meta="pedido" obtienes una fila por línea; el total es una suma, así que el número de filas no cambia el resultado, pero la media sí.
solucion: Con `pd.json_normalize(pedidos, record_path="lineas", meta="pedido")` la tabla tiene 3 + 1 = 4 filas. La suma del importe es la misma por los dos caminos, porque sumar no pondera por filas: 3 líneas más 1 línea suman lo mismo en cualquier orden. La media sí cambia: la media de la tabla reparte el total entre 4 líneas y la media por pedido reparte entre 2 pedidos, así que da valores distintos. La regla es que aplanar multiplica filas y cualquier media o recuento posterior depende de ese grano.
:::

## Comprueba que lo sabes

:::quiz
p: Un JSON con 10 pedidos tiene dentro de cada pedido una lista de líneas, y en total hay 34 líneas. ¿Cuántas filas tiene la tabla si aplanas las líneas?
o: 10, una por pedido
o: 34, una por línea de pedido
o: 44, los pedidos más las líneas
a: 2
e: Aplanar sustituye cada lista por sus elementos y repite las claves del padre, así que sale una fila por línea: 34. Los 10 pedidos dejan de ser filas y pasan a ser un valor repetido en la columna del padre. El 44 sale de sumar dos granularidades distintas, que no significa nada.
:::

:::quiz
p: Aplanas las lecturas de dos sensores, el primero con 2 lecturas y el segundo con 1, y calculas la media de la columna de temperatura. ¿Qué estás calculando?
o: La media por sensor, porque cada sensor aporta sus lecturas
o: La media de las lecturas, donde el sensor con más lecturas pesa más
o: La media del primer sensor, porque el segundo queda al final
a: 2
e: La tabla tiene el grano de la lectura, así que la media es de lecturas: el sensor con 2 lecturas aporta 2 de las 3 filas y pesa el doble. Para la media por sensor hay que agrupar con groupby y promediar los resultados, que es otra cosa. Y el orden de las filas no influye en una media.
:::

:::quiz
p: Una API te devuelve una fecha como "2026-05-04T08:30:00Z" dentro del JSON. ¿Qué tienes al leerla con json.loads?
o: Un objeto datetime listo para restar
o: Una cadena de texto, porque JSON no tiene tipo fecha
o: Un número con los segundos desde 1970
a: 2
e: JSON solo tiene objeto, lista, cadena, número, booleano y null, así que una fecha viaja como texto y llega como str. Para operar con ella hay que convertirla con datetime.fromisoformat y, si hace falta, ponerle la zona horaria. El número de segundos desde 1970 es otra convención distinta, que no es lo que produce este texto.
:::
