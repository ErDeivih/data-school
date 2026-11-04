---
id: algoritmos-de-ejecucion
titulo: Algoritmos de ejecución: VWAP, TWAP e iceberg
fase: 9
nivel: avanzado
rutas: [quant]
prerequisitos: [latencia-y-ejecucion, order-book-y-spread, slippage-y-comisiones, microestructura-de-mercado]
tags: [ejecucion, microestructura, algoritmos, costes]
resumen: Cómo partir una orden grande en trozos para que no la vea el mercado, y cómo cada algoritmo cambia lo que pagas por el mismo pedido.
fuentes: ["Johnson (2010), 'Algorithmic Trading and DMA: An Introduction to Direct Access Trading Strategies'", "Harris (2003), 'Trading and Exchanges: Market Microstructure for Practitioners'", "Almgren y Chriss (2001), 'Optimal Execution of Portfolio Transactions'"]
---

## En una frase

Un algoritmo de ejecución decide **cuándo y cuánto** mandar de cada trozo de una orden grande,
y la elección entre TWAP, VWAP o iceberg no cambia lo que quieres comprar: cambia lo que
acabas pagando por ello.

## La idea

Cuando quieres comprar 500.000 acciones, el problema no es el precio de la acción: es que tu
propia orden es el mercado. Si la mandas entera, te llenas a precios cada vez peores porque vas
agotando los niveles del libro, y además enseñas tu intención a todo el mundo. Ese coste tiene
nombre: [[slippage-y-comisiones|deslizamiento]], y en órdenes grandes suele pesar más que la
comisión entera.

La solución es trocear. Y en cuanto troceas aparece la única pregunta que importa: **¿a qué
ritmo?**. Tres respuestas clásicas:

- **TWAP** (*time weighted average price*): partes el pedido en trozos iguales y mandas uno cada
  intervalo fijo. Vas a piñón: cada diez minutos, la misma cantidad. Es lo más simple y lo más
  robusto, y funciona bien en valores líquidos donde el volumen no cambia demasiado a lo largo
  del día.
- **VWAP** (*volume weighted average price*): repartes el pedido siguiendo el volumen que el
  mercado negocia. Si a las 10:00 se cruza el triple de volumen que a las 13:00, mandas el triple
  de acciones. Así tu porcentaje de participación es más o menos constante en lugar de dispararse
  en los momentos de poca liquidez. El precio medio del día ponderado por volumen es lo que se
  usa como referencia de calidad: se mide en puntos básicos de desviación contra el VWAP del
  mercado.
- **Iceberg**: no reparte en el tiempo, reparte en **visibilidad**. La orden vive en el libro con
  un tamaño pequeño a la vista y el resto escondido; cuando se ejecuta la parte visible, aparece
  otra punta en la misma cola. Sirve para acumular posiciones limitadas sin decir cuánto quieres.

El perfil de volumen intradía tiene forma de U: la primera hora y la última concentran una parte
desproporcionada del volumen del día, y el valle está a mediodía. Eso hace que TWAP y VWAP no
sean intercambiables. Un TWAP de 39 trozos manda el 2,56 % en cada uno, y a mediodía ese 2,56 %
puede ser una porción enorme del volumen que se está negociando en ese momento; un VWAP reduce
la rodaja justo ahí y la engorda en el cierre. La diferencia es [[order-book-y-spread|impacto en
el libro]] puro y duro.

:::figura
fichero: algoritmos-de-ejecucion-perfil-y-ritmo
pie: Izquierda, el perfil de volumen de una sesión: forma de U con un valle a mediodía y un pico en la subasta de cierre. Las rodajas de TWAP son todas iguales (línea de puntos); las de VWAP siguen el volumen (puntos rojos). Derecha, el mismo pedido acumulado: TWAP es una recta y VWAP se adelanta en la apertura, se frena a mediodía y vuelve a cargar al final. La zona sombreada es cuánto se separan los dos ritmos, hasta once puntos del pedido.
fuente: figuras/algoritmos-de-ejecucion-1.py
:::

Todos los algoritmos comparten dos límites que se ponen en los parámetros, no en la idea:

1. **Participación máxima.** «Nunca más del 10 % del volumen que se negocia en ese intervalo».
   Es la defensa contra el impacto: si tu trozo es demasiado grande respecto al flujo, el precio
   se mueve antes de que termines.
2. **Precio límite.** «No pagues más de 101,20». Convierte el algoritmo de agresivo en paciente:
   si el mercado se va, tu orden deja de ejecutarse y te quedas con la posición a medias. Eso
   también es un riesgo, y hay que decidir de antemano cuánto tiempo se persigue el precio.

Y un detalle que cambia la decisión: el benchmark. Si te miden contra el precio de cierre, VWAP
no te sirve de nada; si te miden contra el VWAP del día, un TWAP te va a dejar siempre con una
desviación sistemática. El algoritmo se elige contra la referencia con la que te van a juzgar,
no al revés.

## Definición formal

Con `Q` el tamaño total del pedido, repartido en `n` intervalos con una fracción `w_i` en cada
uno, el trozo que se manda en el intervalo `i` es:

:::formula
q_i = Q · w_i        con        Σ w_i = 1
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `Q` | Tamaño total del pedido que hay que ejecutar | acciones o contratos | Más impacto y más tiempo: el mismo ritmo mueve más el precio en contra |
| `n` | Número de intervalos en los que se parte la ejecución | unidades | Rodajas más pequeñas y menos impacto por trozo, pero más comisiones fijas y más tiempo expuesto al mercado |
| `w_i` | Fracción del pedido que se manda en el intervalo `i` | tanto por uno, suma 1 | Reparte el peso: un `w_i` alto en una franja de poco volumen es justo lo que dispara el precio |
| `q_i` | Cantidad que se manda en el intervalo `i` | acciones o contratos | Es la decisión real del algoritmo; en TWAP vale `Q / n` para todo `i` |
| `V_i` | Volumen que el mercado negocia en el intervalo `i` | acciones o contratos | Más volumen admite más cantidad sin mover el precio: por eso VWAP lo sigue |
| `part_i` | Participación: tu trozo dividido entre el volumen del intervalo | % | Por encima del 10-20 % el impacto deja de ser despreciable y el relleno se vuelve lento |
| `P_i` | Precio medio al que se ejecuta tu trozo del intervalo `i` | EUR por acción | Es lo que se compara con el benchmark para medir la calidad |
| `VWAP` | Precio medio del periodo ponderado por volumen negociado | EUR por acción | El listón: por debajo compraste mejor que el mercado, por encima pagaste tu propia prisa |
| `IS` | Coste de implementación: lo que pagaste de más frente a un precio de referencia | puntos básicos | Es la métrica con la que se juzga la ejecución; se calcula como el signo del lado por la diferencia entre el precio ejecutado y el de referencia, dividida entre el de referencia |

:::

TWAP es el caso `w_i = 1 / n` para todo `i`. VWAP es el caso `w_i = V_i / Σ V_j`, es decir, la
fracción de volumen que el mercado negoció en ese intervalo. Con esa elección, `part_i = Q · w_i
/ V_i` se mantiene constante a lo largo del día, que es exactamente lo que se busca: participación
estable en vez de a golpes.

Y la restricción que convierte el problema en algo con solución única, el **impacto temporal**:
mover el precio cuesta, y esperar también. Repartir más fino reduce el impacto pero alarga la
exposición. El modelo clásico lo escribe como la suma de dos términos que crecen en direcciones
opuestas:

:::formula
coste_total ≈ impacto_temporal · (Q / n) + riesgo_de_precio · n · Δt
:::

- `impacto_temporal` — cuánto se mueve el precio por cada unidad de cantidad que mandas de golpe:
  sube con `Q / n`, el tamaño de cada rodaja.
- `riesgo_de_precio` — cuánto se mueve el precio por unidad de tiempo, multiplicado por la
  volatilidad del valor y por el tiempo total que estás expuesto.
- `Δt` — duración de cada intervalo. Alargar el horizonte total (`n · Δt`) reduce el impacto por
  rodaja, pero te deja más tiempo con la posición a medias y el mercado moviéndose.

Ese compromiso es el motivo de que existan los algoritmos «adaptativos»: fijan un nivel de
urgencia y van decidiendo el ritmo. Un algoritmo con `w_i` demasiado agresivo al principio es un
algoritmo que paga prisa; uno demasiado pasivo al final es un algoritmo que acaba comprando de
golpe en el cierre, que es justo el momento más caro del día.

## Ejemplo

Quieres comprar 50.000 acciones y quedan cinco tramos de diez minutos. El volumen que el mercado
negoció en cada tramo, calculado de un perfil en U:

| Tramo | Volumen del mercado (acciones) | `w_i` sin límite | Rodaja `q_i` (acciones) |
| --- | --- | --- | --- |
| 1 (apertura) | 430.000 | 0,297 | 14.850 |
| 2 | 150.000 | 0,103 | 5.150 |
| 3 (mediodía) | 100.000 | 0,069 | 3.450 |
| 4 | 150.000 | 0,103 | 5.150 |
| 5 (cierre) | 620.000 | 0,428 | 21.400 |
| Total | 1.450.000 | 1,000 | 50.000 |

Con un límite de participación del 5 %, ninguna rodaja puede pasar de `0,05 · V_i`:

- Tramo 1: el 5 % de 430.000 son 21.500, y la rodaja pedía 14.850. Se ejecuta entera, con una
  participación del 3,45 %.
- Tramo 3: el 5 % de 100.000 son 5.000, y la rodaja pedía 3.450. También entra, con el 3,45 %.
- Tramo 5: el 5 % de 620.000 son 31.000, así que la rodaja de 21.400 entra sin problema.

Los pesos sin límite ya dejan la participación constante en el 3,45 % —`50.000 / 1.450.000`—,
que es la propiedad que define a VWAP. Ahora compara con TWAP: el mismo pedido en cinco rodajas
de 10.000 acciones daría una participación del 2,33 % en la apertura, del 10 % a mediodía (el
doble que VWAP) y del 1,61 % en el cierre. La rodaja del mediodía es la que paga el impacto: te
estás llevando una de cada diez acciones que se negocian en la franja con menos liquidez del día.

Y si el tramo 3 fuese aún más seco —50.000 acciones negociadas—, el 5 % serían 2.500 acciones,
menos que las 3.450 que el algoritmo quiere mandar. Entonces el trozo se recorta, se acumula el
sobrante y hay que decidir qué hacer con él: arrastrarlo al siguiente tramo (y arriesgarse a
concentrar el pedido al final) o alargar el horizonte de ejecución. Ese sobrante es el motivo de
que casi ningún VWAP acabe exactamente en el VWAP del mercado.

## Código

```python verificable
# Reparto VWAP sobre un perfil de volumen con forma de U, con limite de participacion
Q = 50_000                          # acciones que hay que comprar
tramos = [430_000, 150_000, 100_000, 150_000, 620_000]   # volumen del mercado por tramo
LIMITE = 0.05                       # nunca mas del 5 % del volumen del tramo

total = sum(tramos)
enviado = []
for i, volumen in enumerate(tramos, start=1):
    rodaja = Q * volumen / total    # peso proporcional al volumen: la definicion de VWAP
    tope = LIMITE * volumen
    real = min(rodaja, tope)
    enviado.append(real)
    print(f"tramo {i}: pediria {rodaja:>7.0f}, tope {tope:>7.0f}, manda {real:>7.0f} "
          f"({real / volumen:.2%} del volumen)")
# -> tramo 1: pediria   14828, tope   21500, manda   14828 (3.45% del volumen)
# -> tramo 2: pediria    5172, tope    7500, manda    5172 (3.45% del volumen)
# -> tramo 3: pediria    3448, tope    5000, manda    3448 (3.45% del volumen)
# -> tramo 4: pediria    5172, tope    7500, manda    5172 (3.45% del volumen)
# -> tramo 5: pediria   21379, tope   31000, manda   21379 (3.45% del volumen)
print(f"total enviado: {sum(enviado):.0f} de {Q}  (falta {Q - sum(enviado):.0f})")
# -> total enviado: 50000 de 50000  (falta 0)
```

:::claves
- `Q * volumen / total` es la definición de VWAP en una línea: el peso de cada tramo es su
  fracción del volumen total. Si en vez de `volumen` pones `1`, te sale TWAP.
- La participación sale siempre la misma (3,45 % = `Q / total`) **siempre que no actúe el tope**.
  Eso no es casualidad: es la propiedad que hace que VWAP y participación constante sean la misma
  cosa. Cuando el tope recorta un tramo, la igualdad se rompe y el pedido se queda corto.
- `min(rodaja, tope)` no reparte el sobrante a los demás tramos. Ese reparto es lo que hace un
  algoritmo real y lo que hay que añadir a mano; sin él, el total no se ejecuta.
- Las cifras salen con decimales y aquí se imprimen redondeadas con `:.0f`: el pedido real es
  14.827,59 acciones del tramo 1 y redondear cada trozo por separado deja unas pocas acciones
  sueltas. En producción se redondea a lote entero y el residuo se cuenta aparte.
- `f"{real / volumen:.2%}"` da el porcentaje con dos decimales y el signo `%`; el valor que se
  formatea es un tanto por uno, no un porcentaje.
:::

```python verificable
# Cuanto cuesta la prisa: el mismo pedido contra dos libros distintos
# Cada libro es una lista de (precio, acciones disponibles); hay que comprar 1.000.
libro_con_prisa = [(100.00, 400), (100.02, 400), (100.05, 500), (100.10, 800)]
libro_paciente = [(100.00, 800), (100.02, 200), (100.05, 500), (100.10, 800)]
pedido = 1_000

def coste_medio(libro):
    """Precio medio de comprar `pedido` acciones agotando niveles del libro."""
    resta, gastado, compradas = pedido, 0.0, 0
    for precio, tamano in libro:
        toma = min(resta, tamano)
        gastado += toma * precio
        compradas += toma
        resta -= toma
    return gastado / compradas, compradas

prisa, n1 = coste_medio(libro_con_prisa)
paciente, n2 = coste_medio(libro_paciente)

print(f"con prisa: {n1} acciones a {prisa:.4f} EUR")
# -> con prisa: 1000 acciones a 100.0180 EUR
print(f"paciente:  {n2} acciones a {paciente:.4f} EUR")
# -> paciente:  1000 acciones a 100.0040 EUR
print(f"diferencia: {(prisa - paciente) * pedido:.2f} EUR en 1.000 acciones")
# -> diferencia: 14.00 EUR en 1.000 acciones
```

```text
Como se elige el algoritmo: no es gusto, es el benchmark
lo que te miden               | lo que encaja          | lo que NO encaja
VWAP del dia                  | VWAP                   | TWAP (desviacion sistematica)
precio de cierre              | al cierre / MOC        | VWAP (llegas al cierre con sobrante)
precio de llegada (arrival)   | lo mas rapido posible  | TWAP (te quedas expuesto)
sin benchmark explicito       | POC / participacion    | cualquiera sin limite de participacion
acumular sin senalar          | iceberg (limite)       | market (ensena el tamano y el precio)
```

## Errores típicos

- **Elegir el algoritmo antes que el benchmark.** Si te miden contra el VWAP del día, un TWAP
  perfecto te deja una desviación sistemática que no se arregla con mejor infraestructura. La
  referencia se fija antes de escribir la primera línea del motor de ejecución.
- **Confundir el VWAP del mercado con tu VWAP.** Son dos números distintos: uno es el precio medio
  de todo lo negociado, el otro el de tus ejecuciones. La calidad se mide contra el primero; si
  te comparas contra el tuyo, siempre ganas.
- **Poner un límite de participación y no repartir el sobrante.** El pedido acaba corto y, peor,
  el sobrante se concentra en los últimos tramos, justo cuando queda menos tiempo para colocarlo.
  Un VWAP sin gestión de residuo termina comprando de golpe en el cierre.
- **Usar market en la punta del iceberg.** El iceberg existe para no enseñar el tamaño; si la
  punta se ejecuta contra lo que haya en el libro, el mercado ve un consumo agresivo repetido en
  el mismo precio y deduce que hay una orden grande detrás. La punta se pone al lado pasivo.
- **Creer que el iceberg oculta la orden.** Oculta el tamaño, no la existencia: la orden está en
  el libro con precio y cola visibles. Cualquiera que siga el flujo ve reaparecer la misma
  cantidad en el mismo nivel y saca la conclusión en dos minutos.
- **Ignorar la subasta de cierre.** En muchos mercados el precio de referencia del día se fija en
  la subasta de cierre y una parte importante del volumen se cruza ahí. Un algoritmo que se apaga
  cinco minutos antes deja el pedido fuera del mejor momento de liquidez.
- **Medir el resultado solo con el precio medio.** Un VWAP que se consigue mandando el 30 % del
  volumen de una franja parece bueno en precio y es malo en huella: has movido el mercado y lo
  vas a pagar en la siguiente operación.

:::practica
enunciado: Tienes que comprar 30.000 acciones en cuatro tramos de diez minutos. El volumen del mercado es 200.000, 80.000, 120.000 y 600.000 acciones. Reparte con VWAP, aplica un límite de participación del 6 % y di cuántas acciones se quedan sin ejecutar.
pista: Calcula primero la participación que resulta del reparto proporcional: es la misma en los cuatro tramos si ningún tope la recorta. Después comprueba tramo a tramo si la rodaja cabe en el 6 % del volumen negociado.
solucion: Volumen total 1.000.000 de acciones, así que la participación objetivo es 30.000 / 1.000.000 = 3 %, por debajo del tope. Rodajas: 6.000, 2.400, 3.600 y 18.000 acciones, y los topes del 6 % son 12.000, 4.800, 7.200 y 36.000. Ninguna rodaja se recorta, así que se ejecutan las 30.000 completas. El problema aparece si el tramo 2 se secara a 30.000 acciones: el tope serían 1.800 y quedarían 600 sin ejecutar, que habría que arrastrar al tramo 3 o al 4, alargando la ejecución o concentrando el pedido en el cierre.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Qué diferencia esencial hay entre TWAP y VWAP?
o: TWAP solo funciona con órdenes de venta y VWAP con órdenes de compra
o: TWAP reparte por tiempo a partes iguales y VWAP reparte siguiendo el volumen que negocia el mercado
o: TWAP esconde el tamaño de la orden y VWAP lo publica en el libro
o: TWAP se usa para acciones y VWAP para derivados
a: 2
e: TWAP manda la misma cantidad en cada intervalo, así que su participación en el volumen sube cuando el mercado se seca. VWAP reparte proporcionalmente al volumen del intervalo, lo que mantiene la participación constante. Ninguno de los dos oculta nada: eso es cosa del iceberg, y los dos sirven para comprar y para vender en cualquier instrumento.
:::

:::quiz
p: Pones un iceberg con una punta de 200 acciones al mejor bid. ¿Qué está enseñando tu orden al mercado?
o: Nada: el iceberg es invisible en el libro hasta que se ejecuta del todo
o: El precio y las 200 acciones de la punta; el tamaño total queda oculto
o: El tamaño total y el número de puntas que quedan
a: 2
e: La orden vive en el libro con su precio y su cantidad visible, así que el mercado ve la punta y la cola. Lo que no ve es cuánto queda por detrás. Por eso la punta se pone al lado pasivo: si se ejecuta con órdenes a mercado, el consumo repetido en el mismo nivel delata la orden grande.
:::

:::quiz
p: Un límite de participación del 5 % recorta la rodaja de un tramo. ¿Cuál es el problema si el sobrante no se reparte?
o: Que el total no se ejecuta y el residuo tiende a concentrarse en los últimos tramos
o: Que la comisión se duplica en ese tramo
o: Que el precio de ejecución pasa a ser el del cierre
a: 1
e: El tope solo limita el trozo, no lo reasigna. Si nadie mueve el sobrante a los tramos siguientes, la ejecución acaba corta y con demasiado peso al final, que es cuando queda menos tiempo para colocarlo y cuando el precio de referencia ya está fijándose. Un VWAP real lleva una regla explícita de gestión del residuo.
:::
