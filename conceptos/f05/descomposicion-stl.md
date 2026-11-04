---
id: descomposicion-stl
titulo: Descomposición STL
fase: 5
nivel: intermedio
rutas: [ds, quant]
prerequisitos: [series-temporales-componentes, estacionariedad]
tags: [series-temporales, estacionalidad, exploracion]
resumen: Separa una serie en tendencia, estacionalidad y residuo con suavizados locales, y deja que el patrón estacional cambie de un ciclo a otro.
fuentes: ["Cleveland, Cleveland, McRae y Terpenning (1990), 'STL: A Seasonal-Trend Decomposition Procedure Based on Loess'", "Hyndman y Athanasopoulos (2021), 'Forecasting: Principles and Practice', cap. 3"]
---

## En una frase

STL descompone una serie en tres trozos que se suman —tendencia, componente estacional y
residuo— usando suavizados locales, y a diferencia de la descomposición clásica permite que el
patrón estacional evolucione con el tiempo y aguanta los valores atípicos.

## La idea

Cuando miras una serie con estacionalidad, el gráfico te cuenta tres historias a la vez: un
movimiento de fondo que dura años, un patrón que se repite cada ciclo y ruido. Descomponer es
separarlas para poder mirarlas una a una.

La descomposición clásica se hace en dos pasos y se calcula a mano:

1. **Tendencia.** Una media móvil centrada de orden igual al periodo estacional: para datos
   trimestrales, la media de los cuatro trimestres que rodean a cada punto, ponderando con 0,5 los
   extremos. Al promediar un ciclo completo elimina la estacionalidad y deja el nivel suavizado.
2. **Estacionalidad.** Se resta la tendencia y se promedian, para cada fase del ciclo, las
   desviaciones que quedan: todas las primaveras juntas, todos los veranos juntos.

Funciona, pero tiene tres defectos que en datos reales se notan: el patrón estacional es siempre el
mismo, así que si la campaña de primavera se ha ido desplazando con los años eso no aparece; un dato
atípico contamina todo el ciclo, porque el promedio por fases es una media; y se pierden los
extremos, ya que la media móvil centrada no se puede calcular en los primeros y últimos puntos,
justo donde más interesa.

**STL** (*Seasonal-Trend decomposition using Loess*) resuelve los tres con el suavizado local
**loess**: en cada punto ajusta una recta ponderando los vecinos con un peso que decrece con la
distancia, en lugar de promediar ventanas rígidas. La ventana `s.window` controla cuánto puede
cambiar el patrón estacional de un ciclo a otro y `t.window` cuánto se suaviza la tendencia: cuanto
mayor, más rígida. Además, en modo **robusto** los puntos con residuo grande reciben menos peso en
la pasada siguiente, así que un atípico deja de arrastrar la tendencia y la estacionalidad y se
queda donde le corresponde: en el residuo.

Dos cosas que STL **no** es: no es un modelo de pronóstico (la tendencia es un suavizado de dos
lados, así que los últimos puntos se revisan cuando llegan datos nuevos) y no da intervalos de
predicción. Para pronosticar hace falta un paso más, con un [[arima-sarima|modelo]] o con
[[suavizado-exponencial|suavizado]]. Y sirve para quitar la estacionalidad antes de modelar, para
ver si el nivel de fondo sube o baja sin que el ruido lo tape y para vigilar el residuo en busca de
[[outliers-y-deteccion|valores atípicos]].

:::figura
fichero: descomposicion-stl-tres-componentes
pie: Arriba solo se ve la serie; los tres paneles de abajo son lo que hay que reconstruir. La tendencia es una media móvil centrada de un ciclo, y por eso los dos extremos se pierden: no tienen cuatro vecinos. La estacionalidad se repite idéntica porque es un promedio por fases, que es justo lo que STL relaja con la ventana estacional. Y el residuo es el panel que de verdad se mira: un pico grande ahí es un candidato a dato mal cargado, no a movimiento del negocio.
fuente: figuras/descomposicion-stl-1.py
:::

## Definición formal

La descomposición aditiva supone

:::formula
y_t = T_t + S_t + R_t
:::

- `y_t` — el valor observado en el instante `t`.
- `T_t` — la **tendencia**: el movimiento suave de largo plazo, sin estacionalidad.
- `S_t` — el componente **estacional**, con la misma forma dentro de cada ciclo y media 0 dentro
  de un ciclo completo (si no, se confundiría con la tendencia).
- `R_t` — el **residuo**: lo que no explican los otros dos.
- En la versión **multiplicativa**, `y_t = T_t · S_t · R_t`, la adecuada cuando la amplitud del
  patrón crece con el nivel. Se resuelve con logaritmos: es la versión aditiva aplicada a `log y_t`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `y_t` | El valor observado en el instante `t` | las de la serie (miles de euros, unidades) | — |
| `T_t` | La tendencia: el movimiento suave de largo plazo, ya sin el ciclo | las de la serie | Una tendencia que sube significa que el negocio crece por encima del patrón estacional; es la parte que un pronóstico puede extrapolar, con cuidado |
| `S_t` | El componente estacional: el efecto de la fase del ciclo a la que pertenece `t` | las de la serie en la versión aditiva, tanto por uno en la multiplicativa | Si crece su amplitud sin que crezca el nivel, la serie es aditiva; si la amplitud escala con el nivel, hay que pasar a la versión multiplicativa y descomponer `log y_t` |
| `R_t` | El residuo: lo que no explican los otros dos | las de la serie | Si crece con el nivel, la descomposición aditiva está mal elegida (es la firma del abanico). Si tiene picos regulares, hay un ciclo sin capturar; si los picos son sueltos, son [[outliers-y-deteccion|valores atípicos]] |
| `Var(R)` | La varianza del residuo | las de la serie, al cuadrado | Sube cuando la descomposición deja de explicar la serie; es la referencia contra la que se miden las dos fuerzas |
| `F_estacional` | `máx(0, 1 − Var(R) / Var(S + R))`: cuánto pesa la estacionalidad | adimensional, entre 0 y 1 | Con más de 0,6 hay patrón estacional que merece la pena modelar; por debajo, el ciclo explica menos que el ruido |
| `F_tendencia` | `máx(0, 1 − Var(R) / Var(T + R))`: cuánto pesa la tendencia | adimensional, entre 0 y 1 | Igual que la anterior pero para el nivel de fondo: en una serie con deriva clara se acerca a 1 aunque haya estacionalidad |
| `m` | El periodo del ciclo, en observaciones | pasos: 4 trimestral, 12 mensual, 7 diario | Fija el ancho de la media móvil centrada y el número de fases. Si no coincide con el ciclo real, la tendencia se come parte de la estacionalidad; con series de menos de dos ciclos el reparto es arbitrario |
:::

El suavizado que usa por dentro es una **regresión local** (loess). En cada punto `x` se ajusta

:::formula
mín_{a,b} Σ_i w_i(x)·(y_i − a − b·(x_i − x))²   ·   w_i(x) = (1 − (/x_i − x/ / d(x))³)³
:::

- `a` y `b` — la ordenada y la pendiente de la recta local; el valor suavizado en `x` es `a`.
- `d(x)` — la distancia al vecino más lejano dentro de la ventana, que fija el ancho de banda.
- `w_i(x)` — el peso tricúbico: vale 1 en el centro y se anula en el borde de la ventana, que es lo
  que hace local al suavizado. `s.window` y `t.window` son los anchos de banda del componente
  estacional y de la tendencia.

El modo robusto añade un bucle exterior con pesos de **bisquare** calculados sobre el residuo:

:::formula
u_t = /R_t − mediana(R)/ / (6 · mediana(/R_t − mediana(R)/))   ·   w_t = (1 − u_t²)²  si u_t < 1, y 0 si u_t ≥ 1
:::

- `mediana(R)` — la mediana de los residuos; se resta para centrar la escala.
- `6 · mediana(...)` — una estimación robusta de la dispersión (desviación absoluta mediana
  escalada); los puntos a más de seis veces esa distancia reciben peso 0.
- `w_t` — el peso con el que ese punto entra en la pasada siguiente. Es la razón de que un atípico
  no arrastre la tendencia.

Finalmente, para decidir si merece la pena mirar cada componente, Hyndman propone dos medidas de
fuerza entre 0 y 1, basadas en la varianza:

:::formula
F_estacional = máx(0, 1 − Var(R) / Var(S + R))   ·   F_tendencia = máx(0, 1 − Var(R) / Var(T + R))
:::

- Si `Var(R)` se come casi toda la varianza de `S + R`, la estacionalidad no aporta nada y
  `F_estacional` se acerca a 0; si el residuo es pequeño comparado con la tendencia, `F_tendencia`
  se acerca a 1.
- La regla práctica: por debajo de 0,6 no hay mucha señal que digerir.

## Ejemplo

Ocho trimestres construidos a mano, con tendencia `T = 100 + 2·t`, estacionalidad que se repite
`(+4, −2, −3, +1)` y un residuo pequeño:

| Trimestre | T | S | R | y |
| --- | --- | --- | --- | --- |
| 1 | 100 | +4 | +1 | 105 |
| 2 | 102 | −2 | −1 | 99 |
| 3 | 104 | −3 | 0 | 101 |
| 4 | 106 | +1 | −0,5 | 106,5 |
| 5 | 108 | +4 | 0 | 112 |
| 6 | 110 | −2 | −1 | 107 |
| 7 | 112 | −3 | +0,5 | 109,5 |
| 8 | 114 | +1 | −1 | 114 |

Descomponer es recorrer ese camino al revés: solo se ve la última columna y hay que reconstruir las
otras tres. La media móvil 2×4 en el punto 3 vale `(0,5·105 + 99 + 101 + 106,5 + 0,5·112)/4 =
103,75`, que estima la tendencia real de ese punto (104) con un error de 0,25, y la desviación
`y₃ − 103,75 = −2,75` estima el efecto estacional del tercer trimestre más el residuo.

Con una serie más larga se ve mejor. Sobre 48 trimestres simulados con la estacionalidad
`(+4, 0, −3, −1)` y ruido de desviación 1,2, la descomposición devuelve un patrón estimado de
`(+3,73; −0,09; −3,10; −0,54)` y un residuo con desviación 1,09, los dos muy cerca de los valores
simulados. Las medidas de fuerza salen **0,84 para la estacionalidad** y **0,97 para la tendencia**.

El caso multiplicativo es el que más se falla. Si la serie crece un 1 % por periodo y su patrón
estacional es `(1,10; 0,95; 0,90; 1,05)`, la amplitud del patrón **en unidades** crece con el
nivel: en una serie que pasa de 100 a 160, la diferencia entre el trimestre más alto y el más bajo
es de 26,4 unidades en crudo y de 0,210 en logaritmos, que es prácticamente `log(1,10) − log(0,90)
= 0,2007`. Descomponiendo el logaritmo y volviendo con la exponencial se recuperan los factores
`(1,106; 0,962; 0,897; 1,048)`. Si haces la descomposición aditiva sobre la serie en crudo, el
residuo sale con forma de abanico y la estacionalidad estimada es un promedio de amplitudes que no
le corresponde a ningún año.

## Código

```python verificable
import numpy as np

rng = np.random.default_rng(4)
n = 48
t = np.arange(n)
estacional = np.tile([4.0, 0.0, -3.0, -1.0], 12)      # patron trimestral fijo
y = 50 + 0.5 * t + estacional + rng.normal(0, 1.2, n)

def descomposicion(y, m):
    """Clasica: tendencia por media movil centrada de orden m y estacional por fases."""
    tend = np.full(y.size, np.nan)
    pesos = np.concatenate([[0.5], np.ones(m - 1), [0.5]]) / m
    for i in range(y.size - m):
        tend[i + m // 2] = pesos @ y[i:i + m + 1]
    detrend = y - tend
    fase = np.array([np.nanmean(detrend[k::m]) for k in range(m)])
    est = np.tile(fase - fase.mean(), y.size // m + 1)[:y.size]
    return tend, est, y - tend - est

tend, est, resid = descomposicion(y, 4)
print("estacional por trimestre", np.round(est[:4], 2))     # -> [ 3.73 -0.09 -3.1  -0.54]
print("tendencia en el punto 10 y en el 40", np.round([tend[9], tend[39]], 2))  # -> [54.42 69.4 ]
print("desv del residuo %.2f  (el ruido simulado era 1.20)" % np.nanstd(resid[3:-3], ddof=1))  # -> 1.09
vr = np.nanvar(resid[3:-3])
print("fuerza estacional %.2f" % max(0, 1 - vr / np.nanvar((est + resid)[3:-3])))   # -> 0.84
print("fuerza de tendencia %.2f" % max(0, 1 - vr / np.nanvar((tend + resid)[3:-3])))  # -> 0.97
```

:::claves
- `np.full(y.size, np.nan)` crea el array de la tendencia **lleno de `NaN`**, no de ceros. Es deliberado: los extremos no tienen ventana suficiente y hay que distinguir «no lo sé» de «vale cero». Un cero ahí arrastraría las medias y las fuerzas de la descomposición hacia abajo.
- `np.concatenate([[0.5], np.ones(m - 1), [0.5]]) / m` monta los pesos de la media móvil 2×4: los dos extremos valen la mitad. Los corchetes no son un capricho: `np.concatenate` necesita una **secuencia de arrays**, y un `0.5` suelto sería un escalar, que no se puede concatenar.
- `pesos @ y[i:i + m + 1]` es un producto escalar: multiplica los cinco pesos por los cinco valores y los suma. Equivale a `(pesos * ventana).sum()`, pero sin crear el array intermedio. El número de elementos tiene que coincidir, y por eso la ventana es `m + 1` valores para `m + 1` pesos.
- `for i in range(y.size - m)` se detiene antes del final para que `y[i:i + m + 1]` siempre tenga los cinco elementos. Y el resultado se escribe en `tend[i + m // 2]`, desplazado al centro de la ventana: la media móvil **centrada** estima la tendencia del punto de en medio, no del primero. Si guardaras en `tend[i]`, la tendencia saldría desplazada dos trimestres.
- `y - tend` funciona aunque `tend` tenga `NaN` en los extremos: NumPy propaga el `NaN`, así que esos puntos quedan fuera de `np.nanmean` sin necesidad de borrarlos a mano. Con `np.mean` en lugar de `np.nanmean` el resultado sería `NaN` entero.
- `est = np.tile(fase - fase.mean(), y.size // m + 1)[:y.size]` repite el patrón de cuatro valores hasta cubrir la serie y luego recorta. El `+ 1` es necesario porque `y.size // m` trunca: con 48 puntos son 12 ciclos justos, pero con 50 harían falta 13 y sobraría un valor que se corta con el `[:y.size]`.
- `fase - fase.mean()` centra el patrón estacional en cero. Sin esa resta, la estacionalidad se llevaría parte del nivel y la tendencia saldría desplazada: es la trampa clásica de las descomposiciones mal hechas.
- `np.nanstd(resid[3:-3], ddof=1)` recorta tres puntos por cada lado para quitar los extremos, que arrastran `NaN`. Y `ddof=1` divide entre `n − 1`, que es lo correcto al estimar una desviación de una muestra; NumPy usa `ddof=0` por defecto, así que sin ese argumento el número saldría algo más pequeño que el simulado.
:::

```python verificable
import numpy as np

rng = np.random.default_rng(5)
n = 48
t = np.arange(n)
tendencia = 100 * np.exp(0.01 * t)                    # crece un 1% por periodo
factor = np.tile([1.10, 0.95, 0.90, 1.05], 12)        # estacionalidad multiplicativa
y = tendencia * factor * np.exp(rng.normal(0, 0.02, n))

def patron_estacional(serie, m=4):
    """Media por fase de la serie sin tendencia (media movil centrada de orden m)."""
    pesos = np.concatenate([[0.5], np.ones(m - 1), [0.5]]) / m
    tend = np.full(serie.size, np.nan)
    for i in range(serie.size - m):
        tend[i + m // 2] = pesos @ serie[i:i + m + 1]
    detrend = serie - tend
    return np.array([np.nanmean(detrend[k::m]) for k in range(m)])

fase = patron_estacional(y)
print("amplitud en crudo       %.1f" % (fase.max() - fase.min()))       # -> 26.4
fase_log = patron_estacional(np.log(y))
print("amplitud en logaritmos  %.3f" % (fase_log.max() - fase_log.min()))  # -> 0.210
print("factores recuperados", np.round(np.exp(fase_log - fase_log.mean()), 3))
# -> [1.106 0.962 0.897 1.048] frente a los simulados 1.10, 0.95, 0.90 y 1.05
```

```python ilustrativo
# STL de verdad: los dos parametros que hay que decidir son las ventanas.
import warnings; warnings.filterwarnings("ignore")
import numpy as np
from statsmodels.tsa.seasonal import STL

res = STL(serie, period=4, seasonal=13, trend=25, robust=True).fit()

res.seasonal    # el patron estacional estimado, que puede cambiar ciclo a ciclo
res.trend       # la tendencia suavizada; los extremos son los menos fiables
res.resid       # lo que queda: aqui se buscan los atipicos

# Con seasonal="periodic" (o una ventana muy grande) el patron se obliga a ser el mismo
# en todos los ciclos; con una ventana pequena, el patron se mueve y hay que comprobar
# que ese movimiento es real y no esta copiando el ruido.
```

## Errores típicos

- **Descomponer de forma aditiva una serie multiplicativa.** Es el error más frecuente y se ve a
  simple vista: el residuo sale con forma de abanico (más disperso al final) y la estacionalidad
  estimada es un promedio de amplitudes distintas. Si la amplitud del patrón crece con el nivel,
  toma logaritmos antes de descomponer.
- **Usar la descomposición clásica y creer que la estacionalidad es fija.** El promedio por fases
  impone el mismo patrón en todos los ciclos. Si el negocio cambia, eso no aparece. Con STL se
  controla con `s.window`; con `seasonal="periodic"` vuelves a imponer un patrón fijo, lo cual está
  bien si de verdad lo es.
- **Elegir la ventana de la tendencia demasiado pequeña.** Si `t.window` baja de un ciclo, la
  tendencia se vuelve tan flexible que se come parte de la estacionalidad y el residuo queda
  artificialmente limpio. La descomposición se ve mejor y es peor: estás mezclando componentes.
- **Leer la tendencia del final como un pronóstico.** El suavizado es de dos lados y el último
  punto tiene menos vecinos a la derecha, así que su estimación es la más ruidosa y se revisará.
  Si necesitas el nivel de hoy, calcula la tendencia con un suavizado de un solo lado y asume el
  retraso.
- **Mirar el residuo solo para comprobar que es pequeño.** El residuo es el diagnóstico: si tiene
  forma de U, hay un ciclo que no has capturado; si tiene picos regulares, la estacionalidad está
  mal estimada; y los picos sueltos son los candidatos a error de carga o a
  [[outliers-y-deteccion|valor atípico]]. Un residuo con estacionalidad es una descomposición mal
  hecha.
- **Descomponer series con menos de dos o tres ciclos completos.** Con un año y medio de datos
  trimestrales no hay forma de separar tendencia de estacionalidad: cualquier reparto es arbitrario
  y las medidas de fuerza salen infladas.

:::practica
enunciado: Doce trimestres consecutivos: 52, 48, 47, 51, 56, 52, 51, 55, 60, 56, 55, 59. Calcula la media móvil centrada 2×4 en los trimestres tercero y séptimo y estima el efecto estacional del tercer trimestre.
pista: La media móvil 2×4 pondera con 0,5 los dos extremos de cinco valores consecutivos y divide entre 4; restarla al valor observado deja estacionalidad más residuo.
solucion: En el tercer trimestre (47) la ventana es 52, 48, 47, 51, 56: (0,5·52 + 48 + 47 + 51 + 0,5·56)/4 = 200/4 = 50, y la desviación es 47 − 50 = −3. En el séptimo (51) la ventana es 56, 52, 51, 55, 60: (0,5·56 + 52 + 51 + 55 + 0,5·60)/4 = 216/4 = 54, y la desviación es 51 − 54 = −3. El efecto estacional estimado del tercer trimestre es −3 millones.
:::

## Comprueba que lo sabes

:::quiz
p: Al descomponer la facturación mensual de una empresa en crecimiento, el residuo se hace cada vez más ancho y tiene forma de abanico. ¿Qué está pasando?
o: Que hay más ruido al final de la serie y no se puede hacer nada
o: Que la descomposición aditiva no es la adecuada: la estacionalidad multiplica al nivel, así que hay que descomponer el logaritmo
o: Que la ventana de la tendencia es demasiado grande
a: 2
e: Un residuo que crece con el nivel es la firma de un patrón multiplicativo: la amplitud estacional escala con el nivel de la serie. La solución es descomponer log(y), donde la relación vuelve a ser aditiva, y volver a la escala original con la exponencial.
:::

:::quiz
p: ¿Qué ventaja concreta aporta el modo robusto de STL frente a la descomposición clásica?
o: Que estima intervalos de predicción para la tendencia
o: Que reparte pesos decrecientes a los puntos con residuo grande, de modo que un atípico no arrastre la tendencia ni la estacionalidad
o: Que permite periodos estacionales impares, cosa que la clásica no permite
a: 2
e: El bucle exterior de STL calcula pesos de bisquare sobre el residuo: los puntos que se alejan mucho de la mediana reciben peso cero en la pasada siguiente. Los intervalos de predicción no los da ninguna descomposición, y la ventaja de los periodos impares es una propiedad aparte de STL, no del modo robusto.
:::

:::aviso
La tendencia que devuelve STL no es el nivel actual de la serie. Es una estimación centrada que usa
datos de los dos lados, así que los últimos valores se corrigen cuando llegan datos nuevos. Si vas
a publicar el «nivel de hoy», calcula la pendiente solo con el pasado y asume que vas con retraso.
:::
