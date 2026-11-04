---
id: operaciones-matriciales
titulo: Operaciones con matrices
fase: 1
nivel: básico
rutas: [core, ds]
prerequisitos: [escalares-vectores-matrices]
tags: [algebra-lineal, matrices, producto]
resumen: Sumar, multiplicar y trasponer matrices tiene reglas propias; el producto no es elemento a elemento y el orden de los factores cambia el resultado.
fuentes: ["Strang (2016), 'Introduction to Linear Algebra'", "Lay, Lay y McDonald (2016), 'Linear Algebra and Its Applications'"]
---

## En una frase

La suma de matrices es elemento a elemento, pero el **producto matricial** combina filas y
columnas enteras, exige que las dimensiones interiores coincidan y **no es conmutativo**:
`AB` y `BA` normalmente son matrices distintas.

## La idea

Con los números normales, multiplicar es fácil y el orden da igual: `3 · 5 = 5 · 3`. Con las
matrices, no. El motivo es que una matriz no es un número grande: es una *acción* sobre el
espacio (lo verás en [[transformaciones-lineales|transformaciones lineales]]). Multiplicar `A`
por `B` significa «aplica primero `B` y después `A`». Ponerte los calcetines y luego los
zapatos no es lo mismo que ponerte los zapatos y luego los calcetines; con matrices pasa
exactamente eso.

La otra diferencia importante es que el producto no se hace casilla a casilla. Para obtener el
elemento de la fila `i` y la columna `j` de `AB` se toma la fila `i` de `A`, la columna `j` de
`B`, se multiplican componente a componente y se suman. Es decir: **cada elemento del producto
es un producto punto** (ver [[producto-punto-y-similitud|producto punto y similitud]]). De ahí
sale la condición de conformidad: la fila de `A` tiene tantos elementos como columnas tiene
`A`, y la columna de `B` tantos como filas tiene `B`; para que se puedan emparejar, las
dimensiones interiores deben coincidir.

:::figura
fichero: producto-no-conmutativo
pie: El mismo cuadrado de partida acaba en dos sitios distintos según se multiplique `A @ B` o `B @ A`: la esquina (1, 1) viaja a (3, 7) en un caso y a (7, 3) en el otro, y las dos figuras tienen la misma área, así que la diferencia no es un error de cuentas. El segundo panel recuerda la única condición que hay que comprobar antes de multiplicar: que la dimensión interior coincida, (m, k) @ (k, n).
fuente: figuras/operaciones-matriciales-1.py
:::

La **traspuesta** `Aᵀ` es girar la tabla: la fila `i` pasa a ser la columna `i`. Es la
operación que aparece cuando cambias el punto de vista entre observaciones y variables, y
tiene una regla que se olvida mucho: `(AB)ᵀ = BᵀAᵀ`, el orden se invierte.

Y la **identidad** `I` es el «1» de este mundo: la matriz con unos en la diagonal y ceros
fuera. Multiplicar por ella no cambia nada, `AI = IA = A`, y sirve para comprobar que tus
productos están bien montados y para definir la inversa.

## Definición formal

Sean `A, B ∈ ℝ^{m×n}` y `c ∈ ℝ` un escalar.

- **Suma:** `(A + B)_ij = a_ij + b_ij`. Solo está definida si ambas tienen la misma forma.
- **Producto por escalar:** `(cA)_ij = c · a_ij`.
- **Producto matricial:** si `A ∈ ℝ^{m×k}` y `B ∈ ℝ^{k×n}`, entonces `AB ∈ ℝ^{m×n}` con
  `(AB)_ij = Σ_{p=1}^{k} a_ip · b_pj`. La dimensión interior `k` es la que se recorre y
  desaparece; la forma del resultado es `(m, n)`. Si las dimensiones interiores no coinciden,
  el producto no existe.
- **Traspuesta:** `Aᵀ ∈ ℝ^{n×m}` con `(Aᵀ)_ij = a_ji`. Propiedades: `(Aᵀ)ᵀ = A` y
  `(AB)ᵀ = BᵀAᵀ`.
- **Identidad:** `I_n ∈ ℝ^{n×n}` con `1` en la diagonal (`i = j`) y `0` fuera. Cumple
  `A I_n = A` y `I_m A = A` para `A ∈ ℝ^{m×n}`.
- **Potencia:** `A² = A A`, solo para matrices cuadradas.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `A`, `B` | Las dos matrices que se multiplican | las de sus elementos | el resultado `AB` solo depende de las dimensiones **exteriores**: `k` se recorre y desaparece |
| `c` | Un escalar que multiplica a una matriz | adimensional, o las de la matriz | cada elemento se multiplica por `c`, y el determinante se multiplica por `c` elevado al número de filas |
| `m` | Filas de `A` y filas de `AB` | entero ≥ 1 | añade filas al resultado; no cambia si el producto es posible o no |
| `k` | La dimensión interior: columnas de `A` y filas de `B` | entero ≥ 1 | cada unidad de `k` añade un sumando a cada elemento; si no coincide con las filas de `B`, el producto simplemente no existe |
| `n` | Columnas de `B` y columnas de `AB` | entero ≥ 1 | añade columnas al resultado; tampoco afecta a la condición de conformidad |
| `(AB)_ij` | El elemento de la fila `i` y la columna `j` de `AB` | las del producto | es el producto punto de la fila `i` de `A` con la columna `j` de `B`: crece al alargarse esas dos |
| `Aᵀ` | La traspuesta: la fila `i` pasa a ser la columna `i` | — | no cambia los números, cambia el orden; `(AB)ᵀ = BᵀAᵀ`, nunca `AᵀBᵀ` |
| `I_n` | La identidad `n × n`, con unos en la diagonal | — | es neutra: `A I = I A = A` para cualquier `A` que encaje |
| `A²` | `A A`, solo si `A` es cuadrada | — | **no** es elevar cada elemento al cuadrado; `A²` y `A * A` dan resultados distintos |
:::

Propiedades que sí se cumplen siempre (cuando las formas encajan): asociativa
`(AB)C = A(BC)` y distributiva `A(B + C) = AB + AC`. La conmutativa **no**: en general
`AB ≠ BA`.

## Ejemplo

Con `A = [[1, 2], [3, 4]]` y `B = [[0, 1], [1, 0]]` (una matriz que intercambia las
coordenadas):

- `AB`: fila 1 por columna 1 → `1·0 + 2·1 = 2`; fila 1 por columna 2 → `1·1 + 2·0 = 1`;
  fila 2 por columna 1 → `3·0 + 4·1 = 4`; fila 2 por columna 2 → `3·1 + 4·0 = 3`.
  Resultado: `[[2, 1], [4, 3]]`.
- `BA`: fila 1 por columna 1 → `0·1 + 1·3 = 3`; fila 1 por columna 2 → `0·2 + 1·4 = 4`;
  fila 2 por columna 1 → `1·1 + 0·3 = 1`; fila 2 por columna 2 → `1·2 + 0·4 = 2`.
  Resultado: `[[3, 4], [1, 2]]`.
- `AB ≠ BA`, y la diferencia no es un error de cuentas: son dos transformaciones distintas.
- `A * B` elemento a elemento daría `[[0, 2], [3, 0]]`, que no tiene nada que ver con
  ninguna de las dos.
- `(AB)ᵀ = [[2, 4], [1, 3]]` y `BᵀAᵀ` da lo mismo; en cambio `AᵀBᵀ = [[3, 1], [4, 2]]`,
  distinto. El orden importa también al trasponer.

Un producto que **no** existe: `A` de forma `(2, 3)` por `A` de forma `(2, 3)`. La dimensión
interior sería `3` en la primera y `2` en la segunda, y no coinciden. En cambio `A` de `(2, 3)`
por `B` de `(3, 2)` sí: el resultado es `(2, 2)`.

## Código

```python verificable
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[0, 1], [1, 0]])

print("A @ B :", (A @ B).tolist())   # -> [[2, 1], [4, 3]]
print("B @ A :", (B @ A).tolist())   # -> [[3, 4], [1, 2]]
print("A * B :", (A * B).tolist())   # -> [[0, 2], [3, 0]]

# La identidad no cambia nada: es el "1" del producto matricial.
print("A @ I = A:", bool(np.array_equal(A @ np.eye(2), A)))   # -> True
```

:::claves
- `A @ B` es el **producto matricial** y `A * B` el **producto elemento a elemento**: no hacen lo mismo y `*` no avisa de nada. `np.matmul(A, B)` y `A.dot(B)` son la misma operación que `@`; `np.multiply(A, B)` es la misma que `*`.
- `(A @ B).tolist()` devuelve una **lista de listas** de Python, no un array: se pierde el tipo de NumPy y ya no hay `.shape`. Sirve para imprimir, no para seguir calculando.
- `np.eye(2)` construye la identidad `2 × 2` sin escribirla a mano. `np.array_equal(...)` devuelve un `bool` de NumPy y compara elemento a elemento; con números en coma flotante casi nunca querrás igualdad exacta sino `np.allclose`, y aquí funciona porque `0` y `±1` se representan exactamente.
- `A @ A` con `A` de forma `(2, 3)` lanza un `ValueError` (no un `LinAlgError`): el mensaje habla de las dimensiones interiores, así que `except ValueError` es lo que hay que capturar. El producto no devuelve un resultado vacío ni `None`, revienta.
- `A @ v` con `v` de forma `(3,)` funciona porque NumPy trata el vector 1D como columna, y el resultado tiene forma `(2,)`, no `(2, 1)`. Si necesitas una columna de verdad: `v.reshape(-1, 1)`.
- `A.T` es una **vista**, no una copia: no duplica memoria y comparte los datos con `A`. Escribir `A.T[0, 0] = 9` cambia también `A[0, 0]`, y esa es la vía por la que un producto «traspuesto» se cuela sin que te des cuenta.
:::

```python verificable
import numpy as np

A = np.array([[1, 2, 3], [4, 5, 6]])      # forma (2, 3)
B = np.array([[1, 0], [0, 1], [2, 2]])    # forma (3, 2)

print("A @ B  :", (A @ B).tolist())        # -> [[7, 8], [16, 17]]
print("(A@B).T:", (A @ B).T.tolist())      # -> [[7, 16], [8, 17]]
print("B.T@A.T:", (B.T @ A.T).tolist())    # -> [[7, 16], [8, 17]]

# Producto matriz-vector: cada componente es un producto punto con una fila.
v = np.array([1, 1, 1])
print("A @ v  :", (A @ v).tolist())        # -> [6, 15]

# Si las dimensiones interiores no coinciden, el producto no existe.
try:
    A @ A
except ValueError:
    print("A @ A: dimensiones interiores incompatibles")   # -> A @ A: dimensiones interiores incompatibles
```

## Errores típicos

- **Usar `*` en numpy creyendo que multiplica matrices.** `*` multiplica elemento a elemento; el producto matricial es `@` (o `np.matmul`). En el ejemplo, `A * B` da `[[0, 2], [3, 0]]` y `A @ B` da `[[2, 1], [4, 3]]`.
- **Suponer que `AB = BA`.** Con `A = [[1, 2], [3, 4]]` y `B = [[0, 1], [1, 0]]` los resultados son `[[2, 1], [4, 3]]` y `[[3, 4], [1, 2]]`. Antes de reordenar un producto, comprueba si las matrices conmutan de verdad.
- **Confundir `(AB)ᵀ` con `AᵀBᵀ`.** Lo correcto es `BᵀAᵀ`. Es el mismo error que cometerás con `(AB)⁻¹`: también se invierte el orden.
- **Dejar que el broadcasting arregle una suma mal dimensionada.** Sumar una matriz `(4, 3)` y un vector de longitud `3` no da error: suma el vector a cada fila. A veces es lo que quieres y a veces no, pero nunca te avisa.
- **Intentar «dividir» matrices.** La división no existe; se multiplica por la inversa, y solo si existe (ver [[determinante-rango-invertibilidad|determinante, rango e inversa]]). Además el lado importa: `A⁻¹B` no es lo mismo que `BA⁻¹`.
- **Olvidar la condición de conformidad.** `(m×k)` por `(k×n)` es lo único válido. Si el error dice «dimensions not aligned», mira las dimensiones interiores antes de tocar nada más.

:::practica
enunciado: Con A = [[2, 0], [1, 3]] y B = [[1, 4], [2, 1]], calcula AB y BA y decide si puedes reordenar el producto sin cambiar el resultado.
pista: Cada elemento es el producto punto de una fila de la primera con una columna de la segunda.
solucion: AB: (2·1 + 0·2) = 2, (2·4 + 0·1) = 8, (1·1 + 3·2) = 7, (1·4 + 3·1) = 7, luego [[2, 8], [7, 7]]. BA: (1·2 + 4·1) = 6, (1·0 + 4·3) = 12, (2·2 + 1·1) = 5, (2·0 + 1·3) = 3, luego [[6, 12], [5, 3]]. No coinciden: el producto no es conmutativo y no puedes reordenarlo.
:::

## Comprueba que lo sabes

:::quiz
p: Con A = [[1, 2], [3, 4]] y B = [[0, 1], [1, 0]], ¿cuánto vale AB y cuánto BA?
o: AB = [[2, 1], [4, 3]] y BA = [[3, 4], [1, 2]]: no coinciden
o: AB = BA = [[0, 2], [3, 0]]
o: AB = [[3, 4], [1, 2]] y BA = [[2, 1], [4, 3]], que es lo mismo que AᵀBᵀ
a: 1
e: Cada elemento del producto es el producto punto de una fila con una columna, y el resultado depende del orden. La opción 2 es el producto elemento a elemento (A * B), que no es el producto matricial; la opción 3 intercambia los resultados y además AᵀBᵀ tampoco es eso.
:::

:::quiz
p: ¿Cuándo se puede multiplicar una matriz de forma (2, 3) por otra de forma (3, 5)?
o: Nunca: solo se pueden multiplicar matrices cuadradas
o: Siempre, porque el número de columnas de la primera coincide con el de filas de la segunda, y el resultado es (2, 5)
o: Solo si las dos son simétricas
a: 2
e: La dimensión interior (3) se recorre y desaparece, así que quedan las exteriores: (2, 5). Las matrices no necesitan ser cuadradas ni simétricas para multiplicarse; lo que hace falta es que las dimensiones interiores coincidan.
:::

:::trampa
Si un resultado te sale «al revés» (por ejemplo, tus coeficientes están traspuestos), el
sospechoso número uno es el orden del producto. Escribe siempre las formas al lado de cada
matriz en un comentario: `A (n×p) @ B (p×k) -> (n×k)`. Cuesta dos segundos y ahorra horas.
:::
