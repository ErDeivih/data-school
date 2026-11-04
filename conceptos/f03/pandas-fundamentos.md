---
id: pandas-fundamentos
titulo: Pandas: fundamentos
fase: 3
nivel: básico
rutas: [core, ds, de]
prerequisitos: [numpy-fundamentos, tipos-y-estructuras-python]
tags: [pandas, dataframes, indexado]
resumen: Un DataFrame es una tabla de columnas con tipo propio y un índice compartido; entender qué devuelve cada corchete evita la mitad de los errores diarios.
fuentes: ["McKinney (2010), 'Data Structures for Statistical Computing in Python'", "McKinney (2017), 'Python for Data Analysis'"]
---

## En una frase

Un `DataFrame` es una tabla con nombre en las columnas, **un índice** que etiqueta las filas y un
tipo de dato por columna; una `Series` es una sola de esas columnas con su índice.

## La idea

Piensa en una hoja de cálculo. La primera fila tiene los nombres de las columnas, cada columna
tiene su propio tipo (una fecha, un importe, un texto) y cada fila tiene una etiqueta: en Excel
el número de fila, en Pandas lo que tú decidas. Esa etiqueta es el **índice**, y es la pieza que
más se malinterpreta.

En Excel, «fila 3» es una posición. En Pandas, `df.loc[3]` busca la **etiqueta** 3, que después
de filtrar o de ordenar puede estar en cualquier posición. Y no es una sutileza académica: si
ordenas una tabla de facturas por importe y luego escribes `df.loc[0]`, no estás cogiendo «la
primera», estás cogiendo la factura cuya etiqueta sea 0, que ahora puede ser la séptima. Pandas,
si la etiqueta no existe, lanza `KeyError`; si existe, te da una fila que no era la que
esperabas y no avisa.

La segunda idea que hay que interiorizar es que **las operaciones se alinean por etiqueta, no por
posición**. Si sumas dos `Series` con índices distintos, Pandas no empareja el primero con el
primero: empareja por nombre y rellena con `NaN` donde falta. Es potentísimo (sumar dos fuentes
de datos que no están en el mismo orden sale gratis) y es la causa de la mitad de los `NaN` que
aparecen en un análisis.

Y la tercera es el coste, que conviene tener presente desde el principio:

- Leer una columna (`df["precio"]`) es barato: no copia los datos.
- Filtrar filas (`df[df["precio"] > 0]`) copia las filas que sobreviven, O(n).
- Añadir una columna es barato; **añadir filas** (concatenar) copia toda la tabla, O(n).
- Recorrer filas con `iterrows()` es lo más caro que puedes hacer en Pandas (ver
  [[vectorizacion]]).

## Definición formal

- **`Series`** — un array de valores **más** un índice de la misma longitud:
  `values` (los datos, normalmente un `ndarray`), `index` (las etiquetas), `name` y `dtype`.
- **`DataFrame`** — una colección ordenada de columnas que **comparten el mismo índice**. Su
  `shape` es `(n_filas, n_columnas)`; cada columna tiene su `dtype`, así que `df.dtypes` es una
  `Series` con un tipo por columna.
- **`index`** — etiquetas de fila. Por defecto, un `RangeIndex` de enteros `0…n−1`; puede ser una
  fecha, un id de cliente o un índice múltiple (`MultiIndex`).

Las dos formas de acceder, que conviene no mezclar nunca:

| Expresión | Accede por | Extremo final |
| --- | --- | --- |
| `df.loc[etiqueta, columna]` | etiqueta de índice y nombre de columna | se incluye |
| `df.iloc[posición, posición]` | posición entera, como en una lista | se excluye |

Y las formas de seleccionar, que es donde se lía todo el mundo:

| Expresión | Devuelve |
| --- | --- |
| `df["precio"]` | una `Series` (una columna) |
| `df[["precio", "unidades"]]` | un `DataFrame` con esas dos columnas |
| `df[mascara]` | las filas donde la máscara booleana es `True` |
| `df.loc[fila, "col"] = valor` | escribe en la tabla original, sin indexado encadenado |
| `df.query("precio > 0")` | lo mismo que la máscara, pero en texto |

Reglas de tipos y de alineación:

- Una columna de enteros que recibe **un solo nulo** se convierte a `float64`, porque `NaN` es un
  número en coma flotante. Si necesitas enteros con nulos, usa el tipo opcional `Int64` (con
  mayúscula).
- El texto tiene su propio dtype (`str`) en Pandas 3; en versiones anteriores era `object`, un
  cajón de sastre que también guarda listas y diccionarios.
- **Alineación:** al operar dos `Series`, el resultado tiene como índice la unión de los dos
  índices; las etiquetas que falten en alguno se rellenan con `NaN`.

## Ejemplo

Cuatro ventas de tres ciudades:

```
ciudad     unidades   precio
Madrid            3     10,0
Sevilla           5      4,0
Madrid            2     10,0
Bilbao            7      2,5
```

- El índice es un `RangeIndex`: 0, 1, 2, 3.
- `df["unidades"].dtype` es `int64` y `df["precio"].dtype` es `float64`.
- La facturación por fila es el producto de dos columnas, que es una operación vectorizada:
  `10 · 3 = 30`, `4 · 5 = 20`, `10 · 2 = 20`, `2,5 · 7 = 17,5`. La suma es **87,5**.
- `df.loc[2, "ciudad"]` y `df.iloc[2, 0]` devuelven lo mismo aquí, **Madrid**, porque el índice
  todavía coincide con la posición.

Ahora ordena por unidades de mayor a menor y mira cómo se rompe esa coincidencia. El índice
queda `[3, 1, 0, 2]`, así que:

- `ordenado["unidades"].iloc[0]` = **7** (la primera fila de la tabla ordenada).
- `ordenado["unidades"].loc[0]` = **3** (la fila cuya etiqueta es 0, que ahora está la tercera).

Ninguno de los dos es un error de Pandas: son dos preguntas distintas. El bug aparece cuando tú
creías estar haciendo una y estabas haciendo la otra.

Alineación, con números pequeños: `a` vale 10, 20, 30 con etiquetas `a, b, c`, y `b` vale 1, 2, 3
con etiquetas `b, c, d`. El resultado de `a + b` tiene cuatro etiquetas: `a` (solo en la
primera) → `NaN`, `b` (20 + 1) → 21, `c` (30 + 2) → 32 y `d` (solo en la segunda) → `NaN`. Si
esperabas tres valores, tienes cuatro y dos son nulos.

## Código

```python verificable
import pandas as pd

ventas = pd.DataFrame({
    "ciudad": ["Madrid", "Sevilla", "Madrid", "Bilbao"],
    "unidades": [3, 5, 2, 7],
    "precio": [10.0, 4.0, 10.0, 2.5],
})

print(ventas.shape)                      # -> (4, 3)
print(ventas["unidades"].dtype)          # -> int64
print(ventas["precio"].dtype)            # -> float64
print(ventas.loc[2, "ciudad"])           # -> Madrid
print(ventas.iloc[2, 0])                 # -> Madrid
print((ventas["unidades"] * ventas["precio"]).sum())   # -> 87.5
```

```python verificable
import pandas as pd

ventas = pd.DataFrame({
    "ciudad": ["Madrid", "Sevilla", "Madrid", "Bilbao"],
    "unidades": [3, 5, 2, 7],
    "precio": [10.0, 4.0, 10.0, 2.5],
})

# Ordenar NO renumera las etiquetas: el indice conserva su valor original
ordenado = ventas.sort_values("unidades", ascending=False)
print(ordenado.index.tolist())              # -> [3, 1, 0, 2]
print(ordenado["unidades"].iloc[0])         # -> 7   (primera fila de la tabla ordenada)
print(ordenado["unidades"].loc[0])          # -> 3   (fila con etiqueta 0 = tercera posicion)
print(ordenado["unidades"].tolist())        # -> [7, 5, 3, 2]
```

```python verificable
import pandas as pd

a = pd.Series([10, 20, 30], index=["a", "b", "c"])
b = pd.Series([1, 2, 3], index=["b", "c", "d"])

suma = a + b                    # se alinea por etiqueta, no por posicion
print(suma.index.tolist())      # -> ['a', 'b', 'c', 'd']
print(suma.tolist())            # -> [nan, 21.0, 32.0, nan]
print(int(suma.notna().sum()))  # -> 2

# Filtrar por una condicion y quedarse con dos columnas
print(a[a > 10].tolist())       # -> [20, 30]
```

## Errores típicos

- **Confundir `loc` con `iloc`.** `df.loc[0]` es «la fila con etiqueta 0» e `df.iloc[0]` es «la
  primera fila». Coinciden solo si el índice es un `RangeIndex` sin filtrar ni ordenar. Si vas a
  filtrar, usa `.iloc` para posiciones y `.loc` para etiquetas, y no los mezcles en la misma
  línea.
- **Asignar con indexado encadenado.** `df[df["a"] > 0]["b"] = 0` no escribe en `df`: el primer
  corchete devuelve un objeto intermedio y la asignación va a ese objeto. Se escribe siempre en
  una operación con `.loc`: `df.loc[df["a"] > 0, "b"] = 0` (ver [[vistas-y-copias]]).
- **`df = df.dropna(inplace=True)`.** Los métodos con `inplace=True` devuelven `None`, así que
  esa línea deja `df` valiendo `None` y el error aparece dos líneas más abajo, cuando algo
  intenta usar `df`. Encadena sin `inplace`: `df = df.dropna()`.
- **Añadir filas con un bucle.** No existe una forma barata de añadir filas: `pd.concat` copia
  toda la tabla. Recoge los trozos en una lista y concatena **una vez** al final. En Pandas 2 y
  posteriores, además, `DataFrame.append` ya no existe.
- **Dar por hecho que las columnas de texto son `object`.** En Pandas 3 el texto tiene su propio
  dtype `str`; comprobar `dtype == object` para detectar texto da falsos negativos. Usa
  `pd.api.types.is_string_dtype` o `is_numeric_dtype` en lugar de comparar con `object`.
- **Sumar series sin mirar el índice.** Una resta entre dos fuentes que no comparten las mismas
  etiquetas produce `NaN` en silencio y la media final sale mal. Antes de operar, comprueba
  `len(a) == len(a.align(b)[0])` o llama a `reset_index(drop=True)` si de verdad quieres alinear
  por posición.

:::practica
enunciado: Con un DataFrame de cuatro ventas (Madrid 3 unidades a 10,0; Sevilla 5 a 4,0; Madrid 2 a 10,0; Bilbao 7 a 2,5), escribe el código que añade la columna `facturacion` (unidades por precio), se queda con las filas cuya facturación supera 25 y dice cuántas quedan y cuánto suman.
pista: La columna nueva es una operación entre columnas enteras y el filtro es una máscara booleana.
solucion: `ventas["facturacion"] = ventas["unidades"] * ventas["precio"]` da 30,0; 20,0; 20,0 y 17,5. La máscara `ventas["facturacion"] > 25` vale `[True, False, False, False]`, así que filtrar deja 1 fila, la de Madrid con 30,0, y esa es también la suma. El filtro copia las filas que sobreviven, O(n), y solo la primera pasa el corte.
:::

## Comprueba que lo sabes

:::quiz
p: Después de `ordenado = df.sort_values("precio")`, ¿qué devuelve `ordenado.iloc[0]`?
o: La fila con etiqueta 0, que puede estar en cualquier posición
o: La primera fila de la tabla ordenada, que es la del precio más bajo
o: Siempre la misma fila que `ordenado.loc[0]`
a: 2
e: `iloc` trabaja por posición y `sort_values` no renumera el índice, así que la primera posición la ocupa la fila de menor precio, sea cual sea su etiqueta. `loc[0]` seguiría buscando la etiqueta 0.
:::

:::quiz
p: `a` tiene índice `[1, 2, 3]` y `b` índice `[2, 3, 4]`. ¿Cuántos elementos tiene `a + b` y cuántos son nulos?
o: Tres elementos, uno nulo
o: Cuatro elementos, dos nulos
o: Error, porque los índices no coinciden
a: 2
e: El índice del resultado es la unión, `[1, 2, 3, 4]`, y las etiquetas 1 y 4 solo existen en uno de los dos, así que se rellenan con `NaN`. Pandas nunca lanza error por índices distintos: alinea y rellena.
:::

:::quiz
p: Una columna de enteros tenía `0, 1, 2` y ahora contiene `0, 1, NaN`. ¿Qué ha pasado con su dtype?
o: Sigue siendo `int64`, porque solo hay un nulo
o: Ha pasado a `float64`, porque `NaN` necesita representación en coma flotante
o: Ha pasado a `str`
a: 2
e: `NaN` es un valor de coma flotante, así que la columna entera se promociona a `float64` y los enteros aparecen como `1.0`. Si necesitas enteros con nulos, usa el dtype opcional `Int64`.
:::

:::nota
`df.info()` y `df.describe()` son las dos primeras cosas que hay que mirar en una tabla
desconocida: la primera da el número de filas, los dtypes y los no nulos; la segunda, el resumen
numérico. Antes de calcular nada, mira si los tipos son los que esperabas (ver
[[perfilado-de-datos]]).
:::
