---
id: descomposicion-svd
titulo: Descomposición en valores singulares
fase: 1
nivel: avanzado
rutas: [core, ds, quant]
prerequisitos: [autovalores-y-autovectores, norma-y-distancias]
tags: [algebra-lineal, svd, compresion, dimensionalidad]
resumen: Cualquier matriz se escribe como giro, estirado y giro; quedarte con los valores singulares grandes comprime y limpia sin perder lo esencial.
fuentes: ["Golub y Van Loan (2013), 'Matrix Computations'", "Trefethen y Bau (1997), 'Numerical Linear Algebra'"]
---

## En una frase

La **descomposición en valores singulares** (SVD) escribe cualquier matriz, cuadrada o no, como
el producto de un giro, un estirado a lo largo de ejes perpendiculares y otro giro; los
factores del estirado son los **valores singulares**, y quedarte solo con los `k` más grandes
da la mejor aproximación de rango `k` que existe.

## La idea

Toda transformación lineal hace siempre lo mismo, por muy rara que parezca la matriz: coge el
espacio, lo **gira**, lo **estira** en direcciones perpendiculares y lo vuelve a **girar**. La
SVD separa esas tres etapas y te dice cuánto estira en cada una. Es como desmontar una receta
en sus pasos: primero orientas los ingredientes, luego los escalas y luego colocas el plato.

Lo importante es que esos estirones están ordenados de mayor a menor. El primer valor singular
es el estirón más grande y su dirección asociada es la que más «pesa» en la matriz. Si el
segundo, el tercero y el resto son diminutos en comparación, la matriz es *casi* de rango 1:
se puede describir con muy poca información. Ahí está la gracia:

- **Compresión.** Guardar los `k` primeros valores singulares y sus vectores ocupa mucho menos que la matriz completa si `k` es pequeño frente a las dimensiones.
- **Limpieza de ruido.** El ruido suele repartirse por igual entre muchísimas direcciones pequeñas. Tirarlas quita ruido y conserva la estructura.
- **Sistemas de recomendación.** En una matriz de valoraciones (usuarios por películas) con muchos huecos, los valores singulares grandes capturan gustos latentes compartidos.
- **Reducción de dimensionalidad.** Aplicada a una matriz de datos **centrada**, la SVD es la forma numéricamente estable de calcular el [[pca|PCA]]: las direcciones principales son las columnas de `V`.

Y hay una segunda lectura, muy práctica: el cociente entre el valor singular mayor y el menor
es el **número de condición**, la medida de cuánto amplifica la matriz los errores. Una matriz
con valores singulares que decaen de `25` a `0,001` no es de fiar para resolver un sistema,
por mucho que sea invertible (ver [[determinante-rango-invertibilidad|determinante, rango e
inversa]]).

## Definición formal

Para cualquier matriz `A ∈ ℝ^{m×n}` existen matrices ortogonales `U ∈ ℝ^{m×m}` y
`V ∈ ℝ^{n×n}` y una matriz `Σ ∈ ℝ^{m×n}` con valores no negativos en la diagonal tales que:

:::formula
A = U Σ Vᵀ = Σᵢ₌₁^r σᵢ uᵢ vᵢᵀ
:::

- `σ₁ ≥ σ₂ ≥ … ≥ σ_r > 0` — los **valores singulares**, con `r = rango(A)`. Son las raíces
  cuadradas de los autovalores de `AᵀA` (y de `AAᵀ`, que comparten los mismos valores no
  nulos). Nunca son negativos.
- `U = [u₁ … u_m]` — **vectores singulares por la izquierda**, ortonormales. Son los
  [[autovalores-y-autovectores|autovectores]] de `AAᵀ`.
- `V = [v₁ … v_n]` — **vectores singulares por la derecha**, ortonormales. Son los
  autovectores de `AᵀA`.
- `uᵢ vᵢᵀ` — una matriz de rango 1 (el **producto exterior**); `A` es la suma ponderada de `r`
  matrices de rango 1.
- **Forma truncada:** si solo te interesan los `k` primeros, `U_k` es `m × k`, `Σ_k` es
  `k × k` y `V_k` es `n × k`, y `A_k = U_k Σ_k V_kᵀ`.
- **Eckart-Young:** entre todas las matrices `B` con `rango(B) ≤ k`, la que minimiza
  `‖A − B‖` (en norma de Frobenius y en norma espectral) es exactamente `A_k`. No hay una
  aproximación de rango `k` mejor.
- **Pseudo-inversa:** `A⁺ = V Σ⁺ Uᵀ`, con `1/σᵢ` en lugar de `σᵢ`. Resuelve el problema de
  mínimos cuadrados incluso cuando `A` no es cuadrada ni invertible.
- **Número de condición:** `κ₂(A) = σ_max / σ_min`.
- **Relación con PCA:** si `X` está centrada por columnas, los componentes principales son las
  columnas de `V` y la varianza explicada por el componente `i` es `σᵢ² / (n − 1)`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `A` | La matriz de datos, cuadrada o no, de tamaño `m × n` | las de los datos | No cambia el método, pero sí el coste: la SVD completa es del orden de `m·n²` operaciones, y con matrices grandes conviene usar una versión truncada |
| `σᵢ` | Los valores singulares, ordenados de mayor a menor | las de los datos | Nunca son negativos. Al tirar los pequeños se pierde poca energía; si el segundo valor es casi tan grande como el primero, truncar es tirar señal, no ruido |
| `U` | Los vectores singulares por la izquierda (`m × m`) | adimensionales | Son las direcciones del espacio de salida: cuantos más conserves, más columnas de `U` guardas (`m × k`) |
| `V` | Los vectores singulares por la derecha (`n × n`) | adimensionales | Son las direcciones del espacio de entrada, y en una matriz de datos centrada son los componentes principales |
| `r` | El rango: cuántos valores singulares son distintos de cero | adimensional | Es un dato de la matriz, no una decisión. Truncar por debajo de `r` da error; truncar por encima solo añade columnas inútiles |
| `k` | Cuántos valores singulares te quedas | adimensional | El error de reconstrucción solo baja, y el número de valores guardados es `k·(m + n + 1)` frente a `m·n`. El precio es información: con `k` pequeño se pierden las diferencias finas |
| `κ₂(A)` | El número de condición `σ_max / σ_min` | adimensional | Mide cuánto amplifica la matriz los errores: por encima de `10³` resolver un sistema con ella deja de ser fiable, aunque sea invertible |
:::

:::figura
fichero: svd-cuanto-pesa-cada-direccion
pie: A la izquierda, los valores singulares de una matriz 60×40 que se construyó con cuatro direcciones fuertes y ruido repartido por todas partes. Los cuatro primeros son diez veces mayores que el resto y el resto ya cae en picado: ese escalón es lo que hace posible truncar. A la derecha, el error relativo al quedarse con los primeros `k`: con `k = 1` solo entra el 39 % de la energía, pero el codo está en `k = 4`, que es el rango real de la señal, y ahí el error cae al 14 %. Si no hubiera escalón, cualquier corte tiraría señal en vez de ruido.
fuente: figuras/descomposicion-svd-1.py
:::

## Ejemplo

**Caso de rango 1 resuelto a mano.** `A = [[1, 2], [2, 4]]`. Sus filas son proporcionales, así
que el rango es 1 y solo hay un valor singular distinto de cero. El candidato natural es
`σ₁ = 5`, con `u₁ = (1, 2) / √5` y `v₁ = (1, 2) / √5`:

- `σ₁ u₁ v₁ᵀ = 5 · (1/5) · [[1, 2], [2, 4]] = [[1, 2], [2, 4]] = A`. Correcto.
- Por tanto `σ₁ = 5` y `σ₂ = 0`. Guardar la SVD truncada ocupa 2 + 1 + 2 = 5 números en lugar
  de 4: en este tamaño no compensa, pero el patrón es el que se explota a lo grande.
- **Ahorro real:** una matriz densa de `1000 × 1000` tiene 1.000.000 de números. Guardar 10
  componentes (`U: 1000×10`, `σ: 10`, `V: 10×1000`) son `1000·10 + 10 + 10·1000 = 20.010`
  números: un 2 % del original.
- **Caso exacto y truncado con una matriz de rango 2:** con

```
D = [ 1   2   3 ]
    [ 4   5   6 ]
    [ 7   8   9 ]
    [ 10  11  12 ]
```

  los valores singulares son `25,4624`, `1,2907` y `0`. Truncando en `k = 1` el error relativo
  es de `0,0506`; truncando en `k = 2` la reconstrucción es exacta (error `0`) porque el rango
  es 2. El tercer valor singular es cero, y ese cero es la firma de la dependencia lineal entre
  columnas.

## Código

```python verificable
import numpy as np

A = np.array([[1.0, 2.0], [2.0, 4.0]])   # rango 1: la 2.a fila es el doble de la 1.a
U, s, Vt = np.linalg.svd(A)

print("valores singulares:", np.round(s, 6).tolist())                  # -> [5.0, 0.0]
print("rango:", int(np.linalg.matrix_rank(A)))                         # -> 1
print("reconstruccion:", np.round(U @ np.diag(s) @ Vt, 6).tolist())    # -> [[1.0, 2.0], [2.0, 4.0]]

# La aproximacion de rango 1 es exacta: sigma1 * u1 * v1^T reconstruye toda la matriz.
print("aproximacion rango 1:", np.round(s[0] * np.outer(U[:, 0], Vt[0, :]), 6).tolist())   # -> [[1.0, 2.0], [2.0, 4.0]]
```

```python verificable
import numpy as np

# Matriz 4x3 de rango 2: truncar en k=2 la reconstruye exactamente.
D = np.array([[1.0, 2.0, 3.0],
              [4.0, 5.0, 6.0],
              [7.0, 8.0, 9.0],
              [10.0, 11.0, 12.0]])
U, s, Vt = np.linalg.svd(D, full_matrices=False)

print("valores singulares:", np.round(s, 4).tolist())   # -> [25.4624, 1.2907, 0.0]
print("rango:", int(np.linalg.matrix_rank(D)))          # -> 2

D1 = U[:, :1] @ np.diag(s[:1]) @ Vt[:1, :]
D2 = U[:, :2] @ np.diag(s[:2]) @ Vt[:2, :]
print("k=1 error relativo:", round(float(np.linalg.norm(D - D1) / np.linalg.norm(D)), 4))   # -> 0.0506
print("k=2 error relativo:", round(float(np.linalg.norm(D - D2) / np.linalg.norm(D)), 4))   # -> 0.0

# Coste de guardar una matriz grande truncada frente a guardarla entera.
print("numeros con k=10 en 1000x1000:", 1000 * 10 + 10 + 1000 * 10, "de", 1000 * 1000)   # -> 20010 de 1000000
```

:::claves
- `np.linalg.svd` devuelve **tres** cosas y la segunda no es una matriz diagonal, sino un **vector** con los valores singulares. Para reconstruir hay que fabricar la diagonal: `np.diag(s)`. Escribir `U @ s @ Vt` falla por formas incompatibles.
- Por defecto `full_matrices=True`, que devuelve `U` de `m × m` y `Vt` de `n × n` aunque la matriz tenga rango 2. Con `full_matrices=False` se queda solo con las `r` columnas que aportan, y entonces `U[:, :k]` corta justo lo que quieres.
- `s` viene **ordenado de mayor a menor** (ese es el regalo de esta función; `eig` no ordena nada). Pero el orden se decide por el cálculo, no por ti: si dos valores singulares son casi iguales, el orden entre ellos puede variar de una ejecución a otra y en máquinas distintas.
- Si `D` tiene más filas que columnas, `np.linalg.norm(D - D1)` calcula la **norma de Frobenius** (la raíz de la suma de los cuadrados) sin avisar de qué norma es. Si cambiaras la forma de la matriz, el mismo código seguiría funcionando y devolvería otro número.
- El corte `U[:, :1] @ np.diag(s[:1]) @ Vt[:1, :]` da una matriz de `4 × 3` y no un número: los tres `[:1]` cortan **filas o columnas según la posición** del índice, y quitar el `:` de en medio cambia el resultado sin dar error.
- `s[0] * np.outer(U[:, 0], Vt[0, :])` reconstruye la matriz de rango 1 término a término. `np.outer` de dos vectores de longitud 2 y 2 da una matriz `2 × 2`, y es la forma de ver la SVD como suma de piezas: `A = σ₁u₁v₁ᵀ + σ₂u₂v₂ᵀ + …`.
:::

## Errores típicos

- **Confundir valores singulares con autovalores.** `σᵢ = √λᵢ(AᵀA)` y son siempre no negativos; los autovalores pueden ser negativos o complejos. Solo coinciden en las matrices simétricas semidefinidas positivas.
- **Creer que `U` y `V` son únicos.** El signo de cada vector singular es libre y, cuando un valor singular se repite, cualquier base ortonormal de ese subespacio vale. Dos librerías pueden dar resultados distintos y ambos correctos.
- **Llamar PCA directamente a la SVD de los datos sin centrar.** Sin restar la media, el primer componente apunta hacia el centro de la nube y no hacia la dirección de máxima varianza. La SVD de `X` no es [[pca|PCA]]; la de `X` centrada sí.
- **Interpretar los factores latentes como causas.** Que la SVD encuentre un patrón no significa que exista un mecanismo detrás. Los componentes son combinaciones matemáticas, no entidades del negocio.
- **Elegir `k` mirando solo el error de reconstrucción y olvidar el coste.** Un error bajo no garantiza mejores predicciones en la tarea que te importa: decide `k` validando la tarea final, con cuidado de no meter información de la prueba en la elección. Y la SVD completa de una matriz grande es cara; para matrices enormes se usan métodos truncados (SVD aleatorizada, Lanczos). Al truncar, además, `U_k` es `m × k`: no sigue siendo cuadrada.
- **Suponer que los valores singulares pequeños son siempre ruido.** Pueden ser señal débil pero real: en datos con variables casi dependientes, el valor singular diminuto es justo lo que explica la diferencia entre grupos.

:::practica
enunciado: La matriz M tiene columnas (4,6; 6,8; 7,6; 9,2) y (5,2; 8,1; 8,9; 10,4). Decide si basta una aproximación de rango 1 y cuántos números guardas frente a los 8 originales.
pista: Divide cada fila de la segunda columna entre la primera y mira si el cociente es casi el mismo en todas.
solucion: Cocientes: 5,2/4,6 = 1,130; 8,1/6,8 = 1,191; 8,9/7,6 = 1,171; 10,4/9,2 = 1,130. Se parecen mucho, así que la segunda columna es casi un múltiplo de la primera. Sus valores singulares son σ₁ ≈ 22,1305 y σ₂ ≈ 0,2442: el segundo es el 1,1 % del primero, por lo que M es casi de rango 1 y la aproximación truncada es buena. Guardando σ₁, los 4 valores de u₁ y el de v₁ son 6 números en lugar de 8, y con matrices grandes el ahorro se dispara.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué dice el teorema de Eckart-Young sobre la aproximación truncada de una SVD?
o: Que la matriz de rango k formada con los k valores singulares mayores es la mejor aproximación de rango k posible
o: Que cualquier truncamiento conserva exactamente la matriz original
o: Que hay que quedarse con los valores singulares más pequeños para no perder detalle
a: 1
e: Entre todas las matrices de rango como mucho k, la que minimiza el error frente a A (en norma de Frobenius y espectral) es la que se queda con los k valores singulares mayores. La reconstrucción es exacta solo si k alcanza el rango de A, y quedarse con los pequeños conserva el ruido, no el detalle.
:::

:::quiz
p: Una matriz de 1000 × 1000 tiene 1.000.000 de números. ¿Cuántos necesitas para guardar su aproximación con 10 valores singulares?
o: 1.000 · 10 + 10 + 10 · 1.000 = 20.010, alrededor del 2 % del original
o: 10.000, porque basta con los 10 valores singulares
o: 1.000.000, porque la SVD no comprime nada
a: 1
e: Hay que guardar 1000 × 10 números de U, los 10 valores singulares y 10 × 1000 números de V, que son 20.010. Los valores singulares solos no reconstruyen nada: hacen falta también sus vectores. Y la SVD no reduce el tamaño por sí misma, solo lo hace si truncas.
:::

:::trampa
Si tu primer valor singular es enorme y todos los demás son diminutos, la matriz es casi de
rango 1: eso puede ser información valiosa (una estructura fuerte) o un síntoma de que has
duplicado una columna o has dejado una variable que es suma de otras. Antes de celebrar la
compresión, mira si el patrón tiene sentido.
:::
