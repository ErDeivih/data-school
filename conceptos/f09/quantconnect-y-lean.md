---
id: quantconnect-y-lean
titulo: QuantConnect y LEAN
fase: 9
nivel: intermedio
rutas: [quant]
prerequisitos: [backtesting-por-eventos, paper-trading]
tags: [plataforma, backtest, datos, nube]
resumen: Una plataforma en la nube con datos incluidos y un motor de código abierto: el mismo algoritmo pasa de backtest a papel y a real sin reescribirlo.
fuentes: ["Documentación oficial de QuantConnect y del motor LEAN", "Jansen (2020), 'Machine Learning for Algorithmic Trading'"]
---

## En una frase

QuantConnect es una plataforma en la nube donde escribes el algoritmo, lo pruebas contra datos
históricos que ya están cargados, lo pasas a operar en papel y de ahí a real, y todo eso ocurre
sobre **LEAN**, su motor de backtesting de código abierto que también puedes instalar en tu
máquina.

## La idea

Montar un backtest en local tiene tres costes que no aparecen en los tutoriales: conseguir datos
históricos decentes, limpiarlos (ajustes por dividendos y splits, cambios de ticker, huecos) y
mantener el motor. QuantConnect propone quitar esos tres de en medio: entras, eliges un activo,
escribes veinte líneas y en un minuto tienes una curva de capital con datos que la plataforma ya
ha preparado.

Lo que compras con eso, y conviene tenerlo claro:

- **Datos con ajustes y calendario gestionados.** Los precios vienen ajustados por splits y
  dividendos, y las series llevan el identificador permanente del activo, no el ticker. Eso
  resuelve el problema clásico de que una empresa cambie de nombre o de que un ticker se reutilice
  años después: si usas el ticker como clave, estás uniendo dos empresas distintas en la misma
  serie.
- **Un único motor para las tres etapas.** El mismo código que hace el backtest se ejecuta en
  *paper trading* (dinero simulado sobre precios reales) y en real a través de un bróker
  conectado. Esto elimina la clase de error más tonta y más frecuente: que la estrategia que
  probaste no sea exactamente la que operas.
- **Modelos de ejecución explícitos.** El motor trae modelos de comisión, de deslizamiento y de
  relleno que se pueden sustituir. Es una ventaja enorme y a la vez la trampa principal: los
  valores por defecto son razonables para acciones estadounidenses líquidas y absurdos para un
  futuro ilíquido o para cripto.
- **Investigación y producción separadas.** Hay un entorno de cuadernos para explorar los datos
  con la misma fuente que usará el algoritmo, y el algoritmo vive en un fichero aparte. Es la
  forma sana de trabajar, y también la que evita que el código de investigación se cuele en
  producción con veinte variables calculadas sobre todo el histórico.

LEAN, el motor, es de código abierto y está escrito en C#. Los algoritmos se pueden escribir en
C# o en Python, y el motor ejecuta Python a través de un puente hacia .NET. Eso explica dos cosas
que se notan al usarlo: los mismos objetos y la misma API en los dos lenguajes, y una latencia de
más en la capa de Python que importa poco en un backtest diario y mucho si pretendes competir en
milisegundos ([[latencia-y-ejecucion]]).

Frente a las librerías locales ([[vectorbt-backtrader-zipline]]) la diferencia no es de calidad:
es de dónde viven los datos, quién paga el cómputo y qué haces cuando la plataforma cambia su API
o sus límites del nivel gratuito. Los niveles gratuitos y sus restricciones cambian con el
tiempo: comprueba las condiciones del día antes de montar el flujo de trabajo encima.

## Definición formal

Un algoritmo en esta plataforma es un programa que responde a sucesos del motor. La estructura
mínima tiene tres piezas:

:::formula
Initialize → OnData(barra_t) → órdenes        y        Universo(t) ⊆ Activos
:::

- `Initialize` — se ejecuta una vez al arrancar. Se declara qué activos siguen, con qué
  **resolución** (tick, segundo, minuto, hora o diario), cuánto capital hay y qué modelos de
  comisión y deslizamiento se usan.
- `OnData(datos)` — se ejecuta una vez por cada unidad de tiempo que publique el motor, con los
  datos de ese instante. Es el equivalente a `next()` de un motor de eventos.
- `Universo(t)` — conjunto de activos elegibles en cada instante. Se puede fijar a mano o dejar
  que el motor lo calcule con un filtro grueso (por precio y volumen) y otro fino (por
  fundamentales o por liquidez), recalculado cada cierto número de sesiones.
- `resolución` — granularidad de los datos. Determina qué puede ver la estrategia: con datos
  diarios, `OnData` se llama una vez al día y no existe forma de saber qué pasó dentro de la
  sesión ([[tick-data-y-ohlcv]]).

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `Initialize` | La función que se ejecuta una sola vez al arrancar: activos, resolución, capital y modelos de coste | — | No es una palanca: es el único sitio donde se declara el escenario. Cambiar aquí la resolución o el modelo de comisión cambia todos los resultados del backtest sin tocar una línea de la estrategia |
| `OnData(barra_t)` | La función que se ejecuta una vez por cada unidad de tiempo que publica el motor, con los datos de ese instante | una llamada por barra | No cambia su contenido: lo que cambia es cuántas veces se llama. Con resolución diaria, una vez al día; con ticks, miles de veces, y el coste de cómputo va con ella |
| `Universo(t)` | El conjunto de activos elegibles en ese instante, ya filtrados | lista de activos | Al subir el umbral de liquidez entran menos activos: menos operaciones, más concentración y más dependencia de cada nombre. Si el filtro aprieta demasiado, el universo se queda vacío y la estrategia deja de operar sin dar error |
| `resolución` | Granularidad de los datos: tick, segundo, minuto, hora o diario | tiempo por barra | Cuanto más fina, más información existe dentro de `OnData` y más caro es el backtest. Con velas diarias no hay forma de saber qué pasó dentro de la sesión: ni el stop, ni el hueco de apertura |
| `Activos` | El conjunto de partida del que sale el universo | — | Es lo que hay antes de filtrar. Si la clave del activo es el ticker y no un identificador permanente, un cambio de nombre o un ticker reutilizado mete dos empresas en la misma serie |
| Sesiones del año | El calendario del activo (252 en acciones estadounidenses, 365 en cripto) | sesiones | No aparece en la fórmula y decide cuándo se dispara lo programado por fecha: un rebalanceo «el día 1 de mes» que cae en sábado se mueve a la sesión siguiente, y un backtest sin calendario no lo hace |
:::

El detalle que decide si el backtest vale algo: el motor entrega los datos **con la marca de
tiempo del momento en que estaban disponibles**, y no hay ninguna variable que contenga el futuro
a menos que la construyas tú. Ese es exactamente el trabajo que hace un
[[backtesting-por-eventos|motor de eventos]], y es la razón de que la plataforma ponga tanto
énfasis en no usar `History` para calcular nada que dependa del final del periodo.

Y una pieza que en un backtest local casi nunca se usa y aquí es central: la **programación por
calendario**. `DateRules` y `TimeRules` describen cuándo se ejecuta una función (el primer día de
cada mes a las 9:31, cada lunes, cada cinco minutos). El motor solo dispara esos sucesos en
sesiones reales del calendario del activo, así que un rebalanceo «el día 1 de cada mes» que caiga
en fin de semana se mueve a la sesión siguiente. Si tu backtest local no tiene calendario, esa
diferencia ya te está separando del resultado real.

## Ejemplo

Filtro de liquidez, que es lo que hace un filtro grueso de universo. Cinco activos con su precio
y su volumen medio diario:

```
simbolo   precio   volumen medio      dolares al dia
AAA         12,50      4.000.000            50,0 millones
BBB        340,00        120.000            40,8 millones
CCC          8,20     25.000.000           205,0 millones
DDD         95,00        900.000            85,5 millones
EEE         45,00      3.100.000           139,5 millones
```

Con un umbral de 60 millones de dólares negociados al día, pasan CCC, DDD y EEE; AAA y BBB se
quedan fuera. Si además ordenas por liquidez y te quedas con los dos primeros, el universo del
día es `CCC, EEE`. Fíjate en que BBB tiene el precio más alto y es el segundo menos líquido: el
precio no dice nada sobre la liquidez, y por eso el filtro se hace sobre precio por volumen, no
sobre el precio.

:::figura
fichero: quantconnect-universo-por-liquidez
pie: Arriba está el filtro que aplica el motor: la barra es precio por volumen y AAA y BBB no llegan al umbral, aunque BBB sea el activo más caro de la tabla. Abajo, el mismo grupo ordenado por precio: si el filtro fuera el precio, el universo del día sería BBB y DDD, justo dos de los que la liquidez deja fuera. Las dos conclusiones van juntas: el precio no dice nada de la liquidez y el orden de los elegidos cambia por completo según qué mides.
fuente: figuras/quantconnect-y-lean-1.py
:::

Segundo ejemplo, el calendario. Programas el rebalanceo para el primer día de cada mes de 2024.
En enero, febrero, marzo, abril y mayo el día 1 es laborable; el 1 de junio de 2024 es sábado, así
que el motor dispara el rebalanceo el lunes 3 de junio. Un backtest casero con `freq="MS"` de
pandas habría rebalanceado el sábado, con los precios del viernes.

## Código

```python verificable
import numpy as np

# Filtro grueso de universo: liquidez, no precio.
simbolos = np.array(["AAA", "BBB", "CCC", "DDD", "EEE"])
precio = np.array([12.5, 340.0, 8.2, 95.0, 45.0])
volumen = np.array([4_000_000, 120_000, 25_000_000, 900_000, 3_100_000], dtype=float)

dolares = precio * volumen
umbral = 60_000_000
pasa = dolares > umbral
orden = np.argsort(-dolares)

for s, d, ok in zip(simbolos, dolares, pasa):
    print(f"  {s}  {d / 1e6:>6.1f} millones  {'pasa' if ok else 'fuera'}")
# ->   AAA    50.0 millones  fuera
# ->   BBB    40.8 millones  fuera
# ->   CCC   205.0 millones  pasa
# ->   DDD    85.5 millones  pasa
# ->   EEE   139.5 millones  pasa

print("elegidos para el universo:", simbolos[orden[:2]].tolist())
# -> elegidos para el universo: ['CCC', 'EEE']
```

:::claves
- `np.array(["AAA", ...])` crea un array de **texto**, no una lista de Python: `simbolos[orden[:2]]` devuelve otro array, y por eso el ejemplo termina en `.tolist()`. Sin ese `.tolist()` verías `['CCC' 'EEE']`, la sintaxis de NumPy, en lugar de `['CCC', 'EEE']`.
- `dolares > umbral` no devuelve `True` ni `False`: devuelve un array de booleanos, uno por símbolo. Se puede usar para indexar (`simbolos[pasa]`) y para contar (`pasa.sum()`), pero **no** se combina con `and` y `or`: para eso están `&` y `|`, y con paréntesis alrededor de cada comparación.
- `np.argsort(-dolares)` devuelve **posiciones**, no importes: el signo menos ordena de mayor a menor y el resultado es `[2, 4, 3, 0, 1]`. Por eso se escribe `simbolos[orden[:2]]`; si escribieras `dolares[orden[:2]]` obtendrías los 205,0 y 139,5 millones, no los tickers.
- `dtype=float` en el volumen fija el tipo de la columna. Con enteros, `precio * volumen` seguiría dando decimales porque el precio es `float`, pero una división entera (`//`) o una asignación con decimales truncaría sin avisar; y un entero de NumPy que se pase de rango desborda en silencio.
- `f"{d / 1e6:>6.1f}"`: `1e6` es un `float`, así que la división siempre da decimales; `>6` rellena con espacios por la izquierda para que la columna quede alineada y `.1f` redondea a un decimal. Cambia el `.1f` por `.0f` y los 40,8 millones de BBB se imprimen como 41 sin que nada te avise.
- `zip(simbolos, dolares, pasa)` se detiene en la lista más corta: si las tres no tienen el mismo tamaño, el bucle termina antes y las filas que falten **no** dan error. Es la clase de fallo que hace que un universo de 500 activos se recorra con doce.
:::

```python verificable
import pandas as pd

# Rebalanceo el dia 1 de cada mes: lo que el motor ajusta al calendario de sesiones.
for primero in pd.date_range("2024-01-01", periods=6, freq="MS"):
    sesion = pd.bdate_range(primero, periods=1)[0]      # primer dia laborable del mes
    aviso = "  (el dia 1 cae en fin de semana)" if sesion != primero else ""
    print(f"{primero:%Y-%m-%d} -> sesion {sesion:%Y-%m-%d}{aviso}")
# -> 2024-01-01 -> sesion 2024-01-01
# -> 2024-02-01 -> sesion 2024-02-01
# -> 2024-03-01 -> sesion 2024-03-01
# -> 2024-04-01 -> sesion 2024-04-01
# -> 2024-05-01 -> sesion 2024-05-01
# -> 2024-06-01 -> sesion 2024-06-03  (el dia 1 cae en fin de semana)
```

```python ilustrativo
# Esqueleto de algoritmo. Los nombres de la API cambian entre versiones: mira la documentacion.
from AlgorithmImports import *          # noqa: F403


class RebalanceoMensual(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2018, 1, 1)
        self.SetCash(100_000)
        self.SetBrokerageModel(BrokerageName.InteractiveBrokersBrokerage)   # comisiones reales
        self.valores = ["SPY", "EFA", "AGG"]
        for ticker in self.valores:
            self.AddEquity(ticker, Resolution.Daily)
        # Rebalancear el primer dia de mes, cinco minutos despues de la apertura.
        self.Schedule.On(self.DateRules.MonthStart(self.valores[0]),
                         self.TimeRules.AfterMarketOpen(self.valores[0], 5),
                         self.Rebalancear)

    def Rebalancear(self):
        peso = 1 / len(self.valores)
        for ticker in self.valores:
            self.SetHoldings(ticker, peso)      # ordenes proporcionales al capital actual
```

## Errores típicos

- **Confundir tener buenos datos con tener una buena idea.** La plataforma te ahorra la parte de
  ingeniería de datos, no la de hipótesis. Un algoritmo sin ventaja da una curva preciosa en el
  backtest y pierde dinero en real, con comisiones perfectamente modeladas.
- **Dejar los modelos de comisión y deslizamiento por defecto sin revisarlos.** Los valores por
  defecto están pensados para acciones líquidas de mercados desarrollados. Si operas futuros,
  divisas o cripto, el coste real puede ser varias veces mayor, y el resultado cambia de signo
  ([[slippage-y-comisiones]]).
- **No usar identificadores permanentes para los activos.** Si guardas resultados por ticker y no
  por identificador, un cambio de nombre o un ticker reutilizado mezcla dos historias en la misma
  serie. Es una fuente de rentabilidad fantasma difícil de detectar después.
- **Pedir la resolución equivocada.** Backtestear una estrategia intradía con velas diarias, o
  gastar cuota de cómputo en ticks para una estrategia que rebalancea una vez al mes. La
  resolución define qué información existe dentro de `OnData` ([[tick-data-y-ohlcv]]).
- **Optimizar con todos los datos y quedarse con el mejor resultado.** Que el barrido de
  parámetros sea cómodo no lo hace honesto: reserva un tramo temporal que no toques y valida ahí
  ([[validacion-temporal]], [[data-snooping-y-multiple-testing]]).
- **Pasar de backtest a real sin pasar por papel y sin comparar.** El *paper trading* existe para
  medir la diferencia entre lo que el motor supone y lo que el bróker hace: ejecuciones
  parciales, rechazos, diferencial real. Saltárselo es renunciar al único dato barato que tienes
  ([[paper-trading]]).

:::practica
enunciado: Una estrategia de la plataforma aguanta tres ETF equiponderados y rebalancea una vez al mes, con dos operaciones por rebalanceo. Cada operación paga 1,00 USD de comisión más 0,11 USD de tasas. ¿Qué porcentaje anual se lleva el coste si la cuenta es de 1.000 USD y si es de 100.000 USD?
pista: El coste es fijo por operación; lo que cambia con el tamaño de la cuenta es el porcentaje.
solucion: Operaciones al año: 12 · 2 = 24. Coste: 24 · 1,11 = 26,64 USD. Sobre 1.000 USD es un 2,66 % anual; sobre 100.000 USD, un 0,027 %. Conclusión: el mismo algoritmo y los mismos modelos de coste pasan de inviable a despreciable solo cambiando el capital, así que revisa el modelo antes de fiarte de una cuenta pequeña.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué ventaja concreta tiene que el motor lleve el calendario de sesiones del activo?
o: Que los sucesos programados por fecha se disparan solo en días de negociación reales, no en el día natural
o: Que el backtest es más rápido porque hay menos días que simular
o: Que no hace falta ajustar los precios por dividendos
a: 1
e: Un rebalanceo programado para el día 1 de mes cae a veces en fin de semana o festivo; con calendario se mueve a la sesión siguiente, que es lo que haría el sistema en producción. La velocidad y los ajustes de precios son cosas distintas, gestionadas por otras partes del motor.
:::

:::quiz
p: Filtras el universo por precio por volumen en lugar de por precio. ¿Por qué?
o: Porque lo que limita tu capacidad de entrar y salir es el dinero que se negocia, no el precio de la acción
o: Porque las acciones caras siempre son menos rentables
o: Porque el precio por volumen evita el sesgo de supervivencia
a: 1
e: La liquidez se mide en dinero negociado: una acción de 8 euros con 25 millones de títulos al día mueve mucho más dinero que una de 340 euros con 120.000 títulos, y admite posiciones mayores sin mover el precio. El precio por sí solo no dice nada de la rentabilidad. Y el sesgo de supervivencia se corrige con el universo histórico, no con este filtro.
:::

:::aviso
En un entorno gestionado, la reproducibilidad depende de la plataforma: la versión del motor, los
datos y los modelos de coste pueden cambiar sin que tú toques una línea. Antes de dar por bueno
un resultado, guarda la configuración con la que lo obtuviste (fecha, resolución, modelos de
comisión y comisiones aplicadas). Un backtest que no puedes repetir no es evidencia.
:::
