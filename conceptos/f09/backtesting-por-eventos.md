---
id: backtesting-por-eventos
titulo: Backtesting por eventos
fase: 9
nivel: experto
rutas: [quant]
prerequisitos: [backtesting-vectorizado, order-book-y-spread, slippage-y-comisiones]
tags: [backtest, ejecucion, microestructura, simulacion]
resumen: Simular el backtest orden por orden, con cola, latencia y ejecuciones parciales, para saber si tu estrategia sobrevive al mercado real.
fuentes: ["López de Prado (2018), 'Advances in Financial Machine Learning', cap. 8", "Johnson (2010), 'Algorithmic Trading and DMA'"]
---

## En una frase

El backtesting por eventos reproduce el mercado como una secuencia de sucesos —llega un precio,
la estrategia decide, se envía una orden, el bróker la acepta, se ejecuta total o parcialmente—
de modo que cada operación tiene una hora, un precio y un tamaño que dependen de lo que había en
ese instante, no de lo que acabaría pasando.

## La idea

Un backtest vectorizado responde a la pregunta «si hubiera estado comprado, ¿cuánto habría
ganado?». Un backtest por eventos responde a una pregunta más incómoda: «¿habría podido estar
comprado, al precio que creo, con el tamaño que creo, en el momento en que lo decidí?».

La diferencia se ve mejor con un ejemplo de mercado real. El libro de órdenes tiene 300 acciones
en compra a 100,00 y 200 en venta a 100,10. Tú quieres comprar 500 acciones y pones una orden
límite a 100,00 para no pagar el diferencial. En un backtest vectorizado, esa orden se ejecuta
entera en cuanto el precio toca 100,00: el array no sabe que hay una cola delante. En la
realidad, tu orden está **detrás** de esas 300 acciones, y solo se ejecutará cuando lleguen
ventas suficientes para consumir primero las 300 de delante y luego las tuyas. Si el precio se
va sin que hayan llegado esas ventas, te quedas fuera o entras a medias.

:::figura
fichero: backtesting-por-eventos-la-cola
pie: Arriba, la cola que hay por delante de tu orden: solo empieza a llenarte cuando llega a cero. Abajo, las acciones que de verdad acabas teniendo contra las 500 que pediste; el hueco entre las dos líneas es la exposición que el backtest vectorizado se inventa.
fuente: figuras/backtesting-por-eventos-1.py
:::

Eso es la **cola** (queue position), y es la razón por la que la mayoría de las estrategias de
límite funcionan peor en real que en el backtest. Hay tres cosas más que solo se pueden modelar
con un reloj:

- **Latencia.** Tu señal se calcula cuando llega el dato, tu orden sale 3 milisegundos después y
  el bróker la acepta 2 milisegundos más tarde. En un mercado rápido, esos 5 ms son el precio.
- **Ejecuciones parciales y cancelaciones.** Una orden de 500 puede ejecutarse en trozos de 100,
  250 y 150 en momentos distintos, cada uno a un precio distinto. Tu posición media no es la que
  pediste.
- **Tipos de orden con semántica propia.** Una orden a mercado cruza el diferencial y paga el
  peor precio disponible; una stop se convierte en orden a mercado justo cuando el precio se
  mueve en tu contra, que es cuando el libro está más fino; una «todo o nada» puede quedarse sin
  ejecutar mientras una normal sí se habría llenado.

El precio de todo esto es que el motor de eventos es entre cien y mil veces más lento que el
vectorizado, y mucho más código. Por eso el flujo sensato es en dos etapas: explorar cien ideas
con [[backtesting-vectorizado|el backtest vectorizado]] y luego reconstruir la que sobrevive con
un motor de eventos, que es donde se descubre si el resultado era del mercado o del array.

## Definición formal

Un backtest por eventos es una simulación de sucesos discretos. El estado del sistema en el
instante `t` es `(cartera, ordenes_vivas, libro)`, y la simulación avanza procesando una
secuencia ordenada de eventos:

:::formula
E = {(t_k, tipo_k, carga_k)}   con   t_k ≤ t_{k+1}
:::

- `t_k` — marca de tiempo del suceso `k`, en el reloj del mercado. Los empates se rompen con una
  prioridad fija (por ejemplo, primero los datos de mercado y después las órdenes), y ese orden
  decide el resultado: cambiarlo cambia el backtest.
- `tipo_k` — uno de: `dato` (nueva barra o tick), `orden_enviada`, `orden_aceptada`,
  `ejecucion`, `cancelacion`, `fin_de_sesion`.
- `carga_k` — el contenido: precio y volumen para un dato; lado, tipo, cantidad y precio límite
  para una orden; cantidad y precio para una ejecución.
- `libro` — el estado del libro de órdenes en ese instante: mejores precios y profundidad
  ([[order-book-y-spread]]).
- **Latencia de envío** `δ`: el evento `orden_enviada` no ocurre en el instante de la decisión,
  sino en `t + δ`. Es un parámetro del modelo, y con `δ = 0` estás suponiendo un mercado
  infinitamente rápido.
- **Cola** `q`: número de acciones (o contratos) que hay por delante de tu orden en su nivel de
  precio. Una orden límite de compra a precio `p` con cantidad `Q` se ejecuta cuando el volumen
  negociado a `p` después de su llegada, `V_p`, supera `q`:
- **Cantidad ejecutada** de una orden límite: `min(Q, máx(0, V_p − q))`.

:::parametros
| Símbolo | Qué es | Unidades | Si sube… |
| --- | --- | --- | --- |
| `t_k` | Marca de tiempo del suceso `k`, en el reloj del mercado | instante (ms, µs) | Los empates se rompen con una prioridad fija, y ese orden decide el resultado: cambiarlo cambia el backtest sin cambiar los datos |
| `δ` | Latencia de envío: la orden sale en `t + δ`, no cuando decides | milisegundos | Con `δ` mayor entras a peor precio. Con `δ = 0` estás suponiendo un mercado infinitamente rápido, y basta unos pocos ms para arruinar una estrategia que vive del diferencial |
| `q` | Cola: acciones que hay por delante en tu nivel de precio | acciones o contratos | Cuanto mayor es `q`, menos se te llena: con `q = 0` te llenas a la primera, y con 300 necesitas que lleguen más de 300 en ventas antes de tocar una sola |
| `V_p` | Volumen negociado a tu precio `p` después de tu llegada | acciones o contratos | Es lo que te llena. Si `V_p` no supera `q`, la ejecución es cero aunque el precio haya tocado tu nivel |
| `Q` | Cantidad que pides en la orden | acciones o contratos | No cambia el precio de tu ejecución, pero cuanto mayor sea `Q` menos probable es que se llene entera: el resultado es una posición media, no la pedida |
| `min(Q, máx(0, V_p − q))` | Cantidad ejecutada de una orden límite | acciones o contratos | Nunca pasa de `Q` ni es negativa: la primera venta de 400 con `q = 300` llena 100, y las que lleguen después solo cuentan por lo que exceda la cola |
| `libro` | Estado del libro en ese instante: mejores precios y profundidad | precio y acciones | Un libro más fino mueve el precio con menos volumen, y es la situación típica cuando se dispara tu orden stop |
:::

El motor debe mantener tres invariantes, y cuando una se rompe el backtest deja de significar
algo:

1. **Nunca se usa información con marca de tiempo posterior** al evento que se está procesando
   ([[sesgo-de-mirar-al-futuro]]). Un motor de eventos bien hecho lo garantiza por construcción,
   que es su mayor ventaja sobre el vectorizado.
2. **El efectivo y las posiciones cuadran en todo momento**: cada ejecución modifica caja,
   inventario y comisión de forma atómica.
3. **Toda orden enviada termina en un estado final**: ejecutada, cancelada o rechazada. Las
   órdenes que quedan colgadas al final de la simulación son un error del motor, no un detalle.

## Ejemplo

Libro: 300 acciones en compra a 100,00 y 200 en venta a 100,10. Enviamos una orden límite de
compra por 500 acciones a 100,00. Delante de nosotros hay 300 acciones en la cola.

Llegan dos ventas a mercado contra el bid:

```
venta de 400  ->  300 consumen la cola, 100 nos llenan a nosotros   (ejecutado 100 de 500)
venta de 250  ->  la cola ya esta vacia, 250 nos llenan             (ejecutado 350 de 500)
```

Después, el precio se aleja y cancelamos lo que queda. Resultado: **350 acciones ejecutadas de
500 (el 70 %)**, todas a 100,00, con 150 acciones de exposición que nunca existieron.

Compara con las dos simplificaciones habituales:

- **Vectorizado, ejecución completa al toque:** 500 acciones a 100,00. Se inventa 150 acciones.
- **Vectorizado, ejecución al cierre de la barra:** 500 acciones a 100,30 (el cierre), y encima
  con un deslizamiento que el modelo no ha pagado.

Si el precio sube un 2 % antes de que salgas, esas 150 acciones que el modelo cree tener valen
`150 · 100 · 0,02 = 300 €` de beneficio imaginario. Sobre una cuenta de 10.000 €, un 3 % de
rentabilidad que aparece y desaparece por no haber modelado una cola de 300 acciones.

## Código

```python verificable
# Cola y ejecucion parcial: la diferencia entre "toco el precio" y "me ejecutan".
cola_por_delante = 300
orden = 500
ejecutado = 0
cola = cola_por_delante

for venta in (400, 250):          # volumen que llega contra nuestro nivel de precio
    consume_cola = min(cola, venta)
    cola -= consume_cola
    disponible = venta - consume_cola
    llena = min(orden - ejecutado, disponible)
    ejecutado += llena
    print(f"venta de {venta:>3} -> cola delante {cola:>3}  ejecutado {ejecutado:>3} de {orden}")
# -> venta de 400 -> cola delante   0  ejecutado 100 de 500
# -> venta de 250 -> cola delante   0  ejecutado 350 de 500

print(f"parcial: {ejecutado} de {orden} ({ejecutado / orden:.0%})")   # -> parcial: 350 de 500 (70%)
```

:::claves
- El bucle recorre `(400, 250)` y **arrastra estado** entre vueltas (`cola`, `ejecutado`): no es una
  operación vectorizable sin pensarlo, y por eso el motor de eventos es un bucle. Ese estado es
  justo lo que el backtest vectorizado no tiene.
- `min(cola, venta)` es el reparto de una sola venta: primero se come lo que hay delante. La resta
  `venta - consume_cola` es lo que sobra para ti, y `min(orden - ejecutado, disponible)` recorta a
  lo que te queda por comprar. Los tres `min` son el modelo entero de la cola.
- `cola -= consume_cola` es asignación aumentada sobre un `int` de Python: `cola` es un entero, no
  un array, así que no hay aliasing ni vistas por ningún lado. Cambiar `cola` no toca
  `cola_por_delante`, que se quedó en 300.
- Ojo con el orden de las dos restas: si calculas `disponible` **antes** de restar la cola, te
  llevas la venta entera y la ejecución sale 500 de 500. Es el mismo código con dos líneas
  intercambiadas y ningún error.
- `f"{ejecutado / orden:.0%}"` divide dos `int` y da `float`. Si en vez de eso hubieras escrito
  `ejecutado // orden`, el resultado sería `0` y el porcentaje saldría `0 %`: la diferencia entre
  división entera y real es la que hace que el 70 % aparezca.
- Con una tercera venta de 180 el resultado no cambia: cuando `orden - ejecutado` llega a 0, el
  `min` devuelve 0 y las ventas siguientes se ignoran. Añadir vueltas al bucle no es una forma de
  llenar más: el tope es `Q`.
:::

```python verificable
# Lo que el backtest vectorizado se inventa cuando da por hecho el llenado completo.
objetivo, ejecutado = 500, 350
precio_entrada, subida = 100.0, 0.02
hueco = objetivo - ejecutado

print(f"el modelo cree tener {objetivo} acciones y tiene {ejecutado}")
print(f"exposicion inexistente: {hueco} acciones")
print(f"beneficio imaginario con una subida del 2 %: {hueco * precio_entrada * subida:.0f} EUR")
# -> beneficio imaginario con una subida del 2 %: 300 EUR
print(f"sobre una cuenta de 10000 EUR es un {(hueco * precio_entrada * subida) / 10000:.1%}")
# -> sobre una cuenta de 10000 EUR es un 3.0%
```

```python ilustrativo
# Esqueleto de un motor de eventos minimo: el bucle y el orden de los sucesos.
import heapq


class Motor:
    def __init__(self):
        self.cola = []          # monticulo de (timestamp, prioridad, tipo, carga)
        self.cartera = {"caja": 10000.0, "posicion": 0}

    def programar(self, t, prioridad, tipo, carga):
        heapq.heappush(self.cola, (t, prioridad, tipo, carga))

    def ejecutar(self, broker, estrategia, datos):
        for t, fila in datos:                       # datos ordenados por timestamp
            self.programar(t, 0, "dato", fila)
            while self.cola and self.cola[0][0] <= t:
                _, _, tipo, carga = heapq.heappop(self.cola)
                if tipo == "dato":
                    estrategia.al_dato(carga, self)          # decide y programa ordenes
                elif tipo == "orden_enviada":
                    broker.aceptar(carga, self)              # aplica latencia y comisiones
                elif tipo == "ejecucion":
                    broker.aplicar(carga, self.cartera)      # caja, posicion e inventario
```

## Errores típicos

- **Dar por hecho el llenado completo y al precio de la señal.** Es el error que convierte un
  motor de eventos en un backtest vectorizado caro: si toda orden límite se ejecuta entera en
  cuanto el precio la toca, has tirado el 90 % del trabajo del motor. Modela cola y volumen
  negociado en ese nivel.
- **Ignorar la cola.** Una orden límite no se ejecuta «porque el precio llegó»: se ejecuta
  cuando el volumen negociado después de tu llegada supera lo que había por delante. En un valor
  líquido esa cola son miles de acciones, y tu orden es la última.
- **Modelar latencia cero.** Con `δ = 0` estás suponiendo que decides, envías y ejecutas en el
  mismo microsegundo. Basta una latencia de unos pocos milisegundos para arruinar una estrategia
  que vive del diferencial ([[latencia-y-ejecucion]]).
- **Usar barras donde hace falta el tick.** Con datos de un minuto no puedes saber si tu orden
  límite, situada en el mínimo de la barra, se ejecutó antes o después de que el precio la
  atravesara. El orden de los sucesos dentro de la barra es justo lo que decide el resultado;
  aquí [[tick-data-y-ohlcv|el tick]] no es un lujo.
- **Medir el coste con el diferencial medio del periodo.** El diferencial se ensancha cuando
  hay volatilidad y se estrecha cuando no; y tu orden stop se ejecuta precisamente en el peor
  momento. Usa el diferencial del instante del suceso, no una media ([[slippage-y-comisiones]]).
- **No cuadrar la cartera al final de la simulación.** Órdenes vivas, posiciones negativas
  imposibles o caja que no cuadra son síntomas de que el motor aplica los sucesos en un orden
  distinto del que el mercado aplica. Revisa el invariante antes de mirar la rentabilidad.

:::practica
enunciado: Compras 800 acciones con una orden a mercado. Tu señal se calcula al ver el precio 25,00, envías 4 ms después y el bróker acepta 3 ms más tarde, cuando el precio ya está en 25,06. Si la ventaja esperada de la estrategia es de 30 puntos básicos sobre el nominal, ¿sigue siendo viable?
pista: Pasa el retraso a dinero por acción y compáralo con la ventaja, ambos sobre el mismo nominal.
solucion: Nominal: 800 · 25,00 = 20.000 €. Ventaja: 20.000 · 0,0030 = 60 €. El retraso de 7 ms cuesta 0,06 € por acción: 800 · 0,06 = 48 €, un 0,24 % del nominal. Queda 60 − 48 = 12 € por operación, y cualquier pico de volatilidad se come ese margen. Conclusión: con esa latencia la ventaja es real pero casi toda se la lleva la ejecución.
:::

## Comprueba que lo sabes

:::quiz
p: Con 300 acciones en cola por delante en tu nivel de precio y una orden límite de compra por 500, llega una venta a mercado de 400. ¿Cuánto se ejecuta de tu orden?
o: 100 acciones, porque 300 se las lleva la cola que estaba delante
o: 400 acciones, porque la venta es mayor que lo que hay en el libro
o: Nada, porque una orden límite no se ejecuta contra órdenes a mercado
a: 1
e: Las 400 acciones de venta consumen primero las 300 que estaban por delante en la cola y solo las 100 restantes llegan a tu orden. Por eso la posición inicial de la cola es un parámetro del modelo y no un detalle: con 0 acciones delante te habrías llenado entero.
:::

:::quiz
p: ¿Qué gana un backtest por eventos respecto a uno vectorizado?
o: Que puede modelar el orden temporal de los sucesos: cola, latencia, parciales y cancelaciones
o: Que es más rápido, porque procesa los datos en el orden natural
o: Que no necesita datos históricos ajustados
a: 1
e: La ventaja es de fidelidad, no de velocidad: el motor de eventos es mucho más lento porque recorre suceso a suceso. Su valor es que obliga a que cada decisión use solo información disponible en ese instante y permite modelar el mecanismo de ejecución. Los datos históricos siguen siendo igual de necesarios y con los mismos problemas de calidad.
:::

:::aviso
Un motor de eventos con supuestos malos es peor que un vectorizado honesto: da la falsa
sensación de rigor. Si tu modelo de ejecución es «se llena todo al cierre», escríbelo en la
documentación del backtest y quédate con el vectorizado; añadir un bucle con reloj no convierte
el supuesto en realidad.
:::
