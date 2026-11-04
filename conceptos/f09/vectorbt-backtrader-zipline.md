---
id: vectorbt-backtrader-zipline
titulo: VectorBT, Backtrader y Zipline
fase: 9
nivel: intermedio
rutas: [quant]
prerequisitos: [backtesting-vectorizado, backtesting-por-eventos]
tags: [backtest, librerias, herramientas]
resumen: Las tres librerías de backtesting que más se usan en Python, qué modelo del mundo tiene cada una y para qué sirve cada modelo.
fuentes: ["Jansen (2020), 'Machine Learning for Algorithmic Trading'", "Documentación oficial de Backtrader, Zipline y VectorBT"]
---

## En una frase

Las tres hacen backtests en Python y no son intercambiables: VectorBT calcula todo con arrays y
barre parámetros a granel, Backtrader simula orden por orden con un motor de eventos, y Zipline
está construida alrededor de datos ingeridos en paquetes y de un motor de factores y filtros
para carteras.

## La idea

Antes de elegir librería, decide qué tienes que modelar. Porque la librería no es un detalle de
estilo: cada una impone una forma de pensar, y esa forma decide qué errores vas a poder cometer
y cuáles te va a impedir el propio código.

**VectorBT** piensa en arrays. Le das una serie de precios, una serie de entradas y otra de
salidas, y te devuelve un objeto `Portfolio` con las métricas calculadas, la curva de capital y
los gráficos. Su función estrella es el barrido de parámetros: en vez de un array de longitud
`n`, le pasas uno de forma `(n, 30)` con 30 combinaciones de parámetros y obtiene los 30
backtests en la misma llamada, más un mapa de calor con el resultado de cada combinación. Está
construido sobre NumPy, pandas y Numba, así que hereda la velocidad de los arrays y también sus
trampas: todo lo que dice [[backtesting-vectorizado]] sobre desplazamientos y `NaN` se aplica
tal cual.

**Backtrader** piensa en objetos y sucesos. Escribes una clase `Strategy` con un método `next()`
que se ejecuta en cada barra, y métodos de notificación como `notify_order` o `notify_trade`
para reaccionar a lo que hace el bróker. El motor (`Cerebro`) lee los datos, llama a tu
estrategia, simula las órdenes con el esquema de comisión que le hayas dado y te deja
analizadores ya hechos (ratio de Sharpe, drawdown, operaciones) y conexión con brókers para
operar en real. Es el camino natural si vienes de [[backtesting-por-eventos]] y quieres una
librería que ya tenga el bucle escrito. A cambio: el proyecto original lleva mucho tiempo sin
publicar versiones, así que conviene comprobar que la versión que instalas funciona con tu
Python y no esperar novedades.

**Zipline** piensa en una cartera institucional. No le das un CSV y ya está: primero **ingieres**
los datos en un *bundle* (un paquete con calendario de sesiones, precios y ajustes), y luego
escribes una función `initialize` y otra `handle_data`, o mejor un `Pipeline` que describe
factores y filtros sobre todo el universo a la vez. Ese motor de pipeline es su rasgo
distinguible: sirve para estrategias transversales del tipo «ordenar 3.000 acciones por una
combinación de factores y comprar el decil superior», con el calendario y los ajustes
gestionados por el motor. Nació en Quantopian; tras el cierre de la plataforma el proyecto
original quedó sin mantenimiento y hoy lo que se usa es la bifurcación que mantiene la
comunidad.

Hay una cuarta opción que no es una librería sino una plataforma, y tiene su propia página:
[[quantconnect-y-lean]]. Y si el destino es MetaTrader, el entorno es otro distinto:
[[mql5-y-metatrader]].

:::figura
fichero: vectorbt-backtrader-zipline-tres-curvas
pie: La misma regla de media móvil sobre los mismos cuatro activos, resuelta con los tres modelos. Arriba, el hueco entre el array y los eventos es lo que cuesta la ejecución: entrar más tarde y solo llenar el 85 % de lo pedido. El pipeline ni se plantea comprar «sí o no»: reparte el capital entre los activos que pasan el filtro en cada fecha.
fuente: figuras/vectorbt-backtrader-zipline-1.py
:::

Resumen para decidir:

| Librería | Modelo | Punto fuerte |
| --- | --- | --- |
| VectorBT | arrays y barrido vectorizado | probar cientos de variantes y ver mapas de calor |
| Backtrader | bucle de eventos en Python | orden por orden, analizadores y brókers reales |
| Zipline | bundles y pipeline de factores | carteras grandes, calendario y ajustes gestionados |

Y una advertencia que vale para las tres: **la librería no arregla los datos**. Un motor
perfecto alimentado con precios mal ajustados, con un universo sesgado o con datos revisados
produce un resultado malo con mucha elegancia.

## Definición formal

Las tres calculan lo mismo —una curva de capital a partir de una regla y unos datos— pero
parametrizan cosas distintas. Vale la pena escribir qué entra en cada una:

:::formula
C_t = C_0 · Π (1 + pos_s · r_s − coste_s)      s = 1 … t
:::

- `C_t` — capital en la barra `t`.
- `pos_s` — posición mantenida durante la barra `s`, en fracción del capital.
- `r_s` — retorno de la barra `s` del activo.
- `coste_s` — comisión más deslizamiento de la barra `s`, en fracción del capital operado.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `C_t` | Capital en la barra `t` | unidades monetarias | Es el resultado, no una palanca: cada librería llega a él por un camino distinto y por eso dos curvas de la misma estrategia no coinciden |
| `C_0` | Capital inicial | unidades monetarias | Solo escala la curva. Si comparas dos librerías con `C_0` distinto, todas las métricas relativas siguen siendo válidas, pero el beneficio absoluto no |
| `pos_s` | Posición mantenida durante la barra `s`, en fracción del capital | fracción (puede pasar de 1 si hay apalancamiento) | Cambia de dónde sale: en un motor vectorizado es un array desplazado, en eventos es el resultado de órdenes que se llenan a trozos, y en un pipeline es un peso de corte transversal |
| `r_s` | Retorno de la barra `s` del activo | tanto por uno | Es lo único que las tres librerías tratan igual, y aun así cada una lo anualiza a su manera al calcular el Sharpe |
| `coste_s` | Comisión más deslizamiento de la barra `s` | fracción del capital operado | Con `coste_s` mayor, la diferencia entre motores crece: el vectorizado lo modela como rotación por una tasa fija y el de eventos lo saca del diferencial de cada suceso |
:::

Lo que cambia entre librerías es cómo se obtiene `pos_s` y cuánto vale `coste_s`:

- En un motor **vectorizado**, `pos_s` sale de un array desplazado y `coste_s` de un producto
  entre la rotación y una tasa fija.
- En un motor de **eventos**, `pos_s` es el resultado de órdenes que pueden llenarse parcialmente
  a precios distintos dentro de la misma barra, y `coste_s` depende del diferencial y del tipo
  de orden de cada suceso.
- En un **pipeline**, `pos_s` se calcula por corte transversal: los pesos se reparten entre los
  activos que superan los filtros en `s`, y el coste depende de cuánto cambia el conjunto
  seleccionado.

Consecuencia práctica: dos librerías dadas las mismas entradas y los mismos datos dan curvas
**distintas**, y no está mal: están respondiendo a preguntas distintas sobre la ejecución. Lo
que sí está mal es comparar sus métricas sin mirar cómo anualiza cada una, qué tasa libre de
riesgo usa y con cuántos grados de libertad calcula la desviación típica.

## Ejemplo

Un barrido de tres medias móviles sobre diez cierres. Los cierres son
`100, 102, 99, 103, 101, 105, 107, 104, 108, 110` y la regla es «estar comprado si el cierre
supera su media de `w` barras», cobrando el retorno de la barra siguiente. Los tres resultados,
en tanto por uno:

- Con `w = 2`: **−0,0393**. La media es muy nerviosa: entra justo después de cada subida y sale
  justo después de cada bajada, así que paga los giros.
- Con `w = 3`: **−0,0099**.
- Con `w = 4`: **−0,0099**, exactamente el mismo resultado, porque en estas diez barras las dos
  medias dan la misma señal en todas las posiciones menos una y esa una cae donde la posición
  era cero.

Lo interesante del barrido no es el número, es lo que dice de la regla: las tres variantes
pierden y dos son idénticas, así que el parámetro no discrimina nada aquí. Eso es exactamente lo
que quieres saber antes de dedicarle una semana al sistema. El caso peligroso es el contrario:
si `w = 2` gana mucho, `w = 3` empata y `w = 4` pierde, lo que tienes no es una estrategia, es
un número ajustado al ruido, que es lo que describe
[[data-snooping-y-multiple-testing]].

## Código

```python verificable
import numpy as np

precios = np.array([100, 102, 99, 103, 101, 105, 107, 104, 108, 110], dtype=float)
ret = np.diff(precios) / precios[:-1]
ventanas = (2, 3, 4)
acum = np.concatenate([[0.0], np.cumsum(precios)])


def media_movil(w):
    """Media simple de las w barras anteriores; NaN en las primeras w-1."""
    mm = np.full(precios.size, np.nan)
    mm[w - 1:] = (acum[w:] - acum[:-w]) / w
    return mm


def backtest(w):
    senal = (precios > media_movil(w)).astype(float)   # NaN compara False -> 0
    posicion = senal[:-1]        # el retorno de i a i+1 se cobra con lo decidido en i
    return float((posicion * ret).sum())


bucle = np.array([backtest(w) for w in ventanas])

# Lo mismo en una sola operacion, con una matriz (variante x barra): el barrido vectorizado.
mm = np.vstack([media_movil(w) for w in ventanas])
senal = (precios[None, :] > mm).astype(float)
posicion = senal[:, :-1]
matriz = (posicion * ret).sum(axis=1)

print("ventanas            ", list(ventanas))                 # -> [2, 3, 4]
print("una a una (bucle)   ", np.round(bucle, 4).tolist())    # -> [-0.0393, -0.0099, -0.0099]
print("de golpe (matriz)   ", np.round(matriz, 4).tolist())   # -> [-0.0393, -0.0099, -0.0099]
print("coinciden           ", bool(np.allclose(bucle, matriz)))  # -> True
```

:::claves
- `media_movil` rellena con `np.full(precios.size, np.nan)`: el array nace **con la longitud
  definitiva** y luego se escribe la cola. Es el patrón habitual porque `mm[w-1:] = ...` exige que
  `mm` ya exista con ese tamaño; crear el array dentro del bucle y concatenar sería mucho más lento.
- `acum = np.concatenate([[0.0], np.cumsum(precios)])` es una suma acumulada **con un cero delante**
  para poder restar `acum[w:] - acum[:-w]` y obtener la suma de `w` barras de una vez. Sin ese cero,
  el índice se desplaza una barra entera y las medias salen corridas sin que nada avise.
- Las primeras `w-1` posiciones son `NaN`, y `precios > media_movil(w)` con `NaN` da `False`: la
  señal arranca en 0. Funciona, pero es un `False` por comparación no válida, no una decisión: si
  en vez de `>` usaras `<`, el `NaN` también daría `False` y la conclusión sería la contraria.
- `senal[:-1]` es la clave del ejemplo: `precios[i]` decide el retorno de `i` a `i+1`, así que hay
  que recortar la señal y no el retorno. Con `senal` completa, `posicion * ret` no encaja de tamaño
  y NumPy lanza un error; el error es la parte buena, porque el fallo de verdad es el que sí
  encaja.
- En el barrido, `np.vstack([media_movil(w) for w in ventanas])` apila tres arrays de longitud `n`
  en una matriz `(3, n)`. `precios[None, :]` añade un eje para que la comparación se emita contra
  las tres filas: sin ese `None` la comparación sería elemento a elemento con `precios` a secas.
- `np.allclose(bucle, matriz)` compara con tolerancia, no con `==`. Los dos caminos suman los
  mismos números en distinto orden y en coma flotante eso puede dar el último bit distinto:
  `bucle == matriz` podría devolver `False` y no significaría que el barrido esté mal.
:::

```python ilustrativo
# VectorBT: el barrido es una dimension mas del array.
import vectorbt as vbt

precios = vbt.YFData.download("SPY").get("Close")          # datos externos
medias = vbt.MA.run(precios, window=[10, 20, 50])          # tres medias de una vez
portfolios = vbt.Portfolio.from_signals(
    precios, entries=medias.ma_crossed_above(precios), exits=medias.ma_crossed_below(precios),
    fees=0.0005, slippage=0.0005,
)
print(portfolios.sharpe_ratio())        # una serie, una entrada por combinacion
print(portfolios.total_return().vbt.heatmap())             # mapa de calor del barrido
```

```python ilustrativo
# Backtrader: bucle de eventos con clase Strategy y notificaciones de orden.
import backtrader as bt


class CruceMedias(bt.Strategy):
    params = dict(rapida=10, lenta=30)

    def __init__(self):
        self.cruce = bt.ind.CrossOver(
            bt.ind.SMA(period=self.p.rapida), bt.ind.SMA(period=self.p.lenta)
        )

    def next(self):
        if not self.position and self.cruce > 0:
            self.buy(size=100)
        elif self.position and self.cruce < 0:
            self.close()

    def notify_order(self, order):
        if order.status == order.Completed:
            self.log(f"ejecutadas {order.executed.size} a {order.executed.price:.2f}")


cerebro = bt.Cerebro()
cerebro.addstrategy(CruceMedias)
cerebro.broker.setcommission(commission=0.0005)     # sin esto, el backtest es gratis
cerebro.run()
```

```python ilustrativo
# Zipline: pipeline de factores sobre todo el universo y rebalanceo programado.
from zipline.api import order_target_percent, schedule_function, date_rules, time_rules
from zipline.pipeline import Pipeline
from zipline.pipeline.factors import AverageDollarVolume, Returns


def initialize(context):
    context.universo = AverageDollarVolume(window_length=60).top(500)


def antes_de_abrir(context, data):
    fundamentales = pipeline_output("mi_pipeline")       # factores y filtros por corte
    seleccion = fundamentales.nlargest(20, "momentum")
    for valor in seleccion.index:
        order_target_percent(valor, 1 / len(seleccion))


def make_pipeline():
    return Pipeline(columns={"momentum": Returns(window_length=126)})
```

## Errores típicos

- **Elegir la librería por popularidad y no por lo que necesitas modelar.** Si tu estrategia
  pone órdenes límite y vive del diferencial, un barrido vectorizado no te va a decir si es
  viable: necesitas cola y ejecución parcial ([[backtesting-por-eventos]]). Si solo quieres
  descartar ideas rápido, montar un motor de eventos es perder el tiempo.
- **Comparar métricas entre librerías sin leer cómo las calculan.** Cada una anualiza de una
  forma, elige su tasa libre de riesgo y calcula desviaciones con criterios distintos. Un Sharpe
  de Backtrader y otro de VectorBT sobre la misma estrategia no son el mismo número hasta que
  igualas los supuestos.
- **Creer que el motor de la librería ya te protege del sesgo de futuro.** No lo hace: si le
  pasas una señal calculada con el cierre de la barra y la ejecutas en esa misma barra, te dará
  un resultado excelente y perfectamente falso ([[sesgo-de-mirar-al-futuro]]).
- **Usar bundles o datos de ejemplo sin comprobar los ajustes.** Series ajustadas por dividendos
  y splits, tickers que cambian de nombre y componentes que entran y salen del índice son la
  fuente habitual de resultados que no se pueden reproducir en real
  ([[sesgo-de-supervivencia]]).
- **Optimizar el parámetro de la estrategia con todos los datos y quedarse con el mejor.** El
  barrido de VectorBT y el optimizador de Backtrader hacen que probar 2.000 combinaciones cueste
  segundos, y eso multiplica el problema de las pruebas múltiples: separa una parte de los datos
  para validar y estate quieto con ella ([[validacion-temporal]]).
- **Montar todo el sistema alrededor de una librería que ya no evoluciona.** Antes de escribir
  5.000 líneas contra una API concreta, comprueba que se instala, que tiene versión reciente y
  que la comunidad sigue viva; migrar un backtest entero es un trabajo de semanas.

:::practica
enunciado: Un barrido con VectorBT tarda 1,5 segundos por combinación. Quieres probar 800 combinaciones y después reconstruir con un motor de eventos las 2 que sobrevivan, que es entre 100 y 1000 veces más lento. ¿Cuánto tarda cada etapa?
pista: El coste crece linealmente con el número de variantes; aplica el factor solo a las dos finalistas.
solucion: Barrido: 800 · 1,5 = 1.200 s, veinte minutos. Motores de eventos: cada backtest cuesta entre 150 s (×100) y 1.500 s (×1000); las 2 finalistas, entre 300 s y 3.000 s, de cinco a cincuenta minutos. En total, entre 25 y 70 minutos, sin escribir un motor para las 800. Conclusión: explorar vectorizado y reconstruir solo lo que sobrevive es la única forma de permitirse las dos cosas.
:::

## Comprueba que lo sabes

:::quiz
p: Quieres probar 400 combinaciones de tres parámetros y ver cuáles son estables. ¿Qué enfoque encaja mejor?
o: Un barrido vectorizado con arrays de varias dimensiones y un mapa de calor de las métricas
o: Un motor de eventos que recorra las 400 combinaciones orden por orden
o: Un pipeline de factores con rebalanceo diario
a: 1
e: El barrido vectorizado está diseñado exactamente para eso: añade dimensiones al array y obtiene todas las combinaciones en una pasada, con mapas de calor para ver la estabilidad. El motor de eventos es para modelar la ejecución de una estrategia concreta, no para explorar. El pipeline sirve para selección transversal de activos, no para barrer parámetros de una regla.
:::

:::quiz
p: ¿Qué diferencia fundamental hay entre Backtrader y Zipline según el modelo de datos?
o: Backtrader consume los datos que le pases, mientras Zipline exige ingerirlos antes en un bundle con calendario y ajustes
o: Backtrader solo funciona con acciones y Zipline solo con divisas
o: Zipline no permite operar en corto y Backtrader sí
a: 1
e: La diferencia está en la preparación de los datos: Zipline trabaja sobre bundles ingeridos, lo que le permite gestionar calendario de sesiones y ajustes de forma homogénea en todo el universo, y hace falta un paso previo para darlos de alta. Backtrader acepta alimentaciones de datos directamente. Los tipos de activo y las posiciones cortas no son la frontera entre las dos.
:::

:::truco
Si dudas entre vectorizado y eventos, aplica esta regla: calcula la estrategia con el
vectorizado, mide cuánta rotación tiene y qué peso tiene el coste en el resultado. Si el coste
es marginal y la estrategia opera con horquillas amplias, el vectorizado te basta. Si el
resultado se decide en el último medio punto porcentual o la estrategia pone órdenes límite,
necesitas eventos.
:::
