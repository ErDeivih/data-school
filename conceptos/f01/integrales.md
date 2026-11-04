---
id: integrales
titulo: Integrales
fase: 1
nivel: intermedio
rutas: [core, ds]
prerequisitos: [limites-y-continuidad, derivadas-y-reglas]
tags: [calculo, areas, esperanza]
resumen: Acumular áreas infinitesimales: la integral es la operación inversa de derivar y el motivo de que casi toda probabilidad se calcule integrando.
fuentes: ["Stewart (2015), 'Calculus: Early Transcendentals'"]
---

## En una frase

Una integral acumula infinitas contribuciones infinitesimales: es el área bajo una curva, la
operación inversa de derivar, y la razón de que la esperanza, la varianza y cualquier
probabilidad de una variable continua se calculen integrando.

## La idea

Piensa en un coche que se mueve a velocidad variable. El velocímetro te dice a cuánto va en
cada instante, pero no cuántos kilómetros ha recorrido. Para recuperar la distancia total
tienes que **acumular** la velocidad: durante un trozo pequeño de tiempo, la distancia es
velocidad × tiempo; si sumas esos trocitos y los haces cada vez más pequeños, obtienes la
distancia exacta. Eso es una integral.

La analogía con los datos es directa: la función de densidad de una variable aleatoria continua
es como un velocímetro de la probabilidad (te dice dónde es densa la probabilidad, pero no
cuánta hay en un intervalo) y la probabilidad de un suceso es el área bajo esa densidad. Por eso
la probabilidad de que una variable continua valga *exactamente* un número es cero: no hay área
bajo un punto. Y por eso `P(X ≤ 3)` se escribe como una integral y no como una suma: hay
infinitos valores posibles, y entre ellos la probabilidad está repartida de forma continua.

El segundo papel de la integral es el inverso del primero: el **teorema fundamental del cálculo**
dice que derivar y acumular se deshacen mutuamente. Si `F` mide lo acumulado por `f`, entonces
`F' = f`. Eso convierte calcular áreas en buscar una primitiva, y de ahí salen las tablas de
integrales que se usan en todas las distribuciones de probabilidad.

## Definición formal

La **integral definida** de `f` entre `a` y `b` es el límite de las sumas de Riemann:

:::formula
∫ₐᵇ f(x) dx = lím_{n→∞} Σᵢ₌₁ⁿ f(xᵢ) · Δx
:::

- `f` — integrando, la función que se acumula.
- `a`, `b` — límites de integración inferior y superior.
- `dx` — ancho infinitesimal de cada trozo; `Δx = (b − a)/n` es el ancho de cada rectángulo.
- `xᵢ` — un punto del i-ésimo subintervalo.
- `∫` — símbolo de integral, una ese alargada que recuerda a «suma».
- `Σ` — suma finita de `n` términos, que se convierte en integral cuando `n → ∞`.

:::figura
fichero: integrales-suma-de-riemann
pie: En el panel de arriba hay ocho rectángulos y se ve el escalón: el área que falta es el hueco entre la curva y las barras. En el de abajo hay cuarenta y la suma ya no se distingue del área exacta. La conclusión no es «cuantos más, mejor» sin más, sino que el error depende del tamaño del trozo: al partir el intervalo en más piezas, cada una pesa menos.
fuente: figuras/integrales-1.py
:::

:::parametros
| Simbolo | Que es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `f` | Integrando: la función que se acumula | las de `f` | Si cambia de signo, el área con signo puede compensarse y salir un número enganoso |
| `a`, `b` | Limites de integración, inferior y superior | las de la variable | Ampliar el intervalo solo anade área; si `b` baja de `a`, el resultado cambia de signo |
| `dx` | Ancho infinitesimal de cada trozo | las de la variable | Es lo que convierte una suma en integral: sin el, `f(x)` no es un área |
| `Δx` | Ancho de cada rectangulo, `(b − a)/n` | las de la variable | Al bajar `n` crece, y con el crece el error; tiende a `dx` cuando `n` tiende a infinito |
| `n` | Numero de trozos de la suma de Riemann | adimensional | Mas trozos, mas exactitud y mas coste: el error de la regla del punto izquierdo baja como `1/n` |
| `F` | Primitiva de `f`, con `F' = f` | las de `f` por las de la variable | No es única: todas se diferencian en una constante que la resta `F(b) − F(a)` cancela |
| `p(x)` | Función de densidad de una variable continua | probabilidad por unidad de `x` | No es una probabilidad: puede valer mas de 1. Solo es probabilidad después de integrarla |
| `E[g(X)]` | Esperanza de la transformación `g(X)` | las de `g(X)` | Crece al crecer `g` y al concentrarse la densidad donde `g` es grande |
:::

**Teorema fundamental del cálculo.** Si `f` es continua en `[a, b]` y `F` es una primitiva suya
(es decir, `F' = f`), entonces:

:::formula
∫ₐᵇ f(x) dx = F(b) − F(a)
:::

- `F` — primitiva de `f`; no es única (todas se diferencian en una constante), pero la resta
  `F(b) − F(a)` cancela esa constante.

**Dos aplicaciones que se usan continuamente en estadística.** Para una variable aleatoria
continua `X` con función de densidad `p(x)`:

:::formula
P(a ≤ X ≤ b) = ∫ₐᵇ p(x) dx      E[g(X)] = ∫ g(x) · p(x) dx
:::

- `p(x)` — función de densidad de probabilidad; debe cumplir `p(x) ≥ 0` e integrar 1 en toda
  la recta, es decir `∫ p(x) dx = 1`.
- `E[g(X)]` — esperanza de la transformación `g(X)`. Con `g(x) = x` sale la media; con
  `g(x) = (x − μ)²` sale la varianza; con `g(x) = 1` sale 1, que es la condición de
  normalización.
- Las integrales se extienden a todo el dominio de `p`; si `p` es cero fuera de un intervalo,
  los límites se recortan a ese intervalo.

## Ejemplo

Sea `X` una variable aleatoria exponencial con tasa `λ = 2`, es decir `p(x) = 2e^{−2x}` para
`x ≥ 0` y `p(x) = 0` para `x < 0`.

**Esperanza.** `E[X] = ∫₀^∞ x · 2e^{−2x} dx`. Integrando por partes con `u = x` y `dv = 2e^{−2x}dx`:
`E[X] = [−x e^{−2x}]₀^∞ + ∫₀^∞ e^{−2x} dx = 0 + [−e^{−2x}/2]₀^∞ = 1/2`. Coincide con la
fórmula conocida `E[X] = 1/λ = 0,5`.

**Probabilidad de un intervalo.** `P(X > 1) = ∫₁^∞ 2e^{−2x} dx = [−e^{−2x}]₁^∞ = e^{−2} = 0,1353`.
Es decir, el 13,5 % de las observaciones superan 1.

**Normalización.** `∫₀^∞ 2e^{−2x} dx = [−e^{−2x}]₀^∞ = 1`. Toda densidad bien definida integra 1;
si tu cálculo no da 1, o la densidad está mal o los límites están mal.

## Código

```python verificable
import numpy as np

# Suma de Riemann: 2000 rectángulos para aproximar el área bajo p(x) = 2*exp(-2x) en [0, 5].
# Con esta rejilla el área sale 0.99996 en vez de 1: la integración numérica siempre tiene error.
x = np.linspace(0, 5, 2001)
y = 2 * np.exp(-2 * x)
area = np.trapezoid(y, x)          # regla de los trapecios sobre una rejilla fina

print("area bajo la densidad ", round(float(area), 5))   # salida: 0.99996
print("P(X > 1) por area    ", round(1 - float(np.trapezoid(y[x <= 1], x[x <= 1])), 6))  # salida: 0.135333
```

:::claves
- El área exacta entre 0 y 5 no es 1: es `1 − e⁻¹⁰ = 0,9999546`. La integral de una densidad vale 1 solo sobre el dominio completo, que aquí llega hasta infinito. Dividir el intervalo en 2000 trozos es lo que deja el error en `5·10⁻⁵`.
- El orden de los argumentos de `np.trapezoid` importa y **no da error si los cambias**: `np.trapezoid(y, x)` devuelve 0,99996, pero `np.trapezoid(x, y)` devuelve `−0,9995`. El primero es la integral de `y` respecto de `x`; el segundo, la de `x` respecto de `y`. Ningun aviso te lo dice.
- `x[x <= 1]` es una **condición booleana sobre el array**, no un bucle: devuelve los valores de `x` que cumplen la condición, y `y[x <= 1]` devuelve los de `y` en las mismas posiciones. Los dos arrays tienen que tener la misma longitud o el resultado es silenciosamente incorrecto.
- `x = np.linspace(0, 5, 2001)` crea 2001 puntos, es decir **2000 intervalos**, no 2001. Si quisieras 2000 intervalos de ancho 0,0025 exacto, ese es el número correcto; con 2000 puntos tendrias 1999 intervalos de ancho distinto.
- `np.trapezoid` se llamaba `np.trapz` hasta NumPy 2.0. Si copias código antiguo y te da `AttributeError`, ese es el motivo; y en una versión vieja, al reves.
- La función `p = lambda x: 2 * np.exp(-2 * x)` solo es una densidad para `x >= 0`. Integrada desde menos infinito no converge, y el resultado no te avisa: la densidad exponencial empieza en cero por definición, no por comodidad.
:::

```python verificable
from scipy import integrate
import numpy as np

# La integral de una densidad es la probabilidad, y E[X] se calcula pesando cada x por su densidad.
p = lambda x: 2 * np.exp(-2 * x)

esperanza, error = integrate.quad(lambda x: x * p(x), 0, np.inf)
prob_mayor_1, _ = integrate.quad(p, 1, np.inf)

print("E[X]      ", round(esperanza, 6), "+-", round(error, 2))   # salida: 0.5 +- 0.0
print("P(X > 1)  ", round(prob_mayor_1, 6))                        # salida: 0.135335
print("e elevado a -2:", round(np.exp(-2), 6))                     # salida: 0.135335
```

## Errores típicos

- **Confundir densidad con probabilidad.** `p(3) = 0,4` no significa «hay un 40 % de
  probabilidad en el punto 3»: una densidad puede valer más de 1 y la probabilidad de un punto
  concreto es cero. Lo que es probabilidad es el área, `p(x)·dx`.
- **Perder la constante de integración o los límites.** `∫ 2e^{−2x} dx = −e^{−2x} + C` es una
  familia de funciones; solo al evaluar entre `a` y `b` obtienes un número. Una probabilidad sin
  límites de integración no significa nada.
- **Integrar en el orden equivocado en dos variables.** En integrales dobles
  `∫∫ f(x, y) dy dx`, los límites internos pueden depender de `x`. Si intercambias el orden sin
  recalcular los límites, el resultado cambia. Cuando la región no es rectangular, dibújala.
- **Suponer que el área bajo una curva siempre es positiva.** El área **con signo** es negativa
  donde `f(x) < 0`; solo el área geométrica es positiva. Al integrar una función de densidad
  esto no importa (es no negativa por definición), pero al integrar errores o residuos sí.
- **Cambiar de variable y olvidar el jacobiano.** Al sustituir `x = g(u)` hay que multiplicar
  por `dx/du`. En probabilidad esto es justo lo que aparece al transformar una variable
  aleatoria: la densidad de `Y = g(X)` **no** es `p(g(y))`, lleva el factor del jacobiano.
- **Calcular `E[g(X)]` como `g(E[X])`.** La esperanza no conmuta con funciones no lineales:
  `E[X²]` no es `(E[X])²` (de hecho la diferencia entre ambas es la varianza). Hay que integrar
  `g(x)·p(x)`, no evaluar `g` en la media.

:::practica
enunciado: El tiempo entre llegadas de un servidor sigue una exponencial de tasa λ = 3, con densidad p(x) = 3e^{−3x}. Calcula P(2 < X < 3) y comprueba con la aritmética que la densidad está bien normalizada en [0, 3].
pista: La primitiva de 3e^{−3x} es −e^{−3x}: evalúa en los dos extremos y resta.
solucion: P(2 < X < 3) = [−e^{−3x}]₂³ = e^{−6} − e^{−9} = 0,002479 − 0,000123 = 0,002356, es decir un 0,24 %. La normalización en [0, 3] da [−e^{−3x}]₀³ = 1 − e^{−9} = 0,99988, que se acerca a 1 al ampliar el intervalo: la masa que falta es la cola que queda por encima de 3.
:::

## Comprueba que lo sabes

:::quiz
p: Para una variable aleatoria continua, ¿qué es P(X = 3) exactamente?
o: La densidad evaluada en 3, es decir p(3)
o: Cero, porque no hay área bajo un solo punto
o: Siempre 0,5, porque el punto divide la recta en dos
a: 2
e: La probabilidad es el área bajo la densidad, y un punto no tiene anchura: la integral de a a a vale cero. La densidad p(3) puede ser perfectamente 0,4 y no es una probabilidad; para obtener una probabilidad hay que integrar sobre un intervalo.
:::

:::quiz
p: ¿Por qué E[X²] no es igual a (E[X])² en general?
o: Porque la esperanza no conmuta con funciones no lineales: hay que integrar x²·p(x), no elevar al cuadrado la media
o: Porque la esperanza solo existe para variables discretas
o: Porque (E[X])² siempre es mayor que E[X²]
a: 1
e: La esperanza de una transformación es la integral de esa transformación pesada por la densidad. Elevar la media al cuadrado es evaluar la función en la media, que solo coincide si la función es lineal. La diferencia entre ambos números es exactamente la varianza, y como la varianza no es negativa, E[X²] es mayor o igual que (E[X])².
:::

:::quiz
p: Integras una densidad bien construida en todo su dominio y obtienes 0,8. ¿Qué concluyes?
o: Que la variable tiene un 20 % de probabilidad de ser infinita
o: Que la densidad está mal definida o los límites de integración se han recortado
o: Que hay que sumar 1 a la densidad para arreglarlo
a: 2
e: Toda función de densidad integra exactamente 1 sobre todo el dominio. Un 0,8 significa que falta masa de probabilidad: o la constante de normalización esta mal, o el soporte de la variable no es el que has usado como límite.
:::
