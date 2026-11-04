---
id: prophet-y-modelos-modernos
titulo: Prophet y modelos modernos
fase: 5
nivel: intermedio
rutas: [ds, quant]
prerequisitos: [series-temporales-componentes, suavizado-exponencial]
tags: [series-temporales, pronostico, prophet, redes]
resumen: Prophet descompone la serie en tendencia, estacionalidad y festivos; N-BEATS apila bloques densos y DeepAR aprende de muchas series. Cuándo aportan.
fuentes: ["Taylor y Letham (2018), 'Forecasting at Scale'", "Oreshkin et al. (2020), 'N-BEATS: Neural basis expansion analysis for interpretable time series forecasting'", "Salinas et al. (2020), 'DeepAR: Probabilistic forecasting with autoregressive recurrent networks'"]
---

## En una frase

Prophet ajusta una regresión legible sobre el calendario (tendencia + estacionalidad + festivos),
N-BEATS apila bloques de capas densas que restan lo que explican y suman lo que pronostican, y DeepAR
aprende de miles de series a la vez; los tres son útiles cuando el problema lo pide, y ninguno
sustituye a comprobar antes si un método simple ya te vale.

## La idea

Imagina que tienes que pronosticar la facturación mensual de una tienda. Miras la serie y ves tres
cosas a la vez: una subida lenta, un pico todos los diciembres y un bache cada Semana Santa. Un
[[suavizado-exponencial|Holt-Winters]] puede con eso, pero te obliga a decidir tú la forma del ciclo.
Prophet hace lo contrario: escribe esas tres piezas como una fórmula explícita y ajusta sus
coeficientes con los datos. El resultado es una descomposición que puedes leer y enseñar, con la
tendencia por un lado y el efecto de cada festivo por otro.

La diferencia con un [[arima-sarima|ARIMA]] no es de precisión, es de naturaleza: ARIMA modela la
dinámica, cómo se relaciona cada valor con los anteriores, mientras que Prophet **no usa los valores
pasados como predictores**, es una regresión sobre el tiempo. Si la tendencia cambia de pendiente,
coloca una rejilla de puntos de cambio candidatos y deja que la penalización apague casi todos.

Con esa idea clara, los otros dos nombres se colocan solos:

- **N-BEATS** renuncia a la recurrencia: bloques de capas densas que producen dos salidas, una que
  reconstruye la parte de la entrada que el bloque explica (*backcast*) y otra que pronostica
  (*forecast*). Cada bloque resta su explicación del residuo y el siguiente trabaja sobre lo que
  sobra. Con bases polinómicas y de Fourier el resultado se lee; con bases aprendidas, es una caja
  negra más potente.
- **DeepAR** ataca otro problema: no una serie, sino miles. Es una red recurrente que en cada paso
  produce los parámetros de una distribución (media y desviación de una normal, o el parámetro de una
  binomial negativa para conteos) y se entrena maximizando la verosimilitud de todas las series a la
  vez: una serie corta se beneficia de los patrones aprendidos en las demás.

Ese último punto decide casi siempre: **¿tienes una serie o un almacén de series?** Con una sola
serie, un modelo global no tiene de dónde aprender y compite en desventaja con Holt-Winters. Con
5.000 productos, un modelo global (DeepAR, o simplemente un [[gradient-boosting|gradient boosting]]
con retardos y variables de calendario) suele ganar a 5.000 modelos entrenados por separado, porque
comparte estructura entre series parecidas.

Y el aviso que toca dar: antes de montar nada de esto, calcula el error de un naive estacional y de un
Holt-Winters en un esquema hacia delante, no en una partición barajada
([[validacion-temporal|validación temporal]]). Si no los bates, el problema no pedía una red.

:::figura
fichero: prophet-calendario-frente-a-naive
pie: A la izquierda, los tres meses siguientes vistos por cada método: Prophet ajusta tendencia y calendario y sigue la subida, mientras el naive estacional repite los valores del año pasado y se queda diez puntos por debajo porque se deja fuera toda la deriva. A la derecha, el error cometido en cada mes: un RMSE de 2,14 frente a 10,61. La conclusión es la del capítulo: el competidor que hay que batir es un naive estacional bien medido, no una red.
fuente: figuras/prophet-y-modelos-modernos-1.py
:::

## Definición formal

**Prophet** es un modelo aditivo (con variante multiplicativa para la estacionalidad) sobre el
tiempo `t`:

:::formula
y(t) = g(t) + s(t) + h(t) + ε_t
:::

- `y(t)` — el valor observado en el instante `t`.
- `g(t)` — la tendencia: lineal a trozos, o logística cuando hay una capacidad de saturación.
- `s(t)` — la estacionalidad: anual, semanal o diaria.
- `h(t)` — el efecto de los festivos, con una variable por festivo y su ventana de días.
- `ε_t` — el error. Prophet no lo modela como serie: lo trata como ruido alrededor de la curva.

La tendencia lineal a trozos tiene `S` puntos de cambio en instantes `s_j`, cada uno con un ajuste de
pendiente `δ_j`:

:::formula
g(t) = (k + Σ_{j : s_j ≤ t} δ_j) · t + (m + Σ_{j : s_j ≤ t} γ_j)
:::

- `k` — la pendiente base, antes de cualquier cambio.
- `δ_j` — cuánto cambia la pendiente en el punto de cambio `j`.
- `m` y `γ_j` — el nivel inicial y los ajustes que mantienen la curva continua al cambiar de
  pendiente.
- Los `δ_j` se estiman con un prior de Laplace, la versión bayesiana de una penalización L1
  ([[regularizacion-l1-l2]]): la mayoría quedan en cero y solo unos pocos cambios sobreviven.
- La banda de predicción sale de simular tendencias futuras con cambios de pendiente parecidos a los
  del pasado. No es el intervalo de un modelo clásico, y se queda corta si el futuro cambia de
  régimen ([[estacionariedad]]).

La estacionalidad se escribe con una serie de Fourier de orden `N` y periodo `P`:

:::formula
s(t) = Σ_{n=1}^{N} ( a_n · cos(2πnt/P) + b_n · sin(2πnt/P) )
:::

- `P` — el periodo del ciclo: 365,25 días para el anual, 7 para el semanal.
- `N` — el número de armónicos. Con `N = 10`, la estacionalidad anual tiene 20 coeficientes; con `N`
  muy alto, el ciclo se ajusta al ruido.
- `a_n`, `b_n` — los coeficientes estimados. Cada armónico es una onda de periodo `P/n`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `y(t)` | El valor observado en el instante `t` | las de la serie (euros, unidades) | — |
| `g(t)` | La tendencia: lineal a trozos, o logística si hay capacidad de saturación | las de la serie | Es la parte que se extrapola al futuro: si sube la pendiente, el pronóstico se separa del naive estacional mes a mes |
| `s(t)` | La estacionalidad: anual, semanal o diaria | las de la serie | Cuanto más fuerte, más se repite el patrón y menos importa el nivel de hoy para el mismo mes del año que viene |
| `h(t)` | El efecto de los festivos, una variable por festivo y su ventana | las de la serie | Cada festivo añade un coeficiente, y con pocos años de historia cada uno se estima con muy pocos datos: es la parte que más se sobreajusta |
| `ε_t` | El error que Prophet no modela como serie | las de la serie | Es lo que se queda en el residuo; si tiene autocorrelación, la serie pedía un modelo autorregresivo y no una regresión sobre el calendario |
| `k` | La pendiente base, antes de cualquier cambio | las de la serie por paso | Una `k` alta proyecta una subida fuerte hacia el futuro; el modelo puede hacerlo, pero a 30 pasos la incertidumbre de esa pendiente domina el pronóstico |
| `δ_j` | Cuánto cambia la pendiente en el punto de cambio `j` | las de la serie por paso | Con un prior de Laplace la mayoría de los `δ_j` quedan en cero. Si subes la escala de ese prior, entran más cambios de pendiente y la tendencia se vuelve nerviosa y menos fiable fuera de muestra |
| `m`, `γ_j` | El nivel inicial y los ajustes que mantienen la curva continua al cambiar de pendiente | las de la serie | No se interpretan por separado: `γ_j = −s_j·δ_j` existe solo para que la recta no se rompa en el punto de cambio |
| `S` | El número de puntos de cambio candidatos | número entero | Más candidatos dan más flexibilidad y más parámetros efectivos: es la perilla que más sobreajuste esconde |
| `P` | El periodo del ciclo de la estacionalidad | pasos: 365,25 anual, 7 semanal | Fija la onda base de la serie de Fourier; equivocarlo reparte el ciclo en armónicos que no le corresponden |
| `N` | El número de armónicos de la serie de Fourier | número entero | Cada armónico añade dos coeficientes (`a_n` y `b_n`): con `N = 10` son 20 parámetros solo para la estacionalidad anual, y con `N` muy alto el ciclo se ajusta al ruido |
| `a_n`, `b_n` | Los coeficientes estimados de cada armónico | las de la serie | Un `b_n` o `a_n` grande en un armónico alto significa que la estacionalidad tiene estructura fina; si solo son grandes los de `n = 1` y `n = 2`, la estacionalidad es una onda suave |
| `L` | El número de bloques de N-BEATS | número entero | Más bloques, más capacidad y más riesgo de bajar el error de entrenamiento sin mejorar el de fuera de muestra |
| `θ^b_ℓ`, `θ^f_ℓ` | Los coeficientes de las bases de retroceso y de pronóstico del bloque `ℓ` | adimensionales | Son los pesos que se aprenden; no se leen uno a uno salvo en la configuración interpretable con base polinómica o de Fourier |
| `x_ℓ` | El residuo tras restar lo que explica el bloque `ℓ` | las de la serie normalizada | Cada bloque trabaja sobre lo que sobra del anterior: si los residuos no bajan, los bloques están repitiendo el mismo patrón |
| `h_t` | El estado oculto de la red recurrente de DeepAR | vector de números reales | Es el resumen de la historia de la serie; no se interpreta, se usa para calcular los parámetros de la distribución de salida |
| `z_t` | El valor de la serie en el paso `t` | las de la serie | En el entrenamiento se le da el valor real; en el pronóstico, el que la red ha muestreado, y de ahí salen las trayectorias que forman la banda |
| `θ(h_t)` | Los parámetros de la distribución de salida (media y desviación, o el parámetro de una binomial negativa) | los de esa distribución | Determinan la forma de la banda de predicción, no solo su centro: es la diferencia con un modelo que solo da un número |
:::

**N-BEATS** apila `L` bloques. Cada bloque `ℓ` produce dos vectores de coeficientes, `θ^b_ℓ` y
`θ^f_ℓ`, que se aplican a sendas funciones base:

:::formula
x_ℓ = x_{ℓ−1} − g^b(θ^b_ℓ)        ŷ = Σ_{ℓ=1}^{L} g^f(θ^f_ℓ)
:::

- `x_ℓ` — el residuo tras restar la parte explicada por el bloque `ℓ`; `x_0` es la entrada
  normalizada.
- `g^b` — la base de retroceso, que reconstruye la parte de la entrada que el bloque explica.
- `g^f` — la base de pronóstico. En la configuración interpretable es un polinomio o una base de
  Fourier; en la genérica, una capa lineal sin restricciones.

**DeepAR** es autorregresivo y probabilístico. Con `h_t` el estado oculto y `x_t` las covariables:

:::formula
h_t = RNN(x_{t−1}, z_{t−1}, h_{t−1})        z_t ~ p( · | θ(h_t) )
:::

- `z_t` — el valor de la serie en el paso `t`. En el entrenamiento se le da el real; en el pronóstico,
  el que la red ha muestreado.
- `θ(h_t)` — los parámetros de la distribución de salida, calculados a partir del estado oculto.
- La función objetivo suma la log-verosimilitud sobre **todas** las series, no sobre una: de ahí que
  necesite muchas series relacionadas.

## Ejemplo

Cuarenta y ocho meses de una serie construida con tendencia de +0,8 al mes, un ciclo anual de
amplitud 6 y ruido de desviación 1,5. Ajustando por mínimos cuadrados una tendencia más dos
armónicos anuales, como hace Prophet:

- Pendiente estimada: **0,798** (la real era 0,8).
- Error cuadrático medio dentro de la muestra: **1,53**, frente a una desviación del ruido de 1,5. El
  modelo captura la estructura, no el ruido.
- El naive estacional (repetir el mismo mes del año anterior) da **9,75**: ignora la tendencia, y en
  doce meses la tendencia mueve la serie 9,6 puntos. Por eso Prophet la modela de forma explícita.
- Pronóstico de los tres meses siguientes: **139,9 · 143,1 · 145,6**.

Esas seis líneas de mínimos cuadrados son el motor de Prophet. Lo que añade es la detección
automática de los cambios de pendiente, varias estacionalidades a la vez, los festivos como variables
propias y una banda de incertidumbre.

## Código

```python verificable
import numpy as np

# Serie mensual sintetica: tendencia lineal + ciclo anual, los componentes de Prophet
rng = np.random.default_rng(3)
t = np.arange(48)
y = (100 + 0.8 * t + 6 * np.sin(2 * np.pi * t / 12)
     + 2 * np.cos(2 * np.pi * t / 12) + rng.normal(0, 1.5, 48))

# Base de Fourier de periodo 12 y orden 2: la estacionalidad tal como la escribe Prophet
def diseno(t, periodo=12, k=2):
    columnas = [np.ones_like(t, dtype=float), t.astype(float)]
    for j in range(1, k + 1):
        columnas += [np.sin(2 * np.pi * j * t / periodo),
                     np.cos(2 * np.pi * j * t / periodo)]
    return np.column_stack(columnas)

beta, *_ = np.linalg.lstsq(diseno(t), y, rcond=None)
ajuste = diseno(t) @ beta
pron = diseno(np.arange(48, 51)) @ beta

print("intercepto %.2f  pendiente %.3f" % (beta[0], beta[1]))   # -> intercepto 100.05  pendiente 0.798
print("coeficientes sin1 cos1 sin2 cos2 %.2f %.2f %.2f %.2f" % tuple(beta[2:]))
# -> coeficientes sin1 cos1 sin2 cos2 5.40 2.12 -0.39 -0.52
print("RMSE del modelo %.2f" % np.sqrt(np.mean((y - ajuste) ** 2)))            # -> RMSE del modelo 1.53
print("RMSE del naive estacional %.2f" % np.sqrt(np.mean((y[12:] - y[:-12]) ** 2)))
# -> RMSE del naive estacional 9.75
print("pronostico %.1f %.1f %.1f" % tuple(pron))                # -> pronostico 139.9 143.1 145.6
```

:::claves
- `t = np.arange(48)` da enteros del 0 al 47, no un rango de fechas. Prophet trabaja con fechas y con una tabla de dos columnas, `ds` e `y`; aquí `t` es solo la variable explicativa de la regresión, y por eso el ejemplo se puede resolver con `np.linalg.lstsq`.
- `y[12:] - y[:-12]` es el naive estacional: resta a cada mes el mismo mes del año anterior. Las dos vistas tienen longitudes distintas de la original pero **la misma entre sí** (36 elementos), que es lo que permite restarlas. Si la serie no fuera múltiplo del periodo, habría que recortarla antes.
- `np.column_stack(columnas)` apila vectores **como columnas** de una matriz. Es lo que convierte las seis listas de `diseno` en una matriz de 48×6; `np.concatenate` habría dado un vector largo y la regresión no tendría sentido.
- `np.linalg.lstsq(A, b, rcond=None)` devuelve una tupla cuya **primera** posición son los coeficientes. De ahí el `beta, *_ = ...`: el `*_` recoge los residuos, el rango y los valores singulares, que aquí no se usan. Es la forma de quedarse solo con lo primero sin indexar a mano.
- `diseno(t)` se llama **dos veces**, una para ajustar y otra para predecir, y también para calcular `ajuste = diseno(t) @ beta`. Eso es lo que hace Prophet por dentro: la misma base de columnas se evalúa en el tiempo histórico y en el futuro. Un error clásico es ajustar con una matriz y predecir con otra construida de forma ligeramente distinta (por ejemplo, sin la columna de unos): el producto `@` da error de dimensiones o, peor, un pronóstico desplazado.
- `np.ones_like(t, dtype=float)` es la columna de intercepto. El `dtype=float` no es imprescindible en este diseño, porque las columnas de seno y coseno ya hacen que `np.column_stack` devuelva `float64`; escribirlo deja claro que esa columna es numérica y no un contador, y no dependes de la promoción de tipos si algún día se quitan los armónicos.
- `beta[0]` es el intercepto y `beta[1]` la pendiente; los coeficientes de `sin` y `cos` empiezan en `beta[2]`. Ese orden lo fija el bucle de `diseno`, no Prophet: si cambias el orden de las columnas, el índice de la pendiente deja de ser 1 y el `print` miente sin dar error.
- `np.linalg.lstsq` **no** detecta si las columnas están casi repetidas: con dos armónicos anuales y solo 14 meses de historia, los coeficientes salen enormes y se cancelan entre sí. El modelo ajusta igual y el pronóstico se dispara. Ese es el motivo real de la regla de los dos ciclos completos por estacionalidad.
- El `print` con `%` es formato de cadena clásico de Python: `%.2f` redondea para imprimir, no cambia el valor guardado. `round()` sí cambia el valor, y por eso en el bloque de la rejilla de Holt-Winters se redondea antes de comparar.
:::

```python ilustrativo
# La via comoda: Prophet estima los puntos de cambio, los festivos y la incertidumbre.
# Necesita el paquete prophet (Stan por debajo), que no forma parte del entorno del portal.
import pandas as pd
from prophet import Prophet

# Dos columnas con nombres fijos: 'ds' para la fecha y 'y' para el valor
ventas = pd.DataFrame({"ds": pd.date_range("2021-01-01", periods=48, freq="MS"), "y": serie})

modelo = Prophet(
    yearly_seasonality=True,     # estacionalidad anual por defecto, con 10 armonicos
    weekly_seasonality=False,    # sin ciclo semanal: los datos son mensuales
    changepoint_prior_scale=0.05 # mas alto = permite cambios de tendencia mas bruscos
)
modelo.add_country_holidays(country_name="ES")
modelo.fit(ventas)

futuro = modelo.make_future_dataframe(periods=3, freq="MS")
pronostico = modelo.predict(futuro)         # trae yhat, yhat_lower e yhat_upper
columnas = ["ds", "yhat", "yhat_lower", "yhat_upper"]
print(pronostico[columnas].tail(3))
componentes = modelo.plot_components(pronostico)   # tendencia, anual y festivos por separado
```

## Errores típicos

- **Buscar en Prophet un modelo autorregresivo.** Prophet no usa los valores pasados como
  predictores: con precios, caudales o cualquier serie cuyo valor de mañana dependa del de hoy, esa
  carencia es decisiva, porque se queda con la tendencia y la estacionalidad y no con la dinámica.
- **Usarlo con pocos datos o sin ciclo claro.** La estacionalidad anual con 10 armónicos son 20
  coeficientes, más los puntos de cambio y los festivos: con 14 meses de historia no hay nada que
  estimar. Como regla, dos ciclos completos por cada estacionalidad que pidas.
- **Leer la banda de Prophet como un intervalo de confianza.** Se obtiene simulando tendencias
  futuras con cambios de pendiente como los históricos. Si el régimen cambia, la banda se queda
  estrecha justo cuando más falta te hacía ([[regimenes-de-mercado|regímenes de mercado]]).
- **Entrenar una red por serie.** El sentido de DeepAR es compartir estructura entre muchas series:
  con una sola le das menos información que a un Holt-Winters y encima tienes que elegir
  arquitectura, tasa de aprendizaje y épocas.
- **Comparar contra un naive de la media.** El listón de verdad es un naive estacional o un
  Holt-Winters, medido en validación hacia delante ([[validacion-temporal]]), nunca con particiones
  barajadas.
- **Elegir el modelo por su error de entrenamiento.** Con N-BEATS y con DeepAR puedes bajarlo hasta
  casi cero y empeorar el pronóstico: el número que decide es el de fuera de muestra
  ([[sobreajuste-en-redes]]).

:::practica
enunciado: Prophet usa una tendencia lineal a trozos con k = 0,5, m = 100 y dos puntos de cambio: en t = 10, δ = 0,3; en t = 20, δ = −0,2, con γ_j = −s_j·δ_j. Calcula la tendencia en t = 25, comprobando la continuidad.
pista: La pendiente efectiva es k más la suma de los δ ya ocurridos; el término de nivel acumula los γ_j, que existen justo para que la recta no se rompa.
solucion: En t = 10 la pendiente pasa a 0,8 y γ = −10·0,3 = −3: g(10) = 0,8·10 + 97 = 105, igual que antes del cambio (0,5·10 + 100 = 105). En t = 20 baja a 0,6 y el ajuste acumulado es −3 + 4 = 1: g(20) = 0,6·20 + 101 = 113. En t = 25, g = 0,6·25 + 101 = 116.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué hace Prophet para modelar la tendencia de una serie?
o: Usa los valores pasados como predictores, como un ARIMA
o: Ajusta una recta a trozos con puntos de cambio candidatos y penaliza los cambios de pendiente
o: Suaviza exponencialmente el nivel con un parámetro alfa estimado
a: 2
e: Prophet es una regresión sobre el tiempo: coloca puntos de cambio candidatos y un prior de Laplace (penalización L1) apaga casi todos. No es autorregresivo, así que no usa los valores pasados como predictores, y el suavizado exponencial es otro método distinto.
:::

:::quiz
p: Tienes 800 productos con 18 meses de ventas cada uno y quieres pronosticar el mes que viene. ¿Qué enfoque encaja mejor con la idea de los modelos globales?
o: Un modelo Prophet por producto, porque cada serie es distinta
o: Un solo modelo entrenado con todas las series, que comparta estructura entre productos parecidos
o: Un modelo por producto con 20 armónicos anuales para capturar el ciclo
a: 2
e: Con 18 meses no hay dos ciclos anuales por producto, así que un modelo por serie va escaso de datos. Un modelo global (DeepAR, o un gradient boosting con retardos y calendario) aprende de las 800 series a la vez y es el caso de uso que justifica estos métodos.
:::

:::nota
En la práctica, el competidor al que hay que batir casi nunca es un ARIMA: es un naive estacional
bien hecho y un gradient boosting con retardos, medias móviles y variables de calendario. Si estos
dos ya te dan el error que necesitas, la red solo añade cómputo.
:::
