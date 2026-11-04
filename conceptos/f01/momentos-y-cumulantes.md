---
id: momentos-y-cumulantes
titulo: Momentos y cumulantes
fase: 1
nivel: avanzado
rutas: [core, ds, quant]
prerequisitos: [valor-esperado, varianza-y-desviacion, asimetria-y-curtosis]
tags: [probabilidad, momentos, colas, riesgo]
resumen: Media, varianza, asimetría y curtosis como una sola familia de números, y los cumulantes que sí se suman al combinar variables independientes.
fuentes: ["Casella y Berger (2002), 'Statistical Inference'", "Billingsley (1995), 'Probability and Measure'"]
---

## En una frase

Los momentos resumen la forma de una distribución con una lista de números (dónde está, cuánto
se ensancha, hacia dónde se inclina y cuánto pesan sus colas), y los cumulantes son la versión
de esa lista que se suma cuando juntas variables independientes.

## La idea

Una distribución es un objeto infinito; cuatro números no la describen entera. Pero son un
resumen sorprendentemente útil, como la ficha de una película: quién sale, cuánto dura, de qué
género y qué nota tiene. Cada momento añade una capa:

- el **primero** dice dónde está el centro (la media);
- el **segundo** dice cuánto se extiende (la varianza);
- el **tercero** dice hacia qué lado arrastra la cola (la asimetría);
- el **cuarto** dice cuánto pesan los valores extremos (la curtosis).

Ese cuarto momento es el que arruina carteras. Una estrategia con curtosis alta pasa la mayor
parte del tiempo con movimientos pequeños y de vez en cuando se lleva por delante todo lo
ganado. La varianza no lo ve: dos activos con la misma volatilidad y distinta curtosis se
comportan de forma muy distinta en el peor día del año. En una normal, un movimiento a cinco
desviaciones típicas es tan raro que no se espera verlo en varias vidas humanas; con la
curtosis que muestran muchas series financieras reales, esos días llegan cada pocos años. Por
eso existen medidas que miran solo la cola, como el VaR y el CVaR.

Los **cumulantes** son la misma información reorganizada para que sea aditiva. La media ya se
sumaba sin problemas, pero la varianza de `X + Y` solo es `Var(X) + Var(Y)` si no hay
covarianza. Con los cumulantes, la propiedad es limpia: los cumulantes de una suma de variables
independientes son la suma de los cumulantes, orden a orden. Cumulante primero es la media,
segundo es la varianza, tercero coincide con el momento central tercero, y a partir del cuarto
empiezan a diferir.

Hay un detalle que explica por qué la normal está en todas partes, y lo verás otra vez en
[[teorema-central-del-limite|el teorema central del límite]]: **todos los cumulantes de orden
3 o superior de una normal son cero**. Cuando sumas muchas causas pequeñas e independientes,
los cumulantes se van sumando y los de orden alto se diluyen entre muchos términos, así que lo
que queda se parece a una distribución con solo dos cumulantes: una normal.

Dos advertencias antes de seguir. Primera: los momentos **no siempre existen**. La t de Student
con 4 grados de libertad tiene curtosis infinita, y con 2 grados de libertad no tiene ni
varianza. Segunda: los momentos **no siempre determinan la distribución**: hay parejas de
distribuciones distintas con todos sus momentos iguales, así que «coinciden en media y
varianza» está muy lejos de «son la misma distribución».

## Definición formal

Para una variable aleatoria `X` con media `μ = E[X]` y desviación típica `σ`:

- **Momentos respecto al origen:** `m_k = E[X^k]`.
- **Momentos centrales:** `μ_k = E[(X − μ)^k]`. En particular `μ₁ = 0` y `μ₂ = Var(X) = σ²`.
- **Asimetría (sesgo estandarizado):** `γ₁ = μ₃/σ³`. Vale 0 si la distribución es simétrica.
- **Curtosis de exceso:** `γ₂ = μ₄/σ⁴ − 3`. El `−3` es una convención para que la normal valga
  0; sin restarlo se habla de curtosis a secas, y entonces la normal vale 3.

Los cumulantes se definen con la función generatriz de momentos `M(t) = E[e^(tX)]`, allí donde
la esperanza exista, y su logaritmo `K(t) = ln M(t)`:

- `κ_k` es la derivada k-ésima de `K(t)` evaluada en `t = 0`.
- Relaciones útiles: `κ₁ = μ`, `κ₂ = σ²`, `κ₃ = μ₃`, `κ₄ = μ₄ − 3·μ₂²`.
- **Aditividad:** si `X` e `Y` son independientes, `κ_k(X + Y) = κ_k(X) + κ_k(Y)` para todo `k`.
  Y para una constante: `κ_k(c·X) = c^k · κ_k(X)`.
- **Normal:** `κ₁ = μ`, `κ₂ = σ²`, `κ_k = 0` para `k ≥ 3`. **Poisson(λ):** todos los
  cumulantes valen `λ`.
- **Estimación muestral:** los k-estadísticos (`k₁ = x̄`, `k₂ = s²`, …) son estimadores
  insesgados de los cumulantes. Sus versiones estandarizadas son las que devuelven
  `scipy.stats.skew` y `scipy.stats.kurtosis`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `μ` | La media de `X`: el momento primero | las de `X` | El centro se desplaza; los momentos centrales no cambian |
| `σ²` | La varianza: el momento central segundo | las de `X`, al cuadrado | Los momentos centrales crecen con ella; la asimetría y la curtosis estandarizadas, no |
| `μ_k` | El momento central de orden `k`: `E[(X − μ)^k]` | las de `X` elevadas a `k` | Con `k` par siempre crece; con `k` impar depende del signo de la desviación |
| `γ₁ = μ₃/σ³` | La asimetría estandarizada | adimensional | Se aleja de 0 hacia el lado de la cola larga; su rango útil es aproximadamente de −3 a 3 |
| `γ₂ = μ₄/σ⁴ − 3` | La curtosis de exceso | adimensional | Más peso en los valores extremos. Vale 0 en la normal, 6 en una t con 5 grados y 110,94 en una lognormal con `σ = 1` |
| `κ_k` | El cumulante de orden `k`, derivada k-ésima de `ln M(t)` en 0 | las de `X` elevadas a `k` | Se suma al juntar variables independientes; en una normal vale 0 para `k ≥ 3` |
:::

La ficha de cuatro números resume, pero no identifica. Las dos distribuciones de la figura
tienen la misma media y la misma varianza, y sin embargo no son la misma distribución: una
produce un día catastrófico cada varias vidas y la otra, cada pocos años.

:::figura
fichero: momentos-misma-varianza-distinta-curtosis
pie: Las dos curvas están centradas en el mismo punto y tienen la misma anchura: la varianza no las distingue. A la derecha, el mismo par de curvas en escala logarítmica: hasta unas 2,1 desviaciones manda la normal y a partir de ahí manda la t, que en la cola crece muy rápido (a 3 desviaciones acumula unas 4 veces más masa y a 4 desviaciones, casi 60). Eso es lo que mide `γ₂`, y es la razón de que dos carteras con la misma volatilidad se arruinen de forma muy distinta.
fuente: figuras/momentos-y-cumulantes-1.py
:::

## Ejemplo

Ocho retornos mensuales de un fondo, en porcentaje: 2,1 · −0,4 · 1,3 · −3,2 · 0,8 · 5,6 · −1,1 ·
0,2. La media es 0,6625, la varianza muestral 6,6055, la asimetría 0,6643 (cola hacia la
derecha, empujada por el 5,6) y la curtosis de exceso 1,6401 (colas más gordas que la normal,
empujadas por el −3,2 y el 5,6).

Los k-estadísticos dan `k₁ = 0,6625`, `k₂ = 6,6055` (idéntico a la varianza muestral, como
tiene que ser), `k₃ = 11,2772` y `k₄ = 71,5613`. Observa que el cuarto cumulante es un número
grande y muy sensible: ese 5,6 elevado a la cuarta potencia pesa más que los otros siete
valores juntos.

Para comparar, valores teóricos de curtosis de exceso: normal 0; t de Student con 5 grados de
libertad 6; t con 4 grados de libertad, infinita; lognormal con `σ = 1`, 110,94. La lognormal
tiene todos sus momentos finitos y aun así una curtosis enorme: colas gordas no es lo mismo que
momentos inexistentes.

**Cartera.** Dos activos con `σ₁ = 0,20`, `σ₂ = 0,10` y correlación 0,3, con pesos 0,6 y 0,4.
Con la fórmula de la varianza: `0,36·0,04 + 0,16·0,01 + 2·0,6·0,4·0,3·0,02 = 0,01888`, o sea
`σ = 13,7 %`. Si te interesa el riesgo de cola de esa cartera, la varianza no basta: necesitas
el tercer y el cuarto momento conjuntos (cosasimetría y cocurtosis), que no se obtienen
combinando los momentos individuales.

## Código

```python verificable
import numpy as np
from scipy import stats

# Ocho retornos mensuales de un fondo, en %.
r = np.array([2.1, -0.4, 1.3, -3.2, 0.8, 5.6, -1.1, 0.2])

print(f"media        = {r.mean():.4f}")                                    # -> 0.6625
print(f"varianza     = {r.var(ddof=1):.4f}")                               # -> 6.6055
print(f"asimetria    = {stats.skew(r, bias=False):.4f}")                   # -> 0.6643
print(f"curtosis ex. = {stats.kurtosis(r, fisher=True, bias=False):.4f}")  # -> 1.6401

# Los k-estadisticos estiman los cumulantes; k2 es la varianza muestral.
print(f"k1 = {stats.kstat(r, 1):.4f}")   # -> 0.6625
print(f"k2 = {stats.kstat(r, 2):.4f}")   # -> 6.6055
print(f"k3 = {stats.kstat(r, 3):.4f}")   # -> 11.2772
print(f"k4 = {stats.kstat(r, 4):.4f}")   # -> 71.5613
```

:::claves
- `stats.skew` y `stats.kurtosis` llevan `bias=True` por defecto, es decir, calculan la versión que divide entre `n` (la misma convención que `np.var()` sin `ddof`). Con ocho datos la diferencia no es un decimal: la curtosis pasa de 0,1143 con `bias=True` a 1,6401 con `bias=False`, y la asimetría de 0,5326 a 0,6643. Si comparas con un libro, mira antes qué versión usa.
- `stats.kurtosis(..., fisher=True)` es lo que devuelve el exceso (`μ₄/σ⁴ − 3`). Con `fisher=False` devuelve la curtosis a secas y la normal vale 3, no 0. Cambiar ese argumento es cambiar la escala, no el dato.
- `stats.kstat(r, 2)` devuelve exactamente 6,6055, lo mismo que `r.var(ddof=1)` y no lo que da `r.var()` (5,7798). El k-estadístico segundo ya lleva la corrección de insesgadez incorporada, así que la diferencia con la varianza poblacional no es un error de la librería.
- `r.var(ddof=1)` divide entre `n − 1`; `r.var()` divide entre `n`. El mismo array da 6,6055 o 5,7798 según el argumento. En NumPy el valor por defecto es `ddof=0` y en pandas es `1`: la misma columna da varianzas distintas en las dos librerías.
- `stats.kstat(r, 4)` vale 71,5613 y se apoya casi por completo en el valor más extremo: cambiar el 5,6 por 3,0 lo hunde hasta 5,9917, doce veces menos. Es un estimador de colas, y las colas no se estiman con ocho números.
- `stats.t.stats(4, moments='k')` devuelve `inf` sin lanzar ningún error ni aviso: la curtosis de una t con 4 grados de libertad no existe. La librería no distingue «no existe» de «es enorme», así que ese `inf` hay que interpretarlo, no imprimirlo y seguir.

:::

```python verificable
import numpy as np
from scipy import stats

# Cumulantes teoricos: la normal solo tiene los dos primeros.
print(f"normal  curtosis de exceso = {stats.norm.stats(moments='k'):.4f}")    # -> 0.0000
print(f"t(5)    curtosis de exceso = {stats.t.stats(5, moments='k'):.4f}")    # -> 6.0000
print(f"t(4)    curtosis de exceso = {stats.t.stats(4, moments='k'):.4f}")    # -> inf
print(f"t(30)   curtosis de exceso = {stats.t.stats(30, moments='k'):.4f}")   # -> 0.2308
print(f"lognormal(s=1) exceso     = {stats.lognorm.stats(s=1.0, moments='k'):.4f}")  # -> 110.9364

# La varianza de una cartera mezcla varianzas y covarianza.
x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
y = np.array([2.0, 1.0, 4.0, 3.0, 6.0])
a, b = 0.6, 0.4
directa = np.var(a * x + b * y, ddof=1)
formula = a**2 * x.var(ddof=1) + b**2 * y.var(ddof=1) + 2 * a * b * np.cov(x, y, ddof=1)[0, 1]
print(f"varianza directa = {directa:.6f}")   # -> 2.692000
print(f"varianza formula = {formula:.6f}")   # -> 2.692000
print(f"cov = {np.cov(x, y, ddof=1)[0, 1]:.4f}  corr = {np.corrcoef(x, y)[0, 1]:.4f}")  # -> cov = 2.5000  corr = 0.8220
```

## Errores típicos

- **Creer que la curtosis mide el «pico» de la distribución.** Lo que mide es el peso de los
  valores extremos en relación con la varianza. Dos distribuciones con el mismo pico pueden
  tener curtosis muy distintas, y una distribución bimodal (dos picos) puede tener curtosis de
  exceso negativa.
- **Estimar la curtosis con pocos datos.** Al elevar a la cuarta potencia, un solo valor
  extremo domina la estimación. Con ocho observaciones, el 1,6401 del ejemplo es casi una
  anécdota sobre ese 5,6; no es una propiedad fiable de la distribución.
- **Comparar curtosis de variables con escalas distintas.** La curtosis solo es comparable en
  su versión estandarizada `μ₄/σ⁴`. Comparar momentos centrales crudos mezcla dispersión con
  forma.
- **Suponer normalidad porque conoces media y varianza.** Son dos números frente a una función
  infinita. La t con 5 grados de libertad y la normal estándar se distinguen justo en la cola,
  que es donde se pierde el dinero.
- **Calcular momentos que no existen.** La t con 4 grados de libertad tiene curtosis infinita y
  la t con 2 no tiene varianza. La media muestral de una Cauchy no converge a nada. Que
  `np.mean` devuelva un número no significa que ese número estime algo real.
- **Sumar momentos al agregar variables.** Los momentos no son aditivos (salvo el primero); los
  cumulantes sí lo son bajo independencia. Si combinas carteras sumando asimetrías o curtosis
  individuales, el resultado no es el de la cartera.

:::practica
enunciado: Dos factores de riesgo independientes siguen una Poisson, uno con λ = 2 y otro con λ = 3. Calcula el cuarto cumulante de su suma por aditividad y compruébalo con κ₄ = μ₄ − 3·μ₂², sabiendo que en una Poisson(λ) es μ₂ = λ y μ₄ = λ + 3λ².
pista: Los cumulantes de una suma de variables independientes se suman orden a orden, y la suma de dos Poisson independientes es otra Poisson con la tasa sumada.
solucion: La suma es Poisson(5), luego κ₄ = 2 + 3 = 5. Comprobación: μ₂ = 5 y μ₄ = 5 + 3 · 25 = 80, así que κ₄ = 80 − 3 · 25 = 5. Coincide. Pero κ₃ = 5 tampoco es cero: la suma sigue siendo asimétrica, y tener los cumulantes altos de una Poisson no la convierte en normal.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué propiedad tienen los cumulantes que no tienen los momentos?
o: Son siempre positivos
o: Se suman cuando las variables son independientes, orden a orden
o: Coinciden siempre con los momentos centrales
a: 2
e: Si X e Y son independientes, κ_k(X + Y) = κ_k(X) + κ_k(Y) para todo k. Los momentos solo cumplen algo parecido en el primer orden, y a partir del segundo aparece la covarianza y el resto de términos cruzados. Por eso los cumulantes son la forma natural de estudiar sumas.
:::

:::quiz
p: Una distribución tiene curtosis de exceso 6, como una t de Student con 5 grados de libertad. ¿Qué implica?
o: Que su varianza es seis veces mayor que la de una normal
o: Que los valores extremos son mucho más frecuentes de lo que predice una normal con esa misma varianza
o: Que la distribución es imposible, porque la curtosis de exceso no puede pasar de 3
a: 2
e: La curtosis de exceso mide el peso de las colas en relación con la varianza, que aquí se mantiene fija. Un valor de 6 no dice nada sobre la dispersión: dice que los sucesos alejados de la media aparecen con mucha más frecuencia que en una normal. No hay cota superior para la curtosis.
:::

:::quiz
p: ¿Por qué no basta con la media y la varianza para describir una distribución?
o: Porque hay distribuciones distintas con esos dos momentos iguales y colas muy diferentes
o: Porque la media y la varianza no siempre existen
o: Porque la varianza no está definida para variables continuas
a: 1
e: Una t con 5 grados de libertad y una normal pueden compartir media y varianza y comportarse de forma opuesta en la cola. Además, hay parejas de distribuciones con todos sus momentos iguales y forma distinta. Es cierto que en colas muy gordas la varianza puede no existir, pero el argumento principal es que dos números resumen muy poco.
:::
