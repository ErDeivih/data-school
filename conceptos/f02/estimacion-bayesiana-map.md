---
id: estimacion-bayesiana-map
titulo: Estimación bayesiana y MAP
fase: 2
nivel: avanzado
rutas: [ds, core]
prerequisitos: [maxima-verosimilitud, teorema-de-bayes, distribuciones-continuas]
tags: [bayes, regularizacion, inferencia]
resumen: Priors, posteriors y MAP: cómo la creencia previa entra en la estimación y por qué la regularización L2 es un prior gaussiano.
fuentes: ["Gelman, Carlin, Stern y Rubin (2013), 'Bayesian Data Analysis'", "Murphy (2022), 'Probabilistic Machine Learning: An Introduction', cap. 4"]
---

## En una frase

La estimación bayesiana no devuelve un número sino una **distribución** sobre el parámetro —lo que
creías antes, actualizado con los datos—, y el **MAP** es solo el punto más alto de esa
distribución, que resulta ser el estimador con penalización que ya usas al regularizar.

## La idea

Volvamos a la moneda. Lanzas 5 veces y salen 5 caras. El [[maxima-verosimilitud|MLE]] dice `p = 1`:
cara con probabilidad 1, cruz imposible. Cualquiera que haya visto una moneda sabe que eso es
absurdo, y la razón es que **ya tenías información antes de lanzar**: las monedas normales salen
cara la mitad de las veces. El enfoque bayesiano escribe esa información como una distribución
**a priori** (*prior*) y la combina con los datos para obtener una distribución **a posteriori**
(*posterior*).

La mecánica es el [[teorema-de-bayes]], sin más:

:::formula
P(θ / datos) ∝ P(datos / θ) · P(θ)
:::

Lee cada pieza en voz alta: «lo que creo después es proporcional a lo verosímil que son los datos
bajo cada `θ`, multiplicado por lo que creía antes». La verosimilitud es la misma función del MLE;
lo nuevo es el factor `P(θ)`.

Eso tiene tres consecuencias prácticas que se notan en el trabajo diario:

1. **Con pocos datos manda el prior; con muchos, los datos.** Si lanzas la moneda 2 veces, tu
   posterior se parece mucho a tu creencia inicial. Si la lanzas 10.000, el prior queda diluido y
   el posterior se pega al MLE. No hay que elegir entre las dos filosofías: la fórmula hace el
   reparto sola.
2. **Sirve para cuantificar la incertidumbre de verdad.** El resultado no es «`p = 0,63`», es una
   distribución completa de la que puedes decir «hay un 95 % de probabilidad de que `p` esté entre
   0,38 y 0,84». Eso es un **intervalo creíble**, y significa lo que todo el mundo cree que
   significa un [[intervalos-de-confianza|intervalo de confianza]] (que no significa eso).
3. **Los priors son regularización.** Un prior que concentra masa alrededor de cero empuja las
   estimaciones hacia cero. Si el prior es una normal centrada en cero, el término que añade a la
   log-verosimilitud es `−λ·θ²`… es decir, la penalización **L2** de ridge. Si el prior es una
   Laplace, sale la penalización **L1** de lasso. La
   [[regularizacion-l1-l2|regularización]] es una creencia previa
   escrita en forma de fórmula, y no un truco de ingeniería.

El precio: hay que elegir el prior. Si es muy informativo y está equivocado, contamina el
resultado; si es muy difuso, no aporta nada y vuelves al MLE. Y en modelos grandes, calcular el
posterior completo exige simulación (MCMC, variacional), no una fórmula cerrada.

:::figura
fichero: bayes-prior-posterior-y-map
pie: El prior (morado) y la verosimilitud (gris) se combinan en el posterior (azul): su pico, 0,643, cae a la izquierda del MLE, 0,700, porque el prior tira hacia 0,5. La banda verde es el 95 % creíble, de 0,384 a 0,837. A la derecha se ve el reparto: con pocos lanzamientos el MAP está a medio camino del prior y a partir de unos cientos de datos MAP y MLE son indistinguibles.
fuente: figuras/estimacion-bayesiana-map-1.py
:::

## Definición formal

Sea un parámetro `θ` y unos datos `x = (x₁, …, xₙ)`.

- `P(θ)` — **prior**: la distribución que resume lo que crees sobre `θ` antes de ver los datos.
- `P(x / θ)` — **verosimilitud**: la misma función `L(θ)` de [[maxima-verosimilitud]].
- `P(θ / x)` — **posterior**: la distribución actualizada tras ver los datos.
- `P(x) = ∫ P(x / θ)·P(θ) dθ` — **evidencia** o verosimilitud marginal. No depende de `θ`; es la
  constante que normaliza el posterior para que integre 1.

El teorema de Bayes da la fórmula exacta:

:::formula
P(θ / x) = P(x / θ) · P(θ) / P(x)
:::

El estimador **MAP** (*maximum a posteriori*) es el valor que maximiza el posterior, que es lo
mismo que maximizar su logaritmo (el denominador no depende de `θ`):

:::formula
θ̂_MAP = argmax_θ [ log P(x / θ) + log P(θ) ] = argmax_θ [ ℓ(θ) + log P(θ) ]
:::

- `ℓ(θ)` — log-verosimilitud, el término que ya aparecía en el MLE.
- `log P(θ)` — log-prior. Es un **término de penalización** que se suma a la log-verosimilitud:
  cuanto menos creíble es un `θ`, más resta.
- `θ̂_MAP` — el máximo del posterior. **No es lo mismo que la media del posterior**, que es
  `E[θ / x]`: coinciden si el posterior es simétrico y unimodal, y difieren si está sesgado.

Dos casos concretos que conviene reconocer de memoria:

- **Prior normal `θ ~ Normal(0, τ²)` con verosimilitud gaussiana.** El término de penalización es
  `−θ²/(2τ²)`, así que la suma `ℓ(θ) − θ²/(2τ²)` se minimiza como una suma de cuadrados con
  penalización. Eso es **ridge**, con `λ = σ²/τ²`. Un prior más estrecho (menor `τ`) equivale a
  regularizar más fuerte.
- **Prior Laplace `θ ~ Laplace(0, b)`.** La penalización `−|θ|/b` es el valor absoluto, y su
  solución es **lasso**: empuja coeficientes a cero. Cambiar de normal a Laplace cambia
  L2 por L1, y eso es todo lo que separa ridge de lasso.

Cuando el prior es uniforme (`P(θ) ∝ constante`), el término de penalización desaparece y el MAP
**coincide con el MLE**. Ese es el sentido preciso de «el MLE es el caso particular sin
información previa».

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `P(θ)` | Prior: lo que crees sobre `θ` antes de ver los datos | densidad | Cuanto más concentrado, más empuja la estimación hacia su centro y menos pesan los datos. Un prior informativo y equivocado contamina el resultado, y eso no se arregla con más muestra |
| `P(x / θ)` | Verosimilitud: la misma `L(θ)` del MLE | densidad | Es el único término donde entran los datos, y crece con `n` de forma multiplicativa. Con 1.000 lanzamientos pesa cien veces más que con 10, y por eso el prior acaba diluido |
| `P(θ / x)` | Posterior: la distribución actualizada tras ver los datos | densidad | Es la respuesta completa, no un número: de ella salen la media, el MAP y los intervalos creíbles. Con modelos grandes no tiene forma cerrada y hay que simularla |
| `P(x)` | Evidencia o verosimilitud marginal, `∫ P(x/θ)·P(θ) dθ` | densidad | No depende de `θ`, solo normaliza el posterior. Por eso el MAP puede maximizar `ℓ(θ) + log P(θ)` sin calcularla, y por eso comparar modelos con ella es otra historia |
| `ℓ(θ)` | Log-verosimilitud | log de densidad | Es el término que ya estaba en el MLE. Si domina, el MAP y el MLE coinciden en la práctica |
| `log P(θ)` | Log-prior: la penalización que se suma a `ℓ` | log de densidad | Es lo que convierte la estimación en un problema con penalización. Con un prior normal es `−θ²/(2τ²)`; con una Laplace, menos el valor absoluto de `θ` dividido por `b` |
| `θ̂_MAP` | Valor de `θ` que maximiza el posterior | las de `θ` | No es la media del posterior (0,643 frente a 0,625 con 7 caras y 3 cruces) y, a diferencia de ella, no es invariante ante reparametrizaciones |
| `τ` | Desviación típica del prior normal | las de `θ` | Más pequeño significa creer más fuerte y regularizar más: `λ = σ²/τ²` sube con el cuadrado, así que pasar de `τ = 0,5` a `τ = 0,25` multiplica la penalización por cuatro |
| `b` | Escala del prior Laplace | las de `θ` | Cambia la geometría de la penalización: `θ²` pasa a valor absoluto de `θ` y aparecen coeficientes exactamente cero. Es la única diferencia entre ridge y lasso |
| `λ` | Fuerza de la penalización en la versión de mínimos cuadrados | — | Con `λ = 0` (prior uniforme) el MAP es el MLE; al subir, la estimación se pega al centro del prior. En el ejemplo, la pendiente baja de 1,0119 a 0,5123 al pasar de 0 a 10 |
:::

## Ejemplo

Moneda lanzada `n = 10` veces con **7 caras y 3 cruces**. El prior es `Beta(3, 3)`, que está
centrado en 0,5 y es bastante ancho: equivale a haber visto 2 caras y 2 cruces antes de empezar.

La familia Beta es la **conjugada** de la Bernoulli: si el prior es `Beta(a, b)` y observas `k`
caras y `n − k` cruces, el posterior es `Beta(a + k, b + n − k)`, sin integrales.

- Posterior: `Beta(3 + 7, 3 + 3) = Beta(10, 6)`.
- **MLE**: `7/10 = 0,700`.
- **MAP**: el máximo de una `Beta(10, 6)` está en `(a − 1)/(a + b − 2) = 9/14 = 0,643`. Comprobado
  sobre una rejilla de 200.001 puntos sale 0,643.
- **Media del posterior**: `a/(a + b) = 10/16 = 0,625`. Distinta del MAP porque la `Beta(10, 6)`
  es ligeramente asimétrica: tirando hacia la izquierda.
- **Intervalo creíble del 95 %**: `[0,384 , 0,837]`, calculado con los cuantiles 2,5 % y 97,5 % de
  la `Beta(10, 6)`.

Fíjate en el orden: `0,643 (MAP) < 0,700 (MLE)`, y `0,625` (media) aún más abajo. El prior tira
hacia 0,5 y arrastra la estimación. Con 1.000 lanzamientos en vez de 10, el prior `Beta(3, 3)`
pesaría lo mismo que antes —es una constante— pero la verosimilitud pesaría cien veces más, y MAP
y MLE quedarían prácticamente pegados. **El prior no se diluye porque se olvide, sino porque los
datos lo superan en cantidad.**

El ejemplo de ridge es aún más directo: si el prior de la pendiente es `Normal(0; 0,5²)` y el ruido
tiene `σ = 1`, entonces `λ = σ²/τ² = 1/0,25 = 4`. Ese `λ = 4` es el mismo número que
pondrías en `Ridge(alpha=4)`. La correspondencia va en los dos sentidos, así que el `alpha` que ajustas a mano tiene una lectura bayesiana concreta: es la fuerza de un prior normal centrado en cero.

## Código

```python verificable
import numpy as np
from scipy import stats

# Mismo problema de la moneda, con una prior Beta(3, 3) centrada en 0,5
caras, cruces = 7, 3
alpha_prior, beta_prior = 3.0, 3.0

# La posterior es Beta(alpha + caras, beta + cruces): conjugada con la binomial
a_post, b_post = alpha_prior + caras, beta_prior + cruces
grid = np.linspace(1e-9, 1 - 1e-9, 200_001)
posterior = stats.beta.pdf(grid, a_post, b_post)

map_ = grid[np.argmax(posterior)]
media_post = a_post / (a_post + b_post)
mle = caras / (caras + cruces)

print(f"MLE          {mle:.3f}")          # -> 0.700
print(f"MAP          {map_:.3f}")         # -> 0.643
print(f"media post.  {media_post:.3f}")   # -> 0.625
print(f"IC 95 % creible [{stats.beta.ppf(0.025, a_post, b_post):.3f}, {stats.beta.ppf(0.975, a_post, b_post):.3f}]")  # -> [0.384, 0.837]
```

:::claves
- `np.linspace(1e-9, 1 - 1e-9, 200_001)` evita los extremos exactos 0 y 1 a propósito: ahí `stats.beta.pdf` puede devolver 0 o infinito y `np.argmax` elegiría un punto del borde. Con 200.001 puntos el MAP sale con cinco decimales, pero el máximo analítico es exacto: `(a − 1)/(a + b − 2) = 9/14 = 0,642857`.
- `grid[np.argmax(posterior)]` devuelve el **primer** índice donde está el máximo. Con dos valores empatados se queda con el de la izquierda, y la precisión del MAP es la de la rejilla, no la de la fórmula.
- `stats.beta.pdf(grid, a_post, b_post)` recibe los parámetros por posición y no comprueba nada: `pdf(grid, b_post, a_post)` (el orden cambiado) dibuja otra curva y no da ningún error. Lo mismo con `ppf`, cuyo primer argumento es la probabilidad acumulada.
- La conjugada es una suma, no una integral: `a_post = alpha_prior + caras` y `b_post = beta_prior + cruces`. Por eso el prior se lee como pseudo-cuentas: `Beta(3, 3)` equivale a haber visto 2 caras y 2 cruces antes de empezar.
- `media_post = a_post / (a_post + b_post)` es la media del posterior, **no** el MAP: con `Beta(10, 6)` valen 0,625 y 0,643, y solo coinciden cuando la distribución es simétrica. `stats.beta.ppf` da el intervalo creíble [0,384; 0,837], que es lo que sí significa «el 95 % de la probabilidad posterior está aquí».
- En el segundo bloque, `(xc @ yc) / (xc @ xc + lam)`: la penalización entra **dentro** del denominador y solo toca a la pendiente porque `x` e `y` están centradas. Si no las centraras, el mismo `λ` penalizaría también el término independiente y la recta entera se desplazaría hacia cero.
:::

```python verificable
import numpy as np

# Regularizar con L2 es poner una prior normal centrada en cero: MAP = ridge.
# Centramos x e y para que la penalizacion solo toque a la pendiente.
x = np.array([1.0, 1.1, 2.0, 2.2, 3.0, 3.1, 4.0, 4.2])
y = np.array([2.1, 2.5, 3.2, 3.6, 4.1, 4.4, 5.2, 5.6])
xc, yc = x - x.mean(), y - y.mean()

pendiente_ols = (xc @ yc) / (xc @ xc)
print(f"pendiente OLS {pendiente_ols:.4f}")   # -> 1.0119

# MAP = argmin de la suma de cuadrados + lambda * pendiente^2
for lam in (0.0, 0.5, 1.0, 2.0, 10.0):
    pendiente_map = (xc @ yc) / (xc @ xc + lam)
    print(f"lambda = {lam:>4.1f}  pendiente {pendiente_map:.4f}")

# Equivalencia con el prior: lambda = sigma^2 / tau^2.
# Con un prior normal de desviacion tau = 0,5 y un ruido de sigma = 1:
sigma, tau = 1.0, 0.5
print(f"lambda equivalente {sigma ** 2 / tau ** 2:.1f}")   # -> 4.0
```

La segunda salida es una **senda de regularización** en miniatura: con `λ = 0` la pendiente es la
de mínimos cuadrados, 1,0119, y va bajando hasta 0,5123 con `λ = 10`. El modelo no aprende
menos: el prior cada vez pesa más y tira de la pendiente hacia su centro, que es cero.

```python ilustrativo
# Con modelos grandes el posterior no tiene forma cerrada y se simula.
# Necesita pymc, que no es una de las librerias del portal: por eso no se ejecuta.
import pymc as pm

with pm.Model() as modelo:
    p = pm.Beta("p", alpha=3, beta=3)                 # prior
    pm.Binomial("caras", n=10, p=p, observed=7)       # verosimilitud
    traza = pm.sample(2000, tune=1000, random_seed=0)  # posterior por MCMC

print(pm.summary(traza))   # media, desviacion, intervalos creibles del posterior
```

## Errores típicos

- **Leer el prior como una opinión arbitraria que hay que evitar.** Un prior uniforme también es un
  prior, y en muchos casos es una elección peor que uno informativo. Además, «sin prior» no existe:
  si usas MLE estás usando el prior uniforme, te guste o no.
- **Confundir MAP con la media del posterior.** Son dos resúmenes distintos de la misma
  distribución. Con el ejemplo de la moneda: MAP 0,643 y media 0,625. En posteriors asimétricos o
  multimodales, elegir uno u otro cambia la respuesta, y el MAP tiene la desventaja de no ser
  invariante ante cambios de variable.
- **Confundir intervalo creíble con intervalo de confianza.** El creíble dice «el 95 % de la
  probabilidad posterior está aquí»; el de confianza dice «el 95 % de los intervalos que construiría
  así contiene el valor fijo». Suenan igual y no lo son. Ver [[intervalos-de-confianza]].
- **Creer que un prior difuso es neutro.** Un prior muy plano sobre `p` no es plano sobre
  `log(p/(1−p))`, ni al revés. En modelos con muchos parámetros, los priors «vagos» pueden empujar
  el posterior a regiones absurdas sin que te enteres.
- **Usar el mismo conjunto de datos para elegir el prior y reportar el posterior.** Es
  p-hacking con otro nombre: si pruebas priors hasta que el intervalo creíble excluya cero, el
  intervalo ya no es creíble. El prior se fija con conocimiento previo o con datos de otro sitio.
- **Regularizar sin saber que estás siendo bayesiano.** `Ridge(alpha=1)` y `Lasso(alpha=0,1)` son
  priors normal y Laplace. Si no lo tienes presente, no puedes escalar `alpha` correctamente cuando
  cambias las unidades de las variables… y los resultados se vuelven incomparables.

:::nota
El MAP no es invariante ante reparametrizaciones: si `θ̂` es el MAP de `θ`, entonces `g(θ̂)` **no**
tiene por qué ser el MAP de `g(θ)`. La media del posterior sí se transforma bien. Es una de las
razones por las que en estadística bayesiana se prefiere reportar el posterior completo antes que un
único punto.
:::

:::practica
enunciado: Lanzas una moneda 8 veces y salen 6 caras y 2 cruces. Tu prior es Beta(5, 5), centrado en 0,5. Calcula el posterior, el MLE y el MAP, y di cuánto arrastra el prior hacia 0,5.
pista: La Beta es conjugada de la binomial: suma las pseudo-cuentas del prior a las observadas. El máximo de una Beta(a, b) está en (a − 1)/(a + b − 2).
solucion: Posterior: Beta(5 + 6, 5 + 2) = Beta(11, 7). MLE: 6/8 = 0,750. MAP: (11 − 1)/(18 − 2) = 10/16 = 0,625; la media posterior es 11/18 = 0,611. El prior aporta 10 pseudo-lanzamientos frente a los 8 reales, así que pesa más que los datos y baja la estimación de 0,75 a 0,625: con tan pocos datos, la creencia previa manda.
:::

## Comprueba que lo sabes

:::quiz
p: Con prior Beta(3, 3) y una muestra de 7 caras y 3 cruces, ¿cuál es el posterior y qué estimadores salen?
o: Posterior Beta(10, 6); MLE 0,700, MAP 0,643 y media posterior 0,625
o: Posterior Beta(7, 3); MLE 0,700 y MAP 0,700
o: Posterior Beta(10, 6); MLE 0,625 y MAP 0,700
a: 1
e: La familia Beta es conjugada de la binomial: se suman las pseudo-cuentas del prior, Beta(3+7, 3+3) = Beta(10, 6). El MLE ignora el prior y da 7/10; el MAP es (10−1)/(16−2) = 0,643; la media posterior es 10/16 = 0,625.
:::

:::quiz
p: ¿Por qué la regularización L2 equivale a un prior gaussiano?
o: Porque ambos usan la misma constante de proporcionalidad
o: Porque el logaritmo de una densidad normal es proporcional a −θ², que es exactamente la penalización L2 que se suma a la log-verosimilitud en el MAP
o: Porque la normal es la única distribución con varianza finita
a: 2
e: En el MAP se maximiza ℓ(θ) + log P(θ). Con P(θ) normal centrada en cero, log P(θ) = −θ²/(2τ²) más constantes, así que el problema es minimizar la suma de cuadrados más λ·θ² con λ = σ²/τ². Cambia la normal por una Laplace y obtienes L1.
:::

:::quiz
p: Tienes 5 lanzamientos con 5 caras. ¿Qué da el MLE y qué da el MAP con un prior Beta(3, 3)?
o: MLE 1,0 y MAP 0,78, porque el prior impide llegar al extremo
o: MLE 1,0 y MAP 1,0, porque el prior no afecta a muestras pequeñas
o: MLE 0,75 y MAP 1,0, porque el MAP usa la media posterior
a: 1
e: El MLE es 5/5 = 1,0. El posterior es Beta(8, 3) y su máximo está en (8−1)/(11−2) = 7/9 = 0,778, que redondeado da 0,78; el prior desplaza la estimación hacia 0,5 y evita la afirmación absurda de que cruz es imposible. El prior nunca deja de afectar: simplemente pesa menos cuando hay más datos.
:::
