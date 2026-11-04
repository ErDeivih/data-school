---
id: mql5-y-metatrader
titulo: MQL5 y MetaTrader
fase: 9
nivel: intermedio
rutas: [quant]
prerequisitos: [slippage-y-comisiones, tick-data-y-ohlcv]
tags: [trading, retail, backtest, mql5]
resumen: El entorno donde opera la mayoría del trading minorista: qué permite de verdad su probador de estrategias y qué te está ocultando mientras te enseña una curva preciosa.
fuentes: ["Documentación oficial de MQL5 y del Probador de Estrategias de MetaTrader 5"]
---

## En una frase

MetaTrader 5 es la plataforma de escritorio con la que la mayoría del trading minorista opera
divisas, índices y CFD, MQL5 es su lenguaje para escribir asesores expertos, y su probador de
estrategias permite backtestear y optimizar dentro de la propia plataforma con el histórico del
bróker.

## La idea

Si has visto un backtest de trading en un vídeo, muy probablemente era esto: una ventana con una
curva de capital creciente, unos parámetros optimizados y un botón de «empezar». El entorno tiene
ventajas reales —todo está integrado, el probador corre en local y conectar con un bróker son dos
clics— y una característica que hay que entender bien: **el probador simula el mercado a partir
del histórico que le da tu bróker**, no del mercado.

Eso significa cuatro cosas concretas:

1. **Los datos son del bróker.** El histórico de ticks, los huecos, el spread y los horarios son
   los de tu bróker. Dos brókers con el mismo asesor experto dan resultados distintos, y ninguno
   de los dos es «el verdadero».
2. **El modo de modelado decide lo que tu robot puede ver.** El probador ofrece varias
   modalidades: ticks generados a partir de velas de un minuto, ticks reales cuando el bróker los
   guarda, OHLC de un minuto y solo precios de apertura. Con «solo precios de apertura» tu robot
   evalúa las condiciones una vez por vela, y toda la lógica que dependa de lo que pasa dentro de
   la vela desaparece. Además, el porcentaje de calidad de modelado no mide si tu backtest es
   bueno: mide qué parte de esos ticks procede de datos reales.
3. **Los costes hay que ponerlos tú.** El spread suele venir de la especificación del símbolo,
   pero muchas veces es el mínimo o uno fijo, y la comisión hay que configurarla a mano. Si no lo
   haces, tu robot opera gratis en el backtest.
4. **El probador no tiene libro de órdenes.** No hay cola, no hay ejecuciones parciales y el
   deslizamiento es un parámetro (o ninguno). Para una estrategia de tendencia con objetivos
   amplios da igual; para una que vive del diferencial, decide entre viable e inviable
   ([[microestructura-de-mercado]]).

Dos funciones del entorno causan la mitad de los autoengaños. La **optimización genética** busca
automáticamente la combinación de parámetros que maximiza el criterio que le pidas, y probar miles
es cuestión de minutos: siempre encontrarás algo excelente en la muestra que usaste. El **modo
forward** reserva una parte final del histórico para que la optimización no la toque y luego
comprueba ahí la combinación elegida. Si tu flujo no incluye esa segunda parte, no has validado
nada ([[validacion-temporal]]).

Y una frontera que conviene tener clara: MetaTrader es una plataforma de **ejecución minorista**,
y eso define su terreno: CFD y divisas con apalancamiento, cuentas modestas, latencia de decenas o
cientos de milisegundos y brókers que en muchos casos son tu contraparte. Si tu estrategia
necesita cola en el libro o latencia de microsegundos, este no es el entorno
([[latencia-y-ejecucion]]). MQL5, por su parte, es de sintaxis tipo C, con clases y eventos
(`OnInit`, `OnTick`, `OnTimer`, `OnTrade`), y **no es MQL4**: la arquitectura de órdenes cambió
—existen los conceptos de *orden* y de *deal*—, así que un asesor experto de MetaTrader 4 no se
compila tal cual en MetaTrader 5.

## Definición formal

El bucle del probador es un motor de eventos como cualquier otro, con dos parámetros que son los
que deciden el realismo:

:::formula
Tick(t) = f(historico_del_broker, modo_de_modelado)        P&L = Σ (precio_salida − precio_entrada) · tamaño · valor_del_punto − costes
:::

- `historico_del_broker` — velas y ticks que el bróker sirve a tu terminal. Es la fuente de
  verdad del backtest y cambia de un bróker a otro.
- `modo_de_modelado` — cómo se construyen los ticks: por generación desde velas de un minuto,
  desde ticks reales del bróker, con OHLC de un minuto, o solo con precios de apertura. Según el
  modo, tu `OnTick` se llama miles de veces por vela o una sola.
- `tamaño` — volumen de la operación en lotes. Para un par de divisas, un lote estándar son
  100.000 unidades de la divisa base.
- `valor_del_punto` — dinero que gana o pierde una operación por cada punto de movimiento. En un
  par con el dólar como divisa cotizada, un lote estándar y un punto de 0,0001, un punto vale
  10 USD; con 0,10 lotes vale 1 USD.
- `costes` — suma de spread, comisión y swap (el interés nocturno por mantener la posición
  abierta). Con apalancamiento y posiciones de varios días, el swap puede convertir una
  estrategia ganadora en perdedora.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `historico_del_broker` | Las velas y los ticks que tu bróker sirve a la terminal | precios y volúmenes por barra | No es una palanca: es la fuente de verdad del backtest. Cambiar de bróker cambia los huecos, el spread y los horarios, y con ellos el resultado del mismo robot |
| `modo_de_modelado` | Cómo se construyen los ticks que verá `OnTick`: generados desde velas de un minuto, ticks reales, OHLC de un minuto o solo aperturas | — | Cuanto más pobre es el modo, menos veces se llama `OnTick` dentro de una vela. Con «solo precios de apertura» el robot evalúa una vez por vela: ni stop, ni objetivo, ni huecos. El porcentaje de calidad de modelado mide qué parte de esos ticks es real, no si el backtest es bueno |
| `tamaño` | Volumen de la operación, en lotes | lotes (1 lote estándar = 100.000 unidades de la divisa base) | Multiplica el P&L y también las pérdidas: el apalancamiento no crea ventaja, solo acelera el resultado. Es la palanca que convierte una esperanza neta negativa en ruina más rápida |
| `valor_del_punto` | Dinero que gana o pierde la posición por cada punto de movimiento | moneda por punto (10 USD por punto y lote estándar en un par con el dólar cotizado) | Es proporcional al tamaño: con 0,10 lotes vale una décima parte. Y si confundes punto con pip en un par de cinco decimales, te sale diez veces mayor de lo que crees |
| `costes` | Suma de spread, comisión y swap | pips o dinero por operación | Es lo que decide entre viable e inviable: en el ejemplo la esperanza bruta es +0,72 pips y los costes suman 1,90 más 0,22 de deslizamiento. Con el spread al mínimo y la comisión a cero, el mismo robot parece rentable |
| Punto frente a pip | En un par de cinco decimales, el punto es el último decimal (0,00001) y el pip son diez puntos (0,0001) | 1 pip = 10 puntos | Si el robot calcula el tamaño contando puntos y tú piensas en pips, la posición sale **diez veces** más grande o más pequeña. Comprueba los decimales del símbolo antes de operar |
:::

Cuidado con una confusión que multiplica el tamaño de tu posición por diez: «punto» (point) y
«pip» no son lo mismo en todos los brókers. En un par de cinco decimales, el punto es el último
decimal (0,00001) y el pip son diez puntos (0,0001).

## Ejemplo

**Repintado.** Tres barras construidas con estos ticks:

```
barra 1:  100,0  100,5   99,5  100,2     (cierre 100,2)
barra 2:  100,3  101,0                   (cierre 101,0)
barra 3:  101,2  100,4                   (cierre 100,4)
```

La regla es «comprar cuando el precio supere 100,2 y salir al cierre de la barra 3».

- Leyendo el indicador de la **barra en formación**: durante la barra 2 el precio toca 100,3,
  supera el umbral y entra a 100,3. Salida a 100,4 → **+0,10 %**.
- Leyendo solo la **barra cerrada**: la señal se confirma al cerrar la barra 2 en 101,0, y la
  compra se ejecuta en el primer tick de la barra 3, a 101,2. Salida a 100,4 → **−0,79 %**.

La misma regla y la misma serie, con nueve décimas de diferencia por decidir con un valor que aún
se estaba formando.

:::figura
fichero: mql5-repintado-barra-en-formacion
pie: La línea azul es la serie de ticks y la raya roja, el umbral (el cierre de la barra 1). El triángulo verde marca la entrada de 100,3, que solo existe si lees la barra que todavía se está formando; el naranja, la entrada de 101,2 que consigues si esperas a que cierre. Nueve décimas sobre la misma regla llevan el resultado de +0,10 % a −0,79 %: la entrada que parece perfecta es la que solo aparece en el backtest.
fuente: figuras/mql5-y-metatrader-1.py
:::

**Costes.** Un robot de rango con objetivo de 6 pips y stop de 6 pips, acierto del 56 %, sobre
0,10 lotes de un par cuyo pip vale 1 USD con ese volumen. Spread de 1,2 pips, comisión de 7 USD
por lote negociado y un deslizamiento de 0,5 pips en las salidas por stop:

- Esperanza bruta: `0,56 · 6 − 0,44 · 6 = +0,72 pips` por operación.
- Coste fijo: `1,2 + 0,7 = 1,90 pips`.
- Deslizamiento esperado: se paga en el 44 % de las operaciones, `0,44 · 0,5 = 0,22 pips`.
- Esperanza neta: `0,72 − 1,90 − 0,22 = −1,40 pips`.

El robot tiene ventaja antes de costes y pierde dinero después. En el probador, ese mismo robot
sale rentable si el spread está puesto al mínimo y la comisión a cero.

## Código

```python verificable
# Repintado: decidir con la barra en formacion o esperar a que cierre.
ticks = [100.0, 100.5, 99.5, 100.2, 100.3, 101.0, 101.2, 100.4]
fin_barra = [4, 6, 8]
barras = [ticks[a:b] for a, b in zip([0] + fin_barra[:-1], fin_barra)]
cierres = [b[-1] for b in barras]
umbral = cierres[0]

entrada_formacion = next(t for t in barras[1] if t > umbral)   # mira la vela a medias
entrada_confirmada = barras[2][0]                             # espera al cierre
salida = cierres[2]

print("cierres de barra:", cierres)                    # -> [100.2, 101.0, 100.4]
print(f"barra en formacion  entrada {entrada_formacion:.1f}  resultado {salida / entrada_formacion - 1:+.2%}")
# -> barra en formacion  entrada 100.3  resultado +0.10%
print(f"barra cerrada       entrada {entrada_confirmada:.1f}  resultado {salida / entrada_confirmada - 1:+.2%}")
# -> barra cerrada       entrada 101.2  resultado -0.79%
```

:::claves
- `zip([0] + fin_barra[:-1], fin_barra)` empareja inicios con finales, y funciona porque `[:-1]` es un corte que **excluye** el último elemento. Si te olvidas de él, `zip` no avisa: se queda con las parejas que caben y pierdes una barra sin ver ningún error.
- `ticks[a:b]` **no** incluye la posición `b`. Por eso `ticks[0:4]` son cuatro ticks (0, 1, 2 y 3) y `fin_barra = [4, 6, 8]` son finales exclusivos. Confundir esto desplaza todas las barras una posición y cambia los cierres.
- `next(t for t in barras[1] if t > umbral)` devuelve el **primer** tick que supera el umbral, pero si ninguno lo supera lanza `StopIteration` en mitad del backtest en lugar de devolver `None`. Con `next(..., None)` tendrías un valor por defecto que puedes comprobar antes de operar.
- `barras[2][0]` es el primer tick de la tercera barra (`101,2`), no el cierre de la segunda (`101,0`). Esperar a que la vela cierre significa operar al primer precio de la vela siguiente: es exactamente la línea que separa +0,10 % de −0,79 %.
- `salida / entrada_formacion - 1` es un retorno simple sobre precios, así que cambia de signo si la entrada supera a la salida. Ese cociente no lleva spread ni comisión: con los costes del bloque siguiente, la operación que aquí gana deja de ganar.
- `f"{resultado:+.2%}"` multiplica por 100 y añade el signo de porcentaje, y el `+` fuerza a que salga el signo aunque el número sea positivo. Si escribes `:.2f` en vez de `:.2%`, el +0,10 % se imprime como `0.00` y parece que no ganaste nada.
:::

```python verificable
# Un robot con ventaja bruta que pierde dinero al poner los costes reales.
lotes = 0.10
unidades_por_lote = 100_000
valor_pip = lotes * unidades_por_lote * 0.0001          # en USD para este par

spread_pips = 1.2
comision_pips = 7.0 * lotes / valor_pip                 # 7 USD por lote, pasado a pips
slippage_pips = 0.5
objetivo, stop, acierto = 6.0, 6.0, 0.56

bruto = acierto * objetivo - (1 - acierto) * stop
coste_fijo = spread_pips + comision_pips
coste_desliz = (1 - acierto) * slippage_pips        # el stop se ejecuta a mercado
neto = bruto - coste_fijo - coste_desliz

print(f"valor del pip con {lotes:.2f} lotes: {valor_pip:.2f} USD")   # -> 1.00 USD
print(f"esperanza bruta: {bruto:+.2f} pips")                        # -> +0.72 pips
print(f"costes fijos:    {coste_fijo:.2f} pips")                    # -> 1.90 pips
print(f"esperanza neta:  {neto:+.2f} pips")                         # -> -1.40 pips
```

```text
// Esqueleto de asesor experto en MQL5: la barra en formacion se detecta con la serie de barras.
void OnTick()
{
   // Copiamos las dos ultimas barras cerradas; el indice 0 es la barra en formacion.
   double cierre_confirmado = iClose(_Symbol, PERIOD_H1, 1);
   double cierre_anterior   = iClose(_Symbol, PERIOD_H1, 2);

   if(PositionsTotal() == 0 && cierre_confirmado > cierre_anterior)
   {
      MqlTradeRequest peticion = {};
      MqlTradeResult  resultado = {};
      peticion.action   = TRADE_ACTION_DEAL;
      peticion.symbol   = _Symbol;
      peticion.volume   = 0.10;
      peticion.type     = ORDER_TYPE_BUY;
      peticion.price    = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
      peticion.deviation = 10;                 // deslizamiento maximo aceptado, en puntos
      peticion.type_filling = ORDER_FILLING_IOC;
      OrderSend(peticion, resultado);
   }
}
```

## Errores típicos

- **Probar en modo «solo precios de apertura» una estrategia intradía.** En ese modo el robot solo
  evalúa condiciones una vez por vela, así que no ve nada de lo que ocurre dentro de ella: ni el
  stop, ni el objetivo, ni los huecos.
- **Operar con el valor del indicador de la barra en formación.** La barra 0 cambia en cada tick:
  un cruce que «ya ha ocurrido» puede deshacerse un segundo después. Si la señal se calcula con
  la barra 0, el backtest encuentra entradas perfectas que en real no existen. Usa la barra 1 y
  asume que entras un poco más tarde.
- **Creer que el histórico del bróker es el mercado.** El spread del probador suele ser el mínimo
  o uno fijo, los ticks se generan a partir de velas de un minuto y las horas de cierre no
  coinciden con las del mercado real. Cambia de bróker y cambia el resultado del mismo robot.
- **No configurar comisión, swap y spread variable.** Con la comisión a cero y el spread mínimo,
  cualquier robot de alta frecuencia parece rentable. Escribe los costes que pagas de verdad
  antes de mirar la curva ([[slippage-y-comisiones]]).
- **Optimizar con el probador y no validar después.** La optimización genética encuentra la
  combinación que mejor se ajusta al pasado, incluidas sus casualidades. Usa el modo forward o
  reserva tú un tramo de datos que no toques, y desconfía de los picos estrechos en el mapa de
  parámetros ([[data-snooping-y-multiple-testing]]).
- **Confundir el resultado del probador con una prueba de viabilidad.** El probador no simula
  rechazos del bróker, ni deslizamiento en noticias, ni huecos de apertura del domingo, y no
  distingue un robot escrito en MetaTrader 5 de un MQL4 trasplantado sin adaptar. Antes de
  arriesgar dinero, pasa por cuenta demo y compara operación a operación ([[paper-trading]]).

:::practica
enunciado: Cuenta de 1.000 €, apalancamiento 1:30, EURUSD a 1,1000. El pip vale 10 USD por lote estándar y arriesgas como máximo el 2 % de la cuenta con un stop de 20 pips. ¿Cuántos lotes permite el bróker y cuántos permite tu control de riesgo?
pista: El margen limita el tamaño; el riesgo por operación lo limita mucho antes.
solucion: Margen: 1.000 · 30 = 30.000 € de posición, es decir 30.000 / 1,10 = 27.272 USD, unos 0,27 lotes. Riesgo: el 2 % de 1.000 son 20 €; un lote pierde 10 USD por pip, así que 20 pips son 200 USD por lote: 20 / 200 = 0,10 lotes. Conclusión: el bróker te deja 0,27 y tu regla solo 0,10; el apalancamiento no es un permiso para arriesgar.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué leer el valor de un indicador en la barra 0 puede darte un backtest mejor que la realidad?
o: Porque la barra en formación cambia en cada tick y una señal que parece confirmada puede desaparecer antes del cierre
o: Porque la barra 0 contiene datos del futuro que el bróker publica antes
o: Porque los indicadores solo son válidos en velas diarias
a: 1
e: La barra 0 no está cerrada: su máximo, su mínimo y su cierre se reescriben con cada tick. Una condición evaluada ahí puede cumplirse y deshacerse en el mismo segundo, y en el backtest queda registrada como una entrada perfecta. La solución es evaluar sobre la barra 1 y aceptar el retardo de una vela.
:::

:::quiz
p: Un robot tiene una esperanza bruta de +0,60 pips, paga 1,2 pips de spread y 0,7 de comisión por operación. ¿Qué concluyes?
o: Que la ventaja no cubre los costes: el resultado neto es negativo antes incluso de contar el deslizamiento
o: Que es rentable, porque la esperanza bruta es positiva
o: Que hay que subir el tamaño de posición para compensar los costes
a: 1
e: Los costes fijos suman 1,90 pips por operación y la ventaja bruta es 0,60, así que cada operación pierde 1,30 pips antes de deslizamiento. Subir el tamaño multiplica también las pérdidas: el apalancamiento no convierte una estrategia sin ventaja neta en rentable, solo acelera el resultado.
:::

:::trampa
Un robot optimizado que muestra una curva de capital impecable en el probador y una caída del
90 % del beneficio al desactivar la optimización no estaba funcionando: estaba memorizando. Antes
de mirar el beneficio, mira cuántas combinaciones de parámetros probó el optimizador y cuántas
sobrevivieron al tramo forward. Si sobrevive una de dos mil, no tienes una estrategia: tienes el
máximo de dos mil intentos.
:::
