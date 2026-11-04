---
id: numpy-broadcasting
titulo: Broadcasting de NumPy
fase: 3
nivel: intermedio
rutas: [core, de, ds]
prerequisitos: [numpy-fundamentos, escalares-vectores-matrices]
tags: [numpy, broadcasting, dimensiones]
resumen: NumPy estira las formas compatibles para operar arrays de tamaños distintos sin copiar datos, y por eso una resta mal alineada puede pasar desapercibida.
fuentes: ["Harris et al. (2020), 'Array programming with NumPy', Nature"]
---

## En una frase

El broadcasting es la regla que usa NumPy para operar arrays de formas distintas: alinea las
dimensiones por la derecha, estira las que valen 1 (sin copiar nada) y da error si dos
dimensiones no coinciden y ninguna es 1.

## La idea

Tienes una tabla de ventas con una fila por factura y una columna por mes, y quieres quitarle a
cada mes su media para ver desviaciones. La media es una fila de un solo elemento por mes: 12
números frente a las 100.000 celdas de la tabla. La operación que quieres es «resta esta fila a
todas las filas», y en casi cualquier lenguaje eso es un bucle doble. El broadcasting te deja
escribir `X - medias` y que NumPy entienda que la fila se repite por cada fila de la tabla.

La analogía útil es la de una receta. Si la receta es para 4 personas y tú cocinas para 8,
multiplicas las cantidades por 2 sin reescribir la receta. El array de forma `(4,)` es la receta
y el de forma `(3, 4)` son las 3 comidas: NumPy recorre las 12 posiciones como si el array
pequeño estuviera repetido, pero **no lo repite en memoria**.

Eso último es lo importante y lo que casi nadie sabe: cuando una dimensión se estira, NumPy le
asigna un **stride de 0 bytes**. Avanzar por esa dimensión no mueve el puntero, así que los
mismos 12 números se leen una y otra vez. No hay copia del array pequeño; lo que sí ocupa
memoria es el **resultado**, que tiene la forma grande.

Y de ahí sale también el peligro. El broadcasting solo compara formas, no significados: si tu
matriz es cuadrada, restar la media por filas o por columnas **no da error**, da dos resultados
distintos y los dos son numéricamente válidos. NumPy no puede saber cuál querías.

## Definición formal

Sean dos formas `A = (a₁, …, aₙ)` y `B = (b₁, …, bₙ)`. Si tienen distinta longitud, la más
corta se rellena con unos **por la izquierda** hasta igualarlas. Entonces, dimensión a dimensión,
el resultado `R` es:

:::formula
R_k = max(a_k, b_k)   siempre que   a_k = b_k   o   a_k = 1   o   b_k = 1
:::

Si en alguna dimensión no se cumple ninguna de las tres condiciones, NumPy lanza
`ValueError`. Ejemplos con formas:

| Forma izquierda | Forma derecha | Resultado | Por qué |
| --- | --- | --- | --- |
| `(3, 4)` | `(4,)` | `(3, 4)` | la segunda se rellena a `(1, 4)` y se estira en el eje 0 |
| `(3, 1)` | `(1, 4)` | `(3, 4)` | cada una se estira en el eje que vale 1 |
| `(3, 4)` | `(3,)` | error | se rellena a `(1, 3)` y 4 frente a 3 no encaja |
| `(3, 4)` | `(3, 1)` | `(3, 4)` | la columna se repite en las 4 columnas |
| `(5, 3, 4)` | `(4,)` | `(5, 3, 4)` | se rellena a `(1, 1, 4)` |
| `(5, 3, 4)` | `(5, 1, 4)` | `(5, 3, 4)` | la dimensión de tamaño 1 se estira |

Símbolos y vocabulario:

- `a_k`, `b_k` — longitud de la dimensión `k`, contando desde la derecha.
- **Estirar** una dimensión significa recorrerla con stride 0: se lee el mismo valor en todas
  las posiciones de esa dimensión.
- `np.newaxis` (o `None`) — añade un eje de tamaño 1 donde lo pongas: `v[:, None]` convierte un
  array `(4,)` en `(4, 1)`.
- `keepdims=True` — conserva el eje que la reducción eliminaría, dejándolo de tamaño 1. Es la
  forma de que `X - X.mean(axis=0, keepdims=True)` funcione **para cualquier número de
  dimensiones** sin escribir índices a mano.

## Ejemplo

Dos arrays que parecen incompatibles y producen una tabla:

```
filas = [[0], [1], [2]]        forma (3, 1)
cols  = [1, 2, 3, 4]           forma (4,)
```

Al alinear, `filas` se estira a lo ancho y `cols` a lo alto, y sale la tabla de multiplicar:

```
[[0, 0, 0, 0],
 [1, 2, 3, 4],
 [2, 4, 6, 8]]
```

Ahora el caso que de verdad aparece en el trabajo: centrar por columnas.

```
X = [[ 1,  2,  3],
     [ 4,  6,  8],
     [ 7, 10, 13]]
```

Las medias por columna son `[4, 6, 8]`, con forma `(3,)`. Como `X` es `(3, 3)`, el vector se
rellena a `(1, 3)` y se estira por las 3 filas:

```
X - [4, 6, 8] = [[-3, -4, -5],
                 [ 0,  0,  0],
                 [ 3,  4,  5]]
```

Fíjate en que la matriz es cuadrada: si por error hubieras restado la media por filas, `[2, 6,
10]`, el resultado sería otro y **tampoco habría error**:

```
X - [[2], [6], [10]] = [[-1,  0,  1],
                        [-2,  0,  2],
                        [-3,  0,  3]]
```

Ese es el bug silencioso del broadcasting: con matrices no cuadradas salta un `ValueError` y lo
arreglas en un minuto; con matrices cuadradas se queda ahí, dando resultados que parecen
razonables.

## Código

```python verificable
import numpy as np

filas = np.arange(3).reshape(3, 1)   # forma (3, 1): una columna
cols = np.arange(1, 5)               # forma (4,): una fila
print(filas.shape, cols.shape, (filas * cols).shape)   # -> (3, 1) (4,) (3, 4)

# Al estirar las dos dimensiones de tamano 1 sale la tabla de multiplicar, sin bucles
print((filas * cols).tolist())   # -> [[0, 0, 0, 0], [1, 2, 3, 4], [2, 4, 6, 8]]
```

```python verificable
import numpy as np

X = np.array([[1.0, 2.0, 3.0],
              [4.0, 6.0, 8.0],
              [7.0, 10.0, 13.0]])   # 3 muestras (filas) x 3 variables (columnas)

por_columna = X.mean(axis=0)        # forma (3,): se alinea con las columnas
print(por_columna.tolist())         # -> [4.0, 6.0, 8.0]
print((X - por_columna).tolist())   # -> [[-3.0, -4.0, -5.0], [0.0, 0.0, 0.0], [3.0, 4.0, 5.0]]

# keepdims conserva el eje de tamano 1: la misma linea vale para 2 o para 5 dimensiones
print(X.mean(axis=0, keepdims=True).shape)   # -> (1, 3)
print(X.mean(axis=1, keepdims=True).shape)   # -> (3, 1)
```

```python verificable
import numpy as np

X = np.ones((3, 4))
print(X.shape, np.ones(3).shape)   # -> (3, 4) (3,)

# Se alinea por la derecha: 4 contra 3 no encaja y NumPy avisa en vez de adivinar
try:
    X + np.ones(3)
    print("no falla")
except ValueError:
    print("ValueError: no se puede alinear (3,4) con (3,)")   # -> ValueError: no se puede alinear (3,4) con (3,)

# Anadir el eje que falta con newaxis es la forma de arreglarlo
print((X + np.ones(3)[:, None]).shape)   # -> (3, 4)
```

## Errores típicos

- **Restar la media del eje equivocado.** `X - X.mean(axis=1, keepdims=True)` resta la media de
  cada fila cuando querías la de cada columna. Con matrices cuadradas no hay error, solo
  resultados mal. Regla práctica: la reducción y la resta llevan **el mismo `axis`**, y si usas
  `keepdims=True` ni siquiera tienes que pensar en la forma del resultado.
- **Creer que el broadcasting alinea por la izquierda.** Se alinea por la derecha: `(3, 4)` con
  `(3,)` falla precisamente porque el 3 se compara con el 4. Para que funcione hay que añadir el
  eje, `v[:, None]`, y obtener `(3, 1)`.
- **Pensar que el array pequeño se copia.** No se copia: se lee con stride 0. Lo que sí ocupa
  memoria es el resultado, y ahí está el riesgo real: `(1_000_000, 1) * (1, 1_000_000)` parece
  barato y crea un array de un billón de elementos.
- **Confundir un vector `(n,)` con un vector columna `(n, 1)`.** NumPy no tiene vectores fila ni
  columna: tiene formas. Un `(n,)` se alinea con la última dimensión, y eso decide si tu
  operación resta por filas o por columnas.
- **Usar `reshape` donde querías `newaxis`.** `a.reshape(1, -1)` y `a.reshape(-1, 1)` tienen
  formas distintas, y `reshape` puede reordenar los datos si el número de elementos no cuadra
  como crees; `a[:, None]` solo añade un eje y nunca reinterpreta el orden.
- **Encadenar broadcasting pesado en memoria.** Cada operación intermedia crea su propio array
  del tamaño grande. En un bucle con arrays enormes conviene escribir en el sitio con `+=` o
  `out=`, o trocear los datos (ver [[vectorizacion]]).

:::practica
enunciado: Con `X = np.array([[2.0, 4.0, 6.0], [4.0, 8.0, 12.0]])` (2 muestras, 3 variables), escribe el código que centra las columnas y luego las divide por su desviación típica. Indica la forma de cada array intermedio y di qué pasaría con `X - X.mean(axis=1, keepdims=True)`.
pista: Centrar por columnas es restar la reducción con `axis=0`; `keepdims` conserva el eje de tamaño 1 y evita tener que pensar en la forma.
solucion: `medias = X.mean(axis=0)` tiene forma `(3,)`, vale `[3, 6, 9]` y se estira por las 2 filas: `X - medias` es `[[-1, -2, -3], [1, 2, 3]]`. Las desviaciones por columna son `[1, 2, 3]`, así que dividiendo el resultado centrado entre `X.std(axis=0, keepdims=True)` queda `[[-1, -1, -1], [1, 1, 1]]`. Con `axis=1` restarías la media de cada fila `[4, 8]`; no daría error y el centrado sería el equivocado.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Cuál es la forma del resultado de operar un array `(5, 3, 4)` con otro `(3, 1)`?
o: `(5, 3, 4)`, porque el segundo se rellena a `(1, 3, 1)` y se estira en los ejes 0 y 2
o: Error, porque las formas no son iguales
o: `(5, 3, 4, 3, 1)`, porque NumPy concatena las dos formas
a: 1
e: Al rellenar por la izquierda, `(3, 1)` se convierte en `(1, 3, 1)`. La dimensión 3 coincide con la del medio y la de tamaño 1 se estira hasta 4, así que el resultado conserva la forma del array grande.
:::

:::quiz
p: Tienes `X` con forma `(1000, 20)` y quieres centrar cada columna. ¿Qué expresión es correcta?
o: `X - X.mean(axis=0)`
o: `X - X.mean(axis=1)`
o: `X - X.mean()`
a: 1
e: `X.mean(axis=0)` da 20 medias con forma `(20,)`, que se alinean con las columnas y se estiran por las 1000 filas. Con `axis=1` obtendrías 1000 medias por fila (y un error de formas en este caso), y `X.mean()` resta un único número global.
:::

:::quiz
p: ¿Por qué `(3, 4)` combinado con `(3,)` da error, pero `(3, 4)` con `(4,)` no?
o: Porque el broadcasting rellena la forma más corta por la izquierda, así que el 3 se compara con el 4
o: Porque los arrays de una sola dimensión solo se pueden sumar a escalares
o: Porque el 4 es par y el 3 impar
a: 1
e: `(3,)` se rellena a `(1, 3)` y sus dimensiones se comparan con `(3, 4)` de derecha a izquierda: 3 contra 4 no encaja. `(4,)` se rellena a `(1, 4)`, encaja con la última dimensión y se estira por las 3 filas.
:::

:::aviso
El broadcasting también aparece en Pandas, y ahí es aún más traicionero porque las etiquetas del
índice y de las columnas entran en juego además de las formas (ver [[pandas-fundamentos]]). Si
restas una Serie a un DataFrame, la alineación no es por posición sino por nombre.
:::
