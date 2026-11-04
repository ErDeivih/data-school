---
id: autocorrelacion-acf-pacf
titulo: Autocorrelación, ACF y PACF
fase: 5
nivel: intermedio
rutas: [ds, quant]
prerequisitos: [estacionariedad, covarianza-y-correlacion]
tags: [series-temporales, autocorrelacion, diagnostico]
resumen: Cuanto se parece una serie a sí misma desplazada k pasos, y qué queda de ese parecido cuando descuentas los retardos intermedios.
fuentes: ["Hyndman y Athanasopoulos (2021), 'Forecasting: Principles and Practice', cap. 8", "Box, Jenkins y Reinsel (2015), 'Time Series Analysis: Forecasting and Control'"]
---

## En una frase

La autocorrelación mide el parecido entre una serie y ella misma desplazada `k` posiciones; la
ACF dibuja ese parecido para todos los retardos y la PACF lo vuelve a medir después de descontar
el efecto de los retardos intermedios.

## La idea

Piensa en una serie en la que cada valor copia el 80 % del valor de ayer más un poco de ruido.
Hoy vale 100; mañana, lo más probable es que ronde 80. Y pasado mañana, ¿qué? También rondará 80,
pero no porque exista una relación directa entre pasado mañana y hoy: existe porque pasado mañana
hereda el 80 % de mañana, que a su vez heredó el 80 % de hoy. La cadena es
0,8 · 0,8 = 0,64.

Eso es lo que mide la **ACF**: el parecido total entre la serie y su copia desplazada, sin
preguntar por dónde viene ese parecido. Con el ejemplo anterior, la ACF en el retardo 1 vale 0,8,
en el 2 vale 0,64, en el 3 vale 0,512, y así bajando hacia cero. No hay ninguna relación directa
entre un día y el de hace dos semanas, pero la ACF no es cero porque la cadena sigue viva.

La **PACF** responde a la pregunta más fina: ¿cuánta relación directa queda entre `y_t` y
`y_{t−k}` una vez que ya sé los valores intermedios? En el mismo ejemplo, la PACF en el retardo 1
vale 0,8 (nada que descontar), pero en el retardo 2 es aproximadamente 0: sabiendo el valor de
ayer, el de anteayer no añade nada.

La PACF es una medida de relación *directa*, como una
correlación parcial en [[regresion-lineal|una regresión]].

Esa diferencia es lo que se usa para leer los dos gráficos. La ACF y la PACF se miran
juntas porque se complementan, y sirven para tres cosas concretas: proponer un orden de modelo,
detectar estacionalidad y detectar que la serie no es estacionaria.

Dos avisos antes de seguir. Primero: **toda autocorrelación calculada con `n` datos tiene ruido**.
Bajo la hipótesis de que no hay autocorrelación, las estimaciones se reparten aproximadamente
alrededor de cero con una desviación típica de `1/√n`; por eso los correlogramas dibujan dos
bandas en `±1,96/√n` y solo se hace caso a lo que sobresale. Con 50 datos, cualquier cosa por
debajo de 0,28 es indistinguible de ruido. Segundo: la ACF **no dice nada sobre relaciones entre
variables distintas**; eso es otra cosa, la [[covarianza-y-correlacion|correlación entre dos variables]].

Hay dos patrones de fondo que conviene reconocer a simple vista:

- **Decaimiento muy lento.** Si la ACF sigue valiendo 0,95 en el retardo 20, no estás viendo una
  memoria larguísima: estás viendo una serie no estacionaria, probablemente con tendencia. Antes
  de interpretar nada, [[estacionariedad|comprueba estacionariedad]] y diferencia.
- **Picos que reaparecen cada `s` retardos.** Si la ACF tiene un pico en 4, otro en 8, otro en 12
  y otro en 16, la serie tiene estacionalidad trimestral. Eso no es un AR(16).

## Definición formal

Con `n` observaciones `y_1, …, y_n` y media muestral `ȳ`, la **autocovarianza** en el retardo `k`
se estima como

:::formula
γ̂_k = (1/n) · Σ_{t=k+1}^{n} (y_t − ȳ)(y_{t−k} − ȳ)   ·   ρ̂_k = γ̂_k / γ̂_0
:::

- `k` — el retardo, en el mismo paso temporal que la serie.
- `γ̂_k` — la autocovarianza estimada en el retardo `k`.
- `γ̂_0` — la autocovarianza en el retardo 0, que es la varianza muestral con denominador `n`.
- `ρ̂_k` — la autocorrelación estimada en el retardo `k`; siempre está entre −1 y 1.
- `Σ_{t=k+1}^{n}` — la suma sobre todos los pares de observaciones separadas exactamente `k`
  pasos. El denominador es `n` (no `n − k`): es el estimador habitual, sesgado hacia cero, pero
  con menos varianza que el insesgado.

La **PACF** en el retardo `k`, que se escribe `α_kk`, es el coeficiente de `y_{t−k}` en la
regresión de `y_t` sobre `y_{t−1}, …, y_{t−k}`:

:::formula
α_kk = último coeficiente de y_t = c + φ₁·y_{t−1} + … + φ_k·y_{t−k} + e_t
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `n` | Número de observaciones de la serie | observaciones | La estimación se vuelve más fiable y la banda `±1,96/√n` se estrecha: con 400 datos es ±0,10 y con 20 es ±0,44. El mismo 0,3 es señal con 1.000 datos y ruido con 20 |
| `k` | El retardo: cuántos pasos separan las dos observaciones que se comparan | pasos (días, meses) | No es un parámetro que se elija, se recorre. A más `k`, menos pares entran en la suma y más ruidosa es la estimación |
| `ρ̂_k` | La autocorrelación estimada en el retardo `k` | adimensional, entre −1 y 1 | Es el resultado. Por encima de `1,96/√n` en valor absoluto se considera distinta de cero; un decaimiento muy lento (0,95 en el retardo 20) no indica memoria larga, indica que la serie no es estacionaria |
| `γ̂_k` | La autocovarianza estimada en el retardo `k` | las de la serie, al cuadrado | Conserva las unidades y depende de la escala; por eso se prefiere `ρ̂_k`, que está normalizada y se puede comparar entre series |
| `γ̂_0` | La autocovarianza en el retardo 0, o sea la varianza | las de la serie, al cuadrado | Es el denominador de `ρ̂_k`. Ojo: es la varianza con denominador `n`, no `n − 1`, así que no coincide exactamente con `serie.var(ddof=1)` |
| `Σ_{t=k+1}^{n}` | La suma sobre los pares separados exactamente `k` pasos | las de la serie, al cuadrado | El denominador de `γ̂_k` es `n`, no `n − k`: es el estimador habitual, sesgado hacia cero pero con menos varianza. Cambiarlo a `n − k` sube un poco todas las barras |
| `α_kk` | La PACF en el retardo `k`: el último coeficiente del AR(k) | adimensional, entre −1 y 1 | En un AR(p) corta en seco tras el retardo `p`; si no corta, hay más estructura que un solo retardo no explica |
| `1,96/√n` | La banda de confianza aproximada al 95 % | adimensional | Marca el listón: por debajo de ella la barra es indistinguible de cero. Bajo la nula, las autocorrelaciones se reparten alrededor de cero con desviación típica `1/√n` |
:::

:::figura
fichero: acf-decaimiento-lento
pie: Dos series dibujadas con su media de todo el periodo: una estacionaria de 400 puntos y un paseo aleatorio de 500. La azul vuelve una y otra vez a su media y su ACF baja rápido; la roja se va y no vuelve, y su ACF sigue en 0,6 tras veinte retardos. Ese decaimiento lento no es memoria larga: es la firma de una raíz unitaria, y antes de interpretar cualquier correlograma hay que comprobar la estacionariedad.
fuente: figuras/autocorrelacion-acf-pacf-1.py
:::

:::figura
fichero: acf-pacf-de-un-ar1
pie: El mismo AR(1) con 400 observaciones mirado con los dos gráficos. La ACF baja despacio, 0,77 y 0,60: parece que el retardo 2 también dice algo. La PACF, en cambio, corta en seco tras el retardo 1, porque ese 0,60 de la ACF era la cadena 0,8 · 0,8 (0,64 en teoría) y no una relación directa. Ese corte es la firma del AR(1), y es la razón de mirar los dos gráficos juntos.
fuente: figuras/autocorrelacion-acf-pacf-1.py
:::

- `α_11` coincide con `ρ̂_1`, porque con un solo retardo no hay nada que descontar.
- `α_kk` se obtiene de forma eficiente con la **recursión de Durbin-Levinson**, que va calculando
  el AR(1), el AR(2), el AR(3)… y se queda con el último coeficiente de cada uno, en lugar de
  ajustar `k` regresiones distintas.
- La **banda de confianza** aproximada al 95 % es `±1,96/√n`.

La forma de los dos gráficos identifica el tipo de modelo:

| Proceso | ACF | PACF |
| --- | --- | --- |
| AR(p) | decae gradualmente (exponencial o sinusoidal) | corta en seco tras el retardo p |
| MA(q) | corta en seco tras el retardo q | decae gradualmente |
| ARMA(p,q) | decae gradualmente | decae gradualmente |
| Con tendencia | decae muy despacio, casi lineal | pico enorme en el retardo 1 |
| Con estacionalidad | picos en s, 2s, 3s… | picos en s, 2s, 3s… |

## Ejemplo

Seis observaciones: `2, 4, 3, 5, 4, 6`, con media `ȳ = 4`. Las desviaciones respecto a la media
son `−2, 0, −1, 1, 0, 2`, y la suma de sus cuadrados es 10.

- Retardo 1: se multiplican las desviaciones por las de un paso antes, se suman y se divide:
  `(−2)·0 + 0·(−1) + (−1)·1 + 1·0 + 0·2 = −1`. Como el denominador es la suma de cuadrados,
  `ρ̂_1 = −1/10 = −0,1`.
- Retardo 2: `(−1)·(−2) + 1·0 + 0·(−1) + 2·1 = 4`, luego `ρ̂_2 = 4/10 = 0,4`.
- Retardo 3: `1·(−2) + 0·0 + 2·(−1) = −4`, luego `ρ̂_3 = −4/10 = −0,4`.

Con `n = 6`, la banda del 95 % es `±1,96/√6 = ±0,80`. Ninguno de los tres valores la supera, así
que con estos datos no hay evidencia de autocorrelación: es lo que esperarías de seis
números casi arbitrarios. Este ejemplo sirve para ver el mecanismo, no para concluir nada.

Para ver un patrón de verdad hace falta una serie larga. Un AR(1) con coeficiente 0,8 y 500
observaciones da una ACF de 0,78, 0,62 y 0,53 en los retardos 1, 2 y 3 (bajando aproximadamente
como `0,8^k`), y una PACF de 0,78, 0,04 y 0,07: el primer retardo es enorme y los siguientes están
dentro de la banda `±0,088`. Ese corte en seco de la PACF con una ACF que se desliza es la firma
de un AR(1).

## Código

```python verificable
import numpy as np

def acf(x, nlags):
    """Autocorrelaciones muestrales con denominador 1/n (el estimador sesgado)."""
    d = x - x.mean()
    g0 = (d @ d) / d.size
    return np.array([1.0] + [(d[k:] @ d[:-k]) / d.size / g0 for k in range(1, nlags + 1)])

y = np.array([2.0, 4.0, 3.0, 5.0, 4.0, 6.0])
desv = y - y.mean()
print("media", y.mean(), " suma de cuadrados", (desv ** 2).sum())        # -> media 4.0 y 10.0
print("numerador del retardo 1", (desv[1:] * desv[:-1]).sum())          # -> -1.0
print("acf retardos 0..3", np.round(acf(y, 3), 3))                      # -> [ 1.  -0.1  0.4 -0.4]
print("banda del 95%", round(1.96 / np.sqrt(y.size), 2))                # -> 0.8
```

:::claves
- `d[k:] @ d[:-k]` es un producto escalar, y **no** incluye el retardo 0 porque el bucle empieza en 1: el 1,0 de la lista se añade a mano (`[1.0] + [...]`). La longitud de lo que se multiplica es `n − k`, pero se divide entre `d.size`, que vale `n`. Ese es el estimador sesgado del que habla la página: con `n = 6` y `k = 1`, la división entre `n − k` daría −0,2 en lugar de −0,1, el doble. Con series largas la diferencia se estrecha, pero en un ejemplo de seis datos es enorme.
- El `@` entre dos vectores devuelve un escalar de NumPy, no un array de un elemento. Si en vez de `d[k:] @ d[:-k]` escribes `d[k:] * d[:-k]`, obtienes un array y el `np.array([...])` de fuera construye una matriz en vez de un vector: la lista de retardos deja de tener la forma que esperas y el `np.round` final devuelve algo distinto. Para multiplicar elemento a elemento y quedarte con un número hace falta `.sum()`.
- `x.mean()` es la media de todo el vector, incluidos los extremos. La ACF se calcula restando **esa** media a todos los valores, así que un dato atípico al final mueve `d` entero y cambia todas las barras, no solo las de los retardos largos.
- `np.round(acf(y, 3), 3)` se queda con tres decimales, y en el segundo bloque `round(1.96 / np.sqrt(y.size), 3)` con tres para que salga 0,088. Redondear la banda a dos decimales da 0,1, más ancha que la real: con datos justo en el filo, la decisión de si una barra es señal cambia.
- `np.zeros((nlags + 1, nlags + 1))` declara una matriz de ceros y el código solo llena la mitad superior. La fila 0 y la columna 0 se quedan sin usar a propósito: así `phi[k, 1:k]` se lee igual que la fórmula, con los retardos empezando en 1. Si empiezas el índice en 0, todos los desplazamientos del bucle se descolocan una posición.
- `phi[k - 1, k - 1:0:-1]` invierte el orden de los coeficientes del paso anterior. Ese `::-1` es el que implementa la recursión de Durbin-Levinson: sin él obtienes números que se parecen pero no son la PACF, y el error no salta a la vista porque el primer retardo sigue saliendo bien.
- `for t in range(1, n)` deja `y[0] = 0` como valor inicial del AR(1), y luego `y = y[100:]` descarta el arranque. Ese descarte es necesario: los primeros valores arrastran el cero inicial, así que la ACF del principio está sesgada. Sin semilla fija, además, los 0,779 y 0,624 cambiarían en cada ejecución.
:::

```python verificable
import numpy as np

def acf(x, nlags):
    d = x - x.mean()
    g0 = (d @ d) / d.size
    return np.array([1.0] + [(d[k:] @ d[:-k]) / d.size / g0 for k in range(1, nlags + 1)])

def pacf(r, nlags):
    """Durbin-Levinson: la PACF es el ultimo coeficiente de cada AR(k)."""
    phi = np.zeros((nlags + 1, nlags + 1))
    phi[1, 1] = r[1]
    for k in range(2, nlags + 1):
        num = r[k] - phi[k - 1, 1:k] @ r[k - 1:0:-1]
        den = 1 - phi[k - 1, 1:k] @ r[1:k]
        phi[k, k] = num / den
        phi[k, 1:k] = phi[k - 1, 1:k] - phi[k, k] * phi[k - 1, k - 1:0:-1]
    return np.array([phi[k, k] for k in range(1, nlags + 1)])

rng = np.random.default_rng(1)
n = 600
y = np.zeros(n)
for t in range(1, n):                     # AR(1) con phi = 0.8
    y[t] = 0.8 * y[t - 1] + rng.normal(0, 1)
y = y[100:]                               # descartamos el arranque

r = acf(y, 3)
print("acf  retardos 1..3", np.round(r[1:], 3))       # -> [0.779 0.624 0.526]
print("pacf retardos 1..3", np.round(pacf(r, 3), 3))  # -> [0.779 0.043 0.069]
print("banda del 95%", round(1.96 / np.sqrt(y.size), 3))  # -> 0.088
```

## Errores típicos

- **Leer el correlograma sin la banda.** Con 60 observaciones, la banda es `±0,25`: un pico de
  0,2 es ruido, no señal. Si no dibujas (o calculas) la banda, acabarás viendo estructura en
  cualquier serie aleatoria.
- **Confundir qué gráfico corta.** Un AR(1) tiene ACF que decae y PACF que corta; un MA(1), lo
  contrario. Si eliges el orden mirando solo uno de los dos, te equivocas en la mitad de los
  casos: míralos siempre juntos.
- **Interpretar el decaimiento lento como memoria larga.** Una ACF que sigue en 0,9 tras 20
  retardos casi siempre significa que la serie tiene tendencia o raíz unitaria. Diferénciala y
  vuelve a mirar antes de hablar de [[hurst-y-memoria|memoria larga]].
- **Comparar ACF de series de distinta longitud.** La banda y la propia estimación dependen de
  `n`. Una ACF de 0,3 con 1.000 datos es señal; con 20 datos, no.
- **Tomar los picos estacionales por un AR de orden alto.** Un pico en 12, 24 y 36 con datos
  mensuales es estacionalidad anual: se resuelve con una diferencia estacional o un modelo
  [[arima-sarima|SARIMA]], no metiendo doce retardos en un AR.
- **Calcular la ACF sobre la serie en niveles cuando el modelo es en diferencias.** Si el modelo
  se ajusta a `Δy_t`, el diagnóstico de residuos y las ACF que comparas tienen que estar en la
  misma escala. Mezclar niveles y diferencias lleva a conclusiones que no se sostienen.

:::practica
enunciado: Tienes 400 observaciones y en el correlograma aparece un pico de 0,12 en el retardo 5. Calcula la banda del 95 % y decide si es señal. Para un AR(1) con coeficiente 0,7, ¿cuánto vale la ACF en el retardo 2 y qué esperas en la PACF de ese mismo retardo?
pista: La banda es 1,96 dividido por la raíz de n. En un AR(1) la ACF decae como φ elevado al retardo.
solucion: La banda es 1,96/√400 = 1,96/20 = 0,098. El pico de 0,12 la supera por poco, así que es señal, aunque débil. La ACF del AR(1) en el retardo 2 es 0,7² = 0,49, y la PACF en ese retardo es aproximadamente 0: en un AR(1) toda la relación pasa por el retardo 1 y la PACF corta en seco tras él.
:::

## Comprueba que lo sabes

:::quiz
p: Un AR(1) con coeficiente 0,8 tiene ACF de 0,8 en el retardo 1 y de 0,64 en el 2. ¿Por qué la PACF en el retardo 2 es casi cero?
o: Porque la ACF siempre miente en el segundo retardo
o: Porque el 0,64 es el efecto indirecto que pasa por el retardo 1, y al descontarlo no queda relación directa
o: Porque con 500 datos la PACF solo puede valer cero o uno
a: 2
e: La PACF mide la relación directa entre y_t y y_{t-2} una vez conocido y_{t-1}. En un AR(1) no hay tal relación directa: el 0,64 aparece porque y_{t-2} influye en y_{t-1} y este en y_t. Esa cadena es la que descuenta la PACF.
:::

:::quiz
p: Con 100 observaciones, la ACF de tu serie vale 0,55 en el retardo 1 y 0,52, 0,50, 0,48 en los siguientes. ¿Qué sospechas?
o: Un AR(1) con coeficiente 0,55
o: Un MA(4), porque hay cuatro retardos apreciables
o: Una serie no estacionaria, porque la ACF decae demasiado despacio
a: 3
e: Una ACF que baja muy lentamente (de 0,55 a 0,48 en cuatro retardos) es la firma de una raíz unitaria o de una tendencia, no de un proceso estacionario con memoria. La banda con n=100 es ±0,196, así que todos esos valores son significativos y el problema no es el ruido.
:::

:::nota
La ACF y la PACF se calculan sobre la serie ya transformada. Si tu modelo trabaja con retornos
logarítmicos, mira la ACF de los retornos; si trabajas con diferencias estacionales, mira la de
las diferencias estacionales. Y el diagnóstico final se hace sobre los **residuos** del modelo,
no sobre la serie original.
:::
