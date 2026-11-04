---
id: determinante-rango-invertibilidad
titulo: Determinante, rango e inversa
fase: 1
nivel: intermedio
rutas: [core, ds, quant]
prerequisitos: [operaciones-matriciales]
tags: [algebra-lineal, matrices, sistemas, multicolinealidad]
resumen: El determinante mide cuánto deforma una matriz; si vale cero, sus columnas son dependientes, el rango baja y la inversa no existe.
fuentes: ["Strang (2016), 'Introduction to Linear Algebra'", "Trefethen y Bau (1997), 'Numerical Linear Algebra'"]
---

## En una frase

El **determinante** es un número que resume cómo deforma la matriz al espacio: si vale cero,
la matriz aplasta alguna dirección, sus columnas son **dependientes**, el **rango** baja y la
**inversa** no existe, así que el sistema `Ax = b` no tiene solución única.

## La idea

Un sistema de ecuaciones es una pregunta: ¿qué valores de `x` hacen que `Ax` sea exactamente
`b`? Si `A` es invertible, la respuesta es una y solo una, `x = A⁻¹b`. Si no lo es, puede
pasar que haya infinitas respuestas o ninguna, y el determinante es el chivato que te avisa
antes de intentarlo.

Piensa en dos ecuaciones con dos incógnitas. Cada ecuación es una recta en el plano: la
solución es donde se cruzan. Si las rectas están en posición general, se cruzan en un punto y
el determinante es distinto de cero. Si son **paralelas**, no se cruzan y no hay solución. Si
son **la misma recta**, hay infinitos puntos. Los dos últimos casos son la misma enfermedad
vista desde fuera: las filas (o las columnas) son proporcionales, la información está
duplicada y la matriz es **singular**.

En datos, esto no es una curiosidad teórica. Si construyes una matriz de variables para una
regresión y una columna es copia exacta de otra (o la suma de otras dos), el sistema no tiene
solución única: hay infinitas combinaciones de coeficientes que predicen igual de bien. Los
programas lo resuelven como pueden y te devuelven números enormes y sin sentido. Y hay una
versión más traicionera: la **casi** dependencia. Dos variables muy correlacionadas no rompen
el rango, pero dejan la matriz **mal condicionada**: el resultado cambia muchísimo con un
error mínimo en los datos.

:::figura
fichero: determinante-area-y-casi-singular
pie: El determinante se ve como el factor por el que la matriz multiplica áreas: 5 en la primera matriz, 0 en la singular (el cuadrado se aplasta sobre una recta) y 0,0001 en la casi singular, que a ojo es idéntica a la anterior. Abajo a la derecha está lo importante al trabajar con datos: mover un dato una diezmilésima cambia la solución, así que «invertible» no significa «fiable».
fuente: figuras/determinante-rango-invertibilidad-1.py
:::

## Definición formal

- **Determinante** de una matriz cuadrada `A ∈ ℝ^{n×n}`: se nota `det(A)`. Para `2 × 2`,
  `det([[a, b], [c, d]]) = a·d − b·c`. Geométricamente, es el factor por el que la matriz
  multiplica áreas (o volúmenes) y su signo indica si invierte la orientación. Propiedades:
  `det(AB) = det(A)·det(B)`, `det(Aᵀ) = det(A)` y `det(A) = 0` si dos filas o dos columnas son
  proporcionales.
- **Dependencia lineal:** las columnas `a₁, …, aₙ` son dependientes si existen coeficientes
  `c₁, …, cₙ`, no todos cero, con `c₁a₁ + … + cₙaₙ = 0`. Si el único modo de conseguirlo es
  `c₁ = … = cₙ = 0`, son **independientes**.
- **Rango:** el número máximo de columnas (o filas) independientes; coincide con la dimensión
  del espacio que generan las columnas. Cumple `rango(A) ≤ min(m, n)`. Si `A` es `n × n` y
  `rango(A) = n`, se dice que tiene **rango completo**.
- **Inversa:** `A⁻¹` es la única matriz con `A A⁻¹ = A⁻¹ A = I`. Existe si y solo si
  `det(A) ≠ 0`, que es equivalente a `rango(A) = n`. Para `2 × 2`:
  `A⁻¹ = (1/det(A)) · [[d, −b], [−c, a]]`.
- **Sistema `Ax = b`:** tiene solución única si `rango(A) = n`; infinitas soluciones si
  `rango(A) = rango(A ampliada con b) < n`; ninguna si `rango(A) < rango(A ampliada con b)`.
- **Número de condición:** `κ(A) = σ_max / σ_min`, el cociente entre el mayor y el menor
  [[descomposicion-svd|valor singular]]. Vale 1 en la mejor de las matrices y crece sin límite
  cuando la matriz se acerca a singular.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `A ∈ ℝ^{n×n}` | Una matriz cuadrada | las de los datos | si deja de ser cuadrada no hay determinante ni inversa, pero sí puede haber rango completo |
| `det(A)` | El factor por el que `A` multiplica áreas (o volúmenes) | las de los datos elevadas a `n` | cuanto mayor es en valor absoluto, más deforma; al acercarse a 0 la matriz se vuelve singular y la inversa, inestable. El signo solo dice si invierte la orientación |
| `a_ij` | El elemento de la fila `i` y la columna `j` | las de la variable `j` | es la palanca de todo lo demás: un cambio minúsculo aquí mueve `det`, el rango y la solución |
| `c₁ … cₙ` | Coeficientes de una combinación de las columnas | adimensionales | si existe una combinación con no todos cero que da el vector cero, las columnas son dependientes y el rango baja |
| `rango(A)` | Cuántas columnas (o filas) independientes hay | entero, como mucho `min(m, n)` | al llegar a `n` la matriz tiene rango completo y el sistema tiene solución única; al bajar, aparecen infinitas soluciones o ninguna |
| `A⁻¹` | La matriz inversa | 1/unidades de los datos | existe solo si `det(A) ≠ 0`. No es un objeto que «crezca»: o existe o no existe |
| `x`, `b` | La incógnita y el término independiente de `Ax = b` | las de los datos | cuanto más se aleja `b` de la imagen de `A`, más cerca está el sistema de no tener solución |
| `κ(A)` | El número de condición, `σ_max / σ_min` | adimensional, ≥ 1 | **es la columna que hay que mirar en datos**: al crecer, la solución se vuelve sensible a errores minúsculos. Por encima de 10³ ya conviene desconfiar |
| `σ_max`, `σ_min` | El mayor y el menor valor singular de `A` | las de los datos | si el menor se acerca a 0, `κ` se dispara aunque el determinante no sea exactamente cero |
:::

## Ejemplo

**Caso singular.** `A = [[1, 2], [2, 4]]`. La segunda columna es el doble de la primera.

- `det(A) = 1·4 − 2·2 = 0` → matriz singular, `rango(A) = 1`, no hay inversa.
- Sistema `x + 2y = 3`, `2x + 4y = 7`: si multiplicas la primera ecuación por 2 obtienes
  `2x + 4y = 6`, que contradice la segunda. **Ninguna solución.**
- Sistema `x + 2y = 3`, `2x + 4y = 6`: la segunda es la primera multiplicada por 2. Son la
  misma recta: **infinitas soluciones**, todas las de la forma `(3 − 2y, y)`.

**Caso invertible.** `B = [[2, 1], [1, 3]]`.

- `det(B) = 2·3 − 1·1 = 5 ≠ 0` → `rango = 2`, invertible.
- `B⁻¹ = (1/5)·[[3, −1], [−1, 2]]`.
- Con `b = (5, 10)`: `x = (3·5 − 1·10)/5 = 1` e `y = (−1·5 + 2·10)/5 = 3`. Comprobación:
  `2·1 + 3 = 5` y `1 + 3·3 = 10`. Correcto.

**Casi singular.** `C = [[1, 2], [2, 4,0001]]`: `det(C) = 0,0001 ≠ 0`, así que es invertible
y el sistema tiene solución única. Pero su número de condición es aproximadamente `2,5 · 10⁵`:
un error de `10⁻⁶` en un dato puede mover la solución en un orden de magnitud. Invertible no
significa fiable.

## Código

```python verificable
import numpy as np

A = np.array([[1.0, 2.0], [2.0, 4.0]])   # la 2.a columna es el doble de la 1.a

print("det(A):", round(float(np.linalg.det(A)), 6))   # -> 0.0
print("rango(A):", np.linalg.matrix_rank(A))          # -> 1

try:
    np.linalg.inv(A)
except np.linalg.LinAlgError:
    print("inv(A): singular, no existe")              # -> inv(A): singular, no existe

# Un determinante diminuto no es cero: invertible, pero numericamente inestable.
C = np.array([[1.0, 2.0], [2.0, 4.0001]])
print("det(C):", round(float(np.linalg.det(C)), 6))   # -> 0.0001
print("cond(C):", f"{np.linalg.cond(C):.3e}")         # -> 2.500e+05
```

:::claves
- `np.linalg.det(A)` devuelve siempre un `float64`, aunque `A` sea entera. En una singular exacta sale `0.0`, pero en cuanto los datos vengan de medidas saldrá algo como `1e-17`: comparar `det(A) == 0` casi nunca es la comprobación correcta.
- `np.linalg.inv(A)` **no** devuelve `None` ni un array vacío cuando no hay inversa: lanza `np.linalg.LinAlgError`, una excepción distinta de `ValueError`. Si no la capturas, el programa se para en esa línea.
- `np.linalg.matrix_rank(A)` no cuenta filas: cuenta filas o columnas independientes usando una **tolerancia** interna. En coma flotante puede devolver 2 donde la teoría dice 1; cuando la respuesta importe, compara los valores singulares con el mayor de ellos.
- `np.linalg.solve(A, b)` evita construir `A⁻¹`, así que es más rápido y comete menos error de redondeo. No es un atajo de `inv(A) @ b`: es el camino recomendado, y falla igual si `A` es singular.
- `round(float(np.linalg.det(A)), 6)` hace dos cosas: `float(...)` convierte el escalar de NumPy en un `float` de Python y `round` redondea. Redondear está bien **para imprimir**; si sigues calculando con el valor redondeado, acumulas error.
- `f"{np.linalg.cond(C):.3e}"` es **formato de texto**, no un cálculo: devuelve una cadena `'2.500e+05'`. Un `if` sobre esa cadena compararía texto, no números; para decidir hay que usar el valor numérico.
:::

```python verificable
import numpy as np

A = np.array([[2.0, 1.0], [1.0, 3.0]])
b = np.array([5.0, 10.0])

print("det(A):", round(float(np.linalg.det(A)), 1))   # -> 5.0
print("rango(A):", np.linalg.matrix_rank(A))          # -> 2

# Resolver el sistema es mas estable que invertir la matriz y multiplicar.
x = np.linalg.solve(A, b)
print("solucion:", np.round(x, 6).tolist())           # -> [1.0, 3.0]
print("A @ x   :", (A @ x).tolist())                  # -> [5.0, 10.0]

# Duplicar una columna deja rango 1: el sistema pierde la solucion unica.
B = np.array([[2.0, 4.0], [1.0, 2.0]])
print("rango(B):", np.linalg.matrix_rank(B))          # -> 1
```

## Errores típicos

- **Invertir la matriz para resolver un sistema.** `np.linalg.inv(A) @ b` es más lento y menos estable que `np.linalg.solve(A, b)`, y si `A` es singular falla igual. Resuelve, no inviertas.
- **Mirar solo el determinante para decidir si hay solución.** `det(A) = 0` dice que no hay inversa, pero el sistema puede tener infinitas soluciones o ninguna; para distinguirlo hay que comparar el rango de `A` con el de la matriz ampliada con `b`.
- **Confundir «determinante pequeño» con «singular».** `det(C) = 0,0001` y `C` es invertible, pero con `κ ≈ 2,5 · 10⁵`. En la práctica eso significa que la solución no es de fiar. Mira el número de condición, no solo el determinante.
- **Creer que el rango es el número de filas.** Es el número de filas o columnas independientes, y nunca supera `min(m, n)`. Una matriz `200 × 5` tiene rango como mucho 5.
- **Pensar que dos variables correlacionadas son una dependencia exacta.** La correlación alta no rompe el rango, pero infla muchísimo la varianza de los coeficientes de una [[regresion-lineal|regresión]]. Duplicar una columna exactamente sí lo rompe, y ahí el ajuste ni siquiera tiene solución única.
- **Fiarse de que el ordenador detecta el rango exacto.** En coma flotante casi ninguna matriz es exactamente singular: `matrix_rank` usa una tolerancia y puede devolver 2 donde matemáticamente hay 1. Cuando sospeches, compara los [[descomposicion-svd|valores singulares]] con el mayor de ellos.

:::practica
enunciado: La matriz A = [[2, k], [1, 3]] contiene una columna que depende de k. ¿Para qué valor de k es singular? Con k = 1, resuelve Ax = (7, 4).
pista: En una 2 × 2 el determinante es a·d − b·c; el sistema es singular cuando vale cero.
solucion: det(A) = 2·3 − k·1 = 6 − k. Es singular si 6 − k = 0, es decir k = 6, y entonces la segunda fila es la mitad de la primera. Con k = 1: det = 5, y A⁻¹ = (1/5)·[[3, −1], [−1, 2]]. Por tanto x = (3·7 − 1·4)/5 = 17/5 = 3,4 e y = (−1·7 + 2·4)/5 = 1/5 = 0,2. Comprobación: 2·3,4 + 0,2 = 7. Hay solución única porque el determinante no es cero.
:::

## Comprueba que lo sabes

:::quiz
p: Con A = [[1, 2], [2, 4]], ¿qué afirmación es correcta?
o: det(A) = 0, rango 1 y la segunda columna es el doble de la primera
o: det(A) = 8, rango 2 e inversa [[4, −2], [−2, 1]]
o: det(A) = 0 y rango 2, así que el sistema siempre tiene solución única
a: 1
e: det = 1·4 − 2·2 = 0; las columnas son proporcionales, así que el rango baja a 1 y no hay inversa. Un sistema con rango 1 puede tener infinitas soluciones o ninguna, pero nunca una única solución.
:::

:::quiz
p: ¿Por qué es mejor resolver Ax = b con np.linalg.solve que con inv(A) @ b?
o: Porque el producto de una matriz por un vector no está definido
o: Porque resolver directamente es más rápido y comete menos error de redondeo, sobre todo si A está mal condicionada
o: Porque inv(A) solo existe cuando A es simétrica
a: 2
e: `solve` resuelve el sistema sin construir A⁻¹, que es un paso extra y una fuente de error cuando la matriz está mal condicionada. El producto matriz-vector sí está definido, y la inversa existe para cualquier matriz cuadrada con determinante distinto de cero, sea simétrica o no.
:::

:::aviso
Detectar la multicolinealidad mirando solo el determinante de la matriz de correlaciones no
basta. Dos variables con correlación 0,99 dan un determinante pequeño pero distinto de cero;
la señal de alarma real es el número de condición y, sobre todo, la varianza de los
coeficientes estimados.
:::
