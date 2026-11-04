---
id: construccion-de-carteras
titulo: Construcción de carteras
fase: 9
nivel: avanzado
rutas: [quant, ds]
prerequisitos: [covarianza-y-correlacion, tamano-de-posicion, correlacion-pearson-spearman]
tags: [cartera, correlacion, capital, diversificacion]
resumen: Combinar varias estrategias o activos con pesos decididos, de forma que el conjunto tenga mejor relación entre rentabilidad y riesgo que cualquiera de las partes.
fuentes: ["López de Prado (2016), 'Building Diversified Portfolios that Outperform Out of Sample'", "Chincarini y Kim (2006), 'Quantitative Equity Portfolio Management'"]
---

## En una frase

Construir una cartera es decidir qué peso le das a cada estrategia o activo, y el objetivo no es
sumar rentabilidades: es repartir el riesgo de forma que el conjunto se comporte mejor que
cualquiera de sus piezas por separado.

## La idea

Esta es la única comida gratis que hay en finanzas. Tienes dos estrategias, cada una con una
rentabilidad esperada del 10 % y una volatilidad del 20 % anual. Por separado, cada una tiene un
[[ratio-de-sharpe]] de 0,5. Si las combinas al 50 % y su correlación es 0,2, la cartera tiene la
misma rentabilidad esperada (10 %) y una volatilidad del 15,49 %: el Sharpe sube a 0,645. Has
mejorado el resultado sin mejorar ninguna de las dos estrategias. Solo por combinarlas.

¿De dónde sale esa mejora? De que las dos no se mueven a la vez. Cuando una pierde, la otra
puede estar ganando, y los retrocesos se compensan parcialmente. Cuanto menor sea la
correlación, mayor es el regalo: con correlación 0 la volatilidad baja al 14,14 % y el Sharpe a
0,707; con correlación 1 no hay regalo ninguno y la cartera es una copia de la estrategia
individual.

Aquí aparece la primera confusión que hay que deshacer: **el peso en capital no es el peso en
riesgo**. Si pones el 50 % del dinero en una estrategia del 20 % de volatilidad y el 50 % en una
del 10 %, no estás repartiendo el riesgo a medias. La volátil aporta tres cuartas partes del
riesgo total. Repartir riesgo (risk parity) es un problema distinto de repartir dinero, y es la
razón de que existan [[risk-parity-y-hrp]].

La segunda confusión es creer que el número de estrategias es el número de apuestas. Si tienes
diez estrategias que ganan y pierden con el mismo mercado, tienes una apuesta con diez nombres.
La medida honesta es cuántas apuestas **independientes** tienes de verdad, y eso se calcula con
los autovalores de la matriz de correlación.

Y la tercera: las correlaciones no son constantes. En un día tranquilo tu cartera parece muy
diversificada; en una crisis, casi todo cae a la vez y las correlaciones suben hacia 1 justo
cuando necesitarías que fueran bajas.

## Definición formal

Con `w` el vector de pesos, `μ` el vector de rentabilidades esperadas y `Σ` la matriz de
covarianzas:

:::formula
μ_p = wᵀ μ          σ_p² = wᵀ Σ w          Sharpe_p = (μ_p − Rf) / σ_p
:::

- `w` — pesos de cada estrategia en la cartera; suman 1 si no hay apalancamiento.
- `μ` — rentabilidad esperada de cada estrategia, en el mismo horizonte.
- `Σ` — matriz de covarianzas: en la diagonal las varianzas y fuera de ella las covarianzas.
- `Rf` — rentabilidad del activo libre de riesgo.

**Caso de dos estrategias con la misma volatilidad.** Si las dos tienen volatilidad `σ`, la
misma `Sharpe = S` y correlación `ρ`, la cartera al 50 % tiene:

:::formula
σ_p = σ · √( (1 + ρ) / 2 )          Sharpe_p = S · √( 2 / (1 + ρ) )
:::

Ese factor `√(2 / (1 + ρ))` es la mejora exacta: con `ρ = 0` vale 1,41; con `ρ = 0,5` vale
1,15; con `ρ = 1` vale 1. **La diversificación se mide por la correlación, no por el número de
posiciones.**

**Reparto del riesgo.** La contribución de cada estrategia al riesgo total de la cartera es:

:::formula
RC_i = w_i · (Σ w)_i / σ_p          suma de RC_i = σ_p
:::

**Número efectivo de apuestas.** Con los autovalores `λ₁ … λ_N` de la matriz de correlación:

:::formula
ENB = ( Σ λ_i )² / Σ λ_i²
:::

Vale `N` cuando todas las correlaciones son cero y vale 1 cuando todas son 1. Es la forma más
limpia de responder a «¿cuántas apuestas tengo de verdad?».

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `w` | Pesos de cada estrategia en la cartera; suman 1 si no hay apalancamiento | tanto por uno | Es la decisión, no un dato. Mueve la rentabilidad esperada de forma lineal (`wᵀμ`) y el riesgo de forma cuadrática (`wᵀΣw`), así que el efecto sobre el Sharpe no es simétrico |
| `μ` | Rentabilidad esperada de cada estrategia en el mismo horizonte | tanto por uno por periodo | Entra en el numerador del Sharpe, pero se estima con muchísimo error: el optimizador que usa `μ` acaba concentrando la cartera en el activo que tuvo mejor suerte en la muestra |
| `Σ` | Matriz de covarianzas: las varianzas en la diagonal y las covarianzas fuera | tanto por uno al cuadrado | Es lo que hace que la cartera no sea una media: si `Σ` fuese diagonal, la volatilidad sería la media ponderada. Las covarianzas son las que regalan la reducción |
| `σ_p` | Volatilidad de la cartera, `√(wᵀΣw)` | tanto por uno por periodo | Es la raíz de una forma cuadrática, así que **siempre sale menor o igual** que la media ponderada de las volatilidades, salvo con correlación 1. Ese hueco es la única comida gratis |
| `Rf` | Rentabilidad del activo libre de riesgo | tanto por uno por periodo | Se resta en el numerador del Sharpe. Con tipos altos, una estrategia que parecía buena deja de serlo sin que su comportamiento haya cambiado |
| `ρ` | Correlación entre las estrategias | adimensional, entre −1 y 1 | Es la variable que decide de verdad, no el número de estrategias. El factor de mejora es `√(2/(1+ρ))`: vale 1,41 con correlación 0 y 1 exacto con correlación 1 |
| `RC_i` | Contribución de la estrategia `i` al riesgo de la cartera, `w_i·(Σw)_i/σ_p` | tanto por uno por periodo | Las `RC_i` suman exactamente `σ_p`, así que se pueden leer como un reparto. Con pesos 50/50 y volatilidades 20 % y 10 %, la primera se lleva el 75,9 % del riesgo |
| `λ_i` | Autovalores de la matriz de correlación | adimensional | Resumen toda la estructura de dependencias. Si todas las correlaciones son cero valen 1 y el ENB sale `N`; si todas son 1, uno de ellos vale `N` y el resto 0, y el ENB cae a 1 |
| `ENB` | Número efectivo de apuestas: `(Σλ_i)² / Σλ_i²` | apuestas | Es cuántas apuestas independientes equivalen a tu cartera. Diez estrategias con correlación 0,2 dan 7,35; con correlación 0,5, poco más de 3. Nunca sube al añadir una estrategia correlacionada con las que ya tienes |
:::

## Ejemplo

Dos estrategias con `μ = 10 %`, `σ = 20 %` y 50 % de capital en cada una:

| Correlación ρ | Volatilidad cartera | Sharpe | Mejora |
| --- | --- | --- | --- |
| 0,0 | 14,14 % | 0,707 | ×1,414 |
| 0,2 | 15,49 % | 0,645 | ×1,291 |
| 0,6 | 17,89 % | 0,559 | ×1,118 |
| 1,0 | 20,00 % | 0,500 | ×1,000 |

Con una tercera estrategia igual y la misma correlación media de 0,2, la volatilidad baja al
13,66 % y el Sharpe sube a 0,732. Pero fíjate en el detalle: las tres estrategias no te dan tres
apuestas independientes. Con `N = 3` y `ρ = 0,2`, el número efectivo de apuestas es **2,78**; con
`N = 10` y la misma correlación, **7,35**. Diez estrategias, siete apuestas y pico.

Ahora el reparto de riesgo, que es donde más gente se equivoca. Dos estrategias con
volatilidades del 20 % y del 10 %, correlación 0,2 y **mitad de capital en cada una**:

- Volatilidad de la cartera: 12,04 %.
- Contribución al riesgo de la primera: 9,13 puntos porcentuales.
- Contribución al riesgo de la segunda: 2,91 puntos porcentuales.

La primera aporta el **75,9 %** del riesgo con la mitad del dinero. Si tu intención era repartir
el riesgo a medias, el 50/50 en capital no lo consigue ni de lejos.

:::figura
fichero: carteras-diversificacion-riesgo-y-apuestas
pie: Arriba a la izquierda, la única comida gratis: la volatilidad de la cartera baja al 15,49 % con una correlación de 0,2 y al 14,14 % con correlación cero, mientras que una estrategia sola se queda en el 20 % (la raya gris). El hueco entre la raya y la curva es rentabilidad que no has tenido que ganar. Arriba a la derecha se ve el mismo efecto en el capital: las tres series tienen la misma media muestral, un 10 % anual, y lo único que cambia es el camino. Abajo a la izquierda está el error más común: con el 50 % del dinero en cada una, la estrategia del 20 % se lleva el 75,9 % del riesgo, porque **el peso en capital no es el peso en riesgo**. Y abajo a la derecha, la cuenta honesta de cuántas apuestas tienes: diez estrategias con correlación 0,2 son 7,35 apuestas y la línea de puntos marca lo que serían si fueran independientes.
fuente: figuras/construccion-de-carteras-1.py
:::

## Código

```python verificable
import numpy as np

mu = np.array([0.10, 0.10])        # rentabilidad esperada anual de cada estrategia
sigma = np.array([0.20, 0.20])     # volatilidad anual de cada una
w = np.array([0.5, 0.5])           # mitad de capital en cada una

for rho in (0.0, 0.2, 0.6, 1.0):
    cov = np.array([[sigma[0] ** 2, rho * sigma[0] * sigma[1]],
                    [rho * sigma[0] * sigma[1], sigma[1] ** 2]])
    sigma_p = float(np.sqrt(w @ cov @ w))
    print(f"rho {rho:.1f}  sigma {sigma_p:.2%}  Sharpe {float(w @ mu) / sigma_p:.3f}")
# -> rho 0.2  sigma 15.49%  Sharpe 0.645
# -> rho 0.0  sigma 14.14%  Sharpe 0.707

# Tres estrategias iguales con la misma correlacion media: menos de tres apuestas.
n, rho = 3, 0.2
sigma_p3 = 0.20 * np.sqrt(1 / n + rho * (n - 1) / n)
print(f"tres estrategias sigma {sigma_p3:.2%}  Sharpe {0.10 / sigma_p3:.3f}")
# -> tres estrategias sigma 13.66%  Sharpe 0.732
```

:::claves
- `w @ cov @ w` es una forma cuadrática y devuelve un **escalar** (la varianza de la cartera), no un vector. Si `w` fuese una matriz de pesos por activo, el mismo producto daría una matriz y `np.sqrt` sobre ella otra matriz: el código seguiría corriendo y el resultado ya no sería una volatilidad.
- La matriz `cov` es de **covarianzas**, no de correlaciones: lleva `sigma[0]**2 = 0,04` en la diagonal, no 1. Meter la correlación directamente daría una «varianza» de 0,5 y una volatilidad de cartera de 0,71, sin ningún error por el camino.
- El término de fuera de la diagonal es `rho * sigma[0] * sigma[1]`, no `rho`. Es el error que más se cuela al escribir la matriz a mano: si pones solo `rho`, la volatilidad sale mucho más baja de lo que es y la diversificación parece mejor de lo que es.
- `float(...)` convierte el escalar de NumPy en un `float` de Python. Sin él todo se imprime igual, pero al guardar en JSON o al comparar tipos el comportamiento cambia, y `np.float64` no es serializable por defecto.
- `float(w @ mu) / sigma_p` es el Sharpe solo si `mu` está ya en exceso del activo sin riesgo. Si `mu` es rentabilidad bruta, el número sale inflado y compara mal entre periodos con tipos distintos.
- `cov` se reconstruye dentro del bucle a partir de `rho`, así que la matriz de fuera del bucle no se usa en ninguna vuelta. Mover esas dos líneas fuera del `for` no cambia el resultado en este caso, pero sí lo cambiaría si `sigma` dependiera de `rho`.
:::

```python verificable
import numpy as np

# Reparto del riesgo: mitad de capital no es mitad de riesgo.
w = np.array([0.5, 0.5])
sigmas = np.array([0.20, 0.10])
rho = 0.2
cov = np.outer(sigmas, sigmas) * np.array([[1.0, rho], [rho, 1.0]])

sigma_p = float(np.sqrt(w @ cov @ w))
rc = w * (cov @ w) / sigma_p          # contribucion de cada estrategia al riesgo
print(f"sigma cartera {sigma_p:.2%}")                       # -> sigma cartera 12.04%
print(f"reparto del riesgo {rc[0] / sigma_p:.1%} y {rc[1] / sigma_p:.1%}")   # -> 75.9% y 24.1%

# Numero efectivo de apuestas con los autovalores de la correlacion.
for n in (3, 10):
    corr = np.full((n, n), 0.2)
    np.fill_diagonal(corr, 1.0)
    autovalores = np.linalg.eigvalsh(corr)
    print(f"N={n:>2}  apuestas efectivas {autovalores.sum() ** 2 / (autovalores ** 2).sum():.2f}")
# -> N= 3  apuestas efectivas 2.78
# -> N=10  apuestas efectivas 7.35
```

```python ilustrativo
import numpy as np
import pandas as pd
from scipy.cluster import hierarchy

# HRP (Lopez de Prado): agrupa por correlacion y reparte riesgo por el arbol.
retornos = pd.read_parquet("retornos_estrategias.parquet")     # datos externos
corr = retornos.corr()
distancia = np.sqrt(0.5 * (1 - corr))

enlace = hierarchy.linkage(distancia, method="single")
orden = hierarchy.leaves_list(hierarchy.optimal_leaf_ordering(enlace, distancia))
print(retornos.columns[orden])
```

## Errores típicos

- **Contar estrategias y no apuestas.** Diez estrategias con correlación 0,2 son 7,35 apuestas
  independientes, no diez. Y si todas van en la misma dirección de mercado, son una. El número
  efectivo de apuestas es la cifra que hay que mirar.
- **Ponderar por capital y llamarlo diversificación.** El reparto 50/50 del ejemplo deja el
  75,9 % del riesgo en una sola estrategia. Si quieres repartir riesgo, tienes que calcular la
  contribución al riesgo, no el peso.
- **Estimar las correlaciones en un régimen tranquilo.** Las correlaciones suben en las crisis,
  y lo hacen justo cuando tienes la cartera construida. Contrasta siempre el resultado con una
  matriz de correlaciones «de estrés» en la que todo esté entre 0,7 y 0,9.
- **Rebalancear sin contar los costes.** Volver a los pesos objetivos cada mes genera
  operaciones; en estrategias con muchos activos, el coste se come la mejora teórica de la
  diversificación ([[rebalanceo]]).
- **Añadir una estrategia por su Sharpe calculado con pocos datos.** Un Sharpe de 1,5 medido en
  seis meses es ruido. Meterlo en la cartera con un peso alto es meter ruido con peso alto, y el
  error de estimación de la media domina cualquier beneficio de diversificación.
- **Optimizar los pesos con las medias estimadas.** Es el problema que trata
  [[markowitz-y-frontera]]: la media muestral es tan ruidosa que el optimizador acaba
  concentrando la cartera en el activo que tuvo mejor suerte en la muestra. Con pocos datos,
  métodos que no usan `μ` (risk parity, HRP, pesos iguales) suelen batirlo fuera de muestra.

:::practica
enunciado: Tres estrategias con un 8 % de rentabilidad esperada y un 18 % de volatilidad anual cada una, con correlación media 0,25 entre todos los pares. Calcula la volatilidad y el Sharpe de la cartera a partes iguales, y el número efectivo de apuestas.
pista: Con N iguales y correlación media ρ, la volatilidad sale de σ · raíz(1/N + ρ(N−1)/N); el ENB, de los autovalores.
solucion: Con N = 3 y ρ = 0,25: 0,18 · raíz(1/3 + 0,25 · 2/3) = 0,18 · 0,7071 = 12,73 %. El Sharpe de cada estrategia suelta es 8/18 = 0,44, y el de la cartera 8/12,73 = 0,63: un 41 % mejor sin tocar ninguna de las tres. Los autovalores de la correlación son 1,5, 0,75 y 0,75: ENB = 3² / (2,25 + 0,5625 + 0,5625) = 9/3,375 = 2,67. Con tres estrategias tienes 2,67 apuestas.
:::

## Comprueba que lo sabes

:::quiz
p: Dos estrategias tienen cada una un Sharpe de 0,5 y una correlación de 0. ¿Qué Sharpe tiene la cartera al 50 %?
o: 0,5, porque el Sharpe de la cartera es la media de los Sharpes
o: 0,707, porque el factor de mejora es la raíz de 2 cuando la correlación es nula
o: 1,0, porque el riesgo se cancela por completo
a: 2
e: El factor de mejora es √(2/(1+ρ)), que con ρ = 0 vale √2 = 1,414; 0,5 × 1,414 = 0,707. El Sharpe de una cartera no es la media de los Sharpes: la volatilidad se reduce por la diversificación mientras la rentabilidad esperada se mantiene.
:::

:::quiz
p: Pones el 50 % del capital en una estrategia con un 20 % de volatilidad y el 50 % en otra con un 10 %, con correlación 0,2. ¿Qué proporción del riesgo aporta la primera?
o: El 50 %, porque el capital está repartido a partes iguales
o: Cerca del 76 %, porque su contribución al riesgo es proporcional al peso por su volatilidad
o: El 66 %, porque su volatilidad es el doble
a: 2
e: La contribución al riesgo es w_i·(Σw)_i/σ_p: la primera aporta 9,13 de los 12,04 puntos de volatilidad, un 75,9 %. El 66 % sale de repartir la suma de volatilidades ponderadas (10 de 15) e ignorar la correlación; con correlación nula la proporción subiría todavía más, hasta el 80 %.
:::

:::quiz
p: Tienes 10 estrategias con una correlación media de 0,2 y un número efectivo de apuestas de 7,35. ¿Qué significa?
o: Que 7,35 de las 10 estrategias son rentables
o: Que la cartera se comporta como si tuviera unas 7 apuestas independientes, no 10
o: Que puedes eliminar 2,65 estrategias sin que cambie nada
a: 2
e: El ENB mide cuántas apuestas independientes equivalen a tu cartera en términos de riesgo, usando los autovalores de la matriz de correlación. No dice nada sobre la rentabilidad de cada estrategia ni sobre cuáles puedes eliminar.
:::
