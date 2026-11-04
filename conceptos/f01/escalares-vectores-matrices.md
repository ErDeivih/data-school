---
id: escalares-vectores-matrices
titulo: Escalares, vectores y matrices
fase: 1
nivel: básico
rutas: [core, ds]
prerequisitos: [notacion-matematica]
tags: [algebra-lineal, vectores, matrices, datos]
resumen: Un escalar es un número, un vector es una lista ordenada y una matriz es una tabla; casi todo dataset es una matriz y conviene saber qué eje es qué.
fuentes: ["Strang (2016), 'Introduction to Linear Algebra'", "Deisenroth, Faisal y Ong (2020), 'Mathematics for Machine Learning'"]
---

## En una frase

Un **escalar** es un solo número, un **vector** es una lista ordenada de números y una
**matriz** es una tabla rectangular; casi cualquier dataset que vayas a analizar es una
matriz, y la mitad de los errores de un análisis vienen de confundir qué eje es cuál.

## La idea

Piensa en la hoja de cálculo que usas para apuntar tus gastos. Cada **fila** es un mes y cada
**columna** es un concepto: alquiler, comida, transporte. Eso ya es una matriz. Si te quedas
con una sola fila, tienes un vector: los gastos de ese mes. Si te quedas con un solo número,
el gasto de comida de marzo, tienes un escalar. No hay nada más exótico que eso.

La confusión aparece cuando los datos cambian de forma. Un vector es una lista *ordenada*: el
tercer elemento es el tercero, y si reordenas la lista tienes otra cosa. En la hoja de cálculo
el orden está a la vista; en el código no, y por eso la convención importa. La convención que
usan numpy, pandas, R y scikit-learn es siempre la misma: **una fila por observación, una
columna por variable**. Una tabla de 500 clientes con 12 columnas es una matriz de 500 × 12.
Si la lees al revés, tus medias serán medias de personas en lugar de medias de variables, y el
resultado no dará error: dará un número plausible y falso.

:::figura
fichero: matriz-filas-y-columnas
pie: La misma tabla, leída por filas o por columnas. La media de cada columna (39,5 años, 168,5 cm, 70 kg) describe una variable; la media de una fila (91) mezcla años con kilos y no significa nada. Si un resumen tuyo sale absurdo, mira primero qué eje has recorrido.
fuente: figuras/escalares-vectores-matrices-1.py
:::

Hay una segunda razón para interiorizar la forma: el álgebra lineal opera sobre estos objetos,
y la mayoría de las operaciones exigen que las dimensiones encajen. Sumar dos vectores de
longitud 3 está bien; sumar uno de longitud 3 con otro de longitud 4 no tiene sentido, y
multiplicar dos matrices solo funciona si la dimensión interior coincide. Cuando el código
revienta con un error de formas, casi siempre es esto.

Por último, un **tensor** es la generalización: un array con más de dos ejes. Una imagen en
color es un tensor de tres ejes (alto, ancho, canal) y un lote de 32 imágenes es un tensor de
cuatro (lote, alto, ancho, canal). Cada eje significa algo concreto, y tenerlos desordenados
es un fallo silencioso muy común al entrenar redes.

## Definición formal

- **Escalar:** un único número real, `a ∈ ℝ`. Ejemplos: la temperatura media de un día, el
  coeficiente de una recta, el precio de un producto.
- **Vector:** una lista ordenada de `n` números, `x ∈ ℝⁿ`, con componentes
  `x = (x₁, x₂, …, xₙ)`. `n` es la **dimensión** del vector (su número de componentes).
  Por convenio se escribe en columna; si va en fila se llama vector fila y se nota `xᵀ`.
- **Matriz:** una tabla de `m · n` números ordenados en `m` filas y `n` columnas,
  `A ∈ ℝ^{m×n}`. El elemento de la fila `i` y la columna `j` se escribe `a_ij`, con
  `i = 1, …, m` y `j = 1, …, n`.
- **Forma (shape):** el par `(m, n)`. `m` es el número de observaciones y `n` el número de
  variables cuando la matriz representa un dataset.
- **Matriz como columnas:** `A = [a₁ a₂ … aₙ]`, donde cada `aⱼ ∈ ℝᵐ` es la columna `j`. Es
  una forma de escribir la misma tabla pensando en variables en lugar de en personas.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `a` | Un escalar: un solo número | las de la magnitud que mide | no hay nada que suba: es el caso de un dato suelto |
| `x` | Un vector de `n` componentes | las de la variable que representa | alargar el vector multiplica sus componentes, no su significado: la dirección no cambia |
| `xᵢ` | La componente `i` del vector | las de la variable | cambia ese dato y solo ese; el resto del vector no se toca |
| `n` | Número de columnas: cuántas variables mides | entero ≥ 1 | cada variable nueva añade una columna: la forma pasa a `(m, n+1)` y hay una dimensión más donde dos puntos pueden parecer lejanos sin serlo |
| `A` | La matriz: `m · n` números en `m` filas y `n` columnas | las de cada columna (pueden ser distintas) | — |
| `m` | Número de filas: cuántas observaciones tienes | entero ≥ 1 | más observaciones, no más variables: la forma pasa a `(m+1, n)` y las medias por columna se estabilizan en lugar de cambiar de significado |
| `a_ij` | El elemento de la fila `i` y la columna `j` | las de la variable `j` | — |
| `(m, n)` | La forma del array | par de enteros | si crece `m` ganas filas (más datos); si crece `n` ganas columnas (más dimensiones que resumir) |
| `A = [a₁ a₂ … aₙ]` | La misma matriz leída como `n` columnas | — | es la lectura que hace falta para multiplicar matrices y para hablar de variables |
:::

En notación matemática los índices empiezan en 1; en numpy, pandas y casi todo lenguaje de
programación empiezan en 0. El elemento `a_23` de un texto es `A[1, 2]` en el código.

## Ejemplo

Cuatro personas con tres variables (edad en años, altura en centímetros, peso en kilogramos):

```
        edad  altura  peso
persona 1   34     171    68
persona 2   51     165    71
persona 3   28     180    84
persona 4   45     158    57
```

Escrita como matriz, `A ∈ ℝ^{4×3}`:

```
A = [ 34  171  68 ]
    [ 51  165  71 ]
    [ 28  180  84 ]
    [ 45  158  57 ]
```

- La forma es `(4, 3)`: 4 filas y 3 columnas.
- `a_23 = 71` (persona 2, peso).
- La columna 3, `a₃ = (68, 71, 84, 57)`, es un vector de 4 componentes: la variable peso.
- La fila 1, `(34, 171, 68)`, es un vector de 3 componentes: las tres variables de la persona 1.
- La media de la columna 1 es `(34 + 51 + 28 + 45) / 4 = 39,5` años. La media de la fila 1 es
  `(34 + 171 + 68) / 3 = 91`; ese número no significa nada, y es exactamente lo que obtienes
  si te equivocas de eje.

## Código

```python verificable
import numpy as np

# Dataset de 4 personas: edad, altura en cm y peso en kg (una fila por persona)
datos = np.array([[34, 171,  68],
                  [51, 165,  71],
                  [28, 180,  84],
                  [45, 158,  57]])

print("forma (filas, columnas):", datos.shape)       # -> (4, 3)
print("elemento fila 2, col 3:", datos[1, 2])        # -> 71
print("una fila (persona 1):", datos[0])             # -> [ 34 171  68]
print("una columna (peso):", datos[:, 2])            # -> [68 71 84 57]
print("numero de valores:", datos.size)              # -> 12
```

:::claves
- `datos.shape` devuelve una **tupla**, no una lista: se puede desempaquetar con `filas, columnas = datos.shape`. `shape[0]` son las filas (observaciones) y `shape[1]` las columnas (variables); intercambiar esos dos índices es el error de eje de todo el capítulo.
- `datos[1, 2]` es un **número**, `datos[1]` es la **fila** entera y `datos[:, 2]` la **columna** entera. Los dos últimos son **vistas**, no copias: escribir dentro de `datos[:, 2]` modifica el array original. Para trabajar sin tocar los datos, `.copy()`.
- `datos.mean(axis=0)` devuelve un array de longitud 3 (una media por columna) y `datos.mean(axis=1)` uno de longitud 4 (una por fila). El eje que escribes es el que **se recorre y desaparece**, no el que queda, y equivocarse no lanza ningún error.
- Los datos son enteros, pero `datos.mean(axis=0)` devuelve `float64`: por eso la salida es `39.5` y no `39`. Si necesitas enteros hay que pedirlo explícitamente con `.round().astype(int)`, y ahí decides tú cómo se redondea.
- `datos.T` **no copia** los datos: es una vista transpuesta del mismo bloque de memoria. Su forma es `(3, 4)` y `datos.T[0]` es la primera variable (34, 51, 28, 45), no la primera persona.
- `np.array([1, 2, 3]).shape` es `(3,)` y no `(3, 1)`: un vector 1D no distingue fila de columna y por eso el broadcasting hace cosas inesperadas. `reshape(-1, 1)` lo hace columna y `reshape(1, -1)` fila; el `-1` significa «calcula tú esa dimensión».
:::

```python verificable
import numpy as np

datos = np.array([[34, 171, 68], [51, 165, 71], [28, 180, 84], [45, 158, 57]])

# axis=0 recorre las filas y resume cada columna (cada variable).
# Si te equivocas y usas axis=1, resumes personas: numeros sin sentido.
print("media por columna:", np.round(datos.mean(axis=0), 1))   # -> [ 39.5 168.5  70. ]
print("suma por fila:    ", datos.sum(axis=1))                 # -> [273 287 292 260]

# La traspuesta cambia el significado: ahora cada fila es una variable.
print("forma traspuesta:", datos.T.shape)                      # -> (3, 4)
print("fila 1 de la traspuesta:", datos.T[0])                  # -> [34 51 28 45]

# Un vector 1D de numpy no distingue fila de columna: su forma es (3,)
v = np.array([1, 2, 3])
print("forma de un vector 1D:", v.shape)                       # -> (3,)
print("como columna:", v.reshape(-1, 1).shape)                 # -> (3, 1)
```

## Errores típicos

- **Confundir filas con columnas.** `(4, 3)` son 4 observaciones y 3 variables, no al revés. La pista rápida: `axis=0` resume columnas (variables) y `axis=1` resume filas (registros). Si tus «medias» salen del orden de cientos cuando esperabas decenas, has cambiado los ejes.
- **Decir «dimensión» sin aclarar cuál.** Se usa para dos cosas distintas: el número de ejes de un array (un DataFrame tiene 2) y el tamaño de un eje (12 variables). Di «forma» o «número de variables» y no habrá ambigüedad.
- **Indexar desde 1 en el código.** En matemáticas `x₁` es el primero; en numpy el primero es `x[0]`. El elemento `a_23` se escribe `A[1, 2]` y no `A[2, 3]`, que es otro (o directamente un error de índice).
- **Meter texto en la misma matriz que los números.** Una tabla con una columna de ciudades no es una matriz de `ℝ^{m×n}`: al pasarla a numpy todo se convierte en texto y cualquier media falla o da resultados absurdos. Separa las columnas numéricas de las categóricas.
- **Creer que un vector 1D de numpy es una columna.** Su forma es `(3,)` y no `(3, 1)`. Muchos errores de broadcasting vienen de ahí: usa `reshape(-1, 1)` para una columna y `reshape(1, -1)` para una fila.
- **Olvidar que un tensor tiene más ejes de los que ves.** Un lote de imágenes es `(lote, alto, ancho, canal)`; si confundes el eje del lote con el de los canales, el modelo entrena y no aprende, sin lanzar ningún error.

:::practica
enunciado: Una matriz de ventas tiene 5 filas (una por tienda) y 3 columnas (pan, leche, huevos). Los euros son 12, 8, 5 / 10, 9, 6 / 14, 7, 4 / 9, 11, 5 / 15, 6, 7. Di la forma, el elemento fila 3 columna 2 y la media de la columna 3.
pista: La forma es (filas, columnas) y la media de una variable recorre las filas: axis=0.
solucion: Forma (5, 3). El elemento fila 3, columna 2 es 7. La columna 3 vale (5, 6, 4, 5, 7); su media es (5 + 6 + 4 + 5 + 7) / 5 = 27 / 5 = 5,4 euros por tienda. Si hicieras la media de una fila, por ejemplo (12 + 8 + 5) / 3 = 8,33, mezclarías unidades distintas y el número no significaría nada.
:::

## Comprueba que lo sabes

:::quiz
p: Un dataset con 500 clientes y 12 variables se guarda como matriz. ¿Qué forma tiene?
o: (12, 500), porque primero se ponen las variables y luego las observaciones
o: (500, 12): 500 filas de observaciones y 12 columnas de variables
o: (6000,), porque en total hay 500 · 12 = 6.000 valores
a: 2
e: La convención de numpy, pandas y scikit-learn es una fila por observación y una columna por variable, así que la forma es (500, 12). La primera opción es la traspuesta, que también aparece en álgebra lineal pero no es el formato de un dataset; la tercera confunde el número total de valores con la forma de la tabla.
:::

:::quiz
p: En una matriz de datos, ¿por qué la media de cada variable se calcula con axis=0 y no con axis=1?
o: Porque axis=0 recorre las filas y deja un valor por columna, que es donde vive una variable
o: Porque axis=1 solo funciona con matrices cuadradas
o: Porque axis=0 y axis=1 dan el mismo resultado cuando los datos son numéricos
a: 1
e: El eje que indicas es el que se recorre y se colapsa: con axis=0 se recorren las filas y queda un número por columna, es decir, por variable. Con axis=1 resumirías cada observación, que casi nunca es lo que quieres. Las otras dos opciones son falsas: axis=1 funciona con cualquier forma y los dos ejes dan resultados distintos salvo en casos muy particulares.
:::
