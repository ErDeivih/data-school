---
id: autovalores-y-autovectores
titulo: Autovalores y autovectores
fase: 1
nivel: avanzado
rutas: [core, ds, quant, alg]
prerequisitos: [transformaciones-lineales, determinante-rango-invertibilidad]
tags: [algebra-lineal, pca, pagerank, estabilidad]
resumen: Son las direcciones que una matriz no gira, solo estira; su autovalor dice cuánto, y de ahí salen PCA, PageRank y el análisis de estabilidad.
fuentes: ["Strang (2016), 'Introduction to Linear Algebra'", "Golub y Van Loan (2013), 'Matrix Computations'"]
---

## En una frase

Un **autovector** de una matriz es una dirección especial que la matriz no gira: al
transformarla solo cambia de longitud, y el factor por el que lo hace es su **autovalor**;
encontrar esas direcciones es la forma de entender qué hace de verdad una transformación.

## La idea

Imagina que estiras una goma elástica dibujada con flechas. Casi todas las flechas cambian de
dirección: unas se tuercen a la derecha, otras a la izquierda. Pero hay un par de direcciones
privilegiadas que no se tuercen: solo se alargan o se acortan. Esas son los autovectores, y
los factores de estiramiento son los autovalores.

Hay un ejemplo cotidiano aún mejor: una peonza girando. Casi todos los puntos del cuerpo se
mueven, pero el eje de giro se queda quieto. En una rotación en tres dimensiones, ese eje es
un autovector con autovalor 1 (no cambia de tamaño). En dos dimensiones, en cambio, una
rotación de 90° no deja quieta ninguna dirección real: sus autovalores son complejos. Que una
matriz tenga o no autovalores reales depende de la matriz, no de tu esfuerzo.

¿Para qué sirve esto? Para tres cosas muy distintas:

1. **Reducir dimensiones.** En una matriz de [[covarianza-y-correlacion|covarianza]], los
   autovectores son las direcciones en las que los datos varían más, y los autovalores cuánta
   varianza hay en cada una. Eso es exactamente [[pca|el análisis de componentes
   principales]]: quedarte con las direcciones de autovalor grande.
2. **Entender el largo plazo.** Si aplicas la misma matriz una y otra vez (`Aᵏx`), el término
   asociado al autovalor más grande se come a todos los demás. Ese es el mecanismo de PageRank
   (la importancia de una página es el autovector dominante de la matriz de enlaces) y de
   cualquier sistema que evoluciona por etapas, como una cadena de Markov.
3. **Estudiar estabilidad.** Un sistema que se multiplica por `A` en cada paso crece si algún
   autovalor tiene módulo mayor que 1, se apaga si todos son menores que 1 y oscila si hay
   autovalores complejos. La misma idea aparece al analizar la convergencia de un método
   iterativo.

## Definición formal

Sea `A ∈ ℝ^{n×n}`. Un vector **no nulo** `v ∈ ℝⁿ` es un **autovector** de `A` con
**autovalor** `λ` si:

:::formula
A v = λ v        ⇔        (A − λ I) v = 0
:::

- `A` — la matriz cuadrada, la transformación.
- `v` — el autovector: la dirección que no cambia. Debe ser distinto de cero, porque `v = 0`
  cumpliría la ecuación para cualquier `λ` y no diría nada.
- `λ` — el autovalor, un escalar que puede ser negativo, cero o complejo.
- `I` — la matriz identidad de tamaño `n × n`.
- `(A − λI) v = 0` con `v ≠ 0` significa que `A − λI` tiene una columna dependiente de las
  demás, es decir, es **singular**. De ahí sale la ecuación que permite calcularlos:

:::formula
det(A − λ I) = 0
:::

:::figura
fichero: autovalores-direcciones-propias
pie: A la izquierda, el círculo unidad (gris) y lo que le hace la matriz A: una elipse girada. Las dos flechas de color son los únicos vectores que no cambian de dirección; solo se alargan hasta valer su autovalor. Cualquier otra dirección del círculo acaba torcida. A la derecha, multiplicar A una y otra vez y normalizar: la distancia a la dirección dominante cae como 1/3 por paso, y por eso el autovalor de mayor módulo acaba mandando.
fuente: figuras/autovalores-y-autovectores-1.py
:::

Ese polinomio en `λ` (el **polinomio característico**) tiene grado `n`, así que hay `n`
autovalores contando multiplicidades, aunque no siempre `n` autovectores independientes
(piensa en `[[1, 1], [0, 1]]`: `λ = 1` doble y una sola dirección propia).

Propiedades que conviene tener a mano:

- **Traza y determinante:** `traza(A) = Σᵢ λᵢ` y `det(A) = Πᵢ λᵢ`. Son dos comprobaciones
  gratuitas de que no te has equivocado.
- **Matrices simétricas** (`A = Aᵀ`): todos los autovalores son reales y los autovectores de
  autovalores distintos son ortogonales. Se puede escribir `A = Q Λ Qᵀ` con `Q` ortogonal
  (columnas ortonormales) y `Λ` diagonal. Es el **teorema espectral**.
- **Definida positiva:** todos los `λᵢ > 0`. Es la condición que garantiza que una función
  cuadrática tiene un mínimo único (ver [[convexidad|convexidad]]).
- **Potencia:** `Aᵏ = Q Λᵏ Q⁻¹`, así que `Aᵏ` se comporta como `λᵢᵏ` en cada dirección. El
  autovalor de mayor módulo (**dominante**) manda cuando `k` crece.
- **Normalización:** si `v` es autovector, cualquier múltiplo suyo también lo es. La dirección
  es lo que importa; `numpy.linalg.eigh` devuelve autovectores de norma 1.
- **Cuidado con el orden:** `np.linalg.eig` no ordena los autovalores; `np.linalg.eigh`
  (para matrices simétricas) los devuelve de menor a mayor.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `A` | La matriz cuadrada que se estudia: la transformación | las de la matriz | Escala todas las longitudes: `Aᵏ` se comporta como `λᵢᵏ`, así que un autovalor mayor acelera el crecimiento o la oscilación |
| `v` | El autovector: la dirección que no cambia | las de los datos | Multiplicarlo por un número no cambia nada: sigue siendo el mismo autovector, porque lo que importa es la dirección, y `eigh` lo devuelve con norma 1 |
| `λ` | El autovalor: cuánto estira esa dirección | adimensional | Con `abs(λ) > 1` la dirección crece, con `abs(λ) < 1` se apaga. Si es negativo alterna de signo, y si es complejo la dirección gira |
| `I` | La matriz identidad del mismo tamaño | las de la matriz | No es un parámetro que se mueva: está fija, y sirve para restar `λ` de la diagonal |
| `n` | El número de filas y columnas | adimensional | El polinomio característico sube de grado: hay `n` autovalores contando multiplicidades, pero no está garantizado que haya `n` autovectores independientes |
:::

## Ejemplo

Con `A = [[2, 1], [1, 2]]`, simétrica:

- Traza `= 4` y determinante `= 2·2 − 1·1 = 3`. Buscamos dos números que sumen 4 y
  multipliquen 3: `λ₁ = 1` y `λ₂ = 3`.
- Para `λ = 3`: `(A − 3I) = [[−1, 1], [1, −1]]`, y `v = (1, 1)` cumple `A v = (3, 3) = 3v`.
- Para `λ = 1`: `(A − I) = [[1, 1], [1, 1]]`, y `v = (1, −1)` cumple `A v = (1, −1) = 1·v`.
- Los dos autovectores son ortogonales: `(1, 1) · (1, −1) = 1 − 1 = 0`. Es lo que garantiza el
  teorema espectral y la razón de que PCA funcione tan bien con matrices de covarianza.

**Por qué manda el autovalor dominante.** Escribe `x₀ = (1, 0)` como combinación de los
autovectores: `(1, 0) = 0,5·(1, 1) + 0,5·(1, −1)`. Entonces:

- `A x₀ = (2, 1)`;
- `A² x₀ = (5, 4)`;
- `A¹⁰ x₀ = 0,5 · 3¹⁰ · (1, 1) + 0,5 · 1¹⁰ · (1, −1) = (29525, 29524)`.

La dirección se ha ido alineando con `(1, 1)`: el cociente entre las componentes es
`29524 / 29525 ≈ 1`. La contribución del autovalor 3 ha crecido como `3¹⁰ = 59049`, mientras
la del autovalor 1 se ha quedado en 0,5. Eso es la **iteración de potencias**, y es la razón
de que el método funcione: a fuerza de multiplicar, la dirección dominante se impone.

## Código

```python verificable
import numpy as np

A = np.array([[2.0, 1.0], [1.0, 2.0]])   # simetrica: autovalores reales y autovectores ortogonales

w, V = np.linalg.eigh(A)     # eigh para simetricas; eig no ordena y devuelve complejos si toca
print("autovalores:", np.round(w, 4).tolist())            # -> [1.0, 3.0]
print("autovectores:", np.round(V, 4).tolist())           # -> [[-0.7071, 0.7071], [0.7071, 0.7071]]
print("traza y determinante:", float(np.trace(A)), round(float(np.linalg.det(A)), 1))   # -> 4.0 3.0

# Comprobacion directa de Av = lambda v para el autovalor dominante.
v2 = V[:, 1]
print("A @ v - 3v:", np.round(A @ v2 - w[1] * v2, 10).tolist())   # -> [0.0, 0.0]
```

```python verificable
import numpy as np

A = np.array([[2.0, 1.0], [1.0, 2.0]])
x0 = np.array([1.0, 0.0])

# Con autovalores 3 y 1, el termino dominante multiplica por 3 en cada paso.
print("A @ x0   :", (A @ x0).tolist())                            # -> [2.0, 1.0]
print("A^2 @ x0 :", (np.linalg.matrix_power(A, 2) @ x0).tolist())  # -> [5.0, 4.0]
print("A^10 @ x0:", (np.linalg.matrix_power(A, 10) @ x0).tolist()) # -> [29525.0, 29524.0]
print("3**10:", 3 ** 10)                                           # -> 59049

# Iteracion de potencias: multiplicar y normalizar acaba dando la direccion dominante.
v = x0.copy()
for _ in range(20):
    v = A @ v
    v = v / np.linalg.norm(v)
print("direccion tras 20 pasos:", np.round(v, 4).tolist())         # -> [0.7071, 0.7071]
```

:::claves
- `np.linalg.eigh` devuelve los autovalores **de menor a mayor**, no de mayor a menor: el dominante es `w[-1]` y su autovector es la última **columna** de `V`, `V[:, -1]`. Escribir `w[0]` o `V[0]` es el fallo más frecuente de esta página.
- `eigh` solo vale para matrices simétricas: usa un algoritmo pensado para ellas y supone que `A = Aᵀ`. Con una matriz no simétrica el resultado no es el conjunto de autovalores, y no avisa.
- El resultado es una **tupla** `(w, V)`, así que `w, V = np.linalg.eigh(A)` desempaqueta dos cosas; si escribes `w = np.linalg.eigh(A)` te llevas la tupla entera y cualquier operación posterior falla con un error de tipos.
- `V[:, 1]` es la segunda **columna** de `V` (un autovector), mientras que `V[1]` es la segunda **fila**. En `numpy` el primer índice recorre filas y el segundo columnas; confundirlos es el error clásico al pasar de las matemáticas al código.
- Los autovectores de `eigh` salen **normalizados** (norma 1) y con un signo arbitrario. Por eso `V[:, 1]` vale `[0,7071, 0,7071]` y no `[1, 1]`: `[1, 1]` es el mismo autovector multiplicado por `√2`, y el signo global no significa nada.
- Comprobación barata de que no te has equivocado: `w.sum()` debe valer `np.trace(A)` y `w.prod()` debe valer `np.linalg.det(A)`. Se cumple salvo por el redondeo del último decimal, que en este ejemplo aparece a partir de `1e-16`.
:::

```python verificable
import numpy as np

# Datos casi sobre una recta: la direccion principal explica casi toda la varianza.
X = np.array([[1.0, 2.1], [2.0, 3.9], [3.0, 6.2], [4.0, 7.8], [5.0, 10.1]])
C = np.cov(X, rowvar=False)
w, V = np.linalg.eigh(C)

print("covarianza:", np.round(C, 4).tolist())              # -> [[2.5, 4.975], [4.975, 9.927]]
print("autovalores:", np.round(w, 4).tolist())             # -> [0.0054, 12.4216]
print("suma de autovalores:", round(float(w.sum()), 4))    # -> 12.427
print("varianza total (traza):", round(float(np.trace(C)), 4))   # -> 12.427
print("varianza del primero:", round(float(w[-1] / w.sum()), 4))   # -> 0.9996
```

## Errores típicos

- **Confundir autovalor con valor singular, o esperar que todo autovalor sea real y no negativo.** Los autovalores pueden ser negativos o complejos: la rotación `[[0, −1], [1, 0]]` tiene `i` y `−i`, y ninguna dirección real se queda quieta. Los [[descomposicion-svd|valores singulares]], en cambio, nunca son negativos. Solo coinciden en las matrices simétricas semidefinidas positivas, y de ahí viene la confusión.
- **Dar por hecho que siempre hay `n` autovectores independientes.** `[[1, 1], [0, 1]]` tiene `λ = 1` con multiplicidad 2 y una sola dirección propia. Estas matrices **defectuosas** no se pueden diagonalizar, aunque sí descomponer por SVD.
- **Suponer que los autovalores de `A + B` son los de `A` más los de `B`.** Es falso en general. Lo que sí se cumple es `traza(A + B) = traza(A) + traza(B)`.
- **Olvidar normalizar.** `(1, 1)` y `(1000, 1000)` son el mismo autovector. `eigh` ya devuelve norma 1, pero si lo calculas a mano o con otro paquete, comprueba la norma antes de compararlo con otro.
- **Calcular los autovalores de una matriz de covarianza sin centrar los datos.** Sin restar la media, la primera dirección apunta al centro de los datos y no a la dirección de máxima varianza; el resultado es un [[pca|PCA]] mal hecho.
- **Creer que el autovalor dominante «causa» algo.** Es una propiedad algebraica de la matriz que has construido. Si la matriz está mal (variables duplicadas, datos sin limpiar), el autovector dominante describe perfectamente ese error.

:::practica
enunciado: Con A = [[3, 1], [2, 2]], halla sus autovalores usando la traza y el determinante, comprueba cuál de ellos domina y decide en qué dirección acaba Aᵏx con x = (1, 0).
pista: La traza es la suma de los autovalores y el determinante su producto; el dominante es el de mayor módulo.
solucion: traza = 5 y det = 3·2 − 1·2 = 4, luego λ² − 5λ + 4 = 0 da λ = 4 y λ = 1. Para λ = 4: (A − 4I) = [[−1, 1], [2, −2]] y v = (1, 1) cumple A v = (4, 4). Para λ = 1: v = (1, −2) cumple A v = (1, −2). Como 4 > 1, el término con λ = 4 crece como 4ᵏ y la dirección de Aᵏx tiende a (1, 1).
:::

## Comprueba que lo sabes

:::quiz
p: Con A = [[2, 1], [1, 2]], ¿cuáles son sus autovalores y qué relación cumplen con la traza y el determinante?
o: 1 y 3; suman 4 (la traza) y multiplican 3 (el determinante)
o: 2 y 2; suman 4 y multiplican 4
o: −1 y 3; suman 2, que es la traza de la matriz identidad
a: 1
e: El polinomio característico es λ² − 4λ + 3 = 0, cuyas raíces son 1 y 3. La suma de los autovalores siempre es la traza (4) y su producto, el determinante (3). Como la matriz es simétrica, los autovectores asociados son ortogonales.
:::

:::quiz
p: ¿Por qué al multiplicar A = [[2, 1], [1, 2]] por (1, 0) muchas veces el resultado acaba en la dirección (1, 1)?
o: Porque (1, 1) es el autovector del autovalor dominante 3 y su contribución crece como 3ᵏ, mientras la del autovalor 1 se queda constante
o: Porque toda matriz acaba convergiendo a la identidad
o: Porque (1, 0) es ortogonal a (1, 1) y la componente ortogonal desaparece
a: 1
e: Al descomponer (1, 0) en la base de autovectores, cada paso multiplica la parte de λ=3 por 3 y la de λ=1 por 1. Tras k pasos el término 3ᵏ domina y la dirección se alinea con (1, 1), que es precisamente la iteración de potencias. (1, 0) no es ortogonal a (1, 1): su producto punto vale 1.
:::

:::aviso
La iteración de potencias converge a razón de `(λ₂ / λ₁)ᵏ`. Si los dos autovalores
dominantes tienen módulos parecidos, la convergencia es lentísima y el número de iteraciones
necesario se dispara. Es la misma mala noticia que aparece al analizar por qué un PageRank
tarda en estabilizarse.
:::
