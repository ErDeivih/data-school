---
id: garch-volatilidad
titulo: GARCH y volatilidad
fase: 5
nivel: avanzado
rutas: [quant, ds]
prerequisitos: [estacionariedad, autocorrelacion-acf-pacf, varianza-y-desviacion]
tags: [volatilidad, riesgo, series-temporales]
resumen: La varianza de hoy depende del shock de ayer y de la volatilidad de ayer; modelarla por separado es lo que permite medir el riesgo cuando cambia.
fuentes: ["Engle (1982), 'Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation'", "Bollerslev (1986), 'Generalized Autoregressive Conditional Heteroskedasticity'", "Tsay (2010), 'Analysis of Financial Time Series'"]
---

## En una frase

GARCH modela la varianza condicional de una serie: la volatilidad de hoy es una mezcla de la
magnitud del shock de ayer y de la volatilidad de ayer, así que los tramos tranquilos y los
violentos se agrupan y se pueden pronosticar.

## La idea

Coge los retornos diarios de cualquier índice de bolsa y calcula dos cosas. Primero, la
correlación de cada retorno con el del día anterior: sale prácticamente cero. Segundo, la
correlación del **valor absoluto** de cada retorno con el del día anterior: sale claramente
positiva, del orden de 0,2 en muchos mercados. Es decir, **el signo de la rentabilidad es
impredecible, pero su magnitud no lo es**. Los días movidos van seguidos de días movidos, y los
tranquilos de tranquilos. Es el fenómeno que Mandelbrot describió en los años sesenta mirando
precios de algodón, y es la regularidad empírica más robusta de todas las series financieras.

La consecuencia práctica es incómoda: si mides el riesgo con la desviación típica de todo el
histórico, usas un número que está mal **precisamente en los peores días**. En un día tranquilo te
sobreestima el riesgo y te quedas corto de posición; en un día de pánico te lo subestima y
arriesgas mucho más de lo que crees. Y como el riesgo es lo que determina el tamaño de la
posición, ese error se traduce directamente en dinero.

La solución de Engle y Bollerslev es tratar la varianza como una serie temporal más. La idea, en
palabras, es esta:

- La varianza de hoy tiene un **suelo** `ω` al que nunca baja.
- Sube con la **magnitud del shock de ayer**: un movimiento grande (da igual si hacia arriba o
  hacia abajo) deja la volatilidad alta. Ese término es la parte **ARCH**, y su coeficiente `α`
  mide cuánto reacciona la volatilidad al último susto.
- Sube también con la **volatilidad de ayer**: si veníamos de una racha agitada, la calma tarda en
  volver. Ese término es la parte **GARCH**, y su coeficiente `β` mide la persistencia.

Todo el modelo cabe en tres parámetros, y de ellos sale una lectura muy útil: la suma `α + β` es
la **persistencia**. Si vale 0,98, un susto tarda muchísimo en desaparecer; si vale 0,85, la
volatilidad vuelve a su nivel en pocos días. En mercados de acciones, `α + β` suele estar entre
0,95 y 0,99: la volatilidad es un proceso muy pegajoso.

Dos hechos que se deducen del modelo y que conviene tener presentes:

1. **Las colas gordas aparecen solas.** Aunque los shocks `z_t` sean normales, la serie resultante
   tiene curtosis mayor que la de una normal, porque la varianza cambia. No hace falta inventar una
   distribución rara para reproducir las colas de los retornos.
2. **La asimetría no aparece.** El GARCH básico trata igual una subida del 3 % y una bajada del
   3 %. En bolsa, las caídas suelen subir más la volatilidad que las subidas de la misma
   magnitud: eso es el efecto apalancamiento, y para capturarlo hacen falta variantes como
   GJR-GARCH o EGARCH, que añaden un término que solo se activa con los shocks negativos.

Y una advertencia que ahorra disgustos: GARCH pronostica **cuánto** se mueve el precio, no **hacia
dónde**. Sirve para riesgo, para tamaño de posición y para valorar opciones, no para saber si
comprar o vender.

## Definición formal

Sea `ε_t` el retorno (ya descontada su media) en el instante `t`. Un GARCH(p,q) se escribe como

:::formula
ε_t = σ_t · z_t   ·   σ²_t = ω + Σ_{i=1}^{q} α_i·ε²_{t−i} + Σ_{j=1}^{p} β_j·σ²_{t−j}
:::

- `ε_t` — el retorno del periodo `t`, que es el producto de su volatilidad por un shock puro.
- `σ²_t` — la **varianza condicional**: la varianza de `ε_t` conocida toda la información hasta
  `t − 1`. Es lo que el modelo pronostica.
- `z_t` — el shock estandarizado, ruido blanco con media 0 y varianza 1, independiente de la
  información pasada. `σ_t = √σ²_t` es la volatilidad condicional.
- `ω > 0` — el suelo de la varianza condicional: el valor por debajo del cual `σ²_t` no baja.
- `α_i ≥ 0` — coeficientes ARCH: peso de los cuadrados de los shocks pasados.
- `β_j ≥ 0` — coeficientes GARCH: peso de las varianzas pasadas.
- `p` y `q` — el número de retardos de varianza y de shocks cuadrados. En la práctica,
  GARCH(1,1) es el estándar y casi siempre basta.

El caso GARCH(1,1), el que se usa de verdad, es

:::formula
σ²_t = ω + α·ε²_{t−1} + β·σ²_{t−1}     con α + β < 1
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `ε_t` | El retorno del periodo `t`, ya descontada su media | tanto por uno o % diario | — |
| `σ²_t` | La varianza condicional: la varianza de `ε_t` sabiendo todo lo anterior a `t` | retorno al cuadrado | Es lo que el modelo pronostica: nada más sube o baja aquí, es la salida |
| `σ_t` | La volatilidad condicional, `√σ²_t` | % diario (o anualizado) | Es la cifra que se usa para dimensionar la posición y calcular el VaR |
| `z_t` | El shock estandarizado: ruido blanco de media 0 y varianza 1 | adimensional | Es lo único impredecible del modelo; su distribución (normal o t) decide lo gordas que salen las colas |
| `ω` | El suelo de la varianza: el término constante | retorno al cuadrado | Sube el nivel de largo plazo `ω / (1 − α − β)` con toda la volatilidad, también en los días tranquilos. Es el parámetro que menos se interpreta solo: casi todo su efecto va a través de la varianza incondicional |
| `α` | Coeficiente ARCH: cuánto reacciona la varianza al último shock | adimensional, `α ≥ 0` | La volatilidad responde más al último susto: los picos son más altos y más bruscos, y el modelo reacciona antes. Alargar demasiado `α` y encoger `β` deja una volatilidad que se apaga de golpe, que no es lo que se ve en los mercados |
| `β` | Coeficiente GARCH: cuánto pesa la volatilidad de ayer | adimensional, `β ≥ 0` | La volatilidad se vuelve más pegajosa. Con `β` alto, un susto tarda meses en desaparecer y los tramos tranquilos y violentos duran mucho |
| `α + β` | La persistencia: la velocidad a la que la varianza vuelve a su nivel | adimensional, tiene que ser menor que 1 | Con 0,85 la calma vuelve en pocos días; con 0,98 un susto tarda 34 días en irse a la mitad; si llega a 1 el modelo es IGARCH y la varianza no tiene nivel de retorno |
| `σ² = ω / (1 − α − β)` | La varianza incondicional de largo plazo | retorno al cuadrado | Sube con `ω` y se dispara cuando `α + β` se acerca a 1: la misma `ω` da una volatilidad de largo plazo mucho mayor cuanto más persistente es el proceso |
| `ln(0,5) / ln(α + β)` | Vida media de un shock, en periodos | periodos (días) | Cuanto más cerca de 1 está `α + β`, más larga: pasa de unos 4 días con persistencia 0,85 a 34 con 0,98 y a más de un año con 0,999 |
| `p`, `q` | Número de retardos de varianza y de shocks cuadrados | número entero | Más retardos, más parámetros que estimar y más sobreajuste con pocos datos. GARCH(1,1) es el estándar y casi siempre basta |
| `h` | El horizonte del pronóstico de la varianza | pasos (días) | La varianza pronosticada se aleja de su nivel actual y converge al incondicional a velocidad `α + β` por paso: a pocos días manda la varianza de hoy, a muchos manda `α + β` |
:::

De ahí salen tres cantidades que se calculan a mano:

- **Varianza incondicional** (el nivel al que vuelve el proceso): `σ² = ω / (1 − α − β)`. Existe
  solo si `α + β < 1`; si la suma es 1 el modelo es IGARCH y la varianza no tiene nivel de
  retorno.
- **Persistencia:** `α + β`. Cada periodo, la desviación respecto al nivel se multiplica por esa
  cantidad.
- **Vida media de un shock**, en periodos: `ln(0,5) / ln(α + β)`. Es el tiempo que tarda la mitad
  del efecto de un susto en desaparecer.
- **Pronóstico de la varianza a `h` pasos:** `E[σ²_{t+h}] = σ² + (α + β)^{h−1}·(σ²_{t+1} − σ²)`.
  Va convergiendo al nivel incondicional a velocidad `α + β`.

:::figura
fichero: garch-volatilidad-se-agrupa-y-vuelve
pie: A la izquierda arriba, la nube que justifica el modelo: la correlación de los signos es 0,05 y la de las magnitudes 0,17, así que el signo de mañana no se puede anticipar pero su tamaño sí. Debajo, esa memoria dura semanas y no un día: las barras sobresalen de la banda de ruido hasta el retardo 11. A la derecha, la volatilidad condicional, con su nivel de largo plazo al 2,24 % diario y en sombra los tramos de exceso: ahí es donde sube el riesgo y donde toca reducir el tamaño de la posición, no adivinar la dirección.
fuente: figuras/garch-volatilidad-1.py
:::

Los parámetros se estiman por [[maxima-verosimilitud|máxima verosimilitud]]: se escribe la
verosimilitud gaussiana condicional de `ε_1, …, ε_T` usando la recursión de la varianza y se
maximiza numéricamente, respetando las restricciones `ω > 0`, `α, β ≥ 0`, `α + β < 1`.

## Ejemplo

Tomemos `ω = 0,00001`, `α = 0,12` y `β = 0,86`. Las cuentas que se pueden hacer a mano:

- Persistencia: `α + β = 0,98`.
- Varianza incondicional: `0,00001 / 0,02 = 0,0005`. Su raíz es `0,02236`, es decir una volatilidad
  diaria del **2,24 %**. Anualizando con 252 días de bolsa (`0,02236 · √252`) sale un **35,5 %**.
- Vida media de un shock: `ln(0,5) / ln(0,98) = −0,693 / −0,0202 = 34,3` días. Un susto tarda más
  de un mes y medio en irse a la mitad.

Ahora supón que la varianza de ayer era `σ²_{t−1} = 0,0004`, o sea un 2 % de volatilidad diaria, y
compara dos días distintos de hoy:

- Hoy el retorno es del **3 %**: `σ²_t = 0,00001 + 0,12 · 0,0009 + 0,86 · 0,0004 = 0,000462`, es
  decir una volatilidad del **2,15 %**.
- Hoy el retorno es del **5 %**: `σ²_t = 0,00001 + 0,12 · 0,0025 + 0,86 · 0,0004 = 0,000654`, es
  decir el **2,56 %**.

La volatilidad pronosticada para el día siguiente pasa del 2,00 % de ayer al 2,15 % con un
movimiento del 3 % y al 2,56 % con uno del 5 %: un 7,5 % y un 28 % más, respectivamente. Y si
mañana el retorno fuera del tamaño típico para esa volatilidad (`ε²_t = σ²_t`), la varianza se
movería hacia 0,0005 cerrando cada día el 2 % del hueco que le queda, porque el factor es
`α + β = 0,98`: subiría en el caso del 3 %, porque 0,000462 está por debajo del nivel de largo
plazo, y bajaría en el del 5 %. Con un retorno exactamente cero (`ε²_t = 0`) el destino no es
0,0005 sino `ω/(1 − β) = 0,0000714`, y el hueco se cierra un 14 % al día.

Ese es el motivo de que GARCH cambie por completo la gestión del riesgo: el mismo 5 % de movimiento
significa cosas distintas según cómo venía la volatilidad, y el modelo lo cuantifica en lugar de
tratarlo como una sorpresa.

## Código

```python verificable
import numpy as np

omega, alpha, beta = 1e-5, 0.12, 0.86
rng = np.random.default_rng(0)
n = 2000
z = rng.standard_normal(n)
eps = np.zeros(n)
var = np.empty(n)
var[0] = omega / (1 - alpha - beta)
for t in range(1, n):                       # GARCH(1,1) simulado
    var[t] = omega + alpha * eps[t - 1] ** 2 + beta * var[t - 1]
    eps[t] = np.sqrt(var[t]) * z[t]

def neglog(p, eps):
    """Menos el log de la verosimilitud gaussiana condicional."""
    w, a, b = p
    if w <= 0 or a < 0 or b < 0 or a + b >= 0.999:
        return 1e10
    v = w / (1 - a - b)
    s = 0.0
    for t in range(1, eps.size):
        v = w + a * eps[t - 1] ** 2 + b * v
        s += np.log(v) + eps[t] ** 2 / v
    return 0.5 * s

# Rejilla gruesa y refinamiento: no hace falta un optimizador para ver el mecanismo
mejor = min(((neglog((1e-5, a, b), eps), a, b)
             for a in np.arange(0.04, 0.26, 0.02) for b in np.arange(0.70, 0.95, 0.02)),
            key=lambda x: x[0])
mejor = min(((neglog((1e-5, a, b), eps), round(a, 3), round(b, 3))
             for a in np.arange(mejor[1] - 0.02, mejor[1] + 0.021, 0.005)
             for b in np.arange(mejor[2] - 0.02, mejor[2] + 0.021, 0.005)),
            key=lambda x: x[0])
print("estimado alpha %.3f  beta %.3f  (simulado 0.120 y 0.860)" % (mejor[1], mejor[2]))
# -> alpha 0.115 y beta 0.865
print("corr de los retornos con su retardo 1     %.3f" % np.corrcoef(eps[1:], eps[:-1])[0, 1])
print("corr del VALOR ABSOLUTO con su retardo 1   %.3f" % np.corrcoef(np.abs(eps[1:]), np.abs(eps[:-1]))[0, 1])
# -> 0.001 frente a 0.195: la direccion es impredecible, la magnitud no
orden = np.argsort(np.abs(eps[:-1]))
hoy = np.abs(eps[1:])
print("media de |eps| tras 200 dias tranquilos %.4f" % hoy[orden[:200]].mean())
print("media de |eps| tras 200 dias agitados   %.4f" % hoy[orden[-200:]].mean())
# -> 0.0140 frente a 0.0231
```

:::claves
- `omega, alpha, beta = 1e-5, 0.12, 0.86` desempaqueta una tupla en tres variables de una vez. `1e-5` es 0,00001: si lo escribieras como `0.00001` sería lo mismo, pero con más ceros que contar y más fácil de equivocarse.
- `np.empty(n)` **no pone ceros**: reserva memoria y deja lo que hubiera antes. Por eso `var[0]` se asigna justo en la línea siguiente; sin esa línea, la recursión arrancaría con basura. Si quieres ceros de verdad, es `np.zeros(n)`.
- `eps[t - 1] ** 2` y `var[t - 1]` miran **un paso atrás**, no el valor actual. Ese detalle es todo el modelo: si cambiaras `t - 1` por `t`, la varianza dependería del retorno que estás intentando explicar y el cálculo sería circular (y el ajuste, espectacularmente bueno y falso).
- En `neglog`, las cotas `if w <= 0 or a < 0 or b < 0 or a + b >= 0.999: return 1e10` no son un adorno: son las restricciones del modelo. Sin ellas, una rejilla que pruebe `a + b > 1` hace que `w / (1 - a - b)` salga negativo o infinito y la log-verosimilitud deja de tener sentido. Devolver un número enorme es una forma barata de decirle al optimizador «por aquí no».
- La rejilla del final usa `min(..., key=lambda x: x[0])` sobre un **generador**: no se construye la lista entera de combinaciones en memoria. Pero cada llamada a `neglog` recorre los 2000 puntos con un bucle de Python; por eso se hace una rejilla gruesa primero y se refina solo alrededor del mejor, en vez de barrer 0,001 a 0,001.
- `round(a, 3)` redondea el valor que se guarda en la tupla, no la estimación: el SSE que se compara sigue siendo el de la rejilla sin redondear. Si redondearas antes de calcular, el mínimo podría cambiar de sitio.
- `np.corrcoef(eps[1:], eps[:-1])[0, 1]` devuelve una **matriz** de correlaciones de 2×2, no un número: hay que sacar el elemento de la posición `[0, 1]`. Y `eps[1:]` y `eps[:-1]` son **vistas** sobre el mismo array, no copias: no ocupan memoria nueva y modificarlas cambiaría `eps` ([[vistas-y-copias|vistas y copias]]).
- `np.argsort(np.abs(eps[:-1]))` devuelve **posiciones**, no valores: los 200 índices de los días más tranquilos y los 200 de los más agitados. Después se indexa el array `hoy` con esas posiciones, y ahí está la prueba de que la magnitud se agrupa: 0,0140 frente a 0,0231.
:::

```python verificable
import numpy as np

omega, alpha, beta = 1e-5, 0.12, 0.86
larga = omega / (1 - alpha - beta)
print("persistencia %.2f" % (alpha + beta))                                  # -> 0.98
print("varianza de largo plazo %.6f  vol diaria %.2f%%" % (larga, 100 * np.sqrt(larga)))  # -> 2.24%
print("volatilidad anualizada %.1f%%" % (100 * np.sqrt(larga * 252)))        # -> 35.5%
print("vida media de un shock en dias %.1f" % (np.log(0.5) / np.log(alpha + beta)))       # -> 34.3

var_ayer = 0.0004                                # la varianza de ayer: 2% diario
for shock in (0.03, 0.05):                       # dos shocks distintos hoy
    v = omega + alpha * shock ** 2 + beta * var_ayer
    print("shock %.0f%%  varianza manana %.6f  vol diaria %.2f%%" % (100 * shock, v, 100 * np.sqrt(v)))
# -> shock 3%: varianza 0.000462 y vol 2.15%   shock 5%: varianza 0.000654 y vol 2.56%
```

```python ilustrativo
# La libreria especializada (no viene instalada en este entorno) trae las variantes
# asimetricas y el diagnostico ya hechos.
from arch import arch_model

modelo = arch_model(retornos * 100, vol="GARCH", p=1, q=1, dist="t")
res = modelo.fit(disp="off")
print(res.summary())          # omega, alpha, beta y grados de libertad de la t
print(res.forecast(horizon=5).variance.tail(1))
```

## Errores típicos

- **Medir el riesgo con la desviación típica de todo el histórico.** Es el error más caro y el más
  común. Ese número ignora que la volatilidad se agrupa: te quedas corto justo en los días en que
  el mercado se mueve de verdad y largo cuando no pasa nada. La alternativa es una volatilidad
  condicional, sea GARCH o [[volatilidad-realizada|volatilidad realizada]] de alta frecuencia.
- **Aplicar GARCH a los precios en vez de a los retornos.** Los precios no son estacionarios y su
  escala crece con el nivel: el modelo no tiene sentido sobre ellos. Trabaja con
  [[retornos-logaritmicos|retornos logarítmicos]] (o, como mucho, con las primeras diferencias),
  después de quitar la media.
- **Confundir volatilidad con riesgo de cola.** GARCH mide la **escala** de las oscilaciones, no la
  forma de la distribución. Con colas gordas, un VaR calculado con la normal y una volatilidad
  GARCH sigue subestimando las pérdidas extremas: por eso se combina con la t de Student o con
  [[var-y-cvar|CVaR]].
- **Olvidar el efecto apalancamiento.** Un GARCH simétrico da la misma volatilidad futura tras una
  caída del 4 % que tras una subida del 4 %. En acciones no es así: las caídas asustan más. Si el
  activo es una acción o un índice, mira GJR-GARCH o EGARCH antes de dar el modelo por bueno.
- **Estimar demasiados parámetros con pocos datos.** Un GARCH(2,2) sobre dos años de datos diarios
  es una máquina de sobreajustar. Empieza por GARCH(1,1); si `α + β` sale pegado a 1 y los errores
  típicos son enormes, el problema es la muestra, no el orden del modelo.
- **Validar el modelo con el ajuste dentro de la muestra.** Un GARCH siempre ajusta mejor que una
  volatilidad constante en la muestra que ha visto. La prueba está fuera: haz un backtesting del
  VaR con [[validacion-temporal|validación temporal]] y comprueba cuántas veces se supera el
  umbral.

:::practica
enunciado: Un GARCH(1,1) da ω = 0,000012, α = 0,15 y β = 0,80, y la varianza pronosticada para mañana es 0,0006. Calcula la varianza a cinco días vista y la vida media de un shock, y decide si en esos cinco días el exceso de volatilidad se habrá reducido a la mitad.
pista: El nivel de largo plazo es ω/(1 − α − β) y el exceso sobre ese nivel se multiplica por (α + β) en cada paso.
solucion: Persistencia α + β = 0,95, luego la varianza de largo plazo es 0,000012/0,05 = 0,00024 (1,55 % diario). A cinco días quedan cuatro pasos: 0,00024 + 0,8145 · (0,0006 − 0,00024) = 0,0005332, un 2,31 % diario. Vida media: ln 0,5 / ln 0,95 = 13,5 días, así que en cinco días el exceso solo se ha reducido un 18,6 %: no llega a la mitad.
:::

## Comprueba que lo sabes

:::quiz
p: En un GARCH(1,1) con omega = 0,00002, alpha = 0,10 y beta = 0,85, ¿cuál es la volatilidad diaria de largo plazo?
o: 0,02 %, porque omega es la varianza mínima a la que tiende el proceso
o: 2 %, porque la varianza de largo plazo es omega/(1-alfa-beta) = 0,00002/0,05 = 0,0004
o: No se puede calcular sin conocer la varianza de ayer
a: 2
e: La varianza incondicional es 0,00002 dividido entre 1 - 0,10 - 0,85 = 0,05, o sea 0,0004, y su raíz cuadrada es 0,02: un 2 % diario. Omega es solo el suelo de la varianza y la varianza de ayer afecta al corto plazo, pero el nivel al que tiende el proceso depende únicamente de los tres parámetros.
:::

:::quiz
p: La correlación entre retornos consecutivos es 0,00 pero la correlación entre sus valores absolutos es 0,30. ¿Qué implica?
o: Que el modelo está mal: si la primera es cero, la segunda también debería serlo
o: Que la dirección es impredecible pero la magnitud se agrupa, que es justo lo que modela un GARCH
o: Que hay autocorrelación en la media y hay que diferenciar la serie
a: 2
e: Las dos correlaciones miden cosas distintas. La primera dice que el signo de la rentabilidad no se puede anticipar; la segunda, que los días movidos van seguidos de días movidos. Esa segunda regularidad es la que explota GARCH, y es compatible con que la media sea impredecible.
:::

:::trampa
GARCH pronostica la varianza condicional de la serie, no su dirección. Un error habitual es
meter la volatilidad pronosticada como señal de compra o de venta: cuando la volatilidad sube, lo
que sube es la incertidumbre, no el retorno esperado. La volatilidad sirve para dimensionar la
posición ([[tamano-de-posicion|tamaño de posición]]) y para calcular el VaR, no para decidir el
lado de la operación.
:::
