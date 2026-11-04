---
id: transformaciones-lineales
titulo: Transformaciones lineales
fase: 1
nivel: intermedio
rutas: [core, ds, alg]
prerequisitos: [operaciones-matriciales, escalares-vectores-matrices]
tags: [algebra-lineal, geometria, rotacion, proyeccion]
resumen: Una matriz es una acción sobre el espacio: rota, escala, proyecta o refleja, y sus columnas son las imágenes de los vectores de la base.
fuentes: ["Strang (2016), 'Introduction to Linear Algebra'", "Axler (2015), 'Linear Algebra Done Right'"]
---

## En una frase

Una **transformación lineal** es una regla que mueve puntos del espacio sin curvar, sin torcer
y sin mover el origen; se representa con una matriz, y las columnas de esa matriz son
exactamente donde acaban los vectores de la base.

## La idea

Hasta ahora has visto la matriz como una tabla de datos (ver
[[escalares-vectores-matrices|escalares, vectores y matrices]]). Aquí cambia el papel: la
matriz es una **máquina de mover puntos**. Le das un vector y te devuelve otro. Lo importante
es que la máquina es *lineal*: si le das la suma de dos vectores, responde con la suma de las
dos respuestas, y si le das un vector estirado, responde estirado.

Eso restringe muchísimo lo que puede hacer. Una transformación lineal puede **rotar** (como
girar una foto), **escalar** (estirar o encoger, igual o distinto en cada eje), **cizallar**
(como inclinar la baraja de cartas: la base se queda y las alturas se desplazan),
**proyectar** (como la sombra de un objeto en el suelo: aplasta una dimensión) y **reflejar**
(como un espejo). Lo que **no** puede hacer es trasladar: mover todo el espacio sin dejar
ningún punto quieto no es lineal, porque el origen tiene que quedarse donde está. Por eso la
[[regresion-lineal|regresión lineal]] siempre lleva un término independiente aparte: la
traslación es otra pieza.

:::figura
fichero: matriz-como-accion
pie: Las cuatro acciones aplicadas al mismo cuadrado gris: rotar lo gira sin estirarlo (det = 1), escalar multiplica las áreas por 6, cizallar cambia la forma pero no el área y proyectar lo aplasta hasta perder una coordenada entera (det = 0). Las flechas son las columnas de la matriz, es decir, dónde acaban los dos vectores de la base: con esas dos imágenes queda decidida toda la transformación.
fuente: figuras/transformaciones-lineales-1.py
:::

La parte útil para el día a día es que componer transformaciones es multiplicar matrices. Y
como el producto no es conmutativo (ver [[operaciones-matriciales|operaciones con matrices]]),
el orden se nota: rotar y luego escalar no es lo mismo que escalar y luego rotar. Ese es el
mismo motivo por el que en un modelo de machine learning el preprocesado y la capa lineal no
se pueden intercambiar alegremente.

## Definición formal

Una función `T : ℝⁿ → ℝᵐ` es **lineal** si para todos `x, y ∈ ℝⁿ` y todo escalar `c`:

:::formula
T(x + y) = T(x) + T(y)        T(c · x) = c · T(x)
:::

Toda transformación lineal de `ℝⁿ` en `ℝᵐ` se puede escribir como `T(x) = A x` con una única
matriz `A ∈ ℝ^{m×n}`.

- `A` — la matriz de la transformación, en la base canónica.
- **Columnas de `A`:** la columna `j` es `T(eⱼ)`, la imagen del vector `j` de la base
  canónica (`e₁ = (1, 0, …, 0)`, etc.). Conocer esas imágenes determina `T` por completo.
- **Kernel o núcleo:** `ker(T) = {x : A x = 0}`, los vectores que la transformación aplasta
  contra el origen. Si el kernel contiene algo más que el vector cero, `T` **pierde
  información** y no es invertible.
- **Imagen o recorrido:** todos los valores que puede tomar `T(x)`; su dimensión es el
  [[determinante-rango-invertibilidad|rango]] de `A`.
- **Determinante:** el factor por el que la transformación multiplica áreas (en `ℝ²`) o
  volúmenes (en `ℝ³`). Si el valor absoluto es 1, conserva el área; si es 0, aplasta; si es
  negativo, invierte la orientación.
- **Composición:** aplicar `B` y después `A` es `A (B x) = (AB) x`. Se lee de derecha a
  izquierda.
- **Matrices típicas en `ℝ²`:** rotación `R(θ) = [[cos θ, −sin θ], [sin θ, cos θ]]`; escalado
  `[[s₁, 0], [0, s₂]]`; cizalladura `[[1, k], [0, 1]]`; proyección sobre el eje x
  `[[1, 0], [0, 0]]`. La proyección cumple `P² = P` (aplicarla dos veces es aplicarla una).

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `T` | La transformación: la regla que mueve cada punto | — | si no cumple `T(x + y) = T(x) + T(y)` no es lineal, y entonces no hay matriz que la represente |
| `x`, `y` | Vectores de entrada | las de la variable que representan | estirar la entrada estira la salida en la misma proporción (esa es la definición) |
| `c` | Un escalar que multiplica a un vector | adimensional | multiplica la salida por el mismo `c`; si esto falla, la regla no es lineal |
| `A ∈ ℝ^{m×n}` | La matriz de la transformación en la base canónica | — | cambiar `A` cambia la acción; no hay más: la matriz **es** la transformación |
| `eⱼ` | El vector `j` de la base canónica `(1, 0)`, `(0, 1)`… | adimensionales | solo hay `n` de ellos, y la columna `j` de `A` es `T(eⱼ)`: con esas imágenes queda determinada toda `T` |
| `ker(T)` | El núcleo: los vectores que acaban en el origen | las de los vectores | si contiene algo más que el vector cero, `T` pierde información y **no** es invertible |
| `det(A)` | El factor de área (en 2D) o de volumen (en 3D) | adimensional | `|det| = 1` conserva el área, `0` aplasta, negativo invierte la orientación. Es el número que dice si se puede deshacer |
| `θ` | El ángulo de una rotación `R(θ)` | radianes | no cambia longitudes ni áreas, sea cual sea: una rotación nunca estira |
| `s₁, s₂` | Los factores de escala de cada eje | adimensionales | el área se multiplica por `s₁ · s₂`; si son **distintos**, escalar y rotar dejan de conmutar y el orden importa |
| `k` | La pendiente de la cizalladura `[[1, k], [0, 1]]` | adimensional | el área no cambia nunca (`det = 1`), pero las distancias y la forma sí: inclina sin estirar |
| `P` | Una proyección, como `[[1, 0], [0, 0]]` | — | cumple `P² = P` y `det(P) = 0`: lo que aplasta la primera vez no vuelve a moverse, y lo aplastado no se recupera |
:::

## Ejemplo

Trabajamos con el punto `p = (3, 1)`.

- **Rotar 90°:** `R = [[0, −1], [1, 0]]` → `R p = (−1, 3)`. La longitud se conserva:
  `‖p‖₂ = √10 ≈ 3,1623` y `‖R p‖₂ = √10`.
- **Escalar:** `S = [[2, 0], [0, 3]]` → `S p = (6, 3)`. El determinante de `S` es 6, así que
  las áreas se multiplican por 6.
- **Orden importa:** `S (R p) = S(−1, 3) = (−2, 9)`, mientras que `R (S p) = R(6, 3) = (−3, 6)`.
  Dos puntos distintos partiendo del mismo `p`.
- **Proyectar:** `P = [[1, 0], [0, 0]]` → `P p = (3, 0)`. `det(P) = 0`, el rango es 1 y el
  kernel es todo el eje y: cualquier `(0, y)` acaba en el origen. Por eso `P` no es
  invertible: la información de la segunda coordenada se ha perdido para siempre.
- **Cizallar:** `H = [[1, 1], [0, 1]]` → `H(2, 1) = (3, 1)`. `det(H) = 1`, así que las áreas
  no cambian aunque las formas sí: es la transformación que inclina sin estirar.
- **Las columnas son las imágenes de la base:** la primera columna de `R` es `(0, 1)`, que es
  `R e₁` con `e₁ = (1, 0)`; la segunda es `(−1, 0)`, que es `R e₂` con `e₂ = (0, 1)`. Con esas
  dos imágenes queda determinada toda la rotación.
- **Una traslación no es lineal:** `T(x) = x + (1, 0)` cumple `T(0) = (1, 0) ≠ 0`. Rompe
  `T(c·0) = c·T(0)` y por eso necesita una columna extra de unos en la regresión.

## Código

```python verificable
import numpy as np

p = np.array([3.0, 1.0])
R = np.array([[0.0, -1.0], [1.0, 0.0]])   # rotar 90 grados en sentido antihorario
S = np.array([[2.0, 0.0], [0.0, 3.0]])    # estirar cada eje de forma distinta

print("R @ p      :", (R @ p).tolist())          # -> [-1.0, 3.0]
print("S @ (R @ p):", (S @ (R @ p)).tolist())    # -> [-2.0, 9.0]
print("R @ (S @ p):", (R @ (S @ p)).tolist())    # -> [-3.0, 6.0]
print("mismo punto:", bool(np.array_equal(S @ (R @ p), R @ (S @ p))))   # -> False
print("norma antes y despues de rotar:", round(float(np.linalg.norm(p)), 4),
      round(float(np.linalg.norm(R @ p)), 4))    # -> 3.1623 3.1623
```

:::claves
- `R @ p` (matriz `2 × 2` por vector `(2,)`) devuelve un array de forma `(2,)`; `R * p` sería el producto elemento a elemento. En `S @ (R @ p)` los paréntesis no cambian el resultado (el producto es asociativo), pero sí el trabajo: `(S @ R) @ p` calcula antes la matriz compuesta y hace menos operaciones.
- `np.array_equal(S @ (R @ p), R @ (S @ p))` compara **elemento a elemento** y devuelve `False`. Con rotaciones de ángulos cualesquiera habría que usar `np.allclose`, porque en coma flotante dos caminos distintos casi nunca dan bits idénticos. Aquí la rotación es de 90° y los valores son `0` y `±1`, que se representan exactos.
- `R @ np.eye(2)` devuelve la propia `R`: multiplicar por la identidad es la forma rápida de **ver** las columnas de una matriz sin copiarlas a mano.
- `np.linalg.det(S)` da `6.0` aunque `S` esté escrita con enteros: `det` siempre devuelve coma flotante. El determinante de un escalado es el producto de los factores, `2 · 3 = 6`, y esa cuenta es la que explica el área.
- `P @ P` es igual a `P` (idempotente) y `np.array_equal(P @ P, P)` lo confirma. Es la comprobación más barata de que una transformación pierde información: si `det` es cero, ningún producto de `P` por sí misma la deshace.
- `np.array([3.0, 1.0])` convierte una lista de Python en un array de `float64`; con `[3, 1]` sería entero y las medias y divisiones posteriores cambiarían de tipo. Escribir los puntos con decimales no es decoración: fija desde el principio que el cálculo es en coma flotante.
:::

```python verificable
import numpy as np

R = np.array([[0.0, -1.0], [1.0, 0.0]])
S = np.array([[2.0, 0.0], [0.0, 3.0]])
P = np.array([[1.0, 0.0], [0.0, 0.0]])

# Las columnas de la matriz son las imagenes de los vectores de la base.
print("columnas de R:", (R @ np.eye(2)).tolist())    # -> [[0.0, -1.0], [1.0, 0.0]]

# El determinante es el factor de area: S multiplica por 6 y P aplasta a cero.
print("det(S) y det(P):", round(float(np.linalg.det(S)), 1),
      round(float(np.linalg.det(P)), 1))             # -> 6.0 0.0

# Proyectar dos veces es proyectar una vez: P es idempotente.
print("P @ P == P:", bool(np.array_equal(P @ P, P)))      # -> True
print("P @ (3,1):", (P @ np.array([3.0, 1.0])).tolist())  # -> [3.0, 0.0]

# Cizallar conserva el area aunque mueva los puntos.
H = np.array([[1.0, 1.0], [0.0, 1.0]])
print("H @ (2,1):", (H @ np.array([2.0, 1.0])).tolist(),
      "det:", round(float(np.linalg.det(H)), 1))         # -> [3.0, 1.0] det: 1.0
```

## Errores típicos

- **Leer la matriz como datos y no como acción.** La misma tabla de números puede ser un dataset o una transformación; confundirlas lleva a «limpiar» una matriz de rotación o a interpretar una rotación como una tabla de clientes.
- **Componer en el orden equivocado.** En `A B x` se aplica **primero** `B`. En el ejemplo, `S(R p) = (−2, 9)` y `R(S p) = (−3, 6)`. Escribe la cadena de derecha a izquierda y no te equivocarás.
- **Suponer que rotar y escalar conmutan.** Solo conmutan cuando el escalado es igual en todos los ejes (`s₁ = s₂`). Con `S = [[2, 0], [0, 3]]` no.
- **Creer que toda transformación se puede deshacer.** Una proyección tiene `det = 0` y un kernel no trivial: la información que aplasta no vuelve. Antes de invertir, mira el determinante y el rango.
- **Llamar lineal a una transformación afín.** `T(x) = Ax + b` con `b ≠ 0` no es lineal, porque mueve el origen. Es lineal más una traslación, y por eso los modelos llevan término independiente.
- **Pensar que multiplicar por una matriz conserva las distancias.** Solo las rotaciones y las reflexiones lo hacen. Un escalado cambia las longitudes por el factor de escala, y una cizalladura cambia las distancias sin cambiar las áreas ni el determinante.

:::practica
enunciado: Con la cizalladura H = [[1, 1], [0, 1]] y el escalado S = [[2, 0], [0, 5]], aplica las dos al punto p = (2, 1) en los dos órdenes y compara.
pista: En A B p se aplica primero B; componer es multiplicar matrices y el orden no da igual.
solucion: Primero H: H p = (2 + 1, 1) = (3, 1); después S: S(3, 1) = (6, 5). Primero S: S p = (4, 5); después H: H(4, 5) = (4 + 5, 5) = (9, 5). Resultados distintos, (6, 5) frente a (9, 5). El determinante lo confirma: det(H) = 1 y det(S) = 10, así que la composición multiplica las áreas por 10 en los dos órdenes, pero mueve los puntos a sitios diferentes.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Cuál es la forma más directa de saber dónde acaba el vector (1, 0) al aplicarle una matriz A de 2 × 2?
o: Es la primera columna de A, porque las columnas son las imágenes de los vectores de la base
o: Es la primera fila de A, porque la matriz actúa por filas
o: Hay que resolver el sistema Ax = (1, 0)
a: 1
e: Toda transformación lineal queda determinada por lo que le pasa a la base: la columna j de A es la imagen del vector j de la base. La primera fila de A da el primer componente del resultado de cualquier vector, no la imagen de e₁.
:::

:::quiz
p: Con R la rotación de 90° y S el escalado [[2, 0], [0, 3]], ¿por qué S(R p) y R(S p) son distintos?
o: Porque el producto matricial no es conmutativo: son dos transformaciones distintas aplicadas en órdenes distintos
o: Porque una de las dos expresiones no está definida
o: Porque R tiene determinante 0 y S no
a: 1
e: Rotar y luego escalar de forma no uniforme no es lo mismo que escalar y luego rotar: `S R ≠ R S`. Ambas expresiones están definidas y ambas matrices son invertibles, con determinantes 1 y 6 respectivamente.
:::

:::trampa
Si un resultado «se sale del sitio» (una imagen girada, unos ejes cambiados, un gráfico
reflejado), antes de tocar los datos comprueba el orden de tus matrices. Y no lo digas en
voz alta: bastantes veces el fallo es un `A @ B` que debería ser `B @ A`.
:::
