---
id: suavizado-exponencial
titulo: Suavizado exponencial
fase: 5
nivel: intermedio
rutas: [ds, quant]
prerequisitos: [series-temporales-componentes, estacionariedad]
tags: [series-temporales, pronostico, suavizado]
resumen: Media ponderada en la que lo reciente pesa más, con variantes para tendencia y estacionalidad; el pronóstico barato que cuesta batir.
fuentes: ["Hyndman y Athanasopoulos (2021), 'Forecasting: Principles and Practice', caps. 8 y 9", "Brown (1959), 'Statistical Forecasting for Inventory Control'"]
---

## En una frase

El suavizado exponencial pronostica el futuro con una media ponderada de todo el pasado en la que
cada dato pesa una fracción fija menos que el siguiente, y sus variantes Holt y Holt-Winters
añaden un término de tendencia y un patrón estacional.

## La idea

Supón que quieres predecir las ventas de mañana y tienes dos herramientas sencillas. La media de
todo el histórico usa toda la información, pero reacciona tardísimo: si las ventas se acaban de
duplicar, seguirá anclada en el pasado durante meses. La media móvil de los últimos `k` días
reacciona rápido, pero necesita guardar `k` valores y da un salto brusco el día que sale de la
ventana un dato muy alto, aunque no haya pasado nada nuevo.

El suavizado exponencial resuelve las dos cosas con una idea muy simple: **que el pasado no se
corte, sino que se desvanezca**. En vez de dar el mismo peso a los últimos `k` datos y cero al
resto, cada dato pesa `(1 − α)` veces lo que el siguiente. Con `α = 0,5`, hoy pesa 0,5, ayer 0,25,
anteayer 0,125, y así hasta desvanecerse; los pesos suman exactamente 1, así que sigue siendo una
media, pero con memoria que se olvida.

El único parámetro es `α`:

- `α` cerca de 1 → el pronóstico es casi el último dato observado. Reacciona a todo, también al
  ruido.
- `α` cerca de 0 → el pronóstico es casi una media de todo el histórico. Muy estable, muy lento.

No se elige a ojo: se busca el valor que minimiza el error de pronóstico a un paso dentro de una
muestra, igual que se ajusta cualquier otro parámetro.

El suavizado simple tiene una limitación evidente: su pronóstico es **plano**. Si la serie sube,
se queda corto; si tiene un pico todos los diciembres, no lo ve. De ahí las dos variantes que se
usan de verdad:

- **Holt** (suavizado lineal) añade un segundo componente, la tendencia, que también se actualiza
  de forma exponencial. El pronóstico deja de ser plano: sigue una recta.
- **Holt-Winters** añade un tercer componente, el patrón estacional de `m` periodos, que se
  actualiza al llegar cada nueva observación de la misma fase. Con `m = 12` para datos mensuales,
  `m = 4` para trimestrales, `m = 7` para diarios con patrón semanal.

La familia completa se conoce como **ETS** (Error, Trend, Seasonal): entre uno y tres parámetros,
ninguna exigencia de estacionariedad estricta y buen comportamiento con series cortas. Un
Holt-Winters es el listón que hay que batir antes de montar algo más complicado.

:::figura
fichero: suavizado-exponencial-alfa-y-memoria
pie: Arriba a la izquierda, el mismo dato pronosticado con tres memorias: el alfa bajo va por detrás del nivel y el alto copia el ruido del último día. Arriba a la derecha, el error de cada alfa sobre la misma serie: el mínimo está en medio, y ese es el alfa que se elige. Abajo a la izquierda está lo que la fórmula esconde, los pesos que cada dato recibe; abajo a la derecha, que el alfa que gana dentro de la muestra no es el que gana con datos nuevos, que es por lo que se valida hacia delante.
fuente: figuras/suavizado-exponencial-1.py
:::

## Definición formal

**Suavizado exponencial simple (SES).** Con `0 < α < 1`:

:::formula
ŷ_{t+1} = α·y_t + (1 − α)·ŷ_t   =   Σ_{k=0}^{∞} α·(1 − α)^k · y_{t−k}
:::

- `y_t` — el valor observado en el instante `t`.
- `ŷ_t` — el pronóstico que se había hecho para el instante `t` con la información hasta `t−1`.
- `ŷ_{t+1}` — el pronóstico para el instante siguiente, que es la media ponderada anterior.
- `α` — el parámetro de suavizado, entre 0 y 1. Es el peso del último dato.
- La segunda igualdad muestra que los pesos forman una progresión geométrica de razón `(1 − α)` y
  que suman 1, porque `Σ α(1 − α)^k = α / (1 − (1 − α)) = 1`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `y_t` | El valor observado en el instante `t` | las de la serie (euros, unidades, visitas) | — |
| `ŷ_t` | El pronóstico que se había hecho para `t` con la información hasta `t−1` | las de la serie | — |
| `ŷ_{t+1}` | El pronóstico para el instante siguiente, que es la media ponderada | las de la serie | — |
| `α` | El peso del último dato observado | adimensional, entre 0 y 1 | El pronóstico se pega al último dato: reacciona antes, pero copia el ruido y pierde memoria. Por encima de 0,7 el modelo es casi un «ayer fue así»; por debajo de 0,1 apenas se mueve del histórico |
| `1 − α` | Lo que decae el peso de cada dato al retroceder un paso | adimensional, entre 0 y 1 | Con `1 − α` grande la memoria es muy larga y el pronóstico tarda meses en reaccionar a un cambio de nivel |
| `k` | Cuántos pasos atrás en la suma infinita de pesos | pasos (días, meses) | El peso del dato que está a `k` pasos es `α(1 − α)^k`: decae de forma geométrica, nunca llega a cero |
| `Σ α(1 − α)^k` | La suma de todos los pesos de la segunda igualdad | adimensional | Vale exactamente 1 para cualquier `α`: por eso sigue siendo una media y no una suma que crece |
:::

**Holt (nivel + tendencia).** Con `ℓ_t` el nivel y `b_t` la tendencia, y `0 < α, β < 1`:

:::formula
ℓ_t = α·y_t + (1 − α)·(ℓ_{t−1} + b_{t−1})   ·   b_t = β·(ℓ_t − ℓ_{t−1}) + (1 − β)·b_{t−1}
:::

- `ℓ_t` — el nivel estimado en `t`, que es una media suavizada ya corregida por la tendencia.
- `b_t` — la pendiente estimada; `β` es su parámetro de suavizado.
- El pronóstico a `h` pasos es `ŷ_{t+h} = ℓ_t + h·b_t`: una recta que arranca en el nivel actual.

**Holt-Winters aditivo** añade `s_t`, el componente estacional, con parámetro `γ` y periodo `m`:

:::formula
s_t = γ·(y_t − ℓ_{t−1} − b_{t−1}) + (1 − γ)·s_{t−m}   ·   ŷ_{t+h} = ℓ_t + h·b_t + s_{t+h−m}
:::

- `s_t` — el efecto estacional de la fase a la que pertenece `t`.
- `s_{t−m}` — el mismo efecto estacional estimado un ciclo antes; por eso el patrón se aprende
  ciclo a ciclo.
- `h` — el horizonte del pronóstico, de 1 a `m`; después de `m` pasos, el patrón se repite.
- En la versión **multiplicativa**, la estacionalidad multiplica en vez de sumar:
  `ŷ_{t+h} = (ℓ_t + h·b_t) · s_{t+h−m}`. Se usa cuando la amplitud del patrón crece con el nivel.

Los parámetros `α`, `β` y `γ` se estiman minimizando la suma de errores al cuadrado a un paso en
la muestra de entrenamiento, y hace falta decidir también **cómo se arrancan** `ℓ_0`, `b_0` y el
primer ciclo de `s`: un valor inicial mal elegido contamina los primeros pronósticos y, en series
cortas, todos.

## Ejemplo

Cuatro observaciones: `10, 12, 11, 13`. Arrancamos el nivel con el primer valor, así que el primer
pronóstico coincide con el dato y no cuenta como error. Con `α = 0,5`:

- `t = 1`: observado 12, pronóstico 10 → error `+2`. Nuevo nivel: `0,5·12 + 0,5·10 = 11`.
- `t = 2`: observado 11, pronóstico 11 → error `0`. Nuevo nivel: `0,5·11 + 0,5·11 = 11`.
- `t = 3`: observado 13, pronóstico 11 → error `+2`. Nuevo nivel: `0,5·13 + 0,5·11 = 12`.
- Pronóstico para `t = 4`: **12**. Suma de errores al cuadrado: `4 + 0 + 4 = 8`. Error absoluto
  medio: `4/3 = 1,33`.

Merece la pena comparar con más memoria y con menos:

- Con `α = 0,25`, los errores son peores: SSE `9,89`.
- Con `α = 0,90` (casi copiar el último dato), el pronóstico para `t = 4` sería 12,81 y el SSE
  `8,33`: mejor que un α bajo, peor que 0,5.

Ninguno de los dos extremos gana. Buscando en una rejilla fina, el mejor valor es `α = 0,65`, con
un SSE de `7,68`: no se elige `α` por convicción, se estima.

Un ejemplo con tendencia y estacionalidad: doce trimestres de ventas
`50, 62, 58, 70, 55, 68, 63, 76, 60, 74, 69, 83`. Un Holt-Winters aditivo de periodo 4 ajustado con
una rejilla da `α = 0,50`, `β = 0,05` y `γ = 0,30`, con un nivel final de 73,8 y una pendiente de
1,3 por trimestre. El pronóstico de los cuatro trimestres siguientes es `65,9 · 78,8 · 74,5 · 88,1`,
y reproduce el patrón observado: el cuarto trimestre el más fuerte y el primero el más flojo.

## Código

```python verificable
import numpy as np

serie = np.array([10.0, 12.0, 11.0, 13.0])

def sse_ses(alfa, y):
    """Suma de errores al cuadrado a un paso de un suavizado exponencial simple."""
    pred = y[0]                      # el primer pronostico es el primer dato
    sse = 0.0
    for t in range(1, y.size):
        sse += (y[t] - pred) ** 2
        pred = alfa * y[t] + (1 - alfa) * pred
    return sse

for a in (0.25, 0.5, 0.9):
    print("alfa %.2f  SSE %.4f" % (a, sse_ses(a, serie)))
# -> alfa 0.25 SSE 9.8906   alfa 0.50 SSE 8.0000   alfa 0.90 SSE 8.3264
mejor = max(np.arange(0.05, 1.0, 0.05), key=lambda a: -sse_ses(a, serie))
print("mejor alfa %.2f  SSE %.4f" % (mejor, sse_ses(mejor, serie)))   # -> 0.65 y 7.6810
```

:::claves
- `np.array([10.0, 12.0, 11.0, 13.0])` es un array de NumPy, no una lista de Python: todos los elementos son del mismo tipo y viven pegados en memoria. Por eso `y.size` da 4 sin contar nada, y `y[t]` devuelve un `np.float64` que se comporta como un número pero no es un `float` de Python.
- Los números se escriben con punto (`10.0`), no con coma. La coma separa argumentos en Python: `sse_ses(0,5, serie)` sería una llamada con tres argumentos y daría error, no un `0,5`.
- `range(1, y.size)` deja fuera el índice 0 a propósito. El bucle arranca en `t = 1` porque el pronóstico inicial se define como el primer dato y no se cuenta como error; si empezara en 0, el primer término de la suma sería siempre cero y el SSE no cambiaría, pero el código mentiría sobre lo que hace.
- Ojo con la indentación: en `sse_ses`, las dos líneas que empiezan por `sse +=` y `pred =` están **dentro** del bucle `for`, y `return sse` está fuera. Si mueves `return` un nivel a la derecha, la función devuelve en la primera vuelta y el bucle nunca se completa. En Python el sangrado es la sintaxis, no un adorno.
- `max(np.arange(0.05, 1.0, 0.05), key=lambda a: -sse_ses(a, serie))` busca el **mínimo**: `max` con la clave negada es un truco para no escribir `min` con la clave normal. El resultado no es el alfa exacto que minimiza el error, sino el mejor de una rejilla de 19 valores separados 0,05; con otra rejilla saldría otro número ([[seleccion-de-hiperparametros|selección de hiperparámetros]]).
- `np.arange(0.05, 1.0, 0.05)` **no incluye** el 1,0 final y acumula error de coma flotante: el último valor no es 0,95 exacto, sale 0,9500000000000001. Para rangos con decimales es más predecible `np.linspace(0.05, 0.95, 19)`.
- El bucle de Python sobre un array de cuatro elementos es instantáneo, pero si lo llamas dentro de una rejilla de 19 alfas son 19 bucles; con una serie de 10.000 puntos eso ya se nota y conviene reescribir la recursión con NumPy o usar `statsmodels` ([[rendimiento-y-perfilado|rendimiento y perfilado]]).
:::

```python verificable
import numpy as np

ventas = np.array([50.0, 62, 58, 70, 55, 68, 63, 76, 60, 74, 69, 83])

def hw(y, m, alfa, beta, gamma):
    """Holt-Winters aditivo: nivel, tendencia y estacionalidad de m periodos."""
    n = y.size
    nivel = y[:m].mean()
    tend = (y[m:2 * m].mean() - nivel) / m
    est = list(y[:m] - nivel) * (n // m + 2)        # un ciclo inicial de estacionalidad
    sse = 0.0
    for t in range(n):
        sse += (y[t] - (nivel + tend + est[t])) ** 2
        nuevo_nivel = alfa * (y[t] - est[t]) + (1 - alfa) * (nivel + tend)
        est[t + m] = gamma * (y[t] - nivel - tend) + (1 - gamma) * est[t]
        tend = beta * (nuevo_nivel - nivel) + (1 - beta) * tend
        nivel = nuevo_nivel
    return sse, nivel, tend, est

mejor = None
for alfa in np.arange(0.1, 0.95, 0.1):
    for beta in np.arange(0.05, 0.65, 0.1):
        for gamma in np.arange(0.1, 0.95, 0.1):
            s, *_ = hw(ventas, 4, alfa, beta, gamma)
            if mejor is None or s < mejor[0]:
                mejor = (s, round(alfa, 2), round(beta, 2), round(gamma, 2))
sse, nivel, tend, est = hw(ventas, 4, mejor[1], mejor[2], mejor[3])
print("rejilla: alfa %.2f  beta %.2f  gamma %.2f  SSE %.1f" % (mejor[1], mejor[2], mejor[3], mejor[0]))
# -> alfa 0.50  beta 0.05  gamma 0.30  SSE 36.8
print("nivel final %.2f  tendencia final %.2f" % (nivel, tend))     # -> 73.80 y 1.30
print("pronostico 4 trimestres", np.round([nivel + h * tend + est[ventas.size + h - 1] for h in range(1, 5)], 1))
# -> [65.9 78.8 74.5 88.1]
print("RMSE dentro de la muestra %.2f" % np.sqrt(sse / ventas.size))  # -> 1.75
```

```python ilustrativo
# La via comoda: statsmodels estima los parametros Y los estados iniciales, por eso su
# error dentro de la muestra es menor que el de la rejilla anterior.
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing

ventas = np.array([50, 62, 58, 70, 55, 68, 63, 76, 60, 74, 69, 83])
mod = ExponentialSmoothing(ventas, trend="add", seasonal="add", seasonal_periods=4,
                           initialization_method="estimated").fit()

print(mod.params["smoothing_level"], mod.params["smoothing_trend"], mod.params["smoothing_seasonal"])
print(mod.forecast(4))
```

## Errores típicos

- **Confundir la media móvil con el suavizado exponencial.** Son primos, no gemelos. La media
  móvil de `k` datos da el mismo peso a los `k` y cero a los anteriores, y da un salto cuando un
  valor sale de la ventana; el SES pesa de forma decreciente, no necesita guardar el histórico y
  nunca da ese salto.
- **Usar suavizado simple con una serie que tiene tendencia o estacionalidad.** El SES converge a
  una constante: te dará el mismo pronóstico para mañana y para dentro de un año. Si la serie
  sube un 2 % al mes, ese pronóstico plano estará mal por construcción. Usa Holt o Holt-Winters.
- **Elegir `α` a ojo porque "así reacciona más".** Un `α` alto también copia el ruido. El valor se
  estima minimizando el error a un paso y, si el pronóstico va a usarse de verdad, se comprueba
  fuera de muestra con [[validacion-temporal|validación temporal]].
- **Comparar SSE entre series o entre tramos distintos.** La suma de errores al cuadrado depende
  de la escala de la serie y del número de puntos. Para comparar usa RMSE, MAE o, mejor, una
  medida relativa como el MASE, que se normaliza con el error de un pronóstico naive.
- **Ignorar la inicialización.** En una serie de 200 puntos da igual, pero con 12 observaciones el
  nivel, la tendencia y el primer ciclo estacional iniciales pesan mucho. statsmodels estima los
  estados iniciales por máxima verosimilitud y por eso su error en muestra sale más bajo (0,53 de
  desviación frente al RMSE de 1,75 de la rejilla de arriba): no es que el método sea mejor, es
  que tiene más parámetros libres.
- **Usar una media móvil centrada como variable de entrada.** La media móvil centrada usa valores
  posteriores al instante que estás prediciendo. Si la metes como característica en un modelo,
  estás [[fuga-de-datos|mirando al futuro]] y el resultado en producción se desmorona. Para
  variables de entrada, medias móviles hacia atrás.

:::practica
enunciado: Ajustas un Holt con α = 0,5 y β = 0,5. El nivel inicial es 100 y la tendencia inicial 10. Llegan dos observaciones: 112 y 124. Calcula el pronóstico que habías hecho para la segunda, el nivel y la tendencia tras ella, y el pronóstico para la tercera.
pista: El pronóstico a un paso es nivel más tendencia, y el nivel nuevo mezcla la observación con ese pronóstico.
solucion: Pronóstico para t = 2: 100 + 10 = 110. Con y = 112, el nivel queda en 0,5·112 + 0,5·110 = 111 y la tendencia en 0,5·(111 − 100) + 0,5·10 = 10,5. Pronóstico para t = 3: 111 + 10,5 = 121,5. La observación de 124 llegó 2,5 por encima del pronóstico.
:::

## Comprueba que lo sabes

:::quiz
p: Con alpha = 0,5 y observaciones 10, 12, 11 y 13, ¿cuál es el pronóstico para el quinto periodo si el nivel arranca en el primer valor?
o: 11,5, la media de los cuatro datos
o: 12, porque el nivel queda en 12 tras la última observación
o: 13, porque el suavizado copia siempre el último dato
a: 2
e: El nivel evoluciona así: 11 tras el 12, 11 tras el 11 y 12 tras el 13. El pronóstico es el nivel actual, 12, no la media de la serie (11,5) ni el último dato (13); con alpha = 0,5 el pronóstico queda a medio camino entre ambos.
:::

:::quiz
p: Tu serie trimestral crece un 3 % cada trimestre y además tiene un pico fuerte en el cuarto. ¿Qué método de suavizado necesitas como mínimo?
o: Suavizado exponencial simple, porque es el más robusto
o: Holt-Winters con tendencia y estacionalidad de periodo 4
o: Holt simple, que ya incorpora la estacionalidad
a: 2
e: El SES da un pronóstico plano y se quedaría corto con la tendencia. Holt añade la tendencia pero no el patrón estacional, así que no vería el pico del cuarto trimestre. Holt-Winters es el que incorpora los tres componentes: nivel, tendencia y estacionalidad de periodo 4.
:::

:::truco
Antes de dar por bueno un modelo complicado, ajusta un Holt-Winters y apunta su error de
validación. Ese número es tu suelo: si tu red neuronal o tu gradient boosting no lo bate con
claridad, el problema no pedía un modelo complejo, pedía mirar mejor los datos.
:::
