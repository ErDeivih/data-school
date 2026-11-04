---
id: latencia-y-ejecucion
titulo: Latencia y ejecución
fase: 9
nivel: avanzado
rutas: [quant]
prerequisitos: [microestructura-de-mercado, order-book-y-spread, slippage-y-comisiones, que-es-un-mercado]
tags: [ejecucion, infraestructura, microestructura]
resumen: El tiempo entre decidir y que el mercado vea tu orden solo importa en relación con lo que dura tu ventaja; medirlo mal invalida el backtest entero.
fuentes: ["Harris (2003), 'Trading and Exchanges: Market Microstructure for Practitioners'", "Johnson (2010), 'Algorithmic Trading and DMA'"]
---

## En una frase

La latencia es el tiempo que transcurre desde que tu sistema decide algo hasta que esa orden
llega a la bolsa y vuelve la confirmación, y cuánto importa depende de una sola comparación:
lo que tarda el precio en moverse en tu contra frente a lo que vale tu ventaja.

## La idea

Cuando un sistema «ve» una oportunidad, entre esa observación y la ejecución hay una cadena
de esperas: el dato de mercado viaja hasta ti, tu programa lo procesa, la orden sale por la
red, la puerta de la bolsa la valida, el motor de casación la cruza con lo que haya en el
libro y la confirmación vuelve por el mismo camino. Súmalo y tienes el tiempo de ida y
vuelta. Cada eslabón se puede medir y cada uno se puede atacar, pero solo el que controlas
—tu proceso— se arregla escribiendo mejor código.

Las cifras útiles son órdenes de magnitud, no promesas de nadie:

| Montaje | Ida y vuelta típica |
| --- | --- |
| Retail por internet doméstico | decenas de milisegundos |
| Servidor alquilado en la misma ciudad que la bolsa | pocos milisegundos |
| Co-location en el centro de datos de la bolsa | decenas o centenas de microsegundos |
| Hardware dedicado (FPGA) en la misma sala | por debajo del microsegundo |

Lo importante no es el número, es la asimetría: entre la primera fila y la última hay un
factor de decenas de miles. Si tu ventaja tarda 200 milisegundos en desaparecer, la primera
fila compite; si tarda 1 milisegundo, la primera fila no existe.

Por eso la pregunta correcta no es «¿tengo poca latencia?» sino «¿cuánto dura mi ventaja?».
Para una estrategia de momentum que aguanta posiciones tres semanas, bajar de 50 ms a 5 ms no
cambia absolutamente nada: el coste de comisiones y el error de la muestra pesan mil veces
más. Para arbitrar un ETF contra su cesta de componentes, o para reaccionar a un dato
macroeconómico, la ventaja vive milisegundos y quien llega segundo no llega: llega tarde.

La latencia se paga de tres formas distintas, y conviene no mezclarlas:

1. **Movimiento adverso.** Mientras tu orden viaja, el libro se mueve. Si vas a comprar, el
   precio que te encontrará será peor que el que viste. Este coste es proporcional a la
   latencia y a la volatilidad del momento.
2. **Posición en la cola.** El libro casa por precio y luego por orden de llegada. Si pones
   una orden limitada al mismo precio que otros, estás detrás de todos los que llegaron antes
   y solo te llenan cuando hay flujo suficiente para agotar lo que hay delante.
3. **Oportunidades perdidas.** Si tu señal caduca antes de que llegue tu orden, no hay
   operación. Eso no aparece en el backtest y sí en la cuenta.

Y un matiz que se olvida siempre: llegar muy rápido a una señal mala no arregla nada. La
latencia es un multiplicador de la ejecución, no una fuente de ventaja por sí misma. Se puede
comprar velocidad con dinero; lo que no se puede comprar es saber hacia dónde va el precio.
Las estrategias puramente de latencia existen, pero son una carrera de infraestructura con
rendimientos decrecientes y costes crecientes, y para casi todo lo demás la variable que
decide el resultado es el coste total por operación.

Para el que construye sistemas sin intención de competir en microsegundos, la latencia
aparece sobre todo en el **backtest**. Un backtest que asume que te llenan al precio que
acababas de ver está mintiendo: hay que introducir un retardo explícito entre la señal y la
ejecución, del orden del que tendrás de verdad, y comprobar con una prueba en vivo (paper o
con dinero pequeño) que los fills reales se parecen a los simulados. La forma de medirlo bien
es con percentiles —p50, p99, p99.9—, no con la media: en ejecución lo que rompe el resultado
es la cola de la distribución, no el caso típico.

:::figura
fichero: latencia-presupuesto-y-montajes
pie: Arriba, cuánta ventaja queda viva según va pasando el tiempo: con esta señal y esta deriva, a los 100 ms no queda nada. Abajo, la misma cuenta al revés para cinco ventajas distintas: cuanto más pequeña es la ventaja, antes se agota, y la barra del arbitraje de un tick se queda a la izquierda de la línea del retail doméstico, es decir que muere antes de que la orden llegue a la bolsa. Fíjate en que la posición de semanas tiene un presupuesto de horas: la latencia no es buena ni mala, es grande o pequeña comparada con lo que dura la ventaja.
fuente: figuras/latencia-y-ejecucion-1.py
:::

## Definición formal

En tiempo continuo, con marcas de tiempo del mismo reloj (sincronizado por NTP o, mejor,
PTP):

:::formula
latencia_ida = t_bolsa − t_decisión          latencia_vuelta = t_confirmación − t_bolsa
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `latencia_ida` | Tiempo desde que tu sistema decide hasta que la bolsa acepta el mensaje | ms o µs | Es la parte que sufre el precio: cuanto mayor, más se habrá movido el libro cuando llegue tu orden |
| `latencia_vuelta` | Tiempo desde que la bolsa acepta hasta que tú tienes la confirmación | ms o µs | No empeora el precio de esa operación, pero te deja a ciegas para decidir la siguiente |
| `t_decisión` | Instante en que tu programa genera la orden, no cuando el humano la aprueba | marca de tiempo | Si mides desde que pulsaste el botón, el número que sale no es latencia: es tu dedo |
| `t_bolsa` | Instante en que la puerta de la bolsa acepta el mensaje | marca de tiempo | Es la referencia que importa, y solo sirve si el reloj está sincronizado con el suyo |
| `t_confirmación` | Instante en que tu sistema recibe el acuse o la ejecución | marca de tiempo | Con relojes desincronizados, las restas salen negativas y no significan nada: primero se sincroniza |
| `e` | Ventaja esperada de la operación | céntimos por acción o pb | Alarga el presupuesto: con más margen por operación aguantas más retardo |
| `v` | Deriva adversa: lo que el precio se mueve en tu contra por unidad de tiempo | pb o EUR por ms | Acorta el presupuesto en proporción inversa. No es una constante: en una apertura o tras un dato macro puede multiplicarse por diez |
| `latencia` | Retardo entre la señal y la llegada al libro, en las unidades de `v` | ms o µs | La operación tiene esperanza positiva mientras se quede por debajo de `e / v`; por encima, se pierde dinero antes de comisiones |
| `p99`, `p99.9` | Percentiles de la distribución de latencias, no la media | ms o µs | Son los que deciden el resultado: una media de 2 ms con un p99 de 300 ms arruina justo los momentos de más volumen |
:::

- `t_decisión` — instante en que tu sistema genera la orden (no cuando el humano la aprueba).
- `t_bolsa` — instante en que la puerta de la bolsa acepta el mensaje.
- `t_confirmación` — instante en que tu sistema recibe el acuse o la ejecución.
- La suma de las dos es el tiempo de ida y vuelta. Si los relojes no están sincronizados, la
  resta no significa nada: primero sincroniza, después mide.

El presupuesto de latencia se escribe como una desigualdad. Con `e` la ventaja esperada de la
operación y `v` la velocidad a la que el precio se mueve en tu contra:

:::formula
beneficio > 0  ⇔  latencia < e / v
:::

- `e` — ventaja esperada, en céntimos por acción o en puntos básicos.
- `v` — deriva adversa por unidad de tiempo, medida con datos de ese instrumento y esa franja
  horaria; no es una constante.
- `latencia` — retardo entre la señal y la llegada al libro, en las mismas unidades de tiempo
  que `v`.

Cuanto más pequeño es `e` y más rápido se mueve el precio, más corto es el presupuesto. Para
una estrategia de [[reversion-a-la-media|reversión]] con ventaja de un tick, el presupuesto se
agota en milisegundos; para una de [[momentum]] con horizonte semanal, es de días.

## Ejemplo

Precio de 100,00 €, ventaja esperada de 5 puntos básicos y un momento de volatilidad alta en
el que el precio se desplaza, en promedio, 0,05 puntos básicos por milisegundo en contra de
la dirección en la que quieres operar.

- La ventaja vale `100,00 · 0,0005 = 0,05 €` por acción.
- La deriva adversa vale `100,00 · 0,000005 = 0,0005 €` por milisegundo.
- Con 1 ms de latencia se pierde 0,0005 €, el **1 %** de la ventaja.
- Con 20 ms se pierden 0,0100 €, el **20 %**.
- Con 100 ms se pierden 0,0500 €, **todo el edge**.
- El punto de ruptura es `0,05 / 0,0005 = 100 ms`. Por encima de ahí, la operación tiene
  esperanza negativa antes de comisiones.

En una orden de 1.000 acciones, esos 100 ms de latencia cuestan 50 € de ventaja, que es
exactamente lo que ganabas. Y ojo con el supuesto: en una apertura o tras un dato macro, `v`
puede ser diez veces mayor, y entonces el presupuesto se reduce a 10 ms.

El segundo coste es la cola. Pones una orden limitada al mejor bid con **3.000 acciones por
delante** al mismo precio. Si en ese precio se cruzan 900 acciones por minuto de media, la
espera esperada es de 3,3 minutos *si el flujo se mantiene*. Pero el flujo no se mantiene: se
seca cuando el precio se aleja de ti, y se dispara cuando el precio viene hacia ti. Es decir,
te llenan sobre todo en los minutos en que el mercado se está moviendo en tu contra: eso es
la selección adversa, y es la razón de que los market makers cobren el diferencial.

## Código

```python verificable
# Presupuesto de latencia: cuanto del edge se come un retardo concreto
precio = 100.00
edge_bps = 5.0                       # ventaja esperada, en puntos basicos
deriva_por_ms = 0.00005 / 10         # el precio se mueve 0,05 pb por milisegundo

edge = precio * edge_bps / 10000     # ventaja en EUR por accion

for latencia_ms in (1, 5, 20, 100):
    adverso = precio * deriva_por_ms * latencia_ms
    queda = 100 * (1 - adverso / edge)
    print(f"{latencia_ms:>4} ms: coste adverso {adverso:.4f} EUR de {edge:.4f} EUR de edge, queda {queda:.1f} %")
# ->    1 ms: coste adverso 0.0005 EUR de 0.0500 EUR de edge, queda 99.0 %
# ->    5 ms: coste adverso 0.0025 EUR de 0.0500 EUR de edge, queda 95.0 %
# ->   20 ms: coste adverso 0.0100 EUR de 0.0500 EUR de edge, queda 80.0 %
# ->  100 ms: coste adverso 0.0500 EUR de 0.0500 EUR de edge, queda 0.0 %
```

:::claves
- `deriva_por_ms = 0.00005 / 10` parece una división decorativa y no lo es: el comentario dice «0,05 pb por milisegundo» y la constante que se usa después vale 0,000005. El `/ 10` es el que convierte puntos básicos en tanto por uno **y** puntos básicos en milisegundos a la vez; si lo quitas, el presupuesto se multiplica por diez y el ejemplo deja de cuadrar.
- `precio * edge_bps / 10000` y `precio * deriva_por_ms * latencia_ms` están en la misma unidad (EUR por acción). Comparar dos magnitudes en unidades distintas es el error que hace que un presupuesto de latencia salga absurdo, así que conviene comprobar siempre que los dos lados de la división final se cancelan.
- `for latencia_ms in (1, 5, 20, 100):` recorre una **tupla**, no un rango. No hace falta que los valores sean equidistantes ni consecutivos: la línea de arriba del bucle es exactamente el número de escenarios que quieras, y añadir 1000 ms es añadir un elemento a la tupla.
- `f"{latencia_ms:>4} ms"` alinea el número a la derecha en cuatro caracteres, para que la salida quede en columna. `:>4` no redondea ni recorta; `{adverso:.4f}` sí limita a cuatro decimales, pero solo en el texto que se imprime.
- `queda = 100 * (1 - adverso / edge)` da un porcentaje de la ventaja que sobrevive. Cuando `adverso` pasa de `edge`, el resultado es negativo: no hay ninguna protección en la fórmula que lo impida, y ese negativo es justo el aviso de que la operación ya no interesa.
- El bucle **no** acumula el coste de las operaciones anteriores ni el de la cola del libro: cada latencia se evalúa como si fuera la única. Es un cálculo de presupuesto, no el resultado de una estrategia.
:::

```python verificable
# Espera en la cola FIFO: no es solo cuestion de latencia de red
delante = 3000            # acciones por delante de tu orden, a tu mismo precio

for flujo in (300, 900, 3000):
    print(f"flujo {flujo:>5} acciones/min -> espera {delante / flujo:>4.1f} min")
# -> flujo   300 acciones/min -> espera 10.0 min
# -> flujo   900 acciones/min -> espera  3.3 min
# -> flujo  3000 acciones/min -> espera  1.0 min
```

```text
Como se mide la latencia de verdad (y por que el percentil importa)
medicion                     | que mide                          | percentil util
decision -> envio            | tu propio codigo                  | p99
envio -> llegada a la bolsa  | red y puerta de acceso            | p99.9
bolsa -> confirmacion        | motor de casacion y vuelta        | p99.9
decision -> confirmacion     | el total que sufre la estrategia  | p99.9
```

## Errores típicos

- **Optimizar latencia sin haber medido cuánto dura la señal.** Si tu ventaja vive horas,
  gastar en co-location no te da nada. Primero calcula `e / v`; casi siempre sale un
  presupuesto enorme y el esfuerzo debe ir a comisiones y a la calidad de la señal.
- **Backtestear con ejecución al precio observado.** Es el error más caro y el más común:
  asumir que compras al ask que viste en el instante `t` cuando tu orden llega en `t + 30 ms`.
  Modela el retardo y deja que el backtest ejecute contra el libro del instante de llegada.
- **Confundir latencia con ancho de banda.** Contratar más megas no reduce el retardo: el
  tiempo de propagación depende de la distancia física y de los saltos de red, no del caudal.
  Son dos problemas distintos y se arreglan con cosas distintas.
- **Suponer que una orden limitada se ejecuta porque el precio la tocó.** Con prioridad
  precio-tiempo, tocar el precio solo te pone en la cola. Si hay 3.000 acciones delante y el
  flujo es de 900 por minuto, puedes esperar minutos, y no te llenarán en el mejor momento.
- **Ignorar la selección adversa.** Los fills llegan cuando el mercado va en tu contra; los
  fills que querrías (justo antes de que el precio se vaya a tu favor) no llegan porque
  alguien más rápido ya se llevó esa liquidez. Un backtest con fill rate del 100 % en órdenes
  limitadas es pura fantasía.
- **Medir la latencia media.** Un promedio de 2 ms con un p99 de 300 ms arruina la ejecución
  en los momentos que importan, que son justo los de más volumen. Mide y publica la cola, con
  los relojes sincronizados, o los números no significan nada.

:::practica
enunciado: Un valor cotiza a 250,00 EUR, tu ventaja medida es de 8 puntos básicos y el precio se desplaza en tu contra 0,2 pb por milisegundo. ¿Cuál es el presupuesto de latencia en milisegundos y qué porcentaje de la ventaja se pierde con 10 ms?
pista: Pasa las dos magnitudes a euros por acción: la ventaja es un importe fijo y la deriva adversa crece con el tiempo.
solucion: Ventaja: 250,00 · 0,0008 = 0,20 EUR por acción. Deriva adversa: 250,00 · 0,00002 = 0,005 EUR por milisegundo. El presupuesto es 0,20 / 0,005 = 40 ms; por encima de eso la operación tiene esperanza negativa antes de comisiones. Con 10 ms pierdes 0,005 · 10 = 0,05 EUR, el 25 %. En una orden de 2.000 acciones la ventaja vale 400 EUR y esos 10 ms ya se comen 100.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Cuándo deja de ser rentable una estrategia por culpa de la latencia?
o: Cuando la latencia supera el tiempo que tarda el precio en moverse en contra lo que vale la ventaja
o: Cuando la latencia supera los 100 milisegundos, que es el umbral del trading de alta frecuencia
o: Cuando la latencia supera el tiempo que tardas en pulsar el botón
a: 1
e: El criterio es la comparación entre la ventaja y la deriva adversa acumulada: latencia menor que ventaja dividida por la velocidad del precio. No hay un umbral universal de 100 ms: para un horizonte de días, 500 ms son irrelevantes, y para arbitraje de milisegundos, 5 ms ya es demasiado.
:::

:::quiz
p: Pones una orden limitada al mejor bid y hay 3.000 acciones por delante. El precio toca tu nivel. ¿Qué pasa?
o: Te ejecutan inmediatamente porque el precio ha llegado a tu orden
o: Solo te ejecutan cuando se crucen las acciones que están por delante de ti en la cola
o: La orden se cancela automáticamente al tocar el precio
a: 2
e: El libro casa por precio y después por orden de llegada: tocar el nivel te pone en la cola, no al principio. Con 3.000 acciones delante y un flujo de 900 por minuto, la espera media es de minutos, y además solo te llenarán si el flujo sigue viniendo a ese precio.
:::

:::quiz
p: ¿Por qué se mide la latencia con percentiles y no con la media?
o: Porque la media no se puede calcular con marcas de tiempo de red
o: Porque los momentos que deciden el resultado son los de latencia alta, que se esconden en el p99
o: Porque el p99 siempre es igual a la media más tres desviaciones típicas
a: 2
e: La media describe el caso típico, y el caso típico no es el problema: las pérdidas llegan en los episodios de congestión, que son precisamente los de alto volumen. El p99.9 sí se puede calcular y no tiene por qué seguir ninguna relación fija con la media: depende de la distribución de la cola.
:::
