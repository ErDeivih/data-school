---
id: metricas-de-riesgo
titulo: "Métricas de riesgo: panorama"
fase: 9
nivel: intermedio
rutas: [quant]
prerequisitos: [ratio-de-sharpe, volatilidad-realizada]
tags: [riesgo, metricas, cartera, backtest]
resumen: Que se mide cuando se mide el riesgo de una estrategia, qué pregunta responde cada familia de métricas y por qué todas se pueden manipular eligiendo la muestra.
fuentes: ["Bacon (2008), 'Practical Portfolio Performance Measurement and Attribution'", "López de Prado (2018), 'Advances in Financial Machine Learning', cap. 14"]
---

## En una frase

Una métrica de riesgo comprime en un número cuánto puedes perder y con qué probabilidad, y sirve
para tres cosas concretas —comparar estrategias, fijar límites de tamaño y detectar cuándo algo
se ha roto— siempre que la acompañes del periodo, del número de observaciones y de los costes.

## La idea

Dos estrategias cierran el año con resultados parecidos: un +19,5 % y un +24,3 %. La primera
sube un 2 % casi todos los meses; la segunda alterna meses de +10 % y de −8 %. El resultado final
es casi el mismo y no son la misma inversión: la segunda te pone en la tesitura de aguantar o
abandonar justo en el peor momento, y si tenías dinero prestado, puede sacarte antes de que llegue
la recuperación. El «+19,5 %» no contiene ninguna información sobre eso, y por eso existe toda una
familia de métricas que intentan resumir la forma del camino.

Se organizan por la pregunta que responden:

| Familia | Pregunta que responde | Métricas típicas |
| --- | --- | --- |
| Dispersión | cuánto se mueve el resultado alrededor de su media | desviación típica, volatilidad realizada |
| Rendimiento ajustado | cuánto gano por unidad de movimiento asumido | Sharpe, Sortino, información |
| Caída | cuánto llegué a perder desde el máximo y cuánto duró | caída máxima, duración, Calmar |
| Cola | cuánto pierdo en los peores días y qué hay detrás | VaR, CVaR, estrés |
| Mercado | cuánto de mi resultado es simplemente el mercado | beta, alpha, correlación |
| Ruina y tamaño | cuánto puedo perder hasta quedarme fuera | riesgo de ruina, Kelly, tamaño de posición |
| Operación | cuánto me cuesta operar y cuánta capacidad tengo | coste por operación, rotación, liquidez |

Lo importante no es memorizar la lista, sino entender que **cada familia mide una cosa y
ninguna lo mide todo**. Un Sharpe alto con caída máxima del 60 % es un sistema que casi nadie
ejecuta hasta el final. Una caída máxima del 10 % con un VaR del 8 % un día cualquiera es un
sistema que se puede llevar por delante en una sesión. Y un Calmar excelente calculado sobre seis
meses no dice nada de nada.

Y hay un segundo asunto, menos agradable: **casi todas se pueden mejorar sin mejorar la
estrategia**, simplemente eligiendo cómo se miden.

- La volatilidad y el Sharpe **suben** si mides con menos frecuencia: retornos mensuales en vez
  de diarios esconden la autocorrelación de corto plazo ([[ratio-de-sharpe]]).
- La caída máxima **baja** si mides con menos frecuencia: la vela mensual no ve el mínimo
  intradía ([[maximo-drawdown]]).
- El VaR **baja** si acortas la ventana (solo mira lo reciente) o si bajas el nivel de confianza
  del 99 % al 95 % ([[var-y-cvar]]).
- El Sortino **sube** si divides la desviación bajista entre el número de meses malos en lugar
  del total ([[sortino-y-calmar]]).
- La beta **baja** si eliges un índice de referencia poco relacionado con lo que operas
  ([[alpha-y-beta]]).
- Todo **mejora** si mides en la misma muestra en la que elegiste la estrategia, y más aún si
  probaste 500 variantes y enseñas la mejor ([[data-snooping-y-multiple-testing]]).

Por eso la regla práctica es siempre la misma: publica el retorno, la métrica de riesgo, el
periodo, el número de observaciones y si los costes están dentro. Un número solo, sin esas cinco
cosas, no es una medida: es un argumento de venta.

:::figura
fichero: metricas-riesgo-frecuencia-de-medida
pie: La línea azul es la cuenta medida cada sesión y los puntos morados, la misma cuenta mirada solo el último día de cada mes: entre dos de esos puntos cabe una caída que la vista mensual no ve. Abajo está el resultado, y es lo que hay que llevarse: el mismo periodo da un 13,2 % de caída medido a diario y un 4,9 % medido a mensual. Ninguna de las dos cifras es falsa, así que un número de riesgo sin la frecuencia con la que se midió no se puede comparar con nada.
fuente: figuras/metricas-de-riesgo-1.py
:::

## Definición formal

Con `r_1 … r_n` los retornos del periodo (diarios, mensuales, lo que sea) y `C_t` la curva de
capital que resulta de componerlos:

:::formula
σ = √( Σ (r_i − r̄)² / (n − 1) )          Sharpe = (r̄ − Rf) / σ
:::

:::formula
Sortino = (r̄ − T) / DD_T          DD_T = √( Σ min(r_i − T, 0)² / n )
:::

:::formula
MDD = max_t ( ( max_{s≤t} C_s − C_t ) / max_{s≤t} C_s )          Calmar = retorno anualizado / MDD
:::

:::formula
VaR_α = −q_α(r)          CVaR_α = −E[ r | r ≤ q_α(r) ]
:::

- `r_i` — retorno de la observación `i`, en tanto por uno.
- `r̄` — media de los retornos del periodo.
- `n` — número de observaciones. Sin este número, ninguna de las métricas de arriba se puede
  interpretar: un Sharpe calculado con 12 datos y otro con 2.500 no son comparables.
- `σ` — volatilidad: desviación típica de los retornos. Se anualiza multiplicando por `√252` si
  son diarios y por `√12` si son mensuales, suponiendo independencia entre periodos.
- `Rf` — retorno del activo libre de riesgo, en la misma frecuencia que `r_i`.
- `T` — rentabilidad mínima aceptable (MAR, *minimum acceptable return*). Si vale 0, el Sortino
  penaliza solo los meses en pérdidas.
- `DD_T` — desviación bajista: la raíz de la media de los cuadrados de las desviaciones
  negativas respecto a `T`. Fíjate en que los periodos buenos entran en la suma con un cero.
- `C_t` — capital en `t`, y `max_{s≤t} C_s` el máximo alcanzado hasta `t` (el pico móvil).
- `MDD` — caída máxima, en tanto por uno.
- `q_α(r)` — cuantil `α` de la distribución de retornos; con `α = 0,05`, el valor que deja un 5 %
  de las observaciones por debajo.
- `VaR_α` — pérdida que no se supera con probabilidad `1 − α`, expresada en positivo.
- `CVaR_α` — pérdida media **condicionada** a estar en ese 5 % peor. También se llama *expected
  shortfall* y es la métrica de cola que de verdad se usa para dimensionar.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `r_i` | El retorno de una observación (un día, un mes) | tanto por uno (0,03 = 3 %) | No es una palanca: es lo que mides. La frecuencia sí lo es: los mismos meses agrupados de otra forma dan volatilidad y caída distintas |
| `r̄` | La media de esos retornos en el periodo | tanto por uno | Es el numerador del Sharpe y del Sortino. Con pocas observaciones un solo dato extremo la mueve: con seis meses, un +10 % cambia la media más de un punto |
| `n` | Número de observaciones | periodos | No aparece en ninguna de las fórmulas y decide si el número significa algo: el error típico de la media y del Sharpe va como `1/√n`. Un Sharpe de 2 sobre 8 meses y otro sobre 200 no son la misma evidencia |
| `σ` | Desviación típica de los retornos: la volatilidad | tanto por uno, en la frecuencia de `r_i` | Sube el denominador del Sharpe y lo baja. Se anualiza multiplicando por `√252` (diarios) o `√12` (mensuales), lo que supone independencia entre periodos: con volatilidad agrupada la cifra anual sale mal |
| `Rf` | Retorno del activo libre de riesgo, en la misma frecuencia | tanto por uno | Si sube, el exceso baja y el Sharpe cae. Restar un tipo anual a retornos mensuales es el error de frecuencia más común: un 3 % anual son 0,25 % al mes, doce veces menos |
| `T` | Rentabilidad mínima aceptable (MAR) | tanto por uno, misma frecuencia que `r_i` | Con `T = 0` solo penalizan los periodos en pérdidas; al subirlo, más periodos cuentan como malos y la desviación bajista crece. Tiene que estar en la frecuencia de los retornos, no en la anual |
| `DD_T` | Desviación bajista: la raíz de la media de los cuadrados de las desviaciones negativas respecto a `T` | tanto por uno | Es el denominador del Sortino. Los periodos buenos entran con un cero, así que se divide entre `n`; si divides entre el número de periodos malos `k`, el denominador es mayor y el Sortino baja sin que la estrategia cambie |
| `C_t` | Capital en el instante `t` | dinero o índice (base 100) | Es la curva, no los retornos. Todo lo que se mide sobre el camino (caída, duración, Calmar) se calcula aquí, y la escala da igual porque las caídas van en porcentaje |
| `MDD` | La mayor caída desde un pico móvil de la curva | tanto por uno | Solo puede crecer cuando añades historia: más datos son más ocasiones de encontrar una caída peor. Con datos diarios sale siempre mayor o igual que con mensuales |
| `q_α(r)` | El cuantil `α` de los retornos: el valor que deja un `α` de las observaciones por debajo | tanto por uno | Con `α = 0,05` es la frontera del 5 % peor. Con pocos datos ese cuantil es una observación concreta (y a menudo interpolada), no una propiedad de la distribución |
| `VaR_α` | La pérdida que no se supera con probabilidad `1 − α`, expresada en positivo | tanto por uno o dinero | Baja, es decir mejora, si acortas la ventana a lo reciente o si rebajas la confianza del 99 % al 95 %. Es la métrica más fácil de maquillar sin tocar la estrategia |
| `CVaR_α` | La pérdida media de los casos que superan el VaR | tanto por uno o dinero | Es siempre mayor o igual que el VaR y depende de la forma de la cola. Necesita muchas observaciones: en el ejemplo de seis meses sale de un único dato |
:::

Dos cantidades que aparecen constantemente al comparar con un índice de referencia y que
completan el panorama: el **tracking error** `σ(r − r_b)`, que mide cuánto te separas del índice,
y el **ratio de información** `(r̄ − r̄_b) / tracking error`, que es el Sharpe de esa separación.

## Ejemplo

Seis retornos mensuales de una estrategia, en tanto por uno:

```
0,03   -0,02   0,04   -0,05   0,01   0,02
```

- Media mensual: 0,005, es decir un 0,5 %.
- Volatilidad mensual: 0,0339; anualizada: `0,0339 · √12 = 0,1175`, un 11,75 %.
- Sharpe mensual: `0,005 / 0,0339 = 0,147`; anualizado: `0,147 · √12 = 0,51`.
- Capital: 100 → 103 → 100,94 → 104,98 → 99,73 → 100,73 → **102,74**. Retorno total: `+2,74 %`,
  que anualizado son `1,0274² − 1 = 5,56 %`.
- Caída máxima: del pico de 104,98 al mínimo de 99,73, un **5,00 %**.
- Calmar: `5,56 / 5,00 = 1,11`.
- VaR al 95 % (histórico): el cuantil 5 % de los seis retornos es `−4,25 %`, así que el VaR es
  **4,25 %**. El CVaR, la media de lo que queda por debajo de ese umbral, es **5,00 %**, y sale de
  **una sola** observación.

Ese último detalle es la lección del ejemplo: con seis datos, la métrica de cola se apoya en un
único mes. El VaR y el CVaR necesitan muchas observaciones para significar algo, y cuando el
periodo es corto lo honesto es decirlo, no enseñar el número. El Sharpe de 0,51 tiene el mismo
problema en menor grado: su intervalo de confianza con seis meses es tan ancho que incluye el
cero.

## Código

```python verificable
import numpy as np

r = np.array([0.03, -0.02, 0.04, -0.05, 0.01, 0.02])      # retornos mensuales
capital = 100 * np.cumprod(1 + r)

vol_mensual = r.std(ddof=1)
picos = np.maximum.accumulate(capital)
mdd = float(((picos - capital) / picos).max())
anualizado = float((capital[-1] / 100.0) ** (12 / r.size) - 1)   # 100 es el capital inicial

print(f"retorno total       {capital[-1] - 100:+.2f} %")     # -> +2.74 %
print(f"volatilidad mensual {vol_mensual:.4f}")              # -> 0.0339
print(f"volatilidad anual   {vol_mensual * np.sqrt(12):.4f}")  # -> 0.1175
print(f"Sharpe anual        {r.mean() / vol_mensual * np.sqrt(12):.2f}")   # -> 0.51
print(f"caida maxima        {mdd:.2%}")                       # -> 5.00%
print(f"retorno anualizado  {anualizado:.2%}")               # -> 5.56%
print(f"Calmar              {anualizado / mdd:.2f}")          # -> 1.11
```

:::claves
- `np.cumprod(1 + r)` **multiplica**, no suma: es la curva de capital compuesta. Si sumaras los retornos (`1 + r.cumsum()`) obtendrías otra curva en cuanto haya más de dos periodos, y el capital final y la caída máxima dejarían de coincidir con el cálculo a mano.
- `.std(ddof=1)` divide entre `n − 1`; el valor por defecto de NumPy es `ddof=0`, que divide entre `n`. Con seis datos la diferencia es de un 10 % en la volatilidad, y se traslada tal cual al Sharpe. pandas usa `ddof=1` por defecto: la misma serie da dos números según la librería por la que pases.
- `np.maximum.accumulate(capital)` construye el pico móvil: en cada posición guarda el máximo **hasta ahí**, no el máximo de toda la serie. Es literalmente `max_{s≤t} C(s)`.
- `(picos - capital) / picos` se calcula elemento a elemento, sin bucles, entre dos arrays del mismo tamaño, y `.max()` devuelve la caída máxima. El `float(...)` de delante convierte el escalar de NumPy en un `float` de Python: al guardarlo en un JSON o pasarlo a una librería que revisa tipos, la diferencia se nota.
- `** (12 / r.size)`: `r.size` es el número de elementos, no el tamaño en bytes (eso sería `r.nbytes`). Con 6 meses eleva a 2; con 250 sesiones escribirías `252 / r.size`. Y el `100` es el capital inicial que pusiste tú: NumPy no lo sabe, y si lo cambias el retorno total cambia mientras el resto de métricas no.
- `capital[-1] - 100` imprime la ganancia en euros sobre una base de 100, no un porcentaje: el `%` del `print` solo añade el símbolo. Con un capital inicial de 1.000, ese mismo cálculo daría +27,40 y parecería un 27 % cuando es un 2,74 %.
:::

```python verificable
import numpy as np

r = np.array([0.03, -0.02, 0.04, -0.05, 0.01, 0.02])
nivel = 0.05
umbral = np.quantile(r, nivel)

var = -umbral
cola = r[r <= umbral]
cvar = -cola.mean()

print(f"cuantil 5 %         {umbral:.4f}")        # -> -0.0425
print(f"VaR 95 % historico  {var:.2%}")          # -> 4.25%
print(f"CVaR 95 %           {cvar:.2%}")         # -> 5.00%
print(f"observaciones en la cola: {cola.size} de {r.size}")   # -> 1 de 6
```

```python verificable
import numpy as np

# Las mismas dos estrategias del principio: resultados parecidos, riesgo muy distinto.
suave = np.array([0.02, 0.01, 0.02, 0.01, 0.02, 0.01, 0.02, 0.01, 0.02, 0.01, 0.02, 0.01])
brusca = np.array([0.10, -0.08, 0.12, -0.07, 0.09, 0.06, 0.10, -0.09, 0.08, 0.05, 0.11, -0.19])


def resumen(x):
    c = np.cumprod(1 + x)
    picos = np.maximum.accumulate(c)
    return (c[-1] - 1), float(((picos - c) / picos).max()), x.std(ddof=1)


for nombre, x in (("suave ", suave), ("brusca", brusca)):
    total, mdd, vol = resumen(x)
    print(f"{nombre}  final {total:+.1%}  caida {mdd:>6.2%}  volatilidad {vol:.2%}")
# -> suave   final +19.5%  caida  0.00%  volatilidad 0.52%
# -> brusca  final +24.3%  caida 19.00%  volatilidad 10.27%
```

## Errores típicos

- **Comparar métricas calculadas a frecuencias distintas.** Un Sharpe anualizado a partir de
  datos diarios, otro a partir de mensuales y otro del anual no son el mismo número, y lo mismo
  pasa con la caída máxima. Elige una frecuencia, úsala en todo y dilo.
- **Enseñar un número sin el número de observaciones.** Un Sharpe de 2 sobre 200 meses y un
  Sharpe de 2 sobre 8 meses no son la misma evidencia. Con pocos datos, da el intervalo de
  confianza o di que no lo tienes.
- **Elegir la métrica después de ver los resultados.** Si pruebas Sharpe, Sortino, Calmar y CVaR
  y enseñas el que mejor queda, has hecho cuatro pruebas y no has corregido por ninguna. Es
  [[multiplicidad-y-fdr|el problema de las pruebas múltiples]] aplicado a tus propias métricas.
- **Medir el riesgo del activo cuando lo que importa es el de la cartera.** Dos estrategias con
  volatilidad del 10 % cada una pueden sumar una cartera del 6 % o del 19 % según su correlación
  ([[covarianza-y-correlacion]], [[construccion-de-carteras]]).
- **Usar solo métricas relativas y olvidar el apalancamiento.** Sharpe, Sortino y Calmar son
  invariantes a escala en primera aproximación: subir el apalancamiento no los empeora y sí
  cambia la probabilidad de quedarte a cero ([[riesgo-de-ruina]], [[criterio-de-kelly]]).
- **Calcular las métricas sobre la curva teórica sin costes.** Comisiones, deslizamiento y el
  coste de rebalancear cambian tanto el retorno como la caída. Un backtest sin costes presume de
  métricas que no vas a vivir ([[slippage-y-comisiones]]).

:::practica
enunciado: Veinte retornos diarios: 0,0000, 0,0210, 0,0020, 0,0085, −0,0350, 0,0140, 0,0100, 0,0060, −0,0150, 0,0170, 0,0040, 0,0090, 0,0070, −0,0220, 0,0120, 0,0030, 0,0055, 0,0130, 0,0015, 0,0110. Calcula la volatilidad anualizada, el Sharpe anualizado con Rf = 0 y el VaR diario al 95 %.
pista: La volatilidad escala con la raíz del tiempo y el retorno con el tiempo; el VaR sale de los cuantiles, no de la desviación.
solucion: Media 0,3625 % diario y desviación 1,344 %; el log-retorno anual es 0,3625 · 252 = 91,35 %, que como rentabilidad efectiva es exp(0,9135) − 1 = 149,3 % (del orden de una sesión excelente repetida, no de una estrategia realista). Volatilidad anual: 1,344 · √252 = 21,3 %. Sharpe diario 0,27, que anualizado es 4,28: con veinte días ese número no distingue una buena estrategia de una racha. VaR al 95 %: con veinte datos, el segundo peor, 2,20 %, frente a una desviación diaria de 1,344 %, así que la cola pesa más de lo que sugiere la desviación. Conclusión: el Sharpe mide el camino medio y el VaR la cola, y aquí el segundo se apoya en una sola sesión.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué mide la diferencia entre el VaR al 95 % y el CVaR al 95 %?
o: El CVaR es la pérdida media de los casos que superan el VaR, así que describe la cola y no solo su borde
o: El CVaR es el doble del VaR en cualquier distribución
o: El CVaR se calcula con la volatilidad y el VaR con los cuantiles
a: 1
e: El VaR marca la frontera: la pérdida que no se supera con el 95 % de probabilidad. El CVaR mira lo que hay detrás de esa frontera y promedia esas pérdidas, que es lo que de verdad importa para dimensionar posiciones. No hay una relación fija entre los dos: depende de la forma de la cola.
:::

:::quiz
p: Dos estrategias acaban el año con un +20 %. ¿Qué información añade la caída máxima?
o: Como de profundo fue el peor tramo por debajo del máximo, que decide si podrías haber aguantado
o: La probabilidad de perder dinero el año que viene
o: El número de operaciones perdedoras que hubo en el año
a: 1
e: La caída máxima describe el camino, no el resultado: dos curvas con el mismo final pueden haber pasado por un retroceso del 5 % o del 40 %, con efectos muy distintos sobre la cuenta y sobre la decisión de seguir. No es una probabilidad de pérdida futura ni cuenta operaciones: mide la peor racha sobre la curva de capital.
:::

:::quiz
p: Tu estrategia tiene un CVaR del 5 % calculado con seis meses de datos. ¿Cuál es la lectura correcta?
o: Que la estimación se apoya en muy pocas observaciones de la cola y no es fiable
o: Que la pérdida máxima posible está acotada en el 5 %
o: Que hace falta subir el apalancamiento para aprovechar el dato
a: 1
e: El CVaR es una media de los peores casos, y con seis observaciones esa media puede salir de una sola: no es una cota de nada, es un resumen de lo que ha pasado. Para métricas de cola hacen falta muchas más observaciones, o un modelo explícito de la cola con sus propios supuestos.
:::

:::aviso
Ninguna métrica de riesgo es una predicción. Todas resumen lo que pasó en la muestra que les diste,
así que si el régimen de mercado cambia, cambian con él. Sirven para comparar y para poner límites,
no para saber cuánto vas a perder el mes que viene ([[regimenes-de-mercado]]).
:::
