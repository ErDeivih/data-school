---
id: distribuciones-continuas
titulo: Distribuciones continuas
fase: 1
nivel: intermedio
rutas: [core, ds]
prerequisitos: [variable-aleatoria, distribuciones-discretas, integrales]
tags: [probabilidad, distribuciones, normal]
resumen: Uniforme, normal, exponencial, t, chi-cuadrado, F, beta, gamma y lognormal: qué mecanismo modela cada una y cómo se relacionan entre sí.
fuentes: ["Casella y Berger (2002), 'Statistical Inference'", "DeGroot y Schervish (2012), 'Probability and Statistics'"]
---

## En una frase

En una distribución continua la probabilidad es área bajo una curva de densidad, y cada familia
(la normal, la exponencial, la t, la chi-cuadrado, la F, la beta, la gamma y la lognormal)
modela un mecanismo distinto.

## La idea

Aquí no hay lista de valores: la variable puede tomar cualquier punto de un intervalo y la
probabilidad de un valor exacto es cero. Lo que se calcula son áreas: `P(a < X ≤ b)` es la
integral de la densidad entre `a` y `b`, y `F(x) = P(X ≤ x)` es la acumulada hasta `x`.

¿Por qué hay tantas familias? Porque cada una responde a una pregunta distinta, y reconocer la
pregunta es lo que te ahorra elegir mal:

- **¿Cuánto tarda algo en ocurrir, sin memoria?** Una **exponencial**: el tiempo hasta el
  siguiente fallo, la siguiente llamada, la siguiente desintegración. Si lleva 3 horas sin
  fallar, la probabilidad de que aguante otra más es la misma que al principio: no envejece.
- **¿Cuánto tarda en ocurrir la vez número `k`?** Una **gamma**, que generaliza la exponencial.
- **¿Cuánto se desvía una medida de su valor real?** Una **normal**, cuando el error es la suma
  de muchísimas causas pequeñas e independientes.
- **¿Cuál es la media de una muestra cuando la varianza es desconocida?** Una **t de Student**,
  que es la normal con las colas engordadas por esa incertidumbre.
- **¿Cuánta variabilidad hay en una muestra?** Una **chi-cuadrado**, que es la suma de cuadrados
  de normales estandarizadas. De ahí salen los intervalos de la varianza y los contrastes.
- **¿Es distinta la variabilidad de dos grupos?** Una **F**, que es el cociente de dos
  chi-cuadrado. Es la distribución del ANOVA y de la comparación de modelos anidados.
- **¿Qué valor tiene una proporción o una probabilidad?** Una **beta**, que vive en el intervalo
  [0, 1] y es la conjugada de la binomial.
- **¿Cómo se reparte una cantidad positiva que multiplica muchos efectos pequeños?** Una
  **lognormal**: ingresos, precios de vivienda, tamaños de partícula, tiempos de latencia.

Todas están conectadas, y esas conexiones ahorran tablas: la exponencial es una gamma con forma
1; la chi-cuadrado con 1 grado de libertad es el cuadrado de una normal estándar; la F es el
cociente de dos chi-cuadrado divididas por sus grados de libertad; la t tiende a la normal
cuando crecen sus grados de libertad; la lognormal es la exponencial de una normal.

La consecuencia práctica más útil: para una continua se trabaja con funciones. `cdf` da
probabilidades, `ppf` (la inversa) da cuantiles y `pdf` da densidades, que sirven para
construir verosimilitudes, no probabilidades.

## Definición formal

Una variable continua queda definida por su densidad `f(x) ≥ 0`, con `∫ f(x)dx = 1`, y su
función de distribución `F(x) = ∫₋∞ˣ f(t)dt`. El cuantil de orden `p` es `q_p = F⁻¹(p)`.

- **Uniforme(a, b).** `f(x) = 1/(b − a)` en `[a, b]`. Media `(a + b)/2`; varianza `(b − a)²/12`.
- **Normal(μ, σ²).** `f(x) = 1/(σ√(2π)) · exp(−(x − μ)²/(2σ²))`. Media `μ`; varianza `σ²`.
  Estandarizando, `Z = (X − μ)/σ` sigue una normal estándar, `N(0, 1)`. Su asimetría es 0 y su
  curtosis de exceso también.
- **Exponencial(λ).** `f(x) = λ·e^(−λx)` para `x ≥ 0`. Media `1/λ`; varianza `1/λ²`. Es sin
  memoria: `P(X > s + t | X > s) = P(X > t)`.
- **Gamma(k, θ).** Forma `k` y escala `θ`. Media `k·θ`; varianza `k·θ²`. Con `k = 1` es la
  exponencial de tasa `1/θ`.
- **t de Student(ν).** Simétrica alrededor de 0, con colas más gordas que la normal. Media 0 si
  `ν > 1`; varianza `ν/(ν − 2)` si `ν > 2`; curtosis de exceso `6/(ν − 4)` si `ν > 4`. Tiende a
  `N(0, 1)` al crecer `ν`.
- **Chi-cuadrado(ν).** La suma de `ν` normales estándar independientes al cuadrado. Media `ν`;
  varianza `2ν`.
- **F(d₁, d₂).** Cociente de dos chi-cuadrado independientes, cada una dividida por sus grados
  de libertad. Asimétrica hacia la derecha.
- **Beta(a, b).** Soporte `[0, 1]`. Media `a/(a + b)` y varianza `a·b/((a + b)²(a + b + 1))`.
- **Lognormal(μ, σ).** `X = e^Y` con `Y` normal de media `μ` y desviación `σ`. Mediana `e^μ`,
  media `e^(μ + σ²/2)`, y siempre media mayor que mediana.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `μ` | En la normal, su centro; en la lognormal, la media del logaritmo | las de `X` (en la lognormal, las del logaritmo) | En la normal desplaza la curva sin deformarla; en la lognormal multiplica la mediana por `e` |
| `σ` | La desviación típica (la varianza es `σ²`) | las de `X` | Ensancha la curva. En la lognormal separa media y mediana: con `σ = 0,5` la media queda un 13 % por encima de la mediana; con `σ = 1`, un 65 % |
| `λ` | Tasa de la exponencial: sucesos por unidad de tiempo | 1 / tiempo | La media baja (`1/λ`) y la cola se acorta. Ojo: la exponencial se parametriza a veces por su media, y ahí `λ` grande significa lo contrario |
| `ν` | Grados de libertad de la t y de la chi-cuadrado | adimensional | En la t, las colas se adelgazan y la distribución se acerca a la normal: con `ν = 5` la curtosis de exceso es 6 y con `ν = 30`, 0,23 |
| `k`, `θ` | Forma y escala de la gamma | adimensional, y las de `X` | La media sube como `k·θ` y la varianza como `k·θ²`: doblar `θ` dobla la media y cuadruplica la varianza |
| `a`, `b` | Formas de la beta | adimensional | La media sube hacia 1 cuando `a` crece respecto a `b`; el soporte sigue siendo `[0, 1]` |
| `d₁`, `d₂` | Grados de libertad del numerador y del denominador de la F | adimensional | Su cociente mueve la masa hacia la derecha; solo hay percentiles publicados para combinaciones concretas |
:::

La lognormal es el caso donde se ve mejor por qué la familia importa: un modelo normal
asignaría probabilidad a valores negativos y, sobre todo, contaría mal el extremo superior.

:::figura
fichero: continuas-lognormal-media-y-mediana
pie: A la izquierda, `X` con `σ = 0,5`: la mediana está en 1,00 y la media en 1,13, separadas por la cola derecha, y el 5 % superior empieza en 2,28, más del doble de la mediana. A la derecha, la misma variable en la escala del logaritmo: simétrica y centrada. La conclusión práctica es que en variables multiplicativas conviene mirar medianas y logaritmos, porque la media se va con la cola.
fuente: figuras/distribuciones-continuas-1.py
:::

## Ejemplo

Valores concretos que conviene tener en la cabeza:

- Normal estándar: `P(−1 ≤ Z ≤ 1) = 0,6827` y `P(Z ≤ 1,96) = 0,9750`.
- t de Student con 5 grados de libertad: `P(T ≤ 2,015) = 0,9500`, pero con el valor de la normal
  `P(T ≤ 1,96) = 0,9464`. Es decir, usar 1,96 con 5 grados de libertad deja un 5,4 % de
  probabilidad en la cola en vez del 5 % nominal. Con 30 grados de libertad el cuantil al 97,5 %
  ya es 2,0423, muy cerca del 1,96 asintótico.
- Chi-cuadrado con 3 grados de libertad: el percentil 95 es 7,8147.
- F con 3 y 20 grados de libertad: el percentil 95 es 3,0984.
- Exponencial con media 2 (tasa 0,5): `P(X ≤ 2) = 0,6321`. La media es 2, pero la mediana es
  `ln(2)/0,5 = 1,386`, porque la exponencial tiene mucha cola a la derecha.
- Lognormal con `μ = 0` y `σ = 0,5`: mediana 1,0, media 1,1331 y percentil 95 igual a 2,2760.
  La media queda un 13 % por encima de la mediana y el 5 % superior de los casos supera el doble
  de la mediana.
- Uniforme(0, 4): varianza `16/12 = 1,3333`. Beta(2, 5): media `2/7 = 0,2857`. Gamma(3, escala
  2): media `3 · 2 = 6`.

## Código

```python verificable
from scipy import stats

# Probabilidades y cuantiles de las familias continuas mas usadas.
print(f"normal  P(-1 <= Z <= 1) = {stats.norm.cdf(1) - stats.norm.cdf(-1):.4f}")  # -> 0.6827
print(f"normal  P(Z <= 1.96)    = {stats.norm.cdf(1.96):.4f}")                    # -> 0.9750
print(f"t(5)    P(T <= 2.015)   = {stats.t.cdf(2.015, 5):.4f}")                   # -> 0.9500
print(f"t(5)    P(T <= 1.96)    = {stats.t.cdf(1.96, 5):.4f}")                    # -> 0.9464
print(f"t(30)   cuantil 0.975   = {stats.t.ppf(0.975, 30):.4f}")                 # -> 2.0423
print(f"chi2(3) cuantil 0.95    = {stats.chi2.ppf(0.95, 3):.4f}")                 # -> 7.8147
print(f"F(3,20) cuantil 0.95    = {stats.f.ppf(0.95, 3, 20):.4f}")                # -> 3.0984
print(f"exp(media 2) P(X <= 2)  = {stats.expon.cdf(2, scale=2):.4f}")             # -> 0.6321
```

:::claves
- `stats.expon.cdf(2, scale=2)` es la trampa de parametrización más cara de esta página: `scale` es la media, no la tasa. `scale=2` significa media 2 (tasa 0,5) y da 0,6321; si querías una tasa de 2 tendrías que escribir `scale=1/2` y el resultado sería 0,9817. La librería no avisa porque las dos son exponenciales válidas.
- `stats.lognorm.ppf(0.95, s=sigma, scale=np.exp(mu))` separa `s` (la desviación del logaritmo) de `scale` (que aquí es la mediana, `e^μ`). Poner `scale=mu` en lugar de `scale=np.exp(mu)` no da error: da otro número.
- `stats.t.cdf(1.96, 5)` devuelve 0,9464 y no 0,9750. El cuantil de la t con 5 grados es 2,015 para el 95 % de una cola y 2,571 para el 97,5 %: cambiar 1,96 por el cuantil de la t es cambiar el intervalo, no afinar el decimal.
- `stats.chi2.ppf(0.95, 3)` funciona igual con `df` posicional y `stats.f.ppf(0.95, 3, 20)` recibe dos grados de libertad en orden (numerador, denominador). Intercambiarlos da un número perfectamente plausible y equivocado.
- La densidad no es una probabilidad: `stats.norm.pdf(0)` vale 0,3989, un número mayor que muchas probabilidades que sí lo son, y `pdf` puede pasar de 1 sin que nada esté mal. Lo que se integra para obtener probabilidades es `pdf`; lo que se compara con un umbral es `cdf` o `sf`.
- `stats.norm.cdf(1.96)` y `stats.norm.sf(1.96)` suman 1 porque son las dos mitades: `cdf` es `P(X ≤ x)` y `sf` es `P(X > x)`. Lo que **no** vale siempre es `cdf(x) + cdf(-x) = 1`: eso exige simetría, y la lognormal no la tiene.
:::

```python verificable
import numpy as np
from scipy import stats

# Lognormal: log(X) es normal, pero la media de X no es exp(mu).
mu, sigma = 0.0, 0.5
print(f"mediana = {np.exp(mu):.4f}")                                           # -> 1.0000
print(f"media   = {np.exp(mu + sigma ** 2 / 2):.4f}")                          # -> 1.1331
print(f"P95     = {stats.lognorm.ppf(0.95, s=sigma, scale=np.exp(mu)):.4f}")   # -> 2.2760

# Otras familias: la beta vive en [0, 1] y la gamma generaliza la exponencial.
print(f"uniforme(0,4) varianza  = {(4 - 0) ** 2 / 12:.4f}")       # -> 1.3333
print(f"beta(2,5) media         = {stats.beta.mean(2, 5):.4f}")   # -> 0.2857
print(f"gamma(3, escala 2) media = {stats.gamma.mean(3, scale=2):.4f}")  # -> 6.0000
```

## Errores típicos

- **Confundir los parámetros de una familia.** La normal se parametriza con `σ²` en unos sitios
  y con `σ` en otros; la exponencial se parametriza con la tasa `λ` o con la media `1/λ` según
  la librería. Una exponencial de tasa 2 tiene media 0,5, no 2. Si no sabes cuál te pide la
  función, comprueba la media que devuelve el propio objeto.
- **Usar la normal para variables positivas y asimétricas.** Ingresos, precios, tiempos de
  atención y tamaños siguen siendo positivos y con cola a la derecha: la lognormal o la gamma
  encajan mucho mejor. La normal asignaría probabilidad positiva a valores negativos imposibles.
- **Aplicar la regla 68-95-99,7 sin comprobar la forma.** Esos porcentajes son de la normal. En
  una distribución de colas gordas, la proporción dentro de `μ ± 2σ` puede ser bastante menor, y
  los extremos aparecen mucho más de lo que sugiere la regla.
- **Usar 1,96 cuando toca la t.** Si estimas la varianza con la muestra y `n` es pequeño, el
  cuantil es el de la t con `n − 1` grados de libertad: con 6 datos (5 grados) es 2,571, no
  1,96. El intervalo queda un 31 % más ancho, y ese ancho es información, no un defecto.
- **Tratar la densidad como una probabilidad o como una verosimilitud.** `pdf(x)` no es
  `P(X = x)` y tampoco es la probabilidad de los datos: para un conjunto de observaciones
  independientes la verosimilitud es el producto de las densidades, y se maximiza en forma de
  suma de logaritmos.
- **Elegir la familia por costumbre.** Poner una normal porque es lo que sale por defecto, o
  forzar simetría donde el mecanismo es multiplicativo, hace que el modelo falle justo en las
  colas, que es donde se toman las decisiones sobre riesgo.

:::practica
enunciado: El tiempo entre fallos de un servidor es exponencial con media 4 horas, o sea con tasa λ = 0,25 fallos por hora. Calcula la mediana, la probabilidad de que un intervalo supere las 6 horas y la de aguantar 2 horas más sabiendo que ya lleva 6 sin fallar.
pista: La mediana de una exponencial es ln(2)/λ, no la media, y sin memoria P(X > s+t | X > s) = P(X > t).
solucion: Mediana = ln(2)/0,25 = 0,6931/0,25 = 2,7726 horas. P(X > 6) = e^(−0,25·6) = e^(−1,5) = 0,2231. Y P(X > 8 | X > 6) = e^(−0,25·2) = e^(−0,5) = 0,6065. Conclusión: la mediana (2,77 h) queda muy por debajo de la media (4 h) por la cola derecha, y llevar 6 horas sin fallar no cambia la probabilidad de aguantar dos más.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué la media de una lognormal es mayor que su mediana?
o: Porque la lognormal puede tomar valores muy grandes, que empujan la media sin mover la mediana
o: Porque sus parámetros se estiman con logaritmos
o: Porque la mediana siempre es menor que la media en cualquier distribución
a: 1
e: La lognormal es asimétrica hacia la derecha: unos pocos valores muy altos tiran de la media, mientras la mediana solo depende del orden. Con mu = 0 y sigma = 0,5, la mediana es 1,0 y la media 1,1331. No es una regla general: en una distribución simétrica coinciden, y en una asimétrica a la izquierda la media es menor.
:::

:::quiz
p: Estimas la media con 6 observaciones y no conoces la varianza poblacional. ¿Qué cuantil usas para un intervalo del 95 %?
o: 1,96, el de la normal estándar
o: 2,571, el de la t de Student con 5 grados de libertad
o: 1,645, porque el intervalo es de una cola
a: 2
e: Al estimar la varianza con los propios datos aparece incertidumbre extra, y eso engorda las colas: la t con n − 1 = 5 grados de libertad da 2,571 para el 97,5 %. Con 1,96 el intervalo sería demasiado estrecho y mentiría sobre su cobertura.
:::

:::quiz
p: ¿Qué relación hay entre la chi-cuadrado con 1 grado de libertad y la normal estándar?
o: Es el cuadrado de una normal estándar
o: Es la mitad de una normal estándar
o: No tienen relación; una es discreta y la otra continua
a: 1
e: La chi-cuadrado con v grados de libertad es la suma de v normales estándar independientes elevadas al cuadrado. Con v = 1 es exactamente Z². De ahí salen la varianza muestral, los contrastes de bondad de ajuste y la distribución F, que es un cociente de dos chi-cuadrado.
:::
