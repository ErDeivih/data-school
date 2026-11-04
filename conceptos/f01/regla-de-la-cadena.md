---
id: regla-de-la-cadena
titulo: Regla de la cadena
fase: 1
nivel: intermedio
rutas: [core, ds]
prerequisitos: [derivadas-y-reglas, limites-y-continuidad]
tags: [calculo, derivadas, composicion]
resumen: Derivar una función compuesta es multiplicar las derivadas de sus piezas en orden, y eso es exactamente la retropropagación.
fuentes: ["Stewart (2015), 'Calculus: Early Transcendentals'"]
---

## En una frase

Si una cantidad depende de otra y esa otra depende de una tercera, la tasa de cambio total es
el producto de las tasas: la regla de la cadena dice que derivar una composición es multiplicar
las derivadas de sus piezas, en orden.

## La idea

Imagina una fábrica de tres pasos encadenados. El primer paso convierte kilos de materia prima
en piezas; el segundo convierte piezas en cajas; el tercero convierte cajas en euros. Si te
preguntas «¿cuántos euros gano por cada kilo extra de materia prima?», no necesitas medir esa
relación directamente: multiplicas los tres rendimientos. Si cada kilo da 4 piezas, cada 5
piezas dan una caja y cada caja se vende por 30 euros, entonces un kilo extra da
4 · (1/5) · 30 = 24 euros. Eso es la regla de la cadena: **los rendimientos se multiplican a lo
largo de la cadena**.

Una función compuesta es lo mismo. `f(g(x))` significa: aplica primero `g` a `x` y al resultado
aplícale `f`. Si `x` cambia un poco, `g(x)` cambia en proporción a `g'(x)`; si ese valor
intermedio cambia, `f` reacciona en proporción a `f'` evaluada ahí. El efecto total es el
producto. Y aquí está la razón de que este concepto sea el más importante del cálculo para
datos: una red neuronal no es más que una cadena larguísima de estas composiciones, y el
algoritmo que la entrena, la retropropagación, no es otra cosa que aplicar esta regla capa por
capa, de atrás hacia delante.

La trampa mental es que mucha gente escribe `(f∘g)' = f'·g'` y se olvida de **dónde se evalúa
cada factor**: `f'` se evalúa en `g(x)`, no en `x`. Ese detalle es la diferencia entre acertar y
fallar la mitad de los ejercicios.

## Definición formal

Si `g` es derivable en `x` y `f` es derivable en `g(x)`, entonces la composición `f∘g` es
derivable en `x` y:

:::formula
(f∘g)'(x) = f'(g(x)) · g'(x)
:::

- `f`, `g` — funciones derivables; `f∘g` es la función que a `x` le asigna `f(g(x))`.
- `g'(x)` — derivada de la función **interna**, evaluada en `x`.
- `f'(g(x))` — derivada de la función **externa**, evaluada en el valor intermedio `g(x)`.
- `·` — producto ordinario de números.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `f`, `g` | Las dos funciones que se componen | las de sus salidas | No son parámetros: son las piezas de la receta. El orden importa: `f∘g` y `g∘f` casi nunca dan lo mismo |
| `x` | El punto donde se evalúa la derivada | las de la entrada | Al moverlo cambia el resultado aunque las funciones sean las mismas: la derivada de `(3x + 1)⁴` vale 4116 en `x = 2` y 12 en `x = 0` |
| `g(x)` | El valor intermedio por el que pasa el cálculo | las de la salida de `g` | Es donde se evalúa la derivada externa. Confundirlo con `x` es el error que hace fallar la mitad de los ejercicios |
| `g'(x)` | La derivada de la interna, en `x` | salida de `g` por unidad de entrada | Es un factor **multiplicativo**: si vale 3, la pendiente total se triplica. Si vale 0, la pendiente total es 0 aunque la externa sea enorme |
| `f'(g(x))` | La derivada de la externa, evaluada en `g(x)` | salida por unidad de `g` | Es el otro factor. En cadenas largas, muchos factores menores que 1 dan un producto diminuto (gradiente que se desvanece); mayores que 1, un producto enorme |
| `n` | El número de etapas encadenadas | adimensional | El producto tiene `n` factores: solo el 60 % de ellos por encima de 1 ya basta para que el resultado crezca sin control |
:::

Con la notación de Leibniz, si `y = f(u)` y `u = g(x)`:

:::formula
dy/dx = (dy/du) · (du/dx)
:::

- `y` — variable de salida; `u` — variable intermedia; `x` — variable de entrada.
- `dy/du` — cuánto cambia `y` por unidad de cambio de `u`.
- `du/dx` — cuánto cambia `u` por unidad de cambio de `x`.

La forma se generaliza a cadenas de cualquier longitud: con `y = f₁(f₂(…f_n(x)))`, la derivada
es el producto de las `n` derivadas, cada una evaluada en su punto. También se generaliza a
varias variables; es la **regla de la cadena multivariante**:

:::formula
∂f/∂xⱼ = Σᵢ (∂f/∂uᵢ) · (∂uᵢ/∂xⱼ)
:::

- `uᵢ` — cada variable intermedia de la que depende `f`; `xⱼ` — cada variable de entrada.
- `Σᵢ` — suma sobre **todos** los caminos intermedios, no solo uno. Si una variable intermedia
  alimenta a la salida por dos rutas, las dos contribuciones se suman; olvidar una es el error
  clásico al derivar un grafo de cómputo con ramificaciones.

:::figura
fichero: cadena-multiplicar-pendientes
pie: A la izquierda, la primera etapa: `u = 3x + 1`. En un paso de una unidad de `x`, `u` sube 3, y ese 3 es la primera pendiente; el triángulo naranja lo dibuja. Multiplicado por la pendiente de la segunda etapa (`4u³` evaluada en `u = 7`) da 4116, la pendiente total. A la derecha está la consecuencia en una cadena larga: el producto de las pendientes es una potencia. Si cada etapa multiplica por 0,7, tras 20 etapas solo queda `8 · 10⁻⁴` y el gradiente de las primeras capas ya no mueve nada; si cada etapa multiplica por 1,4, el mismo producto explota. Ahí nacen los problemas de las redes profundas.
fuente: figuras/regla-de-la-cadena-1.py
:::

## Ejemplo

Sea `f(x) = (3x + 1)⁴`. Aquí `g(x) = 3x + 1` (interna) y `f(u) = u⁴` (externa).

- `g'(x) = 3`.
- `f'(u) = 4u³`, así que `f'(g(x)) = 4(3x + 1)³`.
- Por tanto `f'(x) = 4(3x + 1)³ · 3 = 12(3x + 1)³`.

En `x = 2`: `3x + 1 = 7`, y `f'(2) = 12 · 7³ = 12 · 343 = 4116`. Comprobación con el cociente
incremental: `f(2) = 7⁴ = 2401` y `f(2,001) = (7,003)⁴ = 2405,118…`, luego
`(2405,118 − 2401) / 0,001 ≈ 4118`, que se acerca a 4116 a medida que el paso encoge. Coincide.

Un segundo ejemplo, este más cercano a lo que se hace en un modelo: `L = (y − σ(wx + b))²`,
donde `x` es la entrada, `w` el peso, `b` el sesgo, `σ` la función sigmoide, `y` el valor
observado y `L` el error. Con `u = wx + b`, `p = σ(u)` y `L = (y − p)²`:

- `∂L/∂p = −2(y − p)`.
- `∂p/∂u = σ(u)·(1 − σ(u))`.
- `∂u/∂w = x`.

Multiplicando: `∂L/∂w = −2(y − p) · σ(u)(1 − σ(u)) · x`. Con `x = 1`, `w = 0`, `b = 0` e
`y = 1`: `σ(0) = 0,5`, luego `∂L/∂w = −2(1 − 0,5) · 0,25 · 1 = −0,25`. El gradiente apunta a
que aumentar `w` reduce el error, y la magnitud es 0,25 por unidad de peso.

## Código

```python verificable
import numpy as np

# f(x) = (3x + 1)**4. La regla de la cadena dice f'(x) = 12*(3x+1)**3.
def f(x):
    return (3 * x + 1) ** 4

def df_analitica(x):
    return 12 * (3 * x + 1) ** 3

def df_numerica(x, h=1e-6):
    return (f(x + h) - f(x - h)) / (2 * h)   # diferencia central: error O(h^2)

x = 2.0
print("analitica ", round(df_analitica(x), 4))    # salida: 4116.0
print("numerica  ", round(df_numerica(x), 4))     # salida: 4116.0

```

:::claves
- `def df_numerica(x, h=1e-6)` tiene un **valor por defecto** en `h`: se puede llamar con un solo argumento. El 1e-6 no es un capricho, es un equilibrio entre el error de la fórmula (que baja con `h`) y el redondeo de la resta (que sube cuando `h` es diminuto).
- La diferencia central `(f(x + h) - f(x - h)) / (2 * h)` usa **dos** evaluaciones por punto y el doble de precisión. La diferencia hacia delante del otro ejemplo usa una sola y da menos dígitos: el mismo concepto con distinto coste.
- `(3 * x + 1) ** 4` es una composición escrita como **una sola línea**: no hay una función interna que se pueda llamar por separado. Por eso `df_analitica` repite la expresión `(3 * x + 1) ** 3` en vez de reutilizarla; si se reescribe la fórmula y se olvida la derivada, el programa sigue funcionando y da un número equivocado sin avisar.
- En el ejemplo de retropropagación, las líneas `dL_dz2`, `dL_da1` y `dL_dz1` van **de la salida hacia la entrada**: cada una se calcula con la anterior. Si se reordena el bloque, aparecen `NameError` o, peor, se usan valores antiguos porque en Python las variables no se declaran.
- `a1 = sigmoide(z1)` se multiplica después, en `dL_dz1 = dL_da1 * a1 * (1 - a1)`, por la derivada de la sigmoide evaluada en su **salida**, no en `z1`. Ese `a1 * (1 - a1)` es la derivada escrita de forma compacta: si se sustituye por `z1 * (1 - z1)` el resultado cambia y nada avisa.
- `0.5 * (y - z2) ** 2` define el error, y la derivada que se usa después es `-(y - z2)`: el `0,5` y el `2` del cuadrado se cancelan. Si se cambiara el `0.5` por un `1`, habría que multiplicar todas las derivadas por 2 para que siguieran siendo correctas.
:::

```python verificable
import math

# La misma regla, hacia atrás: retropropagación en una red de dos capas.
# z1 = x*w1, a1 = sigmoide(z1), z2 = a1*w2, L = (y - z2)**2/2  (error cuadrático)
def sigmoide(u):
    return 1 / (1 + math.exp(-u))

x, y = 0.5, 1.0
w1, w2 = 0.8, -0.6

z1, a1, z2 = x * w1, None, None
a1 = sigmoide(z1)
z2 = a1 * w2
L = 0.5 * (y - z2) ** 2

# dL/dz2 -> dL/da1 -> dL/dz1 -> dL/dw1 : cada paso multiplica por la derivada local
dL_dz2 = -(y - z2)
dL_dw2 = dL_dz2 * a1
dL_da1 = dL_dz2 * w2
dL_dz1 = dL_da1 * a1 * (1 - a1)
dL_dw1 = dL_dz1 * x

print("L       ", round(L, 4))          # salida: 0.9237
print("dL/dw2  ", round(dL_dw2, 4))     # salida: -0.8137
print("dL/dw1  ", round(dL_dw1, 4))     # salida: 0.098
```

## Errores típicos

- **Olvidar la derivada de la función interna.** Es el error número uno: derivar `(3x+1)⁴` como
  `4(3x+1)³` y perder el factor 3. La regla de la cadena tiene dos factores; si solo escribes
  uno, la derivada está mal por un factor constante y el descenso de gradiente converge a
  distinta velocidad (o no converge).
- **Evaluar la derivada externa en `x` en vez de en `g(x)`.** `f'(g(x))` y `f'(x)` coinciden
  solo cuando `g(x) = x`. Con `f(u) = u⁴` y `g(x) = 3x+1`, usar `4x³` en vez de `4(3x+1)³` da
  un resultado sin sentido.
- **Tratar `dy/du · du/dx` como una cancelación de símbolos.** La notación de Leibniz sugiere
  que las `du` se cancelan, y con funciones de una variable el resultado es correcto, pero el
  razonamiento es falso: son límites, no fracciones. Confundirlo lleva a «cancelar» cosas que
  no se cancelan en el caso multivariante.
- **Sumar en vez de multiplicar en una cadena larga.** Con tres o más pasos encadenados la
  derivada es un producto de todos los factores locales. Si multiplicas por pasos con factores
  menores que 1, el gradiente se hace diminuto (**desvanecimiento del gradiente**); si son
  mayores que 1, explota. De ahí salen las funciones de activación y las normalizaciones de las
  redes profundas.
- **Perder una rama del grafo.** Cuando una variable intermedia alimenta a la salida por dos
  caminos distintos (por ejemplo, un término residual `x + h(x)`), hay que **sumar** las dos
  contribuciones. Derivar solo una rama es el error más frecuente al implementar
  retropropagación a mano.
- **Aplicar la regla a un producto creyendo que es una composición.** `f(x)·g(x)` se deriva con
  la regla del producto, no con la de la cadena. La cadena es para `f(g(x))`.

:::practica
enunciado: Deriva f(x) = (2x − 1)³ y evalúa la derivada en x = 3. Comprueba el resultado con el cociente incremental tomando f(3,001) − f(3) partido por 0,001.
pista: Es una composición: deriva la potencia y multiplica por la derivada de lo de dentro.
solucion: Con g(x) = 2x − 1 y u³ fuera, f'(x) = 3(2x − 1)² · 2 = 6(2x − 1)². En x = 3: 6 · 5² = 150. Comprobación: (5,002³ − 125)/0,001 = 0,15006/0,001 ≈ 150,06, que se acerca a 150 cuando el paso encoge.
:::

## Comprueba que lo sabes

:::quiz
p: Si h(x) = (3x + 1)⁴, ¿cuál es h'(2)?
o: 4 · 7³ = 1372
o: 12 · 7³ = 4116
o: 4 · 2³ · 3 = 96
a: 2
e: La derivada es 4(3x+1)³ multiplicada por la derivada interna, que es 3: queda 12(3x+1)³. En x = 2 vale 12 · 343 = 4116. La primera opción olvida el factor 3; la tercera evalúa la parte externa en x en vez de en 3x+1.
:::

:::quiz
p: ¿Por qué la regla de la cadena es «literalmente» la retropropagación de una red neuronal?
o: Porque una red es una composición de capas y la retropropagación multiplica las derivadas locales desde la salida hacia la entrada
o: Porque las redes neuronales solo usan funciones lineales
o: Porque la retropropagación ordena los datos antes de entrenar
a: 1
e: Cada capa es una función y la red entera es su composición. El gradiente del error respecto a un peso se obtiene multiplicando las derivadas locales de todas las capas que quedan por delante de ese peso. Eso es la regla de la cadena aplicada de atrás hacia delante, no una regla nueva.
:::

:::quiz
p: Una variable intermedia u alimenta la salida por dos caminos distintos. ¿Cómo entra eso en la derivada?
o: Se toma solo el camino más corto
o: Se multiplican los dos caminos
o: Se suman las contribuciones de los dos caminos
a: 3
e: En la regla de la cadena multivariante se suma sobre todos los caminos intermedios, porque las dos rutas aportan variación a la salida. Multiplicar los caminos describe el caso en serie; omitir uno de ellos da un gradiente incompleto, que es el fallo típico al programar retropropagación a mano.
:::

:::aviso
Si un producto de más de veinte derivadas locales menores que 1 no se te ocurre nada, mira
los valores: en una red profunda sin normalización el gradiente hacia las primeras capas se
vuelve tan pequeño que el entrenamiento se queda clavado. No es un bug de la regla de la
cadena, es la consecuencia aritmética de multiplicar muchos números pequeños.
:::
