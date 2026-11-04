---
id: jacobiano-y-hessiano
titulo: Jacobiano y Hessiano
fase: 1
nivel: avanzado
rutas: [core, quant]
prerequisitos: [derivadas-parciales-y-gradiente, operaciones-matriciales]
tags: [calculo, matrices, optimizacion, curvatura]
resumen: El jacobiano agrupa las derivadas de una función vectorial y el hessiano las segundas derivadas: la curvatura que dice si un punto crítico es mínimo, maximo o silla.
fuentes: ["Stewart (2015), 'Calculus: Early Transcendentals'", "Nocedal y Wright (2006), 'Numerical Optimization'"]
---

## En una frase

El jacobiano es la matriz de todas las derivadas parciales de primer orden de una función
vectorial, y el hessiano es la matriz de las segundas derivadas de una función escalar: el
jacobiano dice cómo se estira el espacio y el hessiano dice hacia dónde se curva, que es lo que
necesitas para saber si un punto crítico es un mínimo, un máximo o una silla.

## La idea

El gradiente contesta a «¿hacia dónde subo?», pero se queda corto en dos situaciones muy
frecuentes.

La primera: cuando la función que quieres derivar devuelve **varios** números, no uno. Piensa en
un modelo que recibe 3 variables y produce 2 predicciones. ¿Cuál es «su derivada»? No hay un
número ni un vector: hay una matriz de 2 filas y 3 columnas, una entrada por cada pareja
(salida, entrada). Esa matriz es el jacobiano. Toda la retropropagación de una red neuronal es
una multiplicación de jacobianos, capa por capa: si la capa `k` transforma `n` entradas en `m`
salidas, su jacobiano es de `m × n`, y encadenarlas es multiplicar matrices.

La segunda: cuando ya has encontrado un punto donde el gradiente se anula y quieres saber qué
has encontrado. Un valle, una cima o un paso de montaña (un punto de silla) cumplen todos
`∇f = 0`. La primera derivada no distingue entre ellos. La segunda sí: en una dimensión, `f''>0`
es un mínimo, `f''<0` un máximo. En varias dimensiones la curvatura ya no es un número sino una
matriz, el **hessiano**, y hay que mirar si es definida positiva (todas las direcciones curvan
hacia arriba), definida negativa, o ninguna de las dos cosas (silla).

Esa distinción tiene consecuencias económicas en optimización: el método de Newton usa el
hessiano para dar pasos mucho más largos y seguros que el descenso de gradiente, pero construir
y resolver un sistema con el hessiano cuesta `O(n³)` y con millones de parámetros es inviable.
De ahí que existan los métodos cuasi-Newton, que estiman el hessiano sin calcularlo.

## Definición formal

**Jacobiano.** Sea `F: ℝⁿ → ℝᵐ`, con componentes `F(x) = (f₁(x), …, f_m(x))`. Su jacobiano en
`x` es la matriz `m × n`:

:::formula
J_F(x)ᵢⱼ = ∂fᵢ/∂xⱼ
:::

- `fᵢ` — la i-ésima función componente de `F` (una salida).
- `xⱼ` — la j-ésima variable de entrada.
- `J_F` — matriz de `m` filas (una por salida) y `n` columnas (una por entrada); la fila `i` es
  el gradiente traspuesto de `fᵢ`.

El jacobiano es la mejor aproximación lineal de `F` cerca de `x`: `F(x + h) ≈ F(x) + J_F(x)·h`,
y ahí `J_F(x)·h` es un producto matriz-vector.

**Hessiano.** Sea `f: ℝⁿ → ℝ` con segundas derivadas parciales continuas. Su hessiano en `x` es
la matriz `n × n`:

:::formula
H_f(x)ᵢⱼ = ∂²f / (∂xᵢ ∂xⱼ)
:::

- `∂²f/(∂xᵢ ∂xⱼ)` — derivada parcial de `∂f/∂xⱼ` respecto de `xᵢ`; es la segunda derivada
  cruzada.
- **Teorema de Schwarz:** si las segundas derivadas son continuas, el orden no importa
  (`∂²f/∂xᵢ∂xⱼ = ∂²f/∂xⱼ∂xᵢ`) y `H` es **simétrica**. Comprobar la simetría es la mejor forma de
  detectar un error de cálculo.
- El hessiano es el jacobiano del gradiente: `H_f = J_{∇f}`.

**Criterio de la segunda derivada.** Con `∇f(x*) = 0` y `H = H_f(x*)`:

- `H` definida positiva (todos los autovalores positivos, o todos los menores principales
  principales positivos) → `x*` es un **mínimo local estricto**.
- `H` definida negativa (todos los autovalores negativos) → `x*` es un **máximo local**.
- `H` indefinida (hay autovalores de los dos signos) → **punto de silla**.
- `H` semidefinida (algún autovalor nulo) → el criterio no decide; hay que mirar derivadas de
  orden superior.

En el caso de dos variables, `H = [[f_xx, f_xy], [f_xy, f_yy]]` y el criterio se reduce al
determinante `D = f_xx·f_yy − f_xy²`: si `D > 0` y `f_xx > 0`, mínimo; si `D > 0` y `f_xx < 0`,
máximo; si `D < 0`, silla.

:::figura
fichero: jacobiano-hessiano-curvatura
pie: Los dos dibujos de la izquierda tienen el mismo gradiente, cero, en el origen: la primera derivada es incapaz de distinguirlos. Lo que decide es el signo de los autovalores del hessiano, y con un autovalor de cada signo el punto es una silla, no un mínimo. La matriz de la derecha enseña el atajo: en un punto crítico, con `f_xx > 0` y el determinante positivo ya tienes mínimo local, sin calcular autovalores.
fuente: figuras/jacobiano-y-hessiano-1.py
:::

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `F` | La función vectorial: recibe `n` números y devuelve `m` | las de las salidas | Al crecer `m`, el jacobiano gana filas: cada salida anade su propio gradiente |
| `J_F(x)` | Jacobiano de `F` en `x`: matriz `m × n` | unidades de salida por unidad de entrada | No es un número ni un vector: no existe «la derivada» de una función vectorial |
| `fᵢ` | La i-esima salida de `F` | las de esa salida | Un cambio en una sola salida cambia una sola fila del jacobiano |
| `xⱼ` | La j-esima variable de entrada | las de la entrada | Mas entradas son mas columnas; confundir filas y columnas rompe el encadenado de capas |
| `H_f(x)` | Hessiano: matriz `n × n` de segundas derivadas | unidades de `f` por unidad de variable al cuadrado | Con `n` parámetros ocupa `n²`: con un millon de pesos no cabe en memoria |
| `∂²f/(∂xᵢ ∂xⱼ)` | Segunda derivada cruzada | las de las segundas derivadas | Si la matriz no sale simetrica, hay un error de derivada, no una rareza matemática |
| `D` | Determinante del hessiano en dos variables | unidades de curvatura al cuadrado | Si es negativo, el punto es silla; si vale cero, el criterio no decide y hay que mirar la función |
| `h` | Paso de la diferencia finita en el calculo numérico | las de las variables | Bajar de `1e-7` lo estropea: al dividir por `h²` el error de redondeo se amplifica |
:::

## Ejemplo

Sea `f(x, y) = 3x²y + y³`.

**Primeras derivadas:** `f_x = 6xy`, `f_y = 3x² + 3y²`. El gradiente se anula si `6xy = 0` y
`3x² + 3y² = 0`; la segunda ecuación obliga a `x = y = 0`. Hay un único punto crítico, el
origen.

**Segundas derivadas:** `f_xx = 6y`, `f_yy = 6y`, `f_xy = 6x`. El hessiano es simétrico:

:::formula
H_f(x, y) = [ [6y, 6x], [6x, 6y] ]
:::

En `(1, 2)`: `H = [[12, 6], [6, 12]]`. Los menores principales son `12 > 0` y
`12·12 − 6·6 = 144 − 36 = 108 > 0`, así que `H` es definida positiva: allí la función se curva
hacia arriba en todas las direcciones. Pero eso **no** convierte a `(1, 2)` en un mínimo, porque
el gradiente no se anula: `∇f(1, 2) = (12, 15)`. El criterio solo se aplica sobre puntos
críticos, y `(1, 2)` no lo es: la función vale `12,86` en `(0,9; 2)` y `15,26` en `(1,1; 2)`, así
que baja hacia un lado y sube hacia el otro. El hessiano describe la curvatura en ese punto, no
los extremos.

En `(0, 0)`: `H = [[0, 0], [0, 0]]`, semidefinida. El criterio no decide. Y de hecho el origen no
es ni mínimo ni máximo: a lo largo de `y = 0` la función vale `0`, mientras que con `x = y = 0,1`
vale `3·0,01·0,1 + 0,001 = 0,004 > 0` y con `(0,1; −0,1)` vale `−0,003 + (−0,001) = −0,004 < 0`. En
unas direcciones sube y en otras baja: es una silla degenerada, y la única forma de verlo es
mirar la función, no el hessiano.

**Jacobiano de una red de una capa.** Con entrada `x ∈ ℝ³`, pesos `W` de `2 × 3` y salida
`F(x) = W·x`, el jacobiano es exactamente `W`: cada fila es el gradiente de una salida y las
derivadas son los propios pesos. Si además se aplica una activación elemento a elemento `σ`, el
jacobiano de `σ(Wx)` es `diag(σ'(Wx)) · W`.

## Código

```python verificable
import numpy as np

# f(x, y) = 3x^2*y + y^3 : hessiano analítico y comprobación numérica por diferencias.
# El punto (1, 2) NO es crítico (su gradiente es (12, 15)), así que este hessiano mide la
# curvatura en ese punto: para hablar de mínimos hay que evaluarlo donde el gradiente se anule.
def f(v):
    x, y = v
    return 3 * x**2 * y + y**3

def hessiano_numerico(v, h=1e-4):
    x, y = v
    fxx = (f([x + h, y]) - 2 * f([x, y]) + f([x - h, y])) / h**2
    fyy = (f([x, y + h]) - 2 * f([x, y]) + f([x, y - h])) / h**2
    fxy = (f([x + h, y + h]) - f([x + h, y - h]) - f([x - h, y + h]) + f([x - h, y - h])) / (4 * h**2)
    return np.array([[fxx, fxy], [fxy, fyy]])

H = hessiano_numerico([1.0, 2.0])
print("hessiano en (1,2)  ", np.round(H, 3).tolist())          # salida: [[12.0, 6.0], [6.0, 12.0]]
print("autovalores        ", np.round(np.linalg.eigvalsh(H), 3))  # salida: [ 6. 18.]
print("menores principales", round(H[0, 0], 3), round(float(np.linalg.det(H)), 3))  # salida: 12.0 108.0
```

:::claves
- `def hessiano_numerico(v, h=1e-4)` recibe una **lista** `[1.0, 2.0]`, y dentro la descompone con `x, y = v`. Pasarle una tupla funciona igual; pasarle dos números sueltos, no.
- Cada diferencia dividida usa un denominador distinto: las segundas puras dividen por `h**2` y la cruzada por `4 * h**2`. Ese 4 no es decorativo: si lo quitas, `f_xy` sale al doble y la matriz deja de ser simetrica.
- El paso `h = 1e-4` no es un capricho. Con `h = 1e-8` el hessiano numérico sale `[[0.0, 4.441], [4.441, 0.0]]`: la resta de cuatro números casi iguales se come los digitos significativos y al dividir por `h**2` el ruido se multiplica por `10¹⁶`.
- `np.linalg.eigvalsh` es solo para matrices **simetricas** y devuelve los autovalores **ordenados de menor a mayor**: por eso la salida es `[6, 18]` y no `[18, 6]`. Con una matriz no simetrica hay que usar `np.linalg.eigvals`, que devuelve números complejos.
- `np.round(H, 3).tolist()` devuelve una lista de listas de `float` de Python, lista para imprimir. Sin `.tolist()` verias `[[12. 6.] [ 6. 12.]]`, que se lee mucho peor aunque sea el mismo contenido.
- `np.round` devuelve una **copia**, no redondea `H` en el sitio. Si después comparas `H` con la matriz analítica, sigue teniendo los valores sin redondear y la comparación debe hacerse con tolerancia.
:::

```python verificable
import numpy as np

# Punto de silla: el hessiano indefinido lo delata aunque el gradiente sea cero.
g = lambda x, y: x**2 - y**2          # silla clásica en el origen
H_silla = np.array([[2.0, 0.0], [0.0, -2.0]])

print("gradiente en (0,0):", [0.0, 0.0])                       # salida: [0.0, 0.0]
print("autovalores silla :", np.linalg.eigvalsh(H_silla))      # salida: [-2.  2.]
print("signos distintos  :", bool(np.any(np.linalg.eigvalsh(H_silla) > 0) and np.any(np.linalg.eigvalsh(H_silla) < 0)))  # salida: True

# La misma silla vista en los valores de la función alrededor del origen
print("punto", (0.1, 0.0), "-> f =", round(g(0.1, 0.0), 4))   # salida: punto (0.1, 0.0) -> f = 0.01
print("punto", (0.0, 0.1), "-> f =", round(g(0.0, 0.1), 4))   # salida: punto (0.0, 0.1) -> f = -0.01
```

## Errores típicos

- **Confundir las dimensiones del jacobiano.** Con `F: ℝⁿ → ℝᵐ` el jacobiano es `m × n`, no
  `n × m`. Si te sale al revés, la multiplicación de jacobianos en cadena no cuadrará de
  dimensiones. Regla mnemotécnica: filas = salidas, columnas = entradas.
- **Calcular el hessiano y no comprobar la simetría.** Si `H` no es simétrica (salvo errores de
  redondeo), hay un error de derivada. Es la comprobación más barata que existe y casi nadie la
  hace.
- **Aplicar el criterio del determinante con `D = 0`.** Con `D = 0` el criterio de la segunda
  derivada no decide nada: hay que analizar la función (o usar derivadas de orden superior). Dar
  por hecho que es una silla es un error tan grave como darlo por mínimo.
- **Creer que el hessiano numérico con `h` muy pequeño es más exacto.** Las segundas diferencias
  dividen por `h²`, así que el error de redondeo se amplifica: con `h = 1e-8` en doble precisión
  el resultado es basura. Usa `h` del orden de `1e-4`.
- **Usar el hessiano en optimización con muchos parámetros como si fuera gratis.** Es `n × n`:
  con un millón de parámetros son 10¹² entradas, imposible de almacenar. De ahí que se use el
  hessiano solo en problemas pequeños, o que se sustituya por una aproximación barata: L-BFGS,
  que estima la curvatura con los gradientes que ya iba calculando, o el reescalado por
  componente de Adam, que estima la **escala** del gradiente y no la curvatura.
- **Suponer que definida positiva = mínimo global.** El criterio da un mínimo **local**. Para
  garantizar el global hace falta [[convexidad|convexidad]] de la función en todo el dominio, y
  eso no lo dice el hessiano evaluado en un punto.

:::practica
enunciado: Para f(x, y) = 4x² + 4xy + 2y², escribe el gradiente y el hessiano, comprueba que el hessiano es simétrico y decide qué tipo de punto crítico es (0, 0). Comprueba la decisión con f(1, 0) y f(0, 1).
pista: El criterio en dos variables es el determinante f_xx · f_yy − f_xy².
solucion: f_x = 8x + 4y y f_y = 4x + 4y, que se anulan solo en (0, 0). Las segundas derivadas son f_xx = 8, f_yy = 4 y f_xy = 4, así que H = [[8, 4], [4, 4]] es simétrico. D = 8·4 − 4·4 = 16 > 0 y f_xx = 8 > 0, luego es un mínimo local. Se ve en los valores: f(1, 0) = 4 y f(0, 1) = 2, ambos mayores que f(0, 0) = 0.
:::

## Comprueba que lo sabes

:::quiz
p: Una función F va de ℝ⁴ a ℝ³. ¿Qué forma tiene su jacobiano?
o: 4 × 3
o: 3 × 4
o: 12 × 1
a: 2
e: Cada fila corresponde a una salida y cada columna a una entrada, así que es 3 × 4. El número de entradas es 3·4 = 12 pero no es una matriz de 12 filas: la aproximación lineal F(x+h) ≈ F(x) + J·h exige que J tenga 3 filas para que el resultado sea un vector de 3 componentes.
:::

:::quiz
p: En un punto crítico el hessiano tiene autovalores 4 y −1. ¿Qué es ese punto?
o: Un mínimo local
o: Un máximo local
o: Un punto de silla
a: 3
e: Hay direcciones que curvan hacia arriba (autovalor 4) y direcciones que curvan hacia abajo (autovalor −1): por eso es indefinido y el punto es una silla. Para mínimo todos los autovalores deben ser positivos, y para máximo todos negativos.
:::

:::quiz
p: ¿Para qué sirve el hessiano en el método de Newton que no basta con el gradiente?
o: Para dar en cuenta de la curvatura y dar pasos más largos y fiables hacia el óptimo
o: Para garantizar que la función es convexa
o: Para calcular el valor de la función sin evaluarla
a: 1
e: El gradiente da la dirección de descenso, pero no cuánto avanzar. El hessiano corrige el paso según la curvatura: x_nuevo = x − H⁻¹∇f. No demuestra convexidad y tampoco evita evaluar la función, solo cambia el tamaño y la forma del paso.
:::

:::aviso
En machine learning casi nunca se construye el hessiano: con `n` parámetros ocupa `n²` y
resolver el sistema cuesta `O(n³)`. Se usan aproximaciones (diagonal, L-BFGS) o directamente
métodos de primer orden con momento. Saber qué es el hessiano sirve para entender *por qué* el
descenso de gradiente va lento en valles estrechos, no para calcularlo.
:::
