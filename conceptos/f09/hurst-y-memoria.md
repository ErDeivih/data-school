---
id: hurst-y-memoria
titulo: Exponente de Hurst
fase: 9
nivel: experto
rutas: [quant, ds]
prerequisitos: [autocorrelacion-acf-pacf, estacionariedad, varianza-y-desviacion]
tags: [series-temporales, memoria, diagnostico]
resumen: Mide cómo crece la dispersión de una serie con el horizonte: 0,5 es un paseo aleatorio, por encima hay persistencia y por debajo, reversión a la media.
fuentes: ["Hurst (1951), 'Long-term storage capacity of reservoirs'", "Mandelbrot y Wallis (1969), 'Robustness of the rescaled range R/S in the measurement of noncyclic long run statistical dependence'"]
---

## En una frase

El exponente de Hurst `H` mide a qué velocidad crece la dispersión de una serie cuando alargas
el horizonte: `H = 0,5` es un paseo aleatorio puro, `H > 0,5` indica persistencia (los
incrementos tienden a repetir signo) y `H < 0,5`, reversión a la media.

## La idea

La pregunta que responde el exponente de Hurst es muy concreta: **¿cuánto se dispersa el
precio cuando dejo pasar el doble de tiempo?** Si los incrementos son independientes, la
respuesta es conocida: la varianza crece de forma proporcional al tiempo. Al doble de
horizonte, el doble de varianza; al cuádruple, el cuádruple. La desviación típica —que es la
raíz— crece con la raíz del tiempo, y así aparece el famoso `√252` que se usa para anualizar
volatilidades.

Cuando los incrementos no son independientes, esa proporción cambia. Si los retornos tienden a
venir en rachas del mismo signo (persistencia), la varianza crece **más** que
proporcionalmente: los movimientos se suman en lugar de compensarse. Si los retornos tienden a
alternar signo (antipersistencia), la varianza crece **menos** que proporcionalmente: los
movimientos se cancelan a medias. El exponente de Hurst es la potencia de esa relación, y `0,5` es el caso de referencia.

La historia viene de lejos y explica el nombre, así que conviene conocerla. Harold Edwin
Hurst trabajaba en el Nilo y estudiaba cómo dimensionar embalses para las crecidas. Observó
que el rango acumulado de las crecidas, medido en unidades de su propia desviación típica,
crecía con el número de años mucho más rápido de lo que predecía un proceso independiente:
había memoria. El estadístico que inventó para medirlo, el rango reescalado `R/S`, sigue
usándose hoy, y su nombre quedó pegado al exponente.

Para una serie financiera, la lectura práctica es esta. `H ≈ 0,5` significa que no hay
estructura aprovechable en la dependencia temporal: la serie se comporta como un paseo
aleatorio y cualquier regla basada en memoria de los retornos compite contra el ruido.
`H > 0,5` sugiere persistencia, el terreno del [[momentum|momentum]], y `H < 0,5` sugiere
reversión, el de la [[reversion-a-la-media|reversión a la media]]. Aquí aparece la advertencia
que hace experto a este concepto: en series financieras líquidas y con ventanas razonables, las
estimaciones suelen quedar **cerca de 0,5**, y las desviaciones que se ven dependen muchísimo de
la ventana, del rango de escalas elegido y del estimador. Un
`H` de 0,62 calculado sobre 300 observaciones no es una prueba de persistencia: es una
estimación con un intervalo de confianza que probablemente incluye el 0,5.

Hay tres estimadores que verás en la práctica y conviene saber qué hace cada uno:

- **Rango reescalado (R/S).** Divide la serie en bloques, calcula en cada bloque el rango
  acumulado de las desviaciones respecto a la media y lo normaliza por la desviación típica del
  bloque, y ajusta la potencia. Es el original, es sensible a la autocorrelación de corto plazo
  y por eso Anis y Lloyd propusieron una corrección.
- **Varianza agregada.** Es el camino directo: se calcula la varianza de los incrementos para
  varios retardos `τ` y se ajusta una recta en escala logarítmica. Es el que usan los ejemplos
  de abajo, porque es fácil de explicar y de programar.
- **DFA (análisis de fluctuación con tendencia eliminada).** Antes de medir la dispersión,
  quita una tendencia local en cada bloque. Es más robusto cuando la serie tiene tendencia
  determinista y es el estándar en aplicaciones de fisiología y de series largas.

Que existan tres estimadores tiene una consecuencia incómoda: **dan números distintos en la misma
serie**. Elegir el que más te gusta después de ver los resultados es una forma de
[[data-snooping-y-multiple-testing|autoengaño]] tan válida como probar 500 estrategias. Fija
el método, el rango de escalas y la ventana antes de mirar.

Dos confusiones que hay que deshacer. La primera: `H` no es el exponente de las colas gordas.
Que los retornos tengan curtosis alta (movimientos extremos frecuentes) es una propiedad de la
distribución, no de la memoria. La segunda: `H` no mide la autocorrelación de los retornos de
forma directa. Se puede tener una serie con `H ≈ 0,5` en los retornos y una volatilidad
fuertemente autocorrelacionada —de hecho es lo normal—, porque la memoria está en la varianza
y no en el signo. Si lo que te interesa es la agrupación de volatilidad, la herramienta es
[[garch-volatilidad|GARCH]] o la [[volatilidad-realizada|volatilidad realizada]], no el
exponente de Hurst.

El concepto tiene una conexión formal con [[diferenciacion-fraccional|la diferenciación
fraccional]]: el parámetro `d` de un proceso fraccionalmente integrado y el exponente de Hurst
se relacionan mediante `H = d + 0,5`. Diferenciar de forma fraccional es, precisamente, buscar
un punto intermedio entre no diferenciar (serie con raíz unitaria, `H` alto) y diferenciar una
vez (serie estacionaria sin memoria). El exponente de Hurst es la brújula que dice dónde
estás.

## Definición formal

Sea `X_t` el logaritmo del precio y `Δ_τ` el incremento en un horizonte de `τ` periodos:
`Δ_τ = X_{t+τ} − X_t`.

:::formula
Var(Δ_τ) ∝ τ^{2H}          log Var(Δ_τ) ≈ 2H · log τ + c
:::

- `X_t` — log-precio (o cualquier serie acumulada: no se estima `H` sobre retornos sueltos).
- `τ` — retardo en periodos; se toman varios, típicamente espaciados en potencias de 2
  (1, 2, 4, 8, 16, 32…).
- `Δ_τ` — incremento de la serie a lo largo de `τ` periodos.
- `Var(Δ_τ)` — varianza de esos incrementos, estimada sobre todas las ventanas disponibles.
- `H` — exponente de Hurst; sale de la pendiente de la recta ajustada en escala logarítmica,
  dividida entre 2.
- `c` — constante de la regresión, sin interés práctico.

Interpretación de `H`:

- `H = 0,5` — incrementos independientes. La varianza crece linealmente con `τ` y la
  desviación típica con `√τ`.
- `H > 0,5` — persistencia. La varianza crece más rápido que `τ`; los incrementos se refuerzan.
- `H < 0,5` — antipersistencia o reversión. La varianza crece más despacio; los incrementos se
  cancelan parcialmente.
- `H = 1` — tendencia perfectamente lineal (varianza creciendo con `τ²`).

**Rango reescalado.** Para un bloque de `n` observaciones `x₁ … x_n`, con `W_k` la suma
acumulada de las desviaciones respecto a la media del bloque y `s_n` su desviación típica:

:::formula
(R/S)(n) = ( max_k (W_k − (k/n) · W_n) − min_k (W_k − (k/n) · W_n) ) / s_n ,   (R/S)(n) ∝ n^H
:::

- `W_k = Σ_{i=1}^{k} (x_i − x̄)` — desviación acumulada hasta `k`.
- `s_n` — desviación típica de las `n` observaciones del bloque.
- `(R/S)(n)` — rango reescalado; se ajusta `log (R/S) = H · log n + a` sobre varios tamaños de
  bloque.

**Relación con la diferenciación fraccional:**

:::formula
H = d + 0,5
:::

donde `d` es el orden de diferenciación fraccional. En un proceso fraccionalmente integrado
estacionario, `d` y `H` miden la misma memoria desde dos ángulos distintos: `d = 0` es una
serie sin memoria y `d` mayor que 0, más persistencia.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `X_t` | El log-precio (la serie acumulada), no el retorno del periodo | logaritmo del precio | Es la serie sobre la que se estima `H`. Si en lugar de acumular usas retornos sueltos, la serie deja de ser integrada y el `H` que sale no mide memoria del precio: mide la de los incrementos |
| `τ` | El retardo o horizonte sobre el que se mide el incremento | periodos (días, meses) | Se recorren varios, espaciados en potencias de 2. Con escalas demasiado cortas manda el ruido de microestructura y `H` sale sesgado hacia abajo, como si hubiera reversión; el extremo largo deja pocos solapamientos y dispara la varianza de la estimación |
| `Δ_τ = X_{t+τ} − X_t` | El incremento acumulado a lo largo de `τ` periodos | logaritmo del precio | No es un parámetro que se elija: es la variable que se mide. Con `τ` mayor, cada observación solapa más con la siguiente y las varianzas dejan de ser independientes entre sí |
| `Var(Δ_τ)` | La varianza de esos incrementos, estimada sobre todas las ventanas disponibles | (log-precio)² | Es la variable dependiente de la regresión. Lo que importa no es su valor en un `τ`, sino cómo crece al doble de horizonte: doblarse es `H = 0,5`, más que doblarse es persistencia y menos es reversión |
| `H` | El exponente de Hurst: la mitad de la pendiente de `log Var` contra `log τ` | adimensional | Es el resultado. Por encima de 0,5 hay persistencia y por debajo, reversión, pero en una ventana de 250 observaciones el error de la estimación es del mismo orden que esas desviaciones, así que un 0,62 no distingue nada |
| `c` | La constante de la regresión log-log | (log-precio)² | No tiene interpretación económica: solo fija la altura de la recta. Cambiarla mueve la recta entera sin tocar la pendiente |
| `d` | Orden de diferenciación fraccional de la serie | adimensional | Se relaciona con `H` mediante `H = d + 0,5`. `d = 0` es una serie sin memoria y cuanto mayor es `d`, más persistencia; como `H` no puede pasar de 1, `d` no puede pasar de 0,5 |
| `n` | Tamaño del bloque en el estimador del rango reescalado `(R/S)(n)` | observaciones | Bloques grandes dan menos puntos para ajustar y más varianza; bloques pequeños se contaminan con la autocorrelación de corto plazo. Además `(R/S)(n)` crece como `n^H`, así que comparar dos `H` calculados con tamaños de bloque distintos no es comparar lo mismo |
| `s_n` | Desviación típica de las `n` observaciones del bloque | las de la serie | Es el denominador de `R/S`: si el bloque tiene una desviación típica casi nula, el cociente se dispara y ese punto domina el ajuste. Por eso se recomienda no usar bloques diminutos |
:::

:::figura
fichero: hurst-pendiente-log-varianza
pie: Lo que hay que mirar no es la altura de las nubes de puntos sino su inclinación: la persistente sube más deprisa que el tiempo (H = 0,60), el paseo aleatorio sube justo como el tiempo (H = 0,51) y la que revierte sube menos (H = 0,42). Las tres parten de la misma varianza a un periodo, así que el panel de la derecha traduce esa pendiente a algo tangible: a diez periodos, la persistente acumula 19 veces la dispersión del primer periodo, el paseo 10 y la que revierte 8. Con esa muestra grande las tres se separan; con 250 observaciones las tres estimaciones se solaparían.
fuente: figuras/hurst-y-memoria-1.py
:::

## Ejemplo

Se mide la varianza de los incrementos de una serie en cuatro horizontes:

| τ (periodos) | Var(Δ_τ) | log τ | log Var |
| --- | --- | --- | --- |
| 1 | 1,0 | 0,000000 | 0,000000 |
| 2 | 2,3 | 0,693147 | 0,832909 |
| 4 | 5,5 | 1,386294 | 1,704748 |
| 8 | 13,0 | 2,079442 | 2,564949 |

La regresión de `log Var` sobre `log τ` con estos cuatro puntos:

- Media de `log τ`: 1,039721. Media de `log Var`: 1,275652.
- Suma de productos de desviaciones: 2,9690.
- Suma de cuadrados de `log τ`: 2,4023.
- Pendiente: 2,9690 / 2,4023 = 1,236, luego **`H = 0,618`**.

Compáralo con el caso de referencia. Un paseo aleatorio con la misma varianza a un periodo
tendría varianzas 1,0; 2,0; 4,0 y 8,0: cada vez que doblas el horizonte, doblas la varianza.
En ese caso `log Var = log τ` para todos los puntos, la pendiente vale 1 y
**`H = 0,5`**.

La diferencia se traduce en algo tangible. Con `H = 0,618`, la varianza a 10 periodos es
`10^{2 · 0,618} = 10^{1,236} ≈ 17,2` veces la varianza a 1 periodo. Un paseo aleatorio daría
`10` veces. Es decir: los movimientos se acumulan un 72 % más de lo que acumularía el azar.
Eso es persistencia, y es la clase de estructura que un sistema de momentum intenta explotar.
Y dicho todo esto: cuatro puntos y una regresión no demuestran nada. La estimación de `H` con
cuatro escalas y una muestra corta tiene un error enorme, y por eso el ejemplo sirve para
entender el mecanismo, no para concluir nada sobre ningún activo.

## Código

```python verificable
import numpy as np

def hurst_agregada(x, lags=(1, 2, 4, 8, 16, 32)):
    """H por regresion log-log de la varianza de los incrementos agregados."""
    x = np.asarray(x, float)
    lags = np.asarray(lags)
    var = np.array([np.var(x[l:] - x[:-l], ddof=1) for l in lags])
    return np.polyfit(np.log(lags), np.log(var), 1)[0] / 2

rng = np.random.default_rng(42)
blanco = rng.normal(0, 1, 20000).cumsum()        # paseo aleatorio: H deberia ser 0,5
ret = np.zeros(20000)
for t in range(1, 20000):                        # AR(1) con phi = 0,3: memoria positiva
    ret[t] = 0.3 * ret[t - 1] + rng.normal(0, 1)
persistente = ret.cumsum()

print(f"paseo aleatorio  H = {hurst_agregada(blanco):.3f}")      # -> 0.506
print(f"con memoria AR1  H = {hurst_agregada(persistente):.3f}")  # -> 0.577
```

:::claves
- `hurst_agregada` no devuelve una varianza ni una vida media: devuelve **la mitad de la pendiente** de una regresión, es decir, un único número adimensional. Por eso `np.polyfit(...)[0] / 2` y no `np.polyfit(...)[0]`: si te olvidas de dividir entre 2, el paseo aleatorio sale 1,0 en lugar de 0,5 y todo el diagnóstico se va al garete.
- `x[l:] - x[:-l]` es la diferencia a distancia `l` y produce un array **más corto que `x`**: tiene `n − l` elementos. Con `l = 32` y 250 observaciones solo quedan 218, así que las varianzas de las escalas grandes se estiman con menos datos y son más ruidosas. Esa es la razón de que el extremo derecho de la nube de puntos baile tanto.
- `np.var(...)` usa `ddof=0` por defecto, y el código escribe `ddof=1` a propósito: divide entre `n − 1` en lugar de entre `n`. Con 20.000 observaciones la diferencia es invisible, pero con 250 no: cambiar `ddof` mueve `H` en la tercera cifra, y si comparas tu resultado con el de otra librería (pandas usa `ddof=1` en `Series.var()`) el desacuerdo suele venir de aquí.
- `lags=(1, 2, 4, 8, 16, 32)` se convierte con `np.asarray(lags)` antes de usarlo, y eso no es decorativo: `np.log` de una tupla de Python falla, porque necesita un array. Y `np.log(var)` con una varianza de 0 devolvería `-inf` y arrastraría toda la regresión, algo que ocurre si algún bloque tiene todos sus valores idénticos.
- El `H` que sale es una estimación puntual **sin intervalo**: `np.polyfit` no da error típico. Para saber si un 0,62 es compatible con 0,5 hay que remuestrear (bootstrap por bloques) o repetir el cálculo en subperiodos. Quitar ese paso es lo que convierte un diagnóstico en una promesa.
- Fíjate en que las dos series se generan con `rng` **después** del mismo `default_rng(42)`: `blanco` consume los primeros 20.000 números y `ret` los siguientes. Cambiar el tamaño de una serie desplaza el flujo del generador y cambia la otra, así que no puedes tocar una línea y esperar que los demás resultados sigan igual.
:::

```python verificable
import numpy as np

def hurst(x, lags=(2, 4, 8, 16, 32, 64)):
    x = np.asarray(x, float)
    lags = np.asarray(lags)
    var = np.array([np.var(x[l:] - x[:-l], ddof=1) for l in lags])
    return np.polyfit(np.log(lags), np.log(var), 1)[0] / 2

rng = np.random.default_rng(0)
# Diez paseos aleatorios puros (H real = 0,500) de solo 250 observaciones cada uno
estimaciones = [hurst(rng.normal(0, 1, 250).cumsum()) for _ in range(10)]

print("H estimada en cada muestra:")
print(np.round(estimaciones, 3))
print(f"minimo {min(estimaciones):.3f}  maximo {max(estimaciones):.3f}")  # -> minimo 0.253  maximo 0.558
print(f"media  {np.mean(estimaciones):.3f}")                              # -> 0.440
```

El segundo bloque es el que hay que tener grabado: diez series que **son** paseos aleatorios,
sin ninguna memoria, dan estimaciones entre 0,253 y 0,558. Cualquier `H` de 0,6 calculado con
250 puntos está dentro de ese ruido.

## Errores típicos

- **Leer `H > 0,5` como una predicción de dirección.** Persistencia significa que los
  incrementos tienden a repetir signo en promedio, no que el precio vaya a subir. Una serie
  persistente puede caer durante meses.
- **Estimar `H` con ventanas cortas y tomarse el número en serio.** Con 250 observaciones, un
  paseo aleatorio puro produce estimaciones entre 0,25 y 0,56, como muestra el código. Reporta
  siempre la ventana, el método, el rango de escalas y, si puedes, un intervalo por bootstrap.
- **Usar escalas demasiado cortas o `R/S` sin la corrección de Anis-Lloyd.** En el extremo
  corto domina el ruido de microestructura —el rebote bid-ask genera autocorrelación negativa
  artificial— y `H` sale sesgado hacia abajo, como si hubiera reversión; empieza en escalas
  donde ese ruido ya no manda y usa potencias de 2. Con `R/S` clásico y autocorrelación de
  corto plazo el sesgo va en el otro sentido, hacia arriba, y se confunde con persistencia de
  largo plazo si no aplicas la corrección.
- **Cambiar de estimador hasta que dé el resultado que te conviene.** R/S, varianza agregada y
  DFA dan números distintos sobre la misma serie. Fija el método antes de mirar los datos o
  estarás haciendo [[data-snooping-y-multiple-testing|selección sobre el resultado]].
- **Confundir `H` con la curtosis o con la autocorrelación de los retornos.** Las colas gordas
  son una propiedad de la distribución; la agrupación de volatilidad es memoria en la varianza.
  Son fenómenos distintos y se miden con herramientas distintas.
- **Presumir de `H` sin comprobar que la serie es la adecuada.** Se calcula sobre log-precios o
  sobre la serie acumulada de los incrementos, no sobre retornos sueltos, y no tiene sentido en
  una serie con tendencia determinista fuerte sin usar un estimador que la elimine, como DFA.

:::practica
enunciado: La varianza de los incrementos de una serie vale 1,0 a un día y 4,1 a ocho días. Estima el exponente de Hurst con esas dos escalas y di si la serie tiende, revierte o pasea.
pista: En escala logarítmica la varianza crece como 2H · log τ, así que H es la mitad de la pendiente entre los dos puntos.
solucion: Pendiente = ln(4,1 / 1,0) / ln(8 / 1) = 1,411 / 2,079 = 0,679. H = 0,679 / 2 = 0,34. Un paseo aleatorio tendría varianza 8,0 a ocho días, ocho veces la de un día, y aquí solo crece 4,1 veces: los incrementos se cancelan en parte. Al quedar H por debajo de 0,5 hay antipersistencia, el terreno de la reversión a la media. Con dos escalas el número es orientativo.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué significa un exponente de Hurst de 0,5 en una serie de log-precios?
o: Que la serie no tiene ninguna tendencia en la muestra
o: Que la varianza de los incrementos crece de forma lineal con el horizonte, como en un paseo aleatorio
o: Que la serie es estacionaria
a: 2
e: H = 0,5 es el caso de incrementos independientes: la varianza crece proporcionalmente a τ y la desviación con √τ. No dice que la muestra no tenga tendencia (un paseo aleatorio puede tenerla) ni que la serie de niveles sea estacionaria, que es justo lo contrario.
:::

:::quiz
p: Si el exponente de Hurst de una serie es 0,7 y la varianza a un día es 1, ¿cuál es la varianza aproximada a 10 días?
o: Unos 10, porque la varianza es lineal en el tiempo
o: Unos 25, porque 10 elevado a 2 · 0,7 es aproximadamente 25
o: Unos 5,0, porque la desviación típica crece con 10 elevado a 0,7
a: 2
e: La relación es Var ∝ τ^(2H), así que con H = 0,7 el exponente es 1,4 y 10^1,4 ≈ 25,2. La opción 1 corresponde a H = 0,5 (paseo aleatorio) y la opción 3 confunde la varianza con la desviación típica: 10^0,7 ≈ 5,0 es el crecimiento de la desviación, y la varianza es su cuadrado.
:::

:::quiz
p: Estimas H en una serie líquida con 250 observaciones y sale 0,62. ¿Cuál es la conclusión correcta?
o: La serie tiene memoria persistente y conviene aplicar momentum
o: La estimación es compatible con un paseo aleatorio: con esa ventana, la incertidumbre del estimador es del mismo orden que la desviación observada
o: El estimador está mal calculado, porque H nunca puede superar 0,5 en finanzas
a: 2
e: Con 250 puntos, un paseo aleatorio puro produce estimaciones entre 0,25 y 0,56, así que un 0,62 está a un paso del ruido. Antes de concluir nada hay que ampliar la ventana, comprobar la estabilidad en subperiodos y calcular un intervalo. Nada prohíbe que H supere 0,5: precisamente esa es la hipótesis que se quiere detectar.
:::

:::nota
El exponente de Hurst es un diagnóstico de estructura, no una señal de trading. Un `H` alto no
te dice el signo del próximo movimiento ni cuánto dura la racha: solo dice que, en la muestra y
en las escalas que has medido, los incrementos se refuerzan más de lo que haría el azar.
:::
