---
id: order-book-y-spread
titulo: Libro de órdenes y diferencial
fase: 9
nivel: avanzado
rutas: [quant]
prerequisitos: [tick-data-y-ohlcv, microestructura-de-mercado]
tags: [libro, spread, liquidez, señales]
resumen: Bid, ask, profundidad y desequilibrio: como leer el libro de órdenes, que cuesta cruzarlo y que se puede y no se puede sacar de el como señal.
fuentes: ["Harris (2003), 'Trading and Exchanges: Market Microstructure for Practitioners'", "Bouchaud et al. (2018), 'Trades, Quotes and Prices'"]
---

## En una frase

El libro de órdenes es la lista de todo lo que está dispuesto a comprar y a vender a cada precio,
el diferencial es la distancia entre lo mejor de cada lado, y juntos determinan cuánto te cuesta
operar ahora mismo y qué presión hay en el mercado.

## La idea

Piensa en una casa de subastas con dos pizarras. En la de la izquierda se apuntan las ofertas de
compra: «doy 100 por 400 acciones», «doy 99,99 por 700». En la de la derecha, las de venta:
«vendo a 100,01, 300 acciones», «vendo a 100,02, 600». La mejor oferta de compra es 100,00 y la
mejor de venta es 100,01. Nadie ha cruzado todavía porque ninguno cede: el comprador no sube de
100,00 y el vendedor no baja de 100,01.

Ese hueco de un céntimo es el **diferencial** (*spread*), y es el precio de la inmediatez. Si
quieres comprar ya, tienes que aceptar 100,01. Si quieres comprar a 100,00, tienes que esperar
en la cola y rezar para que alguien venda antes de que el precio se vaya. No hay una opción
gratis: o pagas el diferencial, o asumes el riesgo de no ejecutar.

La **profundidad** es cuánto hay en cada nivel. Un libro con 400 acciones en el mejor precio y
20.000 dos céntimos más abajo no es lo mismo que uno con 5.000 en el mejor precio. El primero
tiene un diferencial estrecho pero poca resistencia: en cuanto llegue una orden grande, se lo
come y el precio salta. El segundo aguanta. Por eso el diferencial solo no basta para juzgar la
liquidez: hay que mirar **diferencial y profundidad juntos**.

:::figura
fichero: order-book-spread-y-profundidad
pie: A la izquierda, el libro del ejemplo con los dos lados frente a frente: el spread es de 2 pb, pero el primer nivel de venta solo tiene 900 títulos y el de compra 1.200, así que el desequilibrio es +0,143 con un nivel y +0,159 al mirar tres. A la derecha, lo que cuesta cruzar: 10.000 títulos se reparten por los cuatro niveles y el precio medio queda 3,66 pb por encima del mejor ask, cuando el spread cotizado era de 1 pb. Conclusión: el diferencial es el precio de entrar, no el precio de tu orden; necesitas la profundidad para saber qué tamaño admite el libro.
fuente: figuras/order-book-y-spread-1.py
:::

El **desequilibrio** resume la asimetría: si en el lado de compra hay mucho más tamaño que en el
de venta, hay presión compradora en el libro. Es tentador usarlo como señal — «hay más compradores,
el precio subirá» — pero tiene tres problemas: es ruidoso, cambia en milisegundos y, sobre todo,
el libro solo muestra las órdenes **visibles**. Las órdenes iceberg y las ocultas no aparecen, y
quien las usa sabe lo que hace.

:::aviso
El libro que ves por tu bróker suele ser una foto parcial y con retardo. Los libros
consolidados de varios centros, filtrados y agregados en tiempo real, son un producto de pago.
Si tu estrategia depende de reaccionar en microsegundos al libro, compites con quien tiene la
foto completa antes que tú.
:::

Un matiz que se olvida con frecuencia es la diferencia entre tres precios distintos de la misma
operación:

- **Diferencial cotizado:** la distancia entre el mejor bid y el mejor ask en ese instante.
- **Diferencial efectivo:** la diferencia entre el precio al que se ejecutó tu orden y el *mid*
  que había justo antes. Suele ser menor que el cotizado, porque las órdenes no siempre se
  ejecutan contra el mejor nivel o porque mejoras el precio dentro del diferencial.
- **Diferencial realizado:** compara el precio de ejecución con el *mid* unos segundos después.
  Si compraste y el mid subió, tu diferencia realizada es mejor que la efectiva; si bajó,
  pagaste selección adversa. Está es la métrica que revela si tu ejecución es buena de verdad o
  solo rápida.

## Definición formal

Con los niveles ordenados de mejor a peor en cada lado:

:::formula
bid = max(B)     ask = min(A)     spread = ask - bid     mid = (bid + ask) / 2
:::

- `B`, `A` — niveles de compra y de venta, cada uno con precio `p` y cantidad `q`.
- `bid`, `ask` — el mejor precio de compra y de venta disponibles.
- `spread` — el coste inmediato de cruzar, en unidades de precio.
- `mid` — referencia central; no es operable.

En puntos básicos, que es como se comparan mercados distintos:

:::formula
spread_pb = (ask - bid) / mid · 10.000
:::

- **punto básico (pb)** — una diezmilésima parte, es decir 0,01 %. Un spread de 1 pb sobre un
  precio de 100 equivale a 0,01 EUR.

La profundidad y el desequilibrio de los primeros `n` niveles:

:::formula
Q_bid = suma q_i (compra)     Q_ask = suma q_j (venta)     imbalance = (Q_bid - Q_ask) / (Q_bid + Q_ask)
:::

- `Q_bid`, `Q_ask` — cantidad agregada visible en los `n` primeros niveles de cada lado.
- `imbalance` — entre −1 (todo venta) y +1 (todo compra); 0 es equilibrio.

Y el precio al que se ejecuta una orden a mercado de tamaño `Q`, que ya viste al hablar de
microestructura:

:::formula
precio_medio(Q) = ( suma p_k · q_k ) / Q      impacto = precio_medio(Q) - ask
:::

- `p_k`, `q_k` — precio y cantidad de cada nivel consumido.
- `impacto` — lo que el libro se mueve al intentar ejecutar tu orden.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `B`, `A` | Los niveles de compra y de venta, cada uno con su precio y su cantidad | listas de (EUR, títulos) | Cuantos más niveles y más gruesos, más aguanta el libro tu orden. El libro que ves es solo la parte **visible**: las órdenes iceberg muestran una fracción de su tamaño |
| `bid`, `ask` | El mejor precio de compra y el mejor de venta disponibles | EUR por título | Si el `bid` sube o el `ask` baja, el spread se estrecha y operar es más barato. Pero mejor precio no siempre es más profundidad: con poca cantidad en el primer nivel, el precio salta en cuanto llega una orden |
| `mid = (bid + ask) / 2` | La referencia central del precio | EUR por título | No es un precio operable: si compras pagas el ask y si vendes cobras el bid. Sirve para normalizar costes entre activos de precios muy distintos |
| `spread = ask − bid` | El coste inmediato de cruzar, en unidades de precio | EUR por título | Cada céntimo que se ensancha lo pagas íntegro en cada ida y vuelta. Se ensancha con la volatilidad, en la apertura, al cierre y con las noticias: justo cuando más te apetece operar |
| `spread_pb` | Ese mismo spread normalizado por el mid | puntos básicos (1 pb = 0,01 %) | Es el número que permite comparar mercados: 1 pb sobre 100 EUR es lo mismo que 1 pb sobre 5 EUR. Con `spread_pb` alto, tu estrategia necesita ganar eso **por operación** solo para empatar |
| `n` (profundidad mirada) | Cuántos niveles se agregan para medir profundidad y desequilibrio | niveles | Al subirlo, `imbalance` se suaviza porque el ruido de los primeros niveles se diluye, y `Q_bid`/`Q_ask` crecen. También cambia lo que significa liquidez: un nivel es la punta, diez son la resistencia |
| `Q_bid`, `Q_ask` | La cantidad agregada en los `n` primeros niveles de cada lado | títulos | Más cantidad total reduce el impacto de tu orden, pero repartida en muchos niveles no protege el primer precio. Lo que importa para tu coste es cuánta hay **hasta el precio que necesitas alcanzar** |
| `imbalance` | El desequilibrio del libro: `(Q_bid − Q_ask)/(Q_bid + Q_ask)` | adimensional, entre −1 y +1 | Positivo indica presión de compra visible; negativo, de venta. Es una señal débil, ruidosa y solo de lo visible: cuando reaccionas a ella, el libro ya ha cambiado |
| `precio_medio(Q)` | El precio al que se ejecuta de verdad una orden a mercado de tamaño `Q` | EUR por título | Con `Q` pequeño se parece al mejor precio; con `Q` grande se acerca al último nivel consumido. Es lo que hay que meter en un backtest en lugar del precio de cierre |
| `impacto = precio_medio(Q) − ask` | Lo que el libro se mueve al intentar ejecutar tu orden | EUR por título (o pb) | Crece con el tamaño y con la prisa. En el ejemplo, 10.000 títulos pagan 3,66 pb adicionales sobre un spread de 1 pb: el impacto es más de tres veces el coste que creías tener |
:::

## Ejemplo

Libro de un valor líquido:

| Nivel | Compra (precio, cantidad) | Venta (precio, cantidad) |
| --- | --- | --- |
| 1 | 50,00 y 1.200 | 50,01 y 900 |
| 2 | 49,99 y 3.000 | 50,02 y 2.500 |
| 3 | 49,98 y 6.000 | 50,03 y 4.000 |
| 4 | 49,97 y 9.000 | 50,04 y 8.000 |

- `bid` = 50,00, `ask` = 50,01, **spread = 0,01 EUR**.
- `mid` = 50,005; `spread_pb` = 0,01 / 50,005 · 10.000 = **2,0 pb**.
- Primer nivel: `Q_bid` = 1.200, `Q_ask` = 900, `imbalance` = (1.200 − 900) / 2.100 = **+0,143**.
- Tres primeros niveles: `Q_bid` = 10.200, `Q_ask` = 7.400, `imbalance` = **+0,159**. El
  desequilibrio se suaviza al mirar más profundo, que es lo que se suele hacer para quitar ruido.

Tu orden de compra a mercado de **10.000 acciones** recorre el libro: 900 a 50,01, 2.500 a 50,02,
4.000 a 50,03 y 2.600 a 50,04.

- Coste = 900 · 50,01 + 2.500 · 50,02 + 4.000 · 50,03 + 2.600 · 50,04 = 45.009 + 125.050 +
  200.120 + 130.104 = **500.283 EUR**.
- Precio medio = 500.283 / 10.000 = **50,0283 EUR**.
- Impacto frente al mejor ask: 50,0283 − 50,01 = **0,0183 EUR**, es decir **3,7 pb** adicionales.
- Coste total frente al mid: 10.000 · (50,0283 − 50,005) = **233 EUR**, o 4,66 pb sobre el mid.

Si partes la orden en cuatro envíos de 2.500 acciones espaciados, el impacto por envío es menor y
el precio medio mejora, pero asumes riesgo de que el precio se mueva entre envíos. Ahí está el
compromiso real de toda ejecución: rapidez contra precio.

## Código

```python verificable
# Leer el libro y calcular lo que de verdad cuesta una orden a mercado.
bids = [(50.00, 1200), (49.99, 3000), (49.98, 6000), (49.97, 9000)]
asks = [(50.01, 900), (50.02, 2500), (50.03, 4000), (50.04, 8000)]

bid, ask = bids[0][0], asks[0][0]
mid = (bid + ask) / 2

# Un solo nivel frente a tres: el desequilibrio cambia segun la profundidad mirada.
q_b1 = sum(q for _, q in bids[:1]); q_a1 = sum(q for _, q in asks[:1])
q_b3 = sum(q for _, q in bids[:3]); q_a3 = sum(q for _, q in asks[:3])

print("spread en pb :", round((ask - bid) / mid * 10000, 2))              # -> 2.0
print("imbalance 1  :", round((q_b1 - q_a1) / (q_b1 + q_a1), 4))          # -> 0.1429
print("imbalance 3  :", round((q_b3 - q_a3) / (q_b3 + q_a3), 4))          # -> 0.1591

def ejecutar(Q, niveles):
    """Recorre los niveles de arriba abajo: precio medio y cantidad sin ejecutar."""
    resta, gastado = Q, 0.0
    for precio, cantidad in niveles:
        usa = min(resta, cantidad)
        gastado += usa * precio
        resta -= usa
        if resta == 0:
            break
    ejecutado = Q - resta
    return gastado / ejecutado, resta

medio, resto = ejecutar(10000, asks)
print("precio medio :", round(medio, 4))                    # -> 50.0283
print("impacto en pb:", round((medio - ask) / mid * 10000, 2))   # -> 3.66
print("sin ejecutar :", resto)                              # -> 0
```

:::claves
- `bids[:1]` es una **lista con un elemento**; `bids[1]` sería la tupla del segundo nivel. Esa diferencia es la que hace que `imbalance` valga 0,1429 con un nivel y 0,1591 con tres, así que conviene tener claro si estás sumando niveles o mirando uno.
- `sum(q for _, q in bids[:1])` es una expresión generadora: recorre la lista una vez y no construye una lista intermedia. El `_` es la convención para «este valor no me interesa» (el precio), y no es una variable: no se puede usar después.
- `ejecutar` devuelve una **tupla** `(precio_medio, sin_ejecutar)`, por eso `precio_medio_compra(5000, asks)[1]` se queda con la parte no ejecutada en el bloque de la página de microestructura. Si imprimes la función entera verás `(50.0283, 0)` y parecerá una lista; lo idiomático es desempaquetar: `medio, resto = ejecutar(10000, asks)`.
- El denominador es `gastado / ejecutado`, no `gastado / Q`: con una orden parcial, `Q` incluye títulos que no se han ejecutado y el precio medio saldría falsamente bajo. Con 10.000 títulos no se nota porque `resta` vale 0; con 5.000 el error sería del 22 %.
- `usa = min(resta, cantidad)` es la línea que consume un nivel a medias: toma lo que queda de tu orden o lo que hay en el nivel, lo que sea menor. Cambiarla por `cantidad` haría que la orden se comiera más títulos de los que existen y el precio medio quedaría mal **sin lanzar ningún error**.
- `round(medio, 4)` se aplica solo al imprimir. Si en vez de imprimir sigues calculando con el número redondeado, el impacto en puntos básicos se desvía: `(medio − ask)/mid · 10000` con 4 decimales de margen da 3,66 pb, y redondeando antes de dividir puedes obtener 3,60 o 3,80 según el caso.
:::

```python ilustrativo
# El desequilibrio como senal: hay que medirlo antes de creerselo.
# Un backtest honesto necesita el libro con marcas de tiempo y el retardo real
# entre verlo y poder actuar; sin eso, el resultado es ficcion.

def revision_imbalance(libro, retardo_ms, umbral=0.3):
    """Idea a validar: imbalance alto -> el mid sube en los proximos X ms."""
    q_bid = sum(q for _, q in libro["bids"][:5])
    q_ask = sum(q for _, q in libro["asks"][:5])
    imbalance = (q_bid - q_ask) / (q_bid + q_ask)
    if abs(imbalance) < umbral:
        return "sin senal"
    return "senal de compra" if imbalance > 0 else "senal de venta"

libro = {"bids": [(50.00, 1200), (49.99, 3000)], "asks": [(50.01, 200), (50.02, 300)]}
print(revision_imbalance(libro, retardo_ms=50))
```

## Errores típicos

- **Mirar solo el diferencial.** Un spread de 1 pb con 200 acciones en el mejor nivel es peor que
  uno de 3 pb con 10.000. Lo que importa es el coste de ejecutar **tu** tamaño, no el de una
  acción.
- **Confundir el mid con un precio operable.** El mid es una referencia estadística. Si compras,
  pagas el ask; si vendes, cobras el bid. Nadie te da el punto medio.
- **Tomar una foto del libro como si fuera el libro.** Lo que ves es un instante, a menudo
  agregado con retardo. Los tamaños que aparecen y desaparecen sin ejecutarse son órdenes
  retiradas: señalan intención, no compromiso.
- **Operar contra órdenes ocultas.** Una orden iceberg muestra una fracción de su tamaño. Si tu
  modelo asume que lo visible es todo lo que hay, subestimarás el impacto exactamente cuando más
  importa.
- **Usar el desequilibrio instantáneo como predictor en una estrategia lenta.** La información
  del libro caduca en segundos. Si tu sistema decide una vez al día, el imbalance de las 10:00 no
  dice nada sobre el cierre.
- **Ignorar la selección adversa al proveer liquidez.** Si tus órdenes límite se ejecutan justo
  antes de que el precio siga en tu contra, tu diferencial realizado es peor que el cotizado.
  Medirlo exige comparar con el mid posterior, no con el del momento.

:::practica
enunciado: Libro con bid 30,00 y ask 30,02, mid 30,01. Compras 4.000 acciones a mercado: 1.500 se ejecutan a 30,02 y 2.500 a 30,03. Calcula el precio medio, el diferencial efectivo en puntos básicos y compáralo con el cotizado.
pista: El efectivo compara tu precio con el mid anterior y se multiplica por dos, porque mide la distancia en ambas direcciones.
solucion: Coste: 1.500 · 30,02 + 2.500 · 30,03 = 45.030 + 75.075 = 120.105 EUR; el precio medio, 120.105 / 4.000 = 30,02625. Diferencial efectivo: 2 · (30,02625 − 30,01) = 0,0325 EUR por acción, 0,0325 / 30,01 · 10.000 = 10,83 pb sobre el mid. El cotizado era 0,02 / 30,01 · 10.000 = 6,66 pb: pagas 65 EUR más que el mid (4.000 · 0,01625) porque tu orden cruza dos niveles.
:::

## Comprueba que lo sabes

:::quiz
p: Un libro tiene 50,00 x 1.200 en compra y 50,01 x 900 en venta. ¿Cual es el desequilibrio de los primeros niveles?
o: +0,143, porque hay más cantidad en el lado de compra
o: 2,0 pb, porque es la distancia entre los dos mejores precios
o: 0, porque el spread es de un centimo
a: 1
e: El desequilibrio es (Q_bid - Q_ask) / (Q_bid + Q_ask) = (1.200 - 900) / 2.100 = +0,143. Los 2 pb son el spread en puntos básicos, que mide el coste de cruzar y no la asimetria del libro.
:::

:::quiz
p: Compras 10.000 acciones a mercado en un libro con 900 acciones a 50,01, 2.500 a 50,02, 4.000 a 50,03 y 2.600 a 50,04. ¿Que precio medio pagas?
o: 50,01, el mejor precio de venta
o: 50,0283, porque recorres cuatro niveles
o: 50,005, el punto medio del libro
a: 2
e: La orden consume los cuatro niveles y el coste total es 500.283 EUR para 10.000 acciones, es decir 50,0283 de media. El mejor ask solo vale para las primeras 900 acciones y el mid no es un precio al que nadie te venda.
:::

:::trampa
Cuando alguien te enseña una señal de desequilibrio del libro con un backtest, pregúntale dos
cosas: si el libro incluye todas las órdenes o solo las visibles, y cuántos milisegundos pasan
entre ver el libro y enviar la orden. Sin esas dos respuestas, el resultado no es una señal: es
una ilusión construida con datos que en la práctica llegaban tarde o incompletos.
:::
