---
id: markowitz-y-frontera
titulo: Markowitz y la frontera eficiente
fase: 9
nivel: avanzado
rutas: [quant, ds]
prerequisitos: [varianza-y-desviacion, covarianza-y-correlacion, optimizacion-con-restricciones]
tags: [cartera, optimizacion, media-varianza, diversificacion]
resumen: Para cada nivel de riesgo, la cartera con más rentabilidad esperada: la frontera eficiente, por qué es bonita en teoría y por qué se resiste en la práctica.
fuentes: ["Markowitz (1952), 'Portfolio Selection'", "Michaud (1989), 'The Markowitz Optimization Enigma: Is Optimized Optimal?'"]
---

## En una frase

La frontera eficiente es el conjunto de carteras que, para cada nivel de riesgo, dan la máxima
rentabilidad esperada posible; cualquier cartera por debajo de esa curva está desperdiciando
diversificación.

## La idea

Supón que tienes dos activos. El primero da un 8 % con una volatilidad del 15 %; el segundo da un
12 % con una volatilidad del 25 %. Ninguno de los dos domina al otro: uno da más rentabilidad y
el otro es más tranquilo. Lo interesante es que **la mezcla de los dos puede ser mejor que
cualquiera de ellos por separado**, siempre que no estén perfectamente correlacionados.

De ahí sale la idea central de Markowitz: el problema del inversor no es elegir el mejor activo,
sino elegir la mejor **combinación**. Si representas cada cartera posible como un punto en un
plano con la volatilidad en el eje horizontal y la rentabilidad esperada en el vertical, los
puntos eficientes forman una curva: la frontera. Por debajo de ella están las carteras mal
construidas; por encima no hay nada alcanzable con esos activos.

Si añades un activo libre de riesgo (letras del Tesoro, por ejemplo), aparece una recta que sale
de ese punto y toca la frontera en un único punto: la **cartera tangente**. Esa cartera es la de
máximo [[ratio-de-sharpe]], y la recta es la frontera completa cuando puedes mezclar la cartera
tangente con el activo sin riesgo. Es el resultado más elegante de la teoría de carteras: toda
la decisión se separa en dos partes independientes —qué cartera de riesgo tener (la tangente) y
cuánto poner en ella frente al activo sin riesgo—. Eso se llama separación en dos fondos.

Y ahora la parte que los folletos no cuentan. La fórmula necesita dos entradas: las
rentabilidades esperadas `μ` y la matriz de covarianzas `Σ`. `Σ` se estima razonablemente bien con
datos históricos; `μ` no se estima bien de ninguna manera. El resultado es que el optimizador
hace exactamente lo que le pides con datos ruidosos: concentra la cartera en los activos que
tuvieron mejor suerte en la muestra. Ese fenómeno tiene nombre (maximización del error) y explica
por qué la optimización de media-varianza a pelo suele funcionar peor fuera de muestra que
repartir el dinero a partes iguales.

## Definición formal

Con `w` los pesos, `μ` las rentabilidades esperadas y `Σ` la matriz de covarianzas, la cartera de
mínima varianza para una rentabilidad objetivo `μ_obj` es la solución de:

:::formula
mín over w de wᵀ Σ w    sujeto a    wᵀ μ = μ_obj    y    wᵀ 1 = 1
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `w` | Vector de pesos, uno por activo | tanto por uno, suman 1 | Más peso en ese activo: sube su aportación al riesgo y a la rentabilidad |
| `μ` | Rentabilidades esperadas de cada activo | % por periodo (el mismo en todos) | La frontera entera se desplaza hacia arriba: el mismo riesgo da más rentabilidad |
| `Σ` | Matriz de covarianzas entre los activos | % al cuadrado | La frontera se ensancha: para el mismo riesgo objetivo hay menos rentabilidad |
| `μ_obj` | Rentabilidad que se exige a la cartera | % por periodo | La cartera se mueve hacia arriba en la curva, con más volatilidad |
| `Rf` | Rentabilidad del activo sin riesgo | % anual | Sube el listón del Sharpe y la cartera tangente se acerca al activo de más rentabilidad |
| `ρ` | Correlación entre dos activos | adimensional, entre −1 y 1 | Menos diversificación: la cartera de mínima varianza se pega al activo menos volátil |
:::

- `w` — vector de pesos, uno por activo. La restricción `wᵀ 1 = 1` exige que sumen 1.
- `μ` — vector de rentabilidades esperadas por periodo.
- `Σ` — matriz de covarianzas, simétrica y (si no hay redundancias) definida positiva.
- `μ_obj` — rentabilidad objetivo que se recorre para dibujar toda la frontera.

**Caso de dos activos.** Con `σ₁`, `σ₂` y correlación `ρ`, la cartera de mínima varianza pone en
el primer activo:

:::formula
w₁* = ( σ₂² − ρ σ₁ σ₂ ) / ( σ₁² + σ₂² − 2 ρ σ₁ σ₂ )
:::

**Cartera tangente.** Con un activo libre de riesgo de rentabilidad `Rf`, la cartera de máximo
Sharpe es proporcional a:

:::formula
w ∝ Σ⁻¹ ( μ − Rf · 1 )
:::

normalizando después para que los pesos sumen 1. La recta que une el activo sin riesgo con esa
cartera es la línea de asignación de capital:

:::formula
μ_p = Rf + Sharpe_tan · σ_p
:::

:::aviso
`Σ⁻¹` es el corazón de la fórmula y también su punto débil. Si dos activos están muy
correlacionados, la matriz está casi singular y su inversa amplifica el ruido hasta producir
pesos absurdos (grandes y de signo alterno). Por eso en la práctica se imponen restricciones
(prohibido vender en corto, tope del 20 % por activo), se regulariza la matriz o se encoge hacia
una versión más estable.
:::

:::figura
fichero: markowitz-frontera-y-ruido
pie: A la izquierda, el plano riesgo-rentabilidad de tres activos: cada punto de la nube es una cartera con pesos al azar, la curva azul es la frontera (todo lo que está por debajo está mal combinado) y la recta verde es la línea que sale del activo sin riesgo y toca la frontera en la cartera tangente, la de máximo Sharpe. A la derecha, el peso «óptimo» del activo A calculado con 36 meses de datos, repetido 2.000 veces: en un 30 % de las muestras sale negativo y en un 16 % se va tan lejos que ni cabe en el dibujo, con pesos de cinco cifras. El estimador no está sesgado —su centro es el valor verdadero, 0,38—, pero su dispersión es enorme: eso es la maximización del error.
fuente: figuras/markowitz-y-frontera-1.py
:::

## Ejemplo

Dos activos: A con `μ = 8 %` y `σ = 15 %`; B con `μ = 12 %` y `σ = 25 %`; correlación `ρ = 0,3`.
Tipo sin riesgo del 2 %.

**Cartera de mínima varianza.** Aplicando la fórmula:

- `w₁* = (0,0625 − 0,3 · 0,15 · 0,25) / (0,0225 + 0,0625 − 2 · 0,3 · 0,15 · 0,25)`
- `w₁* = (0,0625 − 0,01125) / (0,085 − 0,0225) = 0,05125 / 0,0625 = 0,82`.

Es decir, **82 % en A y 18 % en B**. Esa cartera tiene `μ = 8,72 %` y `σ = 14,31 %`. Compárala
con A en solitario: 8 % de rentabilidad y 15 % de volatilidad. La mezcla da **más rentabilidad y
menos riesgo** que el activo conservador. Eso es la diversificación en estado puro.

**Cartera tangente.** Resolviendo `Σ⁻¹ (μ − Rf)` y normalizando salen pesos de **0,625 en A y
0,375 en B**, con `μ = 9,50 %`, `σ = 15,12 %` y un Sharpe de **0,496**. Cada activo por separado
tiene un Sharpe de 0,400: la cartera mejora un 24 % el Sharpe sin cambiar
ninguna expectativa sobre los activos.

**Y ahora el problema.** Con tres años de datos mensuales (36 observaciones) para estimar esos
parámetros:

| Parámetro | Valor | Error típico | Error relativo |
| --- | --- | --- | --- |
| Rentabilidad media anual | 8 % | 8,66 % | 108 % |
| Volatilidad anual | 15 % | 1,77 % | 12 % |

El error típico de la media es **mayor que la propia media**. El de la volatilidad es una octava
parte de su valor. Traducido: la volatilidad la conoces, la rentabilidad esperada no. Y la
frontera depende críticamente de `μ`. Por eso los pesos «óptimos» calculados con datos reales
rebotan de un mes a otro y por eso mucha gente prefiere métodos que no usan `μ` en absoluto,
como [[risk-parity-y-hrp]].

## Código

```python verificable
import numpy as np

mu = np.array([0.08, 0.12])                # rentabilidad esperada anual
sigma = np.array([0.15, 0.25])             # volatilidad anual
rho = 0.30
cov = np.array([[sigma[0] ** 2, rho * sigma[0] * sigma[1]],
                [rho * sigma[0] * sigma[1], sigma[1] ** 2]])

# Peso de varianza minima en el primer activo (formula cerrada de dos activos).
w1 = (sigma[1] ** 2 - rho * sigma[0] * sigma[1]) / (
    sigma[0] ** 2 + sigma[1] ** 2 - 2 * rho * sigma[0] * sigma[1])

def resumen(pesos):
    return float(pesos @ mu), float(np.sqrt(pesos @ cov @ pesos))

mu_min, sigma_min = resumen(np.array([w1, 1 - w1]))
print(f"varianza minima pesos {w1:.3f} y {1 - w1:.3f}  mu {mu_min:.2%}  sigma {sigma_min:.2%}")
# -> varianza minima pesos 0.820 y 0.180  mu 8.72%  sigma 14.31%

# Cartera tangente con tipo sin riesgo del 2 %: maximiza el Sharpe.
rf = 0.02
w_tan = np.linalg.solve(cov, mu - rf)
w_tan = w_tan / w_tan.sum()
mu_tan, sigma_tan = resumen(w_tan)
print(f"tangente pesos {w_tan[0]:.3f} y {w_tan[1]:.3f}  mu {mu_tan:.2%}  sigma {sigma_tan:.2%}")
# -> tangente pesos 0.625 y 0.375  mu 9.50%  sigma 15.12%
print(f"Sharpe tangente {((mu_tan - rf) / sigma_tan):.3f}")     # -> 0.496
print(f"Sharpe de A {((mu[0] - rf) / sigma[0]):.3f} y de B {((mu[1] - rf) / sigma[1]):.3f}")
# -> Sharpe de A 0.400 y de B 0.400
```

:::claves
- `np.linalg.solve(cov, mu - rf)` devuelve **pesos sin normalizar**: la fórmula da una dirección, no una cartera, y hay que dividir entre la suma. Tampoco avisa si `cov` está casi singular: con dos activos muy correlacionados devuelve números enormes y de signo alterno sin decir nada.
- `pesos @ cov @ pesos` es la **varianza**, no la volatilidad: falta la raíz cuadrada. El `@` va encadenado de izquierda a derecha y el resultado es un escalar, así que `np.sqrt(pesos @ cov @ pesos)` es la volatilidad que va al eje horizontal.
- Anualizar no es multiplicar todo por lo mismo: la rentabilidad media se multiplica por 12 (o 252) y la volatilidad por `√12` (o `√252`). Si anualizas la volatilidad con el factor de la media, el Sharpe sale 3,46 veces más pequeño de lo que es.
- `.mean()` y `.var()` de NumPy dividen entre `n` (`ddof=0` por defecto) y `.cov()` de pandas entre `n − 1` (`ddof=1`). Con 36 meses esa diferencia se nota en los pesos; mezclar los dos criterios en el mismo cálculo mete un sesgo que no está en ningún libro.
- `minimize(...).x` es un `np.array` de floats **sin etiquetas**: no sabes qué peso corresponde a qué activo. Para leerlo hay que envolverlo, `pd.Series(pesos, index=retornos.columns)`, y ordenarlo; si no, el error típico es ejecutar la cartera con los activos cambiados.
:::

```python verificable
import numpy as np

# Con cuantos datos se estima cada parametro: tres anos de retornos mensuales.
sigma_anual, mu_anual, meses = 0.15, 0.08, 36
sigma_mes = sigma_anual / np.sqrt(12)

# La media se anualiza sumando 12 meses; la volatilidad, multiplicando por sqrt(12).
error_media = 12 * sigma_mes / np.sqrt(meses)
error_vol = sigma_anual / np.sqrt(2 * meses)

print(f"error tipico de la media {error_media:.2%} sobre una media de {mu_anual:.0%}")
# -> error tipico de la media 8.66% sobre una media de 8%
print(f"error tipico de la volatilidad {error_vol:.2%} sobre {sigma_anual:.0%}")
# -> error tipico de la volatilidad 1.77% sobre 15%
print(f"error relativo de la media {error_media / mu_anual:.0%}")          # -> 108%
print(f"error relativo de la volatilidad {error_vol / sigma_anual:.0%}")  # -> 12%
```

```python ilustrativo
import numpy as np
import pandas as pd
from scipy.optimize import minimize

# Optimizacion con restricciones sobre datos reales: el flujo de trabajo habitual.
retornos = pd.read_parquet("retornos_activos.parquet")     # datos externos
mu = retornos.mean().values * 252
cov = retornos.cov().values * 252
n = mu.size

def neg_sharpe(w, mu, cov, rf=0.02):
    return -((w @ mu - rf) / np.sqrt(w @ cov @ w))

restricciones = ({"type": "eq", "fun": lambda w: w.sum() - 1},)
limites = [(0.0, 0.20)] * n          # sin cortos y tope del 20 % por activo

# Las restricciones son lo que impide que el optimizador se vuelva loco con el ruido.
pesos = minimize(neg_sharpe, np.full(n, 1 / n), args=(mu, cov),
                 bounds=limites, constraints=restricciones).x
print(pd.Series(pesos, index=retornos.columns).round(3).sort_values(ascending=False))
```

## Errores típicos

- **Optimizar con las medias muestrales y creerte los pesos.** Es la maximización del error: el
  optimizador concentra la cartera en el activo con mejor media en la muestra, que suele ser el
  que tuvo suerte. Con 36 meses de datos, el error típico de `μ` es del 108 % de su valor.
- **Estimar `Σ` en un periodo tranquilo y usarla como si fuera estable.** Las volatilidades y,
  sobre todo, las correlaciones cambian de régimen. Una cartera «diversificada» construida con
  correlaciones de mercado alcista puede ser una sola apuesta en la siguiente crisis.
- **Confundir la frontera con una predicción.** La frontera describe combinaciones, no resultados
  futuros: dice «si estas `μ` y `Σ` fueran las verdaderas, esta cartera sería eficiente». Si las
  entradas están mal, la conclusión también.
- **Optimizar sin restricciones.** Sin tope por activo y sin prohibir los cortos, la solución
  matemática contiene pesos negativos enormes y apuestas contra activos concretos que casi nadie
  puede ni quiere ejecutar. Mira [[optimizacion-con-restricciones]].
- **Ignorar el coste del rebalanceo.** Los pesos óptimos cambian con cada nueva estimación, así
  que seguirlos al pie de la letra genera operaciones constantes; los costes se comen la mejora
  teórica ([[rebalanceo]]).
- **Creer que media y varianza resumen el riesgo.** La media-varianza trata igual una ganancia
  extrema y una pérdida extrema y no ve la asimetría ni las colas gruesas. Con estrategias de
  opciones o activos ilíquidos, el CVaR describe mejor lo que te preocupa
  ([[var-y-cvar]]).

:::practica
enunciado: Activo A con 10 % de rentabilidad y 18 % de volatilidad; activo B con 10 % y 30 %; correlación 0,25. Calcula los pesos de la cartera de mínima varianza, su volatilidad y su rentabilidad.
pista: Con dos activos, w₁* = (σ₂² − ρσ₁σ₂) / (σ₁² + σ₂² − 2ρσ₁σ₂), y la varianza lleva el término cruzado 2w₁w₂ρσ₁σ₂.
solucion: σ₁² = 0,0324, σ₂² = 0,09 y ρσ₁σ₂ = 0,0135. Entonces w₁* = (0,09 − 0,0135) / (0,0324 + 0,09 − 0,027) = 0,0765 / 0,0954 = 0,802, y w₂* = 0,198. La varianza es 0,802² · 0,0324 + 0,198² · 0,09 + 2 · 0,802 · 0,198 · 0,0135 = 0,028656, luego la volatilidad es 16,93 % y la rentabilidad sigue siendo 10 %. La mezcla baja la volatilidad de A del 18 % al 16,93 % sin renunciar a nada: eso es la diversificación.
:::

## Comprueba que lo sabes

:::quiz
p: Dos activos: A con 8 % de rentabilidad y 15 % de volatilidad, B con 12 % y 25 %, correlación 0,3. La cartera de mínima varianza (82 % en A, 18 % en B) tiene 8,72 % de rentabilidad y 14,31 % de volatilidad. ¿Qué conclusión sacas?
o: Que es una cartera peor que A, porque tiene más volatilidad que el 8 % de rentabilidad
o: Que la mezcla domina a A: da más rentabilidad y menos riesgo que el activo conservador por separado
o: Que es imposible, porque una cartera nunca puede tener menos volatilidad que su activo menos volátil
a: 2
e: Es posible precisamente porque la correlación es 0,3 y no 1: al combinar activos imperfectamente correlacionados, la varianza de la cartera no es la media ponderada de las varianzas. Con correlación 1 la cartera estaría siempre sobre la recta que une A y B, y entonces sí sería cierto que no bajaría del 15 %.
:::

:::quiz
p: ¿Por qué la cartera tangente es el punto más útil de la frontera?
o: Porque es la que tiene la volatilidad más baja de todas
o: Porque es la de máximo Sharpe y, mezclada con el activo sin riesgo, genera toda la recta de carteras eficientes
o: Porque es la que reparte el capital a partes iguales entre los activos
a: 2
e: La tangente maximiza (μ_p − Rf) / σ_p. Cualquier combinación de esa cartera con el activo sin riesgo está sobre la recta que sale de Rf y es tangente a la frontera, y esa recta domina a cualquier cartera que no la use. La de mínima volatilidad es otro punto de la frontera.
:::

:::quiz
p: Con tres años de datos mensuales, el error típico de la rentabilidad media anual es del orden del 8,7 % y el de la volatilidad del 1,8 %. ¿Qué implica para la optimización de carteras?
o: Que hay que usar más decimales en el cálculo de los pesos
o: Que la volatilidad se estima con bastante precisión y la media casi no, así que el optimizador amplifica el ruido de μ
o: Que la media no sirve para nada y hay que eliminarla de la fórmula
a: 2
e: El error relativo de la media (108 %) es nueve veces el de la volatilidad (12 %). Como la solución depende de μ, pequeños errores en la media producen pesos muy distintos: es la maximización del error. Por eso se imponen restricciones, se encoge la matriz o se usan métodos que no dependen de μ.
:::

:::trampa
Si tu optimizador te devuelve una cartera con el 90 % en un solo activo y pesos negativos en el
resto, no has encontrado una oportunidad: has encontrado ruido. Antes de ejecutar nada, repite la
optimización con la matriz de covarianzas encogida, con topes por activo y con una media
constante para todos. Si el resultado cambia por completo, la cartera que te gustaba era un
artefacto de la estimación.
:::
