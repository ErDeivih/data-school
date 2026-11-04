---
id: alpha-y-beta
titulo: Alpha y beta
fase: 9
nivel: intermedio
rutas: [quant, ds]
prerequisitos: [regresion-lineal, correlacion-pearson-spearman, varianza-y-desviacion, valor-esperado]
tags: [cartera, regresion, atribucion]
resumen: Beta es lo que tu estrategia se mueve con el mercado y alpha lo que queda cuando descuentas esa parte; sin el error típico, el alpha no dice nada.
fuentes: ["Sharpe (1964), 'Capital Asset Prices: A Theory of Market Equilibrium under Conditions of Risk'", "Grinold y Kahn (1999), 'Active Portfolio Management'"]
---

## En una frase

Beta mide cuánto se mueve tu estrategia por cada punto que se mueve el mercado, y alpha es el
rendimiento medio que sobra después de descontar esa parte: sin beta no puedes saber si el
30 % que ganaste fue habilidad o simplemente una apuesta grande al mercado.

## La idea

Imagina una gestora con dos fondos. El año pasado el mercado subió un 20 %. El fondo A ganó
un 30 % y el fondo B ganó un 12 %. ¿Quién lo hizo mejor? La pregunta no tiene respuesta hasta
saber cuánto riesgo de mercado llevaba cada uno. Si A tenía beta 1,5, el mercado explica
1,5 · 20 % = 30 % de su rentabilidad: no añadió nada, solo apalancó. Si B tenía beta 0,5, el
mercado explica 0,5 · 20 % = 10 %, y su 12 % deja un 2 % que el mercado no explica. El fondo
que ganó menos es el que aportó algo propio.

Ese «algo propio» es el alpha, y esa exposición al mercado es la beta. Juntas salen de una
sola regresión: se toman los retornos de tu estrategia en exceso del activo sin riesgo y se
enfrentan a los del mercado, también en exceso. La pendiente de esa recta es la beta y el
término independiente es el alpha.

Beta tiene una lectura directa: es el multiplicador. Beta 1 significa que te mueves como el
índice; beta 0,5, la mitad; beta 2, el doble en ambas direcciones (también cuando cae); beta
0, que tu estrategia no tiene relación lineal con el mercado; beta negativa, que tiende a
subir cuando el mercado baja, lo que es raro y valioso pero difícil de sostener mucho tiempo.
La beta de una cartera es la media ponderada de las betas de sus posiciones, y por eso puedes
regular tu exposición simplemente moviendo pesos o vendiendo contratos de índice.

El alpha es el número del que todo el mundo presume y el que casi nunca se calcula bien.
Primero, porque un alpha es una **media de residuos**, y una media sin su error típico no
informa de nada: un 0,2 % mensual con cinco observaciones es ruido puro. Segundo, porque
alpha y beta se estiman con datos pasados en una ventana concreta: cambia la ventana, cambia
el índice de referencia o cambia el régimen de mercado, y los dos números se mueven. Un alpha
positivo medido en la misma muestra en la que probaste veinte variantes de la estrategia está
sesgado hacia arriba por construcción, y eso es exactamente lo que corrige
[[sharpe-deflactado|el ajuste por pruebas múltiples]].

Hay un tercer uso, menos lucido y muy práctico: **neutralizar**. Si conoces tu beta, puedes
vender esa cantidad de índice y quedarte solo con el alpha. Eso convierte «una apuesta
direccional con suerte» en una estrategia cuyo resultado no depende de si el mercado sube o
baja, que es lo que permite comparar y escalar. El precio es que si tu alpha era en realidad
mercado disfrazado, al cubrir la beta te quedas con la volatilidad y sin la rentabilidad.

## Definición formal

Con retornos en exceso del activo libre de riesgo ([[ratio-de-sharpe|el Sharpe]] explica por
qué se resta el tipo sin riesgo), el modelo de un factor se escribe:

:::formula
r_{i,t} − r_{f,t} = α_i + β_i · (r_{m,t} − r_{f,t}) + ε_{i,t}
:::

- `r_{i,t}` — retorno de tu estrategia en el periodo `t` (en tanto por uno).
- `r_{m,t}` — retorno del mercado o índice de referencia en el mismo periodo.
- `r_{f,t}` — retorno del activo libre de riesgo en el mismo periodo.
- `β_i` — beta: pendiente de la regresión, cuánto acompaña tu estrategia al mercado.
- `α_i` — alpha: término independiente, retorno medio que el mercado no explica.
- `ε_{i,t}` — residuo: la parte de tu retorno que el modelo no captura en ese periodo.

Los estimadores por mínimos cuadrados tienen forma cerrada:

:::formula
β_i = Cov(r_i, r_m) / Var(r_m)          α_i = media(r_i − r_f) − β_i · media(r_m − r_f)
:::

- `Cov(r_i, r_m)` — covarianza entre los retornos de la estrategia y los del mercado.
- `Var(r_m)` — varianza de los retornos del mercado.
- La beta es, por tanto, una correlación reescalada: `β = ρ · σ_i / σ_m`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `r_{i,t}` | Retorno de tu estrategia en el periodo `t`, ya en exceso del activo sin riesgo | tanto por uno por periodo | Cambiar de retorno bruto a exceso no es un detalle: si no restas `r_f`, el término independiente absorbe el tipo sin riesgo y el alpha deja de ser comparable entre periodos con tipos distintos |
| `r_{m,t}` | Retorno del índice de referencia en el mismo periodo | tanto por uno por periodo | Cambiar de índice cambia la beta y el alpha a la vez. Una beta contra el S&P 500 con datos diarios no es comparable con una contra el IBEX calculada con datos mensuales |
| `r_{f,t}` | Retorno del activo libre de riesgo en ese periodo | tanto por uno por periodo | Es lo que se resta en los dos lados. Si el tipo sube y tú no lo restas, el alpha aparente sube sin que hayas hecho nada distinto |
| `β_i` | La pendiente: cuánto se mueve tu cartera por cada punto del mercado | adimensional | Multiplica el movimiento del mercado en los dos sentidos. Beta 2 con un mercado que cae un 30 % te deja un −60 %; beta 0,5 te deja la mitad del recorrido. Una beta negativa da al revés y parece un desastre en un mercado alcista |
| `α_i` | La ordenada: el retorno medio que el mercado no explica | tanto por uno por periodo | Es el resultado que se presume, y **no** se escala con la beta: se suma tal cual a la parte de mercado. Ojo con las unidades: un 0,2 % mensual compuesto es `(1,002)^12 − 1 = 2,43 %` anual, no un 2,4 % por multiplicar por 12 |
| `ε_{i,t}` | El residuo: la parte del retorno que el modelo no captura en ese periodo | tanto por uno por periodo | Su dispersión es la que fija el error típico del alpha. Si los residuos tienen la media distinta de cero, el modelo está mal especificado: mínimos cuadrados los deja sumando cero por construcción |
| `n` | Número de observaciones de la ventana de estimación | observaciones | Es el parámetro que casi nadie reporta y el que decide si el alpha significa algo: `SE(α)` baja como `1/√n`, así que con 5 observaciones un alpha de 0,2 % es ruido y con 120 puede ser señal |
| `s` | Desviación típica de los residuos (el error típico de la regresión) | tanto por uno por periodo | Divide en `n − 2` y no en `n`: se han gastado dos grados de libertad en estimar `α` y `β`. Es el numerador de `SE(α)`, así que más ruido alrededor de la recta, menos confianza en el alpha |
| `x̄` | Media del exceso de retorno del mercado en la ventana | tanto por uno por periodo | Entra **al cuadrado** en `SE(α)`: si la ventana tiene el mercado muy lejos de cero (una racha alcista fuerte), el error típico del alpha crece y el mismo alpha sale menos significativo |
| `t = α / SE(α)` | El estadístico del contraste de «¿este alpha es distinto de cero?» | adimensional | Por debajo de 2 no se puede afirmar nada. Sube si el alpha sube, si el ruido baja o si la muestra crece, y esas tres cosas no son intercambiables |
| `w_j` | Peso de la posición `j` en la cartera, con `Σ w_j = 1` | tanto por uno | La beta de la cartera es `Σ w_j · β_j`: mover pesos hacia los activos de beta alta sube la beta de toda la cartera. Si los pesos no suman 1, la fórmula deja de ser una media ponderada |
:::

**Beta de una cartera.** Con pesos `w_j` que suman 1 y betas `β_j`:

:::formula
β_cartera = Σ_j w_j · β_j
:::

**Alpha anualizado.** Si `α` es mensual, el alpha compuesto del año es
`(1 + α)^12 − 1`; multiplicar por 12 da una aproximación aceptable solo para valores
pequeños.

**Significatividad.** El contraste habitual es `t = α / SE(α)`, con
`SE(α) = s · √(1/n + x̄² / Σ(x_t − x̄)²)`, donde `s` es la desviación típica de los residuos,
`n` el número de observaciones y `x̄` la media del exceso de retorno del mercado. Un `t` por
debajo de 2 no permite afirmar que el alpha sea distinto de cero.

:::figura
fichero: alpha-y-beta-pendiente-y-altura
pie: En la izquierda, la misma nube de puntos con dos rectas: la pendiente es la beta y el hueco vertical entre las dos rectas justo encima del cero es el alpha. La cartera azul gana más en un mercado que sube, pero no aporta nada propio; la verde se mueve la mitad y arranca dos puntos por encima. En la derecha está el aviso: la estrategia morada se construyó con alpha cero de verdad y su beta estimada es 2, así que el ETF apalancado consigue lo mismo sin ninguna habilidad. Cuando una estrategia gana mucho, lo primero que hay que mirar es si existe ese ETF.
fuente: figuras/alpha-y-beta-1.py
:::

## Ejemplo

Cinco observaciones mensuales, en porcentaje, ya como exceso sobre el tipo sin riesgo:

| Mes | Exceso del mercado | Exceso de la cartera |
| --- | --- | --- |
| 1 | +2 | +3 |
| 2 | −1 | −2 |
| 3 | +3 | +4 |
| 4 | 0 | +1 |
| 5 | +1 | +2 |
| Media | +1,0 | +1,6 |

Se calcula a mano. Las desviaciones del mercado respecto a su media (1,0) son +1, −2, +2, −1
y 0; las de la cartera respecto a su media (1,6) son +1,4, −3,6, +2,4, −0,6 y +0,4.

- Suma de productos: (1 · 1,4) + (−2 · −3,6) + (2 · 2,4) + (−1 · −0,6) + (0 · 0,4) = 1,4 + 7,2
  + 4,8 + 0,6 + 0 = **14,0**.
- Suma de cuadrados del mercado: 1 + 4 + 4 + 1 + 0 = **10,0**.
- **Beta** = 14,0 / 10,0 = **1,40**.
- **Alpha** = 1,6 − 1,40 · 1,0 = **+0,20 % mensual**.
- Si ese alpha se mantuviera, el anual sería (1,002)¹² − 1 = **2,43 %**.

Y ahora la parte que casi nadie hace. La suma de cuadrados de la cartera es 21,2 y la de los
residuos 1,6, así que el R² es 1 − 1,6 / 21,2 = **92,5 %**: casi todo el movimiento de la
cartera es mercado. La desviación típica de los residuos es `√(1,6 / 3) = 0,73` puntos, y el
error típico del alpha, `0,73 · √(0,2 + 0,1) = 0,40` puntos. El estadístico es
`t = 0,20 / 0,40 = 0,50`: con cinco meses, ese alpha del 0,20 % mensual es **indistinguible de
cero**. La conclusión honesta no es «tengo alpha», es «no tengo datos suficientes para
decirlo».

## Código

```python verificable
import numpy as np

mercado = np.array([0.02, -0.01, 0.03, 0.00, 0.01])   # ya en exceso del activo sin riesgo
cartera = np.array([0.03, -0.02, 0.04, 0.01, 0.02])

beta, alpha = np.polyfit(mercado, cartera, 1)          # pendiente y ordenada en el origen
residuo = cartera - (alpha + beta * mercado)
n = mercado.size

s = np.sqrt((residuo ** 2).sum() / (n - 2))            # error tipico de la regresion
se_alpha = s * np.sqrt(1 / n + mercado.mean() ** 2 / ((mercado - mercado.mean()) ** 2).sum())
r2 = 1 - (residuo ** 2).sum() / ((cartera - cartera.mean()) ** 2).sum()

print(f"beta       {beta:.2f}")                 # -> 1.40
print(f"alpha      {alpha * 100:+.2f} %/mes")   # -> +0.20 %/mes
print(f"R2         {r2:.3f}")                   # -> 0.925
print(f"t de alpha {alpha / se_alpha:.2f}")     # -> 0.50
```

:::claves
- `beta, alpha = np.polyfit(mercado, cartera, 1)` funciona, pero el orden de la tupla es al revés de como se lee una recta: **primero la pendiente y después la ordenada**. Si escribes `alpha, beta = np.polyfit(...)` el código no protesta —las dos variables son números— y tu alpha pasa a ser 1,40 y tu beta 0,20. Es el error más silencioso de todo el bloque.
- `np.polyfit` **no** devuelve error típico, ni `R²`, ni nada más que los coeficientes. Por eso el código vuelve a calcular a mano `s`, `se_alpha` y `r2`: aquí `np.polyfit` es solo un atajo de mínimos cuadrados y toda la estadística del alpha está fuera de él. Si necesitas los errores típicos de una vez, el camino es `statsmodels` o montar la matriz de diseño.
- La división es `(n - 2)` y no `n` ni `n - 1`: se han estimado dos parámetros (pendiente y ordenada), así que quedan `n − 2` grados de libertad. Con 5 observaciones eso es dividir entre 3 en lugar de entre 5, y esa diferencia es justo la que hace que el error típico del alpha sea grande y el `t` salga 0,50.
- `residuo ** 2).sum()` eleva al cuadrado **elemento a elemento** y luego suma. Escribir `residuo ** 2` no cambia `residuo`, pero `residuo.sort()` o `residuo += 1` sí lo harían: los arrays de NumPy son mutables y las operaciones con `=` no siempre copian. Aquí no hay riesgo porque se crea un array temporal, pero conviene saberlo antes de reutilizar la variable.
- `mercado.mean() ** 2` es la media **al cuadrado**, no la media de los cuadrados. En `SE(α)` aparece `x̄²`, y confundirlo con `Σ x²/n` es un error de álgebra que cambia el error típico sin que salte ninguna excepción: el resultado sigue siendo un número plausible.
- El segundo bloque encadena la misma semilla para el mercado y para el ruido de la estrategia, así que las dos series están relacionadas por construcción. Cambiar `default_rng(11)` por otra semilla mueve el acumulado del mercado y el de la estrategia a la vez: las cifras comentadas en la página solo se reproducen con esa semilla y con ese orden de llamadas.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(11)
meses = 120
mercado = rng.normal(0.008, 0.04, meses)                 # mercado alcista: +0,8 % mensual
estrategia = 2.0 * mercado + rng.normal(0, 0.02, meses)  # beta 2 y alpha 0 de verdad

beta, alpha = np.polyfit(mercado, estrategia, 1)
acum_mercado = (np.prod(1 + mercado) - 1) * 100
acum_estrategia = (np.prod(1 + estrategia) - 1) * 100

print(f"acumulado del mercado    {acum_mercado:.1f} %")      # -> 185.2 %
print(f"acumulado de la estrategia {acum_estrategia:.1f} %")  # -> 514.6 %
print(f"beta {beta:.2f}  alpha mensual {alpha * 100:+.2f} %")  # -> beta 2.06  alpha mensual -0.11 %
```

La estrategia multiplica el resultado del mercado por casi tres y aun así su alpha estimado
es **negativo**. Lo único que hizo fue llevar beta 2 en un mercado que subió: genial para el
que la vendió como «estrategia», ruido para quien mire el alpha.

## Errores típicos

- **Llamar alpha a cualquier exceso de rentabilidad.** Si no has estimado la beta, no sabes
  cuánto de ese exceso es mercado. Con beta 1,5 y un mercado que sube un 20 %, ganar un 30 %
  es exactamente lo esperado, ni un punto más.
- **Reportar el alpha sin su error típico ni el número de observaciones.** Un `+0,2 %`
  mensual con `t = 0,5` no es evidencia de nada. Da siempre `α`, `SE(α)` y `n`, o directamente
  el intervalo de confianza.
- **Estimar beta en la misma muestra en la que elegiste la estrategia.** Si probaste veinte
  configuraciones y publicas la de mejor alpha, ese alpha está sesgado al alza. Separa muestra
  de estimación y de validación, o aplica [[data-snooping-y-multiple-testing|el ajuste por
  pruebas múltiples]].
- **Suponer que la beta es una constante del activo.** Cambia con la ventana de estimación,
  con el índice de referencia y con el régimen de mercado: una empresa cíclica tiene betas
  distintas en expansión y en recesión. Una beta estimada con 12 meses puede ser 1,8 y con 60
  meses 1,1, y una beta contra el S&P 500 con datos diarios no es comparable con una contra el
  IBEX calculada con datos mensuales.
- **Calcular el alpha con retornos brutos en vez de excesos.** Si no restas el tipo sin
  riesgo, el término independiente absorbe ese tipo y el alpha deja de ser comparable entre
  periodos con tipos distintos. Es el mismo error que invalida un Sharpe mal calculado.
- **Confundir beta alta con buena estrategia.** Beta 2 amplifica en los dos sentidos: en un
  mercado que cae un 30 %, tu cartera cae un 60 %. Y una beta negativa parece un desastre en
  un mercado alcista aunque esté haciendo justo lo que le pediste.

:::practica
enunciado: Cuatro meses de excesos sobre el activo sin riesgo, en porcentaje. Mercado: +3, −2, +1, −2. Cartera: +5, −2, +1, −3. Estima beta y alpha, y di qué parte del resultado es mercado y qué parte es propia.
pista: Beta es la covarianza dividida entre la varianza del mercado; alpha, la media de la cartera menos beta por la media del mercado.
solucion: Medias: mercado 0,0 y cartera +0,25. Σ(x − x̄)(y − ȳ) = 26 y Σ(x − x̄)² = 18, luego β = 26 / 18 = 1,44 y α = 0,25 − 1,44 · 0 = +0,25 % mensual. El R² es 1 − 1,19 / 38,75 = 0,97: el 97 % del movimiento de la cartera es mercado. Compuesto, ese alpha daría (1,0025)¹² − 1 = 3,04 % anual, pero con cuatro meses no se distingue de cero.
:::

## Comprueba que lo sabes

:::quiz
p: Una estrategia tiene beta 1,4 y un alpha mensual de 0,5 %. Si el próximo mes el mercado sube un 2 %, ¿qué retorno esperas, según el modelo?
o: 0,5 % + 1,4 · 2 % = 3,3 %
o: 1,4 · 2 % = 2,8 %, el alpha no entra en la predicción puntual del modelo
o: 0,5 % · 1,4 + 2 % = 2,7 %
a: 1
e: El modelo es exceso de la estrategia igual a alpha más beta por exceso del mercado, así que la predicción es 0,5 % + 2,8 % = 3,3 %. Multiplicar el alpha por la beta o sumar los términos sin ponderar son errores de álgebra: el alpha es aditivo y no se escala con el mercado.
:::

:::quiz
p: ¿Qué significa que el t del alpha sea 0,5 con 5 observaciones?
o: Que el alpha es positivo pero pequeño
o: Que el alpha estimado es compatible con el ruido: no hay evidencia de que sea distinto de cero
o: Que la beta está mal estimada y hay que rehacer la regresión
a: 2
e: Un t de 0,5 significa que el alpha estimado está a media desviación típica de cero, así que el intervalo de confianza incluye valores negativos y positivos con holgura. No dice que la beta esté mal: la beta puede estar perfectamente estimada y aun así no haber muestra para separar el alpha del ruido.
:::

:::quiz
p: Una cartera lleva el 60 % en un fondo con beta 1,5 y el 40 % en otro con beta 0,5. ¿Cuál es su beta?
o: 1,00
o: 1,10
o: 2,00
a: 2
e: La beta de una cartera es la media ponderada: 0,6 · 1,5 + 0,4 · 0,5 = 0,9 + 0,2 = 1,10. El 1,00 saldría de promediar sin ponderar o de suponer que los pesos son iguales, y el 2,00 de sumar las betas en lugar de ponderarlas.
:::
