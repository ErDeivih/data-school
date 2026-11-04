---
id: diagnostico-de-residuos
titulo: Diagnóstico de residuos
fase: 5
nivel: avanzado
rutas: [ds, quant]
prerequisitos: [autocorrelacion-acf-pacf, arima-sarima, supuestos-de-la-regresion]
tags: [series-temporales, residuos, diagnostico, contrastes]
resumen: Los cuatro contrastes que se hacen después de cada ajuste (Ljung-Box, Jarque-Bera, ARCH-LM y Durbin-Watson) y cómo leer la ACF de los residuos.
fuentes: ["Box, Jenkins y Reinsel (2015), 'Time Series Analysis: Forecasting and Control'", "Ljung y Box (1978), 'On a Measure of Lack of Fit in Time Series Models'", "Jarque y Bera (1980), 'Efficient Tests for Normality, Homoscedasticity and Serial Independence of Regression Residuals'", "Engle (1982), 'Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation'", "Durbin y Watson (1951), 'Testing for Serial Correlation in Least Squares Regression I'", "Hyndman y Athanasopoulos (2021), 'Forecasting: Principles and Practice', cap. 5"]
---

## En una frase

Un modelo de series temporales se juzga por lo que deja sin explicar: si sus residuos no tienen
autocorrelación (Ljung-Box y Durbin-Watson), ni colas raras (Jarque-Bera), ni tramos de volatilidad
(ARCH-LM), es que ha recogido la estructura que había.

## La idea

Después de guisar, se prueba lo que queda en la olla. Un modelo ajustado deja un residuo por cada
observación, y ese residuo es exactamente lo que el modelo **no** ha sabido explicar. Si el modelo
ha capturado la estructura de la serie, lo que sobra tiene que ser ruido impredecible: sin memoria,
sin tramos tranquilos y violentos, sin valores extremos de más y centrado en cero. Eso es
[[autocorrelacion-acf-pacf|ruido blanco]].

El diagnóstico consiste en interrogar a ese residuo por cuatro vías distintas, porque «ruido
blanco» son cuatro afirmaciones y cada contraste ataca una:

- **¿Hay memoria?** Si el residuo de hoy se parece al de ayer, al modelo le falta un retardo.
  Lo preguntan el contraste de **Ljung-Box** (para varios retardos a la vez) y el de
  **Durbin-Watson** (solo para el retardo 1).
- **¿La forma de la distribución es razonable?** Si los residuos tienen colas muy gordas o mucha
  asimetría, las bandas de confianza y los intervalos de predicción que calcules con la fórmula
  normal estarán mal. Lo pregunta **Jarque-Bera**.
- **¿La varianza es constante?** Si hay tramos de mucha volatilidad seguidos de tramos tranquilos,
  el modelo acierta la media y falla la incertidumbre. Lo pregunta **ARCH-LM**, que es el paso
  obligatorio antes de decidir si hace falta un [[garch-volatilidad|GARCH]].

Lo importante es que **son cuatro preguntas independientes**, y contestar bien a una no dice nada
de las otras. En el código de esta página hay un ejemplo con residuos que pasan Ljung-Box con
p = 0,662 y fallan ARCH-LM con p = 0,000004: no hay autocorrelación en la serie, pero sí en su
varianza. Si solo hubieras mirado el primer contraste, habrías dado el modelo por bueno.

Y los contrastes dicen **si** queda estructura, no **dónde**. Para eso está el correlograma de los
residuos: la ACF te dice que la estructura que falta está en el retardo 4, y eso ya es una pista
sobre qué término añadir. Los dos se usan juntos: el contraste es el semáforo, el gráfico es el
mapa. Con la banda `±1,96/√n` dibujada, un pico suelto fuera de la banda a la altura del retardo
estacional es la firma de un término estacional olvidado.

:::aviso
Un residuo **no** es un error. El error es la diferencia entre el valor observado y el valor que
generaría el proceso verdadero, que no conoces. El residuo es la diferencia con el valor que
genera **tu** modelo, con los parámetros estimados a partir de esos mismos datos. Por eso los
residuos de un modelo ajustado siempre están un poco correlacionados entre sí y su varianza está
subestimada: no son una muestra independiente. Todos los contrastes de esta página son
aproximados y asintóticos, y con 30 observaciones valen bastante poco.
:::

## Definición formal

Con la serie observada `y_t` y su pronóstico a un paso `ŷ_t`, el residuo es `ê_t = y_t − ŷ_t`.

**Ljung-Box.** Contraste de que las `h` primeras autocorrelaciones son cero:

:::formula
Q = n · (n + 2) · Σ_{k=1}^{h} ρ̂_k² / (n − k)          Q ~ χ² con (h − m) grados de libertad
:::

- `n` — número de observaciones de la serie.
- `h` — número de retardos que se comprueban (el horizonte del contraste).
- `ρ̂_k` — autocorrelación de los residuos en el retardo `k`.
- `m` — número de parámetros estimados en el modelo (no se cuentan la constante ni la varianza).
- La hipótesis nula es «no hay autocorrelación hasta el retardo `h`». Un p-valor pequeño la
  rechaza. El estadístico está diseñado para que **no** haya que elegir un solo retardo: mira
  todos hasta `h` a la vez.

**Jarque-Bera.** Contraste de normalidad basado en la asimetría y la curtosis:

:::formula
JB = (n / 6) · [ S² + (K − 3)² / 4 ]          JB ~ χ² con 2 grados de libertad
:::

- `S` — asimetría de los residuos (0 en una normal).
- `K` — curtosis de los residuos (3 en una normal; lo que se compara es el exceso `K − 3`).
- La nula es «los residuos son normales». Con muchos datos, el contraste detecta desviaciones
  minúsculas: con `n = 5.000`, un exceso de curtosis de 0,17 ya cruza el umbral del 5 %
  (`JB = 6,02`), y uno de 0,20 da `JB = 8,33`.

**ARCH-LM (Engle).** Contraste de heterocedasticidad condicional. Se construye una regresión
auxiliar de los residuos al cuadrado sobre una constante y sus `q` primeros retardos:

:::formula
ê_t² = α₀ + α₁·ê_{t−1}² + … + α_q·ê_{t−q}² + u_t          LM = n · R² ~ χ² con q grados de libertad
:::

- `q` — número de retardos de la parte cuadrática.
- `R²` — coeficiente de determinación de esa regresión auxiliar.
- La nula es «no hay heterocedasticidad condicional», es decir, todos los `α` valen cero. Si se
  rechaza, la varianza tiene memoria y el modelo de la media está bien pero le falta un modelo
  para la varianza.

**Durbin-Watson.** Contraste de autocorrelación de orden 1:

:::formula
DW = Σ_{t=2}^{n} (ê_t − ê_{t−1})² / Σ_{t=1}^{n} ê_t²          DW ≈ 2 · (1 − ρ̂₁)
:::

- Vale entre 0 y 4. Alrededor de **2** significa «sin autocorrelación de orden 1»; por debajo de 2,
  autocorrelación positiva; por encima, negativa.
- La igualdad con `2·(1 − ρ̂₁)` es exacta salvo por el primer y el último residuo:
  `DW = 2 − 2·ρ̂₁ − (ê₁² + ê_n²)/Σê_t²`.
- Solo mira el retardo 1, y deja de ser válido si entre las variables explicativas hay una
  variable dependiente retardada.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `h` | Número de retardos que comprueba Ljung-Box | retardos (entero) | Más retardos cubren más estructura, pero reparten la potencia entre más términos y el contraste se vuelve más exigente. La costumbre es `h = 10` con datos no estacionales y `h = 2·m` con estacionalidad de periodo `m` (24 con datos mensuales) |
| `n` | Observaciones de la serie | observaciones | Todo se vuelve más fino: el estadístico crece con `n` y la banda `±1,96/√n` se estrecha. Con `n = 100`, un `ρ̂₁` de 0,2 no es nada; con `n = 2.000`, ese mismo 0,2 es una autocorrelación clarísima |
| `ρ̂_k` | Autocorrelación de los residuos en el retardo `k` | adimensional, entre −1 y 1 | Entra al cuadrado en Ljung-Box, así que da igual el signo: un residuo que rebota (negativo en el retardo 1) también es estructura sin recoger |
| `m` | Parámetros estimados en el modelo | parámetros (entero) | Resta grados de libertad en el contraste: `χ²_{h−m}`. Olvidarse de restarlos hace el contraste demasiado indulgente, sobre todo con `h` pequeño |
| `S` y `K` | Asimetría y curtosis de los residuos | adimensionales | Son los dos sumandos de Jarque-Bera, al cuadrado. La curtosis entra como exceso sobre 3: una `K` de 5 aporta `(5−3)²/4 = 1`, mientras una asimetría de 0,5 aporta 0,25. Son los valores extremos los que mueven la curtosis, no los del montón |
| `q` | Retardos de la parte cuadrática en ARCH-LM | retardos (entero) | Más retardos detectan memoria más larga en la varianza a cambio de potencia. Con `q = 5` se cubre una semana de datos diarios; con datos mensuales suele bastar con 12 |
| `DW` | Estadístico de Durbin-Watson | adimensional, entre 0 y 4 | Se aleja de 2 en ambos sentidos: hacia 0 si el residuo de hoy copia el de ayer, hacia 4 si lo invierte. Un `DW` de 1,2 es autocorrelación positiva clara; uno de 2,8, negativa |
| `α` | Nivel de significación de los contrastes | probabilidad (0,05 habitual) | Es el listón del p-valor. Con cuatro contrastes al 5 % sobre los mismos residuos, la probabilidad de que al menos uno rechace por puro azar ronda el 18 %: con cuatro semáforos, alguno se pone en rojo sin que haya nada |
:::

## Ejemplo

Cinco residuos de un ajuste: `1`, `−2`, `0,5`, `1` y `−0,5`.

- La suma de cuadrados es `1 + 4 + 0,25 + 1 + 0,25 = 6,5`.
- Las diferencias consecutivas son `−3`, `2,5`, `0,5` y `−1,5`, y sus cuadrados suman
  `9 + 6,25 + 0,25 + 2,25 = 17,75`.
- `DW = 17,75 / 6,5 = 2,731`. Por encima de 2: hay un poco de autocorrelación **negativa**.
- La autocorrelación del retardo 1 es `ρ̂₁ = [1·(−2) + (−2)·0,5 + 0,5·1 + 1·(−0,5)] / 6,5 =
  −3 / 6,5 = −0,4615`, y `2·(1 − ρ̂₁) = 2,923`. La diferencia con el 2,731 exacto es el primer y el
  último residuo: `(1² + 0,5²)/6,5 = 0,192`, y `2,923 − 0,192 = 2,731`. Con series largas ese
  término desaparece y las dos cuentas coinciden.
- Con `h = 1`, Ljung-Box vale `Q = 5·7·(−0,4615)²/4 = 1,864`, y el p-valor de una `χ²` con un grado
  de libertad es 0,172: con cinco residuos no se rechaza nada. Y es normal: este ejemplo enseña el
  mecanismo, no concluye nada, porque el contraste es asintótico y con `n = 5` no vale.

## Código

```python verificable
import warnings

import numpy as np
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
from statsmodels.stats.stattools import durbin_watson

# statsmodels avisa de un cambio de API futuro en het_arch; la salida se lee mejor sin el aviso.
warnings.filterwarnings("ignore", category=FutureWarning)

azar = np.random.default_rng(11)
n = 400
y = np.zeros(n)
for t in range(1, n):                       # AR(1) con phi = 0,7
    y[t] = 0.7 * y[t - 1] + azar.normal(0, 1)

r = sm.tsa.ARIMA(y, order=(1, 0, 0)).fit().resid
rho1 = sm.tsa.acf(r, nlags=1)[1]
print("Ljung-Box h=10 p", round(float(acorr_ljungbox(r, lags=[10])["lb_pvalue"].iloc[0]), 3))
# -> Ljung-Box h=10 p 0.729
print("Jarque-Bera p", round(float(stats.jarque_bera(r).pvalue), 3))
# -> Jarque-Bera p 0.239
print("ARCH-LM q=5 p", round(float(het_arch(r, nlags=5, result_object=False)[1]), 3))
# -> ARCH-LM q=5 p 0.997
print("Durbin-Watson", round(float(durbin_watson(r)), 3))       # -> Durbin-Watson 1.938
print("2(1 - rho1)", round(2 * (1 - rho1), 3))                  # -> 2(1 - rho1) 1.938
print("ACF residuos 1..4", np.round(sm.tsa.acf(r, nlags=4)[1:], 3),
      "banda", round(1.96 / np.sqrt(r.size), 3))
# -> ACF residuos 1..4 [ 0.031 -0.044  0.013  0.014] banda 0.098
```

:::claves
- `acorr_ljungbox` devuelve un **DataFrame** con una fila por retardo y las columnas `lb_stat` y `lb_pvalue`, aunque pidas un solo retardo. De ahí el `["lb_pvalue"].iloc[0]` para sacar el número: si te quedas con el DataFrame, el `round` falla con `TypeError`. Y usa por defecto tantos grados de libertad como retardos le pides, como si el modelo no hubiera estimado nada: si has ajustado un ARIMA con `p + q` parámetros, pásale `model_df=p + q`, porque sin ese ajuste el p-valor sale más alto de lo que toca.
- `het_arch` devuelve una **tupla** de cuatro elementos: estadístico, p-valor, estadístico F y su p-valor. El que se reporta es el segundo, y en statsmodels 0.15 hay que pasar `result_object=False` para que siga siendo una tupla y no aparezca un aviso de cambio de API.
- `sm.tsa.ARIMA(...).fit().resid` devuelve los residuos **en la escala del modelo** y con la misma longitud que `y`, no `n − m`. Ese detalle importa al calcular la banda `±1,96/√n`: si usas `n` menos los parámetros, la banda sale más ancha de lo que toca.
- `sm.tsa.acf(r, nlags=1)` devuelve un array de **dos** valores: el retardo 0 (que siempre vale 1) y el retardo 1, así que se indexa con `[1]`. Es el fallo más común al comparar `DW` con `2(1−ρ̂₁)`, porque `nlags=1` no significa «un valor», significa «hasta el retardo 1».
- `stats.jarque_bera` viene de **scipy**, no de statsmodels, y devuelve un objeto con `.statistic` y `.pvalue`. El de statsmodels, `statsmodels.stats.stattools.jarque_bera`, devuelve una tupla con los cuatro momentos: son implementaciones distintas y conviene no mezclarlas en el mismo informe.
- `durbin_watson(r)` no devuelve ningún p-valor: solo calcula el estadístico. La decisión de si 1,8 es aceptable se toma con tablas o con la regla de «entre 1,5 y 2,5, razonable», que es una convención y no un contraste. Y `warnings.filterwarnings("ignore", category=FutureWarning)` está ahí porque statsmodels anuncia un cambio de API y avisa en cada llamada: en un script de análisis se puede silenciar, en una librería propia no.
:::

```python verificable
import warnings

import numpy as np
import statsmodels.api as sm
from scipy import stats
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch

warnings.filterwarnings("ignore", category=FutureWarning)
n = 400

# (1) El modelo se ha dejado fuera una media movil estacional: e_t + 0,6 * e_{t-4}.
azar = np.random.default_rng(11)
e = azar.normal(0, 1, n + 10)
y = np.zeros(n + 10)
for t in range(1, n + 10):
    y[t] = 0.7 * y[t - 1] + e[t] + 0.6 * e[t - 4]
r = sm.tsa.ARIMA(y[10:], order=(1, 0, 0)).fit().resid
print("MA(4) escondida -> Ljung-Box p %.2e" % float(acorr_ljungbox(r, lags=[10])["lb_pvalue"].iloc[0]))
# -> MA(4) escondida -> Ljung-Box p 1.06e-13
print("  ACF de los residuos 1..5", np.round(sm.tsa.acf(r, nlags=5)[1:], 3))
# ->   ACF de los residuos 1..5 [-0.024 -0.135  0.015  0.403 -0.004]
print("  banda del 95%", round(1.96 / np.sqrt(r.size), 3))      # ->   banda del 95% 0.098
print("  ARCH-LM p", round(float(het_arch(r, nlags=5, result_object=False)[1]), 3))
# ->   ARCH-LM p 0.211

# (2) Ruido blanco en la media, pero con la volatilidad agrupada: GARCH(1,1).
azar2 = np.random.default_rng(4)
z = azar2.normal(0, 1, n)
s2 = np.ones(n)
for t in range(1, n):
    s2[t] = 0.3 + 0.5 * s2[t - 1] + 0.4 * z[t - 1] ** 2
r2 = sm.tsa.ARIMA(np.sqrt(s2) * z, order=(1, 0, 0)).fit().resid
print("GARCH escondido -> Ljung-Box p", round(float(acorr_ljungbox(r2, lags=[10])["lb_pvalue"].iloc[0]), 3))
# -> GARCH escondido -> Ljung-Box p 0.662
print("  Jarque-Bera p %.2e" % float(stats.jarque_bera(r2).pvalue))
# ->   Jarque-Bera p 2.65e-03
print("  ARCH-LM p %.2e" % float(het_arch(r2, nlags=5, result_object=False)[1]))
# ->   ARCH-LM p 4.25e-06
print("  ACF de los cuadrados 1..5", np.round(sm.tsa.acf(r2 ** 2, nlags=5)[1:], 3))
# ->   ACF de los cuadrados 1..5 [ 0.234 -0.004 -0.015  0.131  0.002]
```

:::claves
- Los dos bloques simulan datos, y cada simulación tiene **su propia semilla** (`default_rng(11)` y `default_rng(4)`). Si compartieran generador, la segunda serie dependería de cuántos números hubiera consumido la primera y los resultados dejarían de ser reproducibles al cambiar una línea de arriba.
- `y[10:]` descarta los diez primeros valores. La recursión arranca en cero, así que esos diez puntos arrastran el valor inicial: sin descartarlos, los residuos del principio no son estacionarios y la ACF sale sesgada.
- Para que la volatilidad agrupada sea **estacionaria** hace falta `α + β < 1`, aquí `0,4 + 0,5 = 0,9`. Con `α + β = 1` la varianza es integrada y la serie se dispara; el contraste ARCH-LM seguirá detectando algo, pero el modelo GARCH que ajustes después no convergerá bien.
- Fíjate en que el segundo caso **pasa** Ljung-Box (0,662) y **falla** ARCH-LM (4,25e-06). No es una contradicción: la media de la serie es ruido blanco y la varianza no. Los contrastes miden cosas distintas sobre los mismos residuos.
- `r2 ** 2` eleva al cuadrado residuo a residuo, y la ACF de esos cuadrados es la versión dibujada del contraste ARCH-LM. Su primer retardo, 0,234, está muy por encima de la banda de 0,098: la varianza de hoy depende de la de ayer.
- `%.2e` imprime en notación científica porque `round(1.06e-13, 3)` daría 0,0 y parecería que el contraste no ha detectado nada. Cuando un p-valor es diminuto, se reporta en escala logarítmica o científica, nunca redondeado a dos decimales.
:::

:::figura
fichero: diagnostico-de-residuos-acf
pie: La ACF de los residuos de dos modelos ajustados a series simuladas de 400 puntos, con la banda ±1,96/√n en rojo. A la izquierda, el modelo correcto: todas las barras dentro de la banda, el residuo no tiene memoria y Ljung-Box da p = 0,729. A la derecha, un modelo al que le falta un término de media móvil estacional de orden 4: la barra del retardo 4 se sale de la banda con 0,403, y Ljung-Box da p = 1,06e-13. El contraste dice que queda estructura y el correlograma dice exactamente en qué retardo está, que es lo que necesitas para saber qué término añadir.
fuente: figuras/diagnostico-de-residuos-1.py
:::

:::figura
fichero: diagnostico-de-residuos-volatilidad
pie: Residuos de una serie que es ruido blanco en la media pero tiene la volatilidad agrupada. A la izquierda, los residuos en el tiempo: no hay tendencia ni memoria en el signo, pero sí zonas de temblor y zonas planas, que es justo lo que Ljung-Box no ve (p = 0,662). A la derecha, la ACF de los residuos al cuadrado: el retardo 1 vale 0,234, muy por encima de la banda de 0,098, y el de Jarque-Bera sale 2,65e-03 porque los días de mucha volatilidad dejan valores extremos. ARCH-LM resume esa memoria de la varianza con p = 4,25e-06 y es lo que decide si hace falta un GARCH.
fuente: figuras/diagnostico-de-residuos-2.py
:::

## Errores típicos

- **Mirar solo el p-valor y no el correlograma.** Un p-valor de 0,06 en Ljung-Box con un pico claro
  en el retardo 12 no significa «no hay nada»: significa que el contraste, con ese `h`, no ha
  llegado a reunir evidencia suficiente. El gráfico te dice dónde mirar.
- **Aplicar Ljung-Box a la serie en vez de a los residuos.** Sobre una serie con tendencia rechaza
  siempre, y eso no informa de nada: lo que se contrasta es lo que el modelo no ha explicado.
- **Usar Durbin-Watson con la variable dependiente retardada en el modelo.** Si entre las
  explicativas hay un `y_{t−1}`, el estadístico se sesga hacia 2 y deja de detectar la
  autocorrelación. Ahí se usa el contraste de Breusch-Godfrey, que es el caso general.
- **Elegir mal las dos cifras de Ljung-Box: `h` y los grados de libertad.** Con `h` demasiado
  pequeño no ves la estructura estacional, y con `h` del orden de `n/4` el contraste pierde toda la
  potencia; para datos mensuales, `h = 24` recoge los dos ciclos anuales. Y los grados de libertad
  son `h − m`, con `m` los parámetros estimados: con un ARIMA de seis parámetros y `h = 10` quedan
  4, así que usar 10 hace el contraste demasiado indulgente y te deja pasar residuos con estructura.
- **Dar el modelo por bueno porque los contrastes pasan.** Cada contraste solo ve la alternativa
  para la que está diseñado. Un cambio de régimen, una no linealidad o un valor atípico pueden
  pasar los cuatro y seguir arruinando el pronóstico. Los contrastes descartan; no confirman.
- **Encadenar contrastes sin corregir por comparaciones múltiples.** Con cuatro contrastes al 5 %,
  la probabilidad de que alguno salga significativo por azar es de aproximadamente el 18 %. Si vas
  a decidir con el más extremo, baja el nivel o repite el análisis en otra muestra.

:::trampa
Un p-valor de Jarque-Bera de 0,001 en una serie de 5.000 puntos casi siempre significa «hay mucha
muestra», no «los residuos son raros». El contraste es asintótico y su potencia crece con `n`: con
datos suficientes detecta un exceso de curtosis de 0,2, que no cambia ninguna predicción. Antes de
tocar el modelo, mira la curtosis estimada y el gráfico de cuantiles: si la desviación es pequeña,
lo que hay que corregir es la confianza que pones en los intervalos, no el modelo entero.
:::

:::practica
enunciado: Un ARIMA(1,1,1) ajustado a 240 observaciones mensuales da Ljung-Box con h = 24 y p = 0,002, ACF de los residuos con un pico de 0,31 en el retardo 12 y p = 0,04 en el retardo 24, Jarque-Bera p = 0,21 y ARCH-LM con q = 12 y p = 0,0003. ¿Qué harías, en qué orden, y qué grados de libertad tiene el contraste?
pista: Mira primero qué contraste falla con más claridad y en qué retardo está el pico de la ACF. La banda con n = 240 es ±0,127.
solucion: Los dos picos caen exactamente en los múltiplos del periodo estacional (12 y 24) y valen 0,31 y 0,04; el primero está muy por encima de la banda de 0,127, así que falta estructura estacional: el modelo debería ser un SARIMA con parte estacional, no un ARIMA. Los grados de libertad del contraste son h menos los parámetros que consume el modelo, 24 − 2 = 22, porque un ARIMA(1,1,1) estima un coeficiente autorregresivo y uno de media móvil (la diferencia no añade parámetros y la varianza no se cuenta). En statsmodels eso se pide con el argumento model_df=2; si no lo pasas, el contraste usa 24 grados de libertad y resulta algo indulgente. Jarque-Bera no da problema y ARCH-LM sí (p = 0,0003), así que después de arreglar la parte estacional hay que volver a mirar los residuos y probablemente ajustar un GARCH sobre la varianza, reestimando antes el modelo de la media.
:::

## Comprueba que lo sabes

:::quiz
p: Los residuos de tu modelo dan Ljung-Box con p = 0,662 y ARCH-LM con p = 0,000004. ¿Qué significa?
o: Que los contrastes se contradicen y hay un error en el código
o: Que la media de la serie no tiene memoria, pero la varianza sí: el modelo está bien para el nivel y le falta un modelo para la volatilidad
o: Que el modelo es correcto porque Ljung-Box es el contraste importante
a: 2
e: Los dos contrastes miran cosas distintas sobre los mismos residuos. Ljung-Box comprueba si el residuo se parece a sí mismo; ARCH-LM comprueba si su cuadrado se parece a sí mismo. Una serie puede ser impredecible en el signo y muy predecible en la magnitud, que es exactamente lo que pasa con la volatilidad financiera.
:::

:::quiz
p: ¿Por qué el estadístico de Durbin-Watson no es válido si el modelo incluye la variable dependiente retardada entre las explicativas?
o: Porque entonces el estadístico se sesga hacia 2 y deja de detectar la autocorrelación que hay
o: Porque con un retardo el estadístico vale siempre exactamente 2
o: Porque Durbin-Watson solo funciona con regresión lineal simple
a: 1
e: Con un `y_{t−1}` entre las variables explicativas, el residuo y el regresor están correlacionados y la distribución del estadístico se desplaza hacia el valor 2, que es justo el que indica «no hay autocorrelación». El resultado es que el contraste se vuelve ciego. La alternativa es el contraste de Breusch-Godfrey, que admite retardos de la variable dependiente y varios órdenes de autocorrelación.
:::

:::quiz
p: Con 5.000 observaciones, Jarque-Bera da p = 0,001 y la curtosis de los residuos es 3,2. ¿Qué concluyes?
o: Que hay que cambiar el modelo, porque los residuos no son normales
o: Que la desviación de la normalidad es minúscula y lo que hay que ajustar es la confianza en los intervalos de predicción, no el modelo de la media
o: Que hay 5.000 errores en los datos
a: 2
e: El contraste es asintótico y su potencia crece con la muestra: con 5.000 datos detecta cualquier desviación, por pequeña que sea. Una curtosis de 3,2 en vez de 3 apenas mueve las colas, así que no cambia las predicciones puntuales. Lo que sí cambia es que los intervalos calculados con la fórmula normal serán algo estrechos, y eso se corrige con intervalos empíricos o por bootstrap.
:::

:::nota
El diagnóstico se hace **después de cada ajuste**, y también después de cada cambio: si añades un
término estacional, vuelve a mirar los residuos. Y hazlo en el mismo orden en el que has
transformado la serie: si el modelo trabaja con diferencias, los residuos que se contrastan son
los de las diferencias, no los de los niveles.
:::
