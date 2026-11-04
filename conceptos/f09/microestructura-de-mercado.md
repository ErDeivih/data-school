---
id: microestructura-de-mercado
titulo: Microestructura de mercado
fase: 9
nivel: avanzado
rutas: [quant]
prerequisitos: [que-es-un-mercado]
tags: [microestructura, ejecución, órdenes, costes]
resumen: Como se casan las órdenes, quién asume el riesgo de inventario y por qué esa mecánica decide si tu estrategia es viable o solo bonita en papel.
fuentes: ["Harris (2003), 'Trading and Exchanges: Market Microstructure for Practitioners'", "O'Hara (1995), 'Market Microstructure Theory'"]
---

## En una frase

La microestructura es el conjunto de reglas con las que las órdenes se convierten en
operaciones: tipos de orden, prioridad de precio y tiempo, quien cotiza, donde está el libro y
cuánto cuesta cruzar, y todo eso determina tu coste real de entrar y salir.

## La idea

Vuelve al mercadillo, pero ahora fíjate en el puesto de naranjas. El vendedor tiene un cartel:
«vendo a 1,20; compro a 1,15». No sabe si hoy vendrá alguien a comprarle o alguien a venderle,
así que cotiza los dos lados y espera. Si le compras, te quedas las naranjas y él se queda con
1,20; si le vendes las tuyas, te da 1,15. Ese margen de 5 centavos es su sueldo por estar ahí,
con fruta en el puesto, dispuesto a operar en cualquier momento.

La microestructura estudia exactamente eso: cómo se organiza ese puesto, quien pone los carteles,
en qué orden se atiende a los clientes y qué pasa cuando llega un camión entero a comprar. No es
un tema académico: es la diferencia entre un backtest que gana un 20 % y una cuenta que pierde
dinero con el mismo sistema.

Cinco piezas que hay que entender:

1. **Tipos de orden.** La orden a **mercado** se ejecuta ya, al precio que haya; garantiza la
   ejecución y no el precio. La orden **límite** fija un precio máximo de compra o mínimo de
   venta; garantiza el precio y no la ejecución. Hay variantes: por lo mejor, stop, iceberg
   (oculta parte del tamaño), todo o nada, y las que solo son válidas en la subasta.
2. **Prioridad precio-tiempo.** A mejor precio, antes; a igual precio, quien llegó antes. De ahí
   que la **posición en la cola** valga dinero: dos órdenes límite idénticas no son equivalentes
   si una lleva esperando desde las 9:00 y la otra acaba de llegar.
3. **Quién provee liquidez.** El creador de mercado cotiza los dos lados y asume el riesgo de
   inventario; el operador que cruza el diferencial **consume** liquidez y paga por ello. Las
   tarifas suelen distinguir ambos papeles: en muchos mercados, quien pone la orden límite paga
   menos comisión (o recibe un pequeño reembolso) y quien la cruza paga más.
4. **Dónde vive el libro.** Un mismo activo puede negociarse en varios centros a la vez. Esa
   fragmentación obliga a agregar libros para saber cuál es el mejor precio disponible, y crea
   oportunidades para quien ve el conjunto antes que los demás.
5. **Selección adversa.** Si el creador de mercado te vende y un segundo después el precio sube,
   probablemente sabías algo que él no. Ese riesgo es la razón de que el diferencial no sea más
   pequeño y de que se ensanche cuando hay noticias o volatilidad.

La consecuencia para ti es una sola frase: **tu estrategia no compite contra el gráfico, compite
contra otros participantes por el mismo flujo de órdenes**. Si tu ventaja es más pequeña que el
coste de capturarla, no hay ventaja.

:::aviso
La orden a mercado no tiene precio garantizado. En un libro fino, una orden grande puede
recorrer varios niveles y ejecutarse a un precio medio bastante peor que el mejor del libro.
Eso no es un fallo del bróker: es como funciona un libro de órdenes.
:::

:::figura
fichero: microestructura-libro-e-impacto
pie: A la izquierda, el libro del ejemplo nivel a nivel: en azul lo que espera a comprar, en naranja lo que espera a vender y en rojo los dos niveles que se lleva una orden a mercado de 800 títulos. Fíjate en que el spread es de 1 pb, así que parece un mercado barato, y en que el primer nivel de venta solo tiene 300 títulos. A la derecha, el precio medio que pagas según el tamaño: 800 títulos cuestan 0,63 pb sobre el mejor ask, y a partir de 4.100 el libro se agota y quedan órdenes sin ejecutar. Conclusión: el diferencial que ves en la pantalla no es tu coste; tu coste es el recorrido que hace **tu** tamaño por el libro.
fuente: figuras/microestructura-de-mercado-1.py
:::

## Definición formal

El estado del libro en un instante se resume con el mejor precio de cada lado y las cantidades
disponibles:

:::formula
bid = max(B)     ask = min(A)     spread = ask - bid     mid = (bid + ask) / 2
:::

- `B`, `A` — conjuntos de órdenes de compra y de venta, cada una con su precio y su cantidad.
- `bid` — el precio más alto al que alguien está dispuesto a comprar ahora.
- `ask` — el precio más bajo al que alguien está dispuesto a vender ahora.
- `spread` — el diferencial: lo que cuesta cruzar de inmediato, en unidades de precio.
- `mid` — el punto medio; se usa como referencia del precio, pero no es operable: nadie te
  vende al mid.

El coste de una orden a mercado de tamaño `Q` sale de recorrer el libro nivel a nivel:

:::formula
precio_medio(Q) = ( suma sobre los niveles consumidos de p_k · q_k ) / Q
:::

- `p_k`, `q_k` — precio y cantidad del nivel k del lado contrario.
- `Q` — el tamaño total de tu orden. Si `Q` supera lo disponible, la orden no se ejecuta entera.
- **impacto** — la diferencia entre `precio_medio(Q)` y el mejor precio del libro al empezar.

Y una medida que se usa como señal, el desequilibrio del libro:

:::formula
imbalance = ( q_bid - q_ask ) / ( q_bid + q_ask )
:::

- `q_bid` — cantidad agregada en el lado de compra (los primeros niveles).
- `q_ask` — cantidad agregada en el lado de venta.
- `imbalance` — entre −1 y +1. Positivo significa que hay más presión de compra en el libro.
  Es una señal débil y muy ruidosa: sirve como variable más, nunca como oráculo.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `Q` | El tamaño total de tu orden a mercado | títulos | Es el parámetro que más cambia el resultado: al crecer, el precio medio se aleja del mejor precio y, si supera lo que hay en el libro, la orden queda **parcialmente** sin ejecutar. No hay forma de cruzar más de lo que hay |
| `p_k`, `q_k` | El precio y la cantidad de cada nivel que consumes | EUR y títulos | Los niveles con mucha cantidad amortiguan el impacto; los finos obligan a bajar (o subir) al siguiente precio. La fórmula pondera cada precio por su cantidad, así que un nivel grande pesa más en la media |
| `precio_medio(Q)` | El precio medio al que se ejecuta realmente una orden a mercado de tamaño `Q` | EUR por título | Con `Q` pequeño se parece al mejor precio del libro; con `Q` grande se acerca al peor nivel tocado. Es lo que debes usar en un backtest en lugar del precio de la última operación |
| `impacto` | La diferencia entre ese precio medio y el mejor precio del libro al empezar | EUR por título (o puntos básicos) | Crece con el tamaño y con la prisa, y es lo que un backtest que opera al cierre ignora. Medirlo permite saber qué tamaño admite tu estrategia antes de que el coste se coma la ventaja |
| `spread` | La distancia entre el mejor bid y el mejor ask | EUR por título | Es el coste de la inmediatez: cruzarlo es instantáneo y gratuito solo en apariencia. Se ensancha con la volatilidad, en la apertura y al cierre, justo cuando más gente quiere operar |
| `mid` | El punto medio entre bid y ask | EUR por título | Es una referencia estadística, no un precio al que puedas operar: si compras pagas el ask y si vendes cobras el bid. Sirve para normalizar costes entre activos de precios muy distintos |
| `q_bid`, `q_ask` | La cantidad agregada visible en los primeros niveles de cada lado | títulos | Al mirar más niveles, `imbalance` se suaviza porque el ruido de los primeros se diluye. Un desequilibrio grande con poca cantidad total no significa nada |
| `imbalance` | El desequilibrio del libro, normalizado entre −1 y +1 | adimensional | Positivo indica más presión de compra visible; negativo, de venta. Es una señal débil, muy dependiente de la latencia y solo de lo **visible**: las órdenes iceberg y las ocultas no aparecen |
:::

## Ejemplo

Este es el libro de un valor, con los cuatro mejores niveles de cada lado:

| Nivel | Compra (precio, cantidad) | Venta (precio, cantidad) |
| --- | --- | --- |
| 1 | 100,00 y 400 | 100,01 y 300 |
| 2 | 99,99 y 700 | 100,02 y 600 |
| 3 | 99,98 y 900 | 100,03 y 1.200 |
| 4 | 99,97 y 1.500 | 100,04 y 2.000 |

Cálculos básicos:

- `bid` = 100,00 y `ask` = 100,01; **spread = 0,01 EUR**.
- `mid` = (100,00 + 100,01) / 2 = **100,005 EUR**.
- Spread en puntos básicos sobre el mid: 0,01 / 100,005 = **1,0 pb**. Es un valor líquido.
- Profundidad total mostrada: 3.500 títulos en compra y 4.100 en venta.
- `imbalance` = (400 − 300) / (400 + 300) = **+0,143**, presión de compra leve.

Tu orden a mercado de **800 acciones** se ejecuta así: 300 a 100,01 y 500 a 100,02.

- Coste total = 300 · 100,01 + 500 · 100,02 = 30.003 + 50.010 = **80.013 EUR**.
- Precio medio = 80.013 / 800 = **100,01625 EUR**.
- Coste respecto al mejor precio del libro: 800 · (100,01625 − 100,01) = **5 EUR** de impacto,
  más los 800 · 0,005 = 4 EUR que ya pagas por cruzar medio diferencial desde el mid.
- Con una orden de **5.000 acciones** solo hay 4.100 en el libro: se ejecutarían 4.100 y
  quedarían **900 sin ejecutar**. Eso es una orden parcial, no un error.

Si en lugar de cruzar hubieras puesto una límite de compra a 100,00, tendrías mejor precio pero
esperarías en la cola detrás de las 400 acciones que ya están a ese precio. Si el precio sube sin
ejecutarte, no has perdido dinero: has perdido la operación, que a veces es peor.

## Código

```python verificable
# Recorrer el libro para saber a que precio se ejecuta de verdad una orden a mercado.
bids = [(100.00, 400), (99.99, 700), (99.98, 900), (99.97, 1500)]
asks = [(100.01, 300), (100.02, 600), (100.03, 1200), (100.04, 2000)]

bid, ask = bids[0][0], asks[0][0]
mid = (bid + ask) / 2
q_bid, q_ask = bids[0][1], asks[0][1]

print("spread            :", round(ask - bid, 4))            # -> 0.01
print("mid               :", round(mid, 4))                  # -> 100.005
print("spread en pb      :", round((ask - bid) / mid * 10000, 3))   # -> 1.0
print("desequilibrio     :", round((q_bid - q_ask) / (q_bid + q_ask), 4))   # -> 0.1429

def precio_medio_compra(Q, niveles):
    """Consume niveles de venta de arriba a abajo y devuelve (precio medio, sin ejecutar)."""
    resta, gastado = Q, 0.0
    for precio, cantidad in niveles:
        usa = min(resta, cantidad)
        gastado += usa * precio
        resta -= usa
        if resta == 0:
            break
    return gastado / (Q - resta), resta

medio, resto = precio_medio_compra(800, asks)
print("precio medio 800  :", round(medio, 5))     # -> 100.01625
print("impacto en euros  :", round(800 * (medio - ask), 2))   # -> 5.0
print("sin ejecutar 5000 :", precio_medio_compra(5000, asks)[1])   # -> 900
```

:::claves
- `bids` y `asks` son **listas de tuplas**, no arrays de NumPy: cada elemento mezcla un precio decimal con una cantidad entera. Por eso lo que recorre el libro es un bucle de Python y no una operación vectorizada, y por eso `sum(q for _, q in bids[:1])` necesita el guion bajo: está tirando el precio y quedándose con la cantidad.
- `bids[:1]` es una lista con **un** elemento (el nivel 1), mientras que `bids[1]` sería una tupla y `bids[:3]` los tres primeros. Ese off-by-one es el que explica que el desequilibrio del ejemplo pase de 0,1429 (un nivel) a 0,1591 (tres).
- `precio_medio_compra` devuelve una **tupla** `(precio, sin_ejecutar)`, y `[1]` toma el segundo elemento. Si imprimes la función sin índice verás `(100.01625, 0)` y creerás que devuelve una lista; para usarla bien se desempaqueta: `medio, resto = precio_medio_compra(800, asks)`.
- El denominador es `gastado / (Q - resta)`, no `gastado / Q`. En una orden parcial `Q` incluye títulos que **no** se han ejecutado, así que dividir por `Q` daría un precio medio falsamente bajo. Con `Q = 800` no se nota porque `resta` vale 0; con 5.000 el error es del 22 %.
- `usa = min(resta, cantidad)` es la línea que hace que un nivel se consuma a medias: toma lo que queda de tu orden o lo que hay en el nivel, lo que sea menor. Cambiar ese `min` por la cantidad entera ejecutaría más títulos de los que hay en el libro y el precio medio saldría mal sin dar ningún error.
- `round(medio, 5)` redondea a cinco decimales porque el precio medio de una orden que cruza niveles tiene muchos más. Para imprimir no hace falta redondear: `print("%.5f" % medio)` te da el mismo texto sin tocar el número que usarás en los cálculos siguientes.
:::

```python ilustrativo
# Lo que un backtest suele ignorar: la cola y el tiempo de espera de una limite.
# Una simulacion realista necesita el libro completo con marcas de tiempo,
# no solo el ultimo precio, porque la ejecucion depende de la posicion en la cola.

estado = {
    "orden": {"lado": "compra", "precio": 100.00, "cantidad": 400},
    "cola_por_delante": 400,      # acciones que llegaron antes a ese precio
    "libro": {"bid": 100.00, "ask": 100.01},
}

# Solo se ejecuta si el precio cruza y la cola de delante se agota primero.
if estado["libro"]["ask"] <= estado["orden"]["precio"]:
    print("se ejecuta solo si la cola de delante se agota")
else:
    print("la orden espera; no hay garantia de ejecucion")
```

## Errores típicos

- **Modelar la ejecución con el precio de cierre.** Los backtests que compran y venden al cierre
  del día ignoran el diferencial, la cola y el impacto. En un sistema de alta frecuencia ese error
  se come cualquier ventaja; incluso en uno diario falsea el resultado.
- **Asumir que tu orden límite se ejecuta siempre.** Si el precio toca tu nivel, no significa que
  tu orden se haya ejecutado: hay una cola delante. En la vida real, la orden que toca el precio
  de la última operación puede quedarse sin cruzar.
- **Ignorar la fragmentación.** Un activo cotiza en varios centros. El mejor precio puede estar
  en otro sitio, y las reglas de enrutamiento de tu bróker deciden donde va tu orden. Sin datos
  agregados, tu visión del libro está incompleta.
- **Tratar la liquidez como constante.** El diferencial se ensancha con la volatilidad, en la
  apertura, al cierre y cuando hay noticias. Un backtest con un coste fijo de 1 pb sobre un valor
  que en tus horas de operación tiene 5 pb está midiendo otra cosa.
- **Confundir volumen negociado con liquidez disponible.** El volumen es historia; la liquidez es
  lo que hay ahora en el libro. Un valor puede haber negociado mucho hoy y tener un libro vacío
  en este instante.
- **Usar el desequilibrio del libro como señal predictiva sin medirlo.** Es una variable con
  información, pero débil y muy dependiente de la latencia: cuando tú reaccionas, el libro ya ha
  cambiado. Si no has medido su capacidad predictiva con datos propios, no la uses.

:::practica
enunciado: Un valor cotiza bid 75,20 y ask 75,21. La compra tiene 600 a 75,20, 1.400 a 75,19 y 2.000 a 75,18. Envías una venta a mercado de 2.500 acciones: ¿a qué precio medio vendes y cuánto te cuesta el impacto, en euros y en puntos básicos sobre el mid?
pista: El precio medio sale de repartir el importe total entre los títulos, y el impacto se mide contra el mejor bid y contra el mid.
solucion: Vendes 600 a 75,20 (45.120), 1.400 a 75,19 (105.266) y 500 a 75,18 (37.590): 187.976 EUR por 2.500 acciones, precio medio 75,1904. Frente al mejor bid pierdes 75,20 − 75,1904 = 0,0096 EUR por acción, 24 EUR en total. El mid es 75,205, así que el impacto son 0,0096 / 75,205 · 10.000 = 1,28 pb, del orden del propio diferencial.
:::

## Comprueba que lo sabes

:::quiz
p: Con el libro del ejemplo (compra 100,00 x 400 y venta 100,01 x 300), envias una orden a mercado de 800 acciones. ¿A que precio medio se ejecuta?
o: A 100,01, porque es el mejor precio de venta disponible
o: A 100,01625, porque consume 300 a 100,01 y 500 a 100,02
o: A 100,005, el punto medio entre los dos mejores precios
a: 2
e: La orden a mercado recorre el libro: primero las 300 acciones a 100,01 y después 500 a 100,02. El coste total es 80.013 EUR para 800 acciones, es decir 100,01625 de media. El mid (100,005) no es un precio operable y 100,01 solo valdria para las primeras 300 acciones.
:::

:::quiz
p: ¿Por que dos órdenes límite idénticas, al mismo precio y en el mismo lado, no valen lo mismo?
o: Porque la más antigua tiene prioridad en la cola y se ejecuta antes
o: Porque la más reciente paga menos comisión
o: Porque el bróker ejecuta primero las órdenes más grandes
a: 1
e: La prioridad es precio y luego tiempo: a igual precio, la orden que llegó antes está delante en la cola y se ejecuta primero. Con la misma cantidad delante y poco volumen, la que llega después puede no ejecutarse en absoluto. De ahi que la posición en la cola tenga valor económico.
:::

:::trampa
Si tu estrategia gana menos de dos veces el coste de ida y vuelta, el resultado depende más de
tu ejecución que de tu idea. Antes de optimizar la señal, mide el coste con datos reales de tu
mercado y en tus horas de operación: apertura, cierre y horas valle tienen diferenciales muy
distintos.
:::
