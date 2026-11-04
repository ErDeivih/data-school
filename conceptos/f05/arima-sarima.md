---
id: arima-sarima
titulo: ARIMA y SARIMA
fase: 5
nivel: avanzado
rutas: [ds, quant]
prerequisitos: [estacionariedad, autocorrelacion-acf-pacf, test-adf-kpss]
tags: [series-temporales, pronostico, arima]
resumen: Autorregresión, diferencias y media móvil combinadas para pronosticar una serie, con la versión estacional que repite la estructura cada s periodos.
fuentes: ["Box, Jenkins y Reinsel (2015), 'Time Series Analysis: Forecasting and Control'", "Hyndman y Athanasopoulos (2021), 'Forecasting: Principles and Practice', cap. 9"]
---

## En una frase

ARIMA describe una serie como una combinación de sus propios valores pasados (parte AR), de los
errores de predicción pasados (parte MA) y de sus diferencias (la I de integrada); SARIMA repite
esa misma estructura en los retardos estacionales.

## La idea

Casi todos los modelos de series temporales se construyen con tres piezas, y conviene entenderlas
por separado antes de juntarlas.

**Autorregresión (AR).** El valor de hoy depende de los valores anteriores. Si ayer hizo calor,
hoy también hace calor. Un AR(1) dice literalmente: «el valor de hoy es una fracción `φ` del de
ayer, más un empujón nuevo». Ese `φ` es la memoria del nivel: si vale 0,8, un valor alto hoy
anuncia un valor alto mañana, y su efecto se desvanece como `0,8^h`.

**Media móvil (MA).** Aquí la memoria no está en el nivel, sino en los **shocks**. Si una máquina
se averió ayer y la producción cayó, hoy probablemente siga algo por debajo de lo normal, no
porque el nivel de ayer importe, sino porque el accidente de ayer todavía se nota. Un MA(1) dice:
«el valor de hoy es la media más el shock de hoy, más una fracción `θ` del shock de ayer». La
diferencia con AR es sutil y es la clave de todo el capítulo: en AR el pasado *observado* importa;
en MA solo importa la parte del pasado que **no se pudo predecir**.

**Integración (I).** Ya sabes por [[estacionariedad]] que muchas series no oscilan alrededor de una
media estable: pasean. El paseo aleatorio se convierte en ruido al diferenciarlo, y muchas series
económicas necesitan una o dos diferencias. Esa `d` es el número de veces que diferencias antes de
ajustar el ARMA.

Con las tres piezas se construye ARIMA(p,d,q): se diferencia `d` veces y a la serie resultante se
le ajusta un ARMA con `p` retardos autorregresivos y `q` de media móvil. El método clásico para
llegar hasta ahí es el bucle de Box-Jenkins, y sigue siendo el orden correcto:

1. **Identificar.** Mira la serie, decide si necesita diferencias (con [[test-adf-kpss|ADF y
   KPSS]]) y mira la [[autocorrelacion-acf-pacf|ACF y la PACF]] para hacerte una idea de `p` y `q`.
2. **Estimar.** Ajusta los coeficientes por máxima verosimilitud (o por mínimos cuadrados
   condicionales, que es lo que hace el bloque de código de abajo) y compara candidatos con
   AIC o BIC.
3. **Diagnosticar.** Mira los residuos: si queda autocorrelación, el modelo está mal y sus
   intervalos de predicción son mentira.
4. **Pronosticar**, y volver a empezar cuando lleguen datos nuevos.

La versión **estacional**, SARIMA(p,d,q)(P,D,Q)_s, nace de una observación simple: en datos
trimestrales, el cuarto trimestre de este año se parece al cuarto trimestre del año pasado. Eso es
una autorregresión en el retardo 4, una media móvil en el retardo 4 y, muchas veces, una
diferencia estacional `y_t − y_{t−4}`. SARIMA añade esos tres ingredientes en los retardos
múltiplos de `s` sin renunciar a los de corto plazo.

Dos límites que hay que tener presentes. Primero, ARIMA es **univariante y lineal**: solo usa el
pasado de la propia serie. Si tienes variables explicativas, el marco se amplía a una regresión
con errores ARIMA (lo que statsmodels llama SARIMAX). Segundo, ARIMA supone **varianza
constante**: con retornos financieros, donde la volatilidad se agrupa, el modelo se queda corto y
hace falta un [[garch-volatilidad|modelo de volatilidad]] aparte.

:::figura
fichero: arima-memoria-ar-frente-a-ma
pie: A la izquierda, los pronósticos de un AR(1): parten del último dato, 13, y se acercan a la media de largo plazo recortando la distancia en un factor `φ` por paso, hasta aplanarse en 10. A la derecha, un MA(1): el shock de ayer pesa solo en el primer paso y a partir del segundo el pronóstico es la media. Esa es la diferencia práctica entre las dos piezas: el AR arrastra el nivel durante muchos periodos y el MA arrastra el shock durante uno.
fuente: figuras/arima-sarima-1.py
:::

## Definición formal

Empieza por las dos piezas básicas, con `ε_t` ruido blanco de media 0 y varianza `σ²`:

:::formula
AR(1): y_t = c + φ·y_{t−1} + ε_t        MA(1): y_t = μ + ε_t + θ·ε_{t−1}
:::

- `y_t` — el valor de la serie en `t`; `ε_t` — el shock impredecible de ese instante.
- `c` — la constante; en un AR(1) la media de largo plazo es `c / (1 − φ)`.
- `φ` — el coeficiente autorregresivo. El proceso es estacionario si su valor absoluto es menor
  que 1.
- `μ` — la media del proceso en el caso MA.
- `θ` — el coeficiente de media móvil. El proceso es invertible si su valor absoluto es menor que
  1, lo que garantiza que se puede reescribir como un AR de infinitos términos.

En general, con `B` el operador de retardo (`B·y_t = y_{t−1}`), `φ(B) = 1 − φ₁B − … − φ_pB^p` y
`θ(B) = 1 + θ₁B + … + θ_qB^q`:

:::formula
φ(B)·(1 − B)^d · y_t = θ(B)·ε_t        SARIMA: φ(B)·Φ(B^s)·(1 − B)^d·(1 − B^s)^D · y_t = θ(B)·Θ(B^s)·ε_t
:::

- `d` — número de diferencias simples; `D` — número de diferencias estacionales.
- `(1 − B)^d · y_t` — la serie diferenciada `d` veces; `(1 − B^s)^D` hace lo mismo con el retardo
  estacional `s`.
- `Φ(B^s)` y `Θ(B^s)` — los polinomios autorregresivo y de media móvil **estacionales**, de
  órdenes `P` y `Q`.
- `s` — el periodo estacional (4 en datos trimestrales, 12 en mensuales, 7 en diarios con patrón
  semanal).
- La estacionariedad exige que las raíces de `φ(B)` y `Φ(B^s)` caigan **fuera** del círculo
  unidad; la invertibilidad, lo mismo para `θ(B)` y `Θ(B^s)`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `y_t` | El valor de la serie en el instante `t` | las de la serie (euros, retornos) | — |
| `ε_t` | El shock impredecible de ese instante | las de la serie | — |
| `σ²` | La varianza del ruido blanco `ε_t` | las de la serie, al cuadrado | Ensancha los intervalos de predicción; con varianza cambiante el modelo se queda corto, que es el hueco que cubre GARCH |
| `c` | La constante del AR | las de la serie | Sube toda la serie: la media de largo plazo pasa a `c / (1 − φ)` |
| `μ` | La media del proceso en el caso MA | las de la serie | Desplaza el pronóstico entero; en un MA es el nivel al que vuelve tras el shock |
| `φ` | Coeficiente autorregresivo: la memoria del nivel | adimensional, entre −1 y 1 para ser estacionario | El pronóstico se pega al último valor y tarda más en volver a la media. Por encima de 1 el proceso ni siquiera es estacionario y el pronóstico se dispara |
| `θ` | Coeficiente de media móvil: cuánto dura el shock | adimensional, entre −1 y 1 para ser invertible | El susto de ayer pesa más en el pronóstico de mañana; con `θ` pegado a −1 el modelo está cancelando una diferencia que sobraba |
| `p` | Orden autorregresivo: cuántos valores pasados entran | número entero, 0, 1, 2… | Más memoria y más parámetros; a partir de 3 o 4 en series cortas casi todo es ruido estimado |
| `d` | Cuántas veces se diferencia la serie antes de ajustar | número entero, 0, 1, 2 | Quita tendencia, pero de más infla la varianza y deja una raíz unitaria artificial. Con `d = 0` el modelo ajusta el nivel |
| `q` | Orden de media móvil: cuántos shocks pasados entran | número entero, 0, 1, 2… | Recoge más estructura de corto plazo, a costa de parámetros y de estabilidad del ajuste |
| `B` | El operador de retardo: `B·y_t = y_{t−1}` | no tiene | — |
| `φ(B)` | El polinomio autorregresivo `1 − φ₁B − … − φ_pB^p` | no tiene | Sus raíces tienen que caer fuera del círculo unidad; si alguna entra, la serie no es estacionaria |
| `θ(B)` | El polinomio de media móvil `1 + θ₁B + … + θ_qB^q` | no tiene | Sus raíces tienen que caer fuera del círculo unidad para que el modelo sea invertible |
| `P`, `Q` | Órdenes estacionales autorregresivo y de media móvil | número entero, 0 o 1 casi siempre | Añaden memoria en los retardos `s`, `2s`, `3s`. Con `P = Q = 1` ya se recoge casi toda la estacionalidad de una serie trimestral |
| `D` | Número de diferencias estacionales `(1 − B^s)^D` | número entero, 0 o 1 | Quita la estacionalidad, pero de más deja un coeficiente estacional pegado a −1: señal de que sobraba |
| `s` | El periodo estacional | pasos: 4 trimestral, 12 mensual, 7 diario | Determina en qué retardos se busca el patrón; equivocarlo desplaza toda la parte estacional |
| `Φ(B^s)`, `Θ(B^s)` | Polinomios autorregresivo y de media móvil estacionales | no tienen | Igual que `φ(B)` y `θ(B)` pero en los retardos múltiplos de `s` |
| `AIC`, `BIC` | Criterios de información: `−2·log L` más una penalización por parámetro | adimensionales, comparables solo sobre la misma serie diferenciada | La penalización sube con `k` (y el BIC además con `log n`): más parámetros tienen que ganarse el sitio con verosimilitud |
:::

Para comparar modelos ajustados a la **misma** serie diferenciada se usan los criterios de
información `AIC = −2·log L + 2k` y `BIC = −2·log L + k·log(n)`, donde `L` es la verosimilitud
maximizada, `k` el número de parámetros y `n` el número de observaciones. Penalizan la
complejidad, que es justo lo que hace falta cuando comparas docenas de combinaciones.

## Ejemplo

**AR(1) a mano.** Sea `c = 5` y `φ = 0,5`. La media de largo plazo es `5 / (1 − 0,5) = 10`. Si la
última observación es `y_4 = 13`, los pronósticos salen de aplicar la recursión:

- `ŷ_5 = 5 + 0,5 · 13 = 11,5`
- `ŷ_6 = 5 + 0,5 · 11,5 = 10,75`
- `ŷ_7 = 5 + 0,5 · 10,75 = 10,375`

El pronóstico vuelve a la media a velocidad `φ^h`: la desviación inicial era `13 − 10 = 3`, y
después de `h` pasos queda en `3 · 0,5^h` → 1,5, 0,75, 0,375… Un AR(1) estacionario **siempre**
acaba pronosticando la media; lo que cambia entre modelos es la velocidad.

**MA(1) a mano.** Con `μ = 10` y `θ = 0,6`, si el shock del último periodo fue `ε = −2`, el
pronóstico para el siguiente es `10 + 0,6 · (−2) = 8,8`. Y para el siguiente, 10: un MA(1) olvida
el shock después de un paso. Esa es la diferencia práctica entre AR y MA: el AR arrastra el nivel
durante muchos periodos; el MA arrastra el shock durante uno o dos.

**Un ARIMA(1,1,0) completo.** Simulamos 300 puntos con `φ = 0,6` y una raíz unitaria (la serie es
la suma acumulada de un AR(1)), y ajustamos por mínimos cuadrados la regresión de `Δy_t` sobre
`Δy_{t−1}`. El coeficiente estimado es **0,56**, cerca del 0,6 simulado. El último valor es 61,15 y
los pronósticos a uno, dos y tres pasos son **59,9**, **59,14** y **58,65**: cada paso encadena la
diferencia pronosticada y la suma al nivel anterior. Ese es exactamente el mecanismo de la I de
ARIMA.

**Con estacionalidad.** Si ajustas un SARIMA(0,1,1)(0,1,1)_4 a la serie de ventas trimestrales
`50, 62, 58, 70, 55, 68, 63, 76, 60, 74, 69, 83`, el modelo necesita una media móvil simple y otra
estacional, y su pronóstico reproduce el patrón: cuarto trimestre el más alto, segundo por detrás,
tercero flojo y primero el más bajo.

## Código

```python verificable
import numpy as np

c, phi = 5.0, 0.5                     # media de largo plazo: c/(1-phi) = 10
ultimo = 13.0                         # ultima observacion de la serie
print("media de largo plazo", c / (1 - phi))          # -> 10.0
for h in range(1, 4):
    ultimo = c + phi * ultimo
    print(f"pronostico h={h}: {ultimo:.3f}")
# -> h=1: 11.500   h=2: 10.750   h=3: 10.375
```

:::claves
- Los números van con punto decimal: `3.5`, no `3,5`. Y `1e-5` es notación científica de Python: vale 0,00001 y se lee igual que en una calculadora.
- La línea `ultimo = c + phi * ultimo` **reutiliza la misma variable** en cada vuelta del bucle. En el primer paso `ultimo` es el dato 13; en el segundo ya es 11,5, el pronóstico anterior. Eso es exactamente la recursión del AR(1), pero también significa que la observación original se pierde para siempre: si más adelante necesitas el dato, guárdalo antes en otra variable.
- Como `ultimo` se reasigna, el bucle **depende del orden**: los pronósticos a dos y tres pasos solo existen porque se han calculado los anteriores. No se pueden calcular en paralelo ni con una sola operación vectorizada.
- `f"pronostico h={h}: {ultimo:.3f}"` es un *f-string*: el valor se formatea dentro del texto. `.3f` son tres decimales y `h` sale como entero sin más. Ojo: el f-string no cambia el valor que queda en la variable, solo cómo se imprime.
- `print("media de largo plazo", c / (1 - phi))` imprime `10.0`, no `10`, porque en Python 3 la división `/` **siempre** devuelve un número en coma flotante, aunque el resultado sea exacto. Si quisieras el entero, sería `c // (1 - phi)`, que aquí daría 10 pero con una división truncada que casi nunca es lo que quieres.
- El comentario `# -> h=1: 11.500` no lo comprueba nadie al ejecutar: es documentación. Estos comentarios sí se verifican al generar el portal, así que si cambias el bucle hay que cambiar el comentario, o el validador avisa.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(2)
n = 300
phi = 0.6
x = np.zeros(n)
for t in range(1, n):                       # diferencias: un AR(1) estacionario
    x[t] = phi * x[t - 1] + rng.normal(0, 1)
y = 100 + np.cumsum(x)                      # la serie: un ARIMA(1,1,0)

dy = np.diff(y)
X = np.column_stack([np.ones(dy.size - 1), dy[:-1]])   # constante y retardo 1
b, *_ = np.linalg.lstsq(X, dy[1:], rcond=None)
print("phi estimado %.3f  (el simulado era %.1f)" % (b[1], phi))   # -> 0.560

# Pronostico: se predice la diferencia y se vuelve a integrar sobre el ultimo nivel
pred = dy[-1]
camino = [y[-1]]
for h in range(3):
    pred = b[0] + b[1] * pred
    camino.append(camino[-1] + pred)
print("ultimo dato %.2f" % y[-1])                        # -> 61.15
print("pronostico 1 a 3 pasos", np.round(camino[1:], 2))  # -> [59.9  59.14 58.65]
print("efecto de un shock de -2 en un MA(1) con theta=0.6: %.2f" % (0.6 * -2))  # -> -1.20
```

```python ilustrativo
# La via comoda con statsmodels: ajusta por maxima verosimilitud y da errores tipicos.
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX

rng = np.random.default_rng(0)
n = 48
t = np.arange(n)
y = 50 + 0.5 * t + np.tile([4.0, 0.0, -3.0, -1.0], 12) + rng.normal(0, 1.5, n)

mod = SARIMAX(y, order=(0, 1, 1), seasonal_order=(0, 1, 1, 4),
              enforce_stationarity=False, enforce_invertibility=False)
res = mod.fit(disp=False)
print(res.summary())          # coeficientes, AIC y contrastes sobre los residuos
print(res.forecast(4))        # los cuatro trimestres siguientes
```

## Errores típicos

- **Elegir `d` a ojo.** Diferenciar de más infla la varianza y deja un coeficiente de media móvil
  pegado a −1 (raíces que se cancelan); diferenciar de menos deja la raíz unitaria dentro y el
  pronóstico se dispara. Decide `d` con [[test-adf-kpss|ADF y KPSS]], no con la vista.
- **Identificar `p` y `q` solo con la ACF y la PACF y no comprobar nada más.** En la práctica hay
  varios modelos que encajan con el mismo correlograma. Ajusta un puñado de candidatos, compáralos
  con AIC o BIC y quédate con el que además deje los residuos limpios.
- **No diagnosticar los residuos.** Si el ACF de los residuos tiene picos fuera de la banda, el
  modelo no ha capturado toda la estructura y sus intervalos de predicción estarán mal
  calibrados. El contraste de Ljung-Box resume varios retardos en un [[p-valor|p-valor]].
- **Olvidar la parte estacional.** Un ARIMA(1,1,1) ajustado a datos trimestrales con estacionalidad
  deja picos en los residuos en los retardos 4, 8 y 12. Si la ACF de la serie tiene picos en
  múltiplos de `s`, necesitas la parte estacional, no un AR de orden alto.
- **Extrapolar la tendencia lineal para siempre.** Un ARIMA con deriva proyecta la pendiente
  indefinidamente. Que el modelo pueda hacerlo no significa que sea creíble: a 30 pasos, la
  incertidumbre de la pendiente domina por completo al pronóstico.
- **Suponer que la varianza es constante.** Los residuos de un ARIMA sobre retornos financieros
  tienen heterocedasticidad: hay tramos tranquilos y tramos violentos. El modelo acierta la media
  y falla la incertidumbre, que es justo lo que hace falta para dimensionar posiciones.

:::practica
enunciado: Comparas dos modelos ajustados a la misma serie de n = 400. El ARIMA(1,0,0) tiene log L = −520 y 3 parámetros; el ARIMA(1,1,1), log L = −514 y 4 parámetros. Calcula AIC y BIC de cada uno con ln 400 = 5,99 y decide cuál eliges.
pista: AIC suma 2 por parámetro y BIC suma ln n por parámetro, siempre sobre −2·log L.
solucion: ARIMA(1,0,0): AIC = 1040 + 6 = 1046 y BIC = 1040 + 3·5,99 = 1057,97. ARIMA(1,1,1): AIC = 1028 + 8 = 1036 y BIC = 1028 + 4·5,99 = 1051,96. Los dos criterios son menores en el segundo modelo, así que eliges el ARIMA(1,1,1); el BIC le ha cobrado 5,99 más de penalización y aun así gana.
:::

## Comprueba que lo sabes

:::quiz
p: Un AR(1) con c = 4 y phi = 0,6 tiene como última observación 20. ¿Cuál es el pronóstico a un paso y hacia dónde tiende el pronóstico a largo plazo?
o: 16 y tiende a 20, porque el modelo copia el último valor
o: 16 y tiende a 10, que es la media c/(1-phi)
o: 24 y tiende a infinito, porque el modelo tiene tendencia
a: 2
e: El pronóstico a un paso es 4 + 0,6*20 = 16 y la media de largo plazo es 4/(1-0,6) = 10. Un AR(1) estacionario siempre vuelve a su media; lo hace con velocidad phi por paso. No hay tendencia: la constante es un nivel, no una pendiente.
:::

:::quiz
p: Ajustas un ARIMA a datos trimestrales y el ACF de los residuos tiene un pico claro en el retardo 4. ¿Qué haces?
o: Nada: un pico aislado entra dentro de lo normal
o: Añadir la parte estacional al modelo, porque queda estructura en el retardo 4 que un ARIMA no estacional no recoge
o: Diferenciar otra vez la serie para quitar el pico
a: 2
e: Un pico significativo en el retardo 4 (o en 8, 12) con datos trimestrales es la firma de estacionalidad no capturada, y se resuelve con los órdenes estacionales P, D y Q. Diferenciar de nuevo no elimina la estacionalidad de periodo 4 y añade un problema nuevo: la varianza inflada y las raíces que se cancelan.
:::

:::aviso
Un coeficiente de media móvil estacional cercano a −1 suele indicar que has aplicado una
diferencia estacional innecesaria: la parte MA está cancelando la parte AR que acabas de
introducir. Si el ajuste te lleva ahí, vuelve atrás y contrasta si de verdad hacía falta la
diferencia estacional.
:::
