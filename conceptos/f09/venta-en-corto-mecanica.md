---
id: venta-en-corto-mecanica
titulo: Vender en corto: préstamo, coste y recalls
fase: 9
nivel: intermedio
rutas: [quant]
prerequisitos: [que-es-un-mercado, order-book-y-spread, metricas-de-riesgo]
tags: [corto, prestamo, margen, riesgo]
resumen: Vender algo que no tienes tiene fecha de caducidad y precio: quién te lo presta, cuánto cobra por ello y qué pasa cuando te lo reclama.
fuentes: ["Johnson (2010), 'Algorithmic Trading and DMA: An Introduction to Direct Access Trading Strategies'", "Harris (2003), 'Trading and Exchanges: Market Microstructure for Practitioners'", "Hull (2018), 'Options, Futures, and Other Derivatives'"]
---

## En una frase

Vender en corto es pedir prestadas unas acciones, venderlas y recomprarlas después: ganas si el
precio baja, pero pagas alquiler mientras las tienes y el dueño puede reclamarlas cualquier día.

## La idea

Casi todo el mundo entiende la parte bonita: si el precio baja, la diferencia es tuya. La parte
que se aprende a golpes es la otra mitad.

Cuando vendes en corto, alguien te presta acciones que no son tuyas. Ese alguien cobra por
prestarlas, y lo cobra **por día**. Así que una posición corta tiene un reloj: cada jornada que
pasa, el alquiler se come una parte de la ganancia que esperabas. No es un coste de entrada y
salida como la comisión: es un goteo continuo, y por eso una tesis que era buena el lunes deja de
serlo el viernes sin que el precio se haya movido.

El segundo problema es que las acciones prestadas no están realmente disponibles: el dueño las
prestó, pero puede pedirlas de vuelta. Eso es un **recall**, y no depende de ti ni del precio.
Cuando llega, el bróker tiene que conseguir acciones para devolverlas, y si no las encuentra,
te cierra la posición a mercado. Da igual que tu tesis siga intacta y que el precio esté en
máximos: compras, y compras ya.

La analogía útil es el coche prestado. Te lo dejan, conduces, pagas por cada día de uso, y si el
dueño lo necesita el jueves, lo devuelves el jueves. Lo que no puedes hacer es decir «espera a
que baje el precio y luego te lo devuelvo», porque el coche no es tuyo y el calendario lo pone
otro.

Y hay algo estructural que no se puede arreglar: la ganancia máxima de un corto es el 100 % —el
precio no baja de cero— mientras que la pérdida no tiene techo, porque el precio puede subir sin
límite. En el ejemplo de esta página, 100 acciones vendidas a 50 EUR con 2.500 EUR de garantía
aguantan hasta unos 60 EUR; a partir de ahí, el bróker pide dinero o cierra la posición, y tu
tesis de que el precio iba a bajar ya da igual.

Lo tercero, y lo que decide si un corto es viable, es la **disponibilidad**. No todos los valores
se pueden prestar. Los fáciles de prestar se alquilan a tipos de un dígito bajo y hay mucho papel;
los que están muy cortos —poca oferta y mucha demanda de préstamo— se alquilan a tipos anuales de
tres cifras, si es que hay. Los brokers publican una lista de valores «difíciles de prestar», y
los tipos cambian a diario. Un corto con alquiler del 40 % anual cuesta
`0,40 / 365 ≈ 0,11 %` del valor de la posición **cada día**: un 8 % en tres meses.

:::figura
fichero: venta-en-corto-coste-y-dias
pie: Izquierda, la ventaja de la operación se acumula como una recta con los días (línea negra) y el alquiler también: cada tasa anual diaria resta y acaba cruzando el cero. Con un 40 % anual la posición deja de ser viable en 0,4 días; con un 2 %, aguanta 7,3. Derecha, ese mismo punto de equilibrio en días según la ventaja esperada y la tasa de alquiler: la celda de arriba a la izquierda son 0,4 días, y la de abajo a la derecha, 46.
fuente: figuras/venta-en-corto-mecanica-1.py
:::

Cuesta creer que un coste del 0,1 % diario sea decisivo, pero es que un corto disciplinado genera
ventajas pequeñas: si tu tesis vale 4 puntos básicos al día, un alquiler del 0,11 % diario la
borra. Y hay un cuarto coste que se suele olvidar: el lado del diferencial. Vendes al bid y
recompras al ask, así que [[order-book-y-spread|el diferencial]] se paga dos veces, una al abrir
y otra al cerrar.

## Definición formal

El resultado de una posición corta, con los costes de préstamo separados del movimiento del
precio:

:::formula
P&L = (P_venta − P_compra) · N − alquiler · N · P · t / 365 + rebate · N · P · t / 365
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `P_venta` | Precio al que vendes las acciones prestadas | EUR por acción | Ganas más por acción: la referencia de tu tesis |
| `P_compra` | Precio al que recompras para devolver el préstamo | EUR por acción | Cada euro de subida es una pérdida para el corto; no hay techo |
| `N` | Número de acciones prestadas y vendidas | acciones | Escala el resultado y el coste: el alquiler se cobra sobre el valor de la posición, sea cual sea el precio |
| `alquiler` | Tasa anual de préstamo que cobra el prestamista | tanto por uno anual | Es el goteo: con `N · P = 50.000 EUR`, pasar del 3 % al 12 % son `50.000 · 0,09 / 365 ≈ 12,3 EUR` más por día |
| `rebate` | Interés que se paga por el efectivo en garantía | tanto por uno anual | Compensa en parte el alquiler. Muchos brókeres no lo repercuten al cliente; si no lo recibes, ponlo a cero |
| `P` | Precio de referencia de la acción para calcular el coste; en la práctica se usa el de cada día | EUR por acción | El coste diario es proporcional a él, así que un corto que sube también sube el alquiler |
| `t` | Días que mantienes la posición abierta | días | Cada día extra es un día de alquiler: el tiempo juega contra ti por los dos lados, porque la tesis también se puede agotar |
| `m` | Margen de mantenimiento exigido sobre el valor de la posición | tanto por uno | Si subes el margen exigido, aguantas menos subida antes de que te liquiden |

:::

El día en que la posición deja de ganar dinero, suponiendo que `P_venta = P` y que la tesis aporta
una ventaja diaria `d`:

:::formula
t* = d / ((alquiler − rebate) · P / 365)
:::

- `t*` — días que puedes mantener la posición antes de que el alquiler se coma toda la ventaja
  esperada. Es un techo temporal, no una predicción: si el precio se mueve a tu favor antes,
  no llegas a él.
- `d` — ventaja esperada por acción y día, en las mismas unidades que el coste.
- `alquiler − rebate` — coste neto del préstamo. Si el rebate supera al alquiler, el cociente sale
  negativo: la posición te **paga** por mantenerla y el techo desaparece.

Ese `t*` es la restricción que convierte un corto en una operación con fecha: o la tesis se cumple
antes de `t*` días, o el préstamo se ha comido la operación.

Y la otra condición, la que decide si una subida te saca de la posición. Con una cuenta que
contiene la garantía `C` y el efectivo de la venta:

:::formula
equity = C + P_venta · N − P · N        y        margen = m · P · N
:::

- `equity` — lo que vale tu cuenta: la garantía más el efectivo de la venta menos lo que costaría
  recomprar las acciones ahora mismo.
- `m · P · N` — margen exigido. El mínimo inicial habitual en Estados Unidos es el 50 % del valor
  de la posición, además del 100 % que aporta el importe de la venta: en total, el 150 % del valor
  queda cubierto. El mantenimiento típico de una acción corriente está en el 30 %.
- Un **margin call** ocurre cuando `equity < margen`. El bróker exige más dinero o compra para
  cerrar; no negocia contigo el momento.

## Ejemplo

Vendes en corto 100 acciones a 50,00 EUR, con una ventaja esperada de 4 puntos básicos al día, un
alquiler del 12 % anual y un rebate del 1 %. La garantía exigida al abrir es el 50 % del valor de
la posición: 2.500 EUR.

Costes por día, en euros:

- Alquiler: `50,00 · 0,12 / 365 = 0,01644` EUR por acción y día, o 1,64 EUR por las 100 acciones.
- Rebate: `50,00 · 0,01 / 365 = 0,00137` EUR por acción, o 0,14 EUR por las 100 acciones.
- Coste neto: 1,50 EUR al día.

Ventaja diaria: 4 puntos básicos de 50,00 son `50,00 · 0,0004 = 0,02` EUR por acción y día, o
2,00 EUR por las 100 acciones. Ganancia neta: **0,50 EUR al día**.

El techo temporal sale directo de la fórmula: `0,02 / (0,01644 − 0,00137) = 1,33` días. Es decir,
si la tesis no se cumple prácticamente el primer día, el alquiler se come la ventaja. Y si el
alquiler fuese del 3 % anual en vez del 12 %, el techo subiría a `0,02 / 0,00274 = 7,3` días: el
mismo corto, con otro préstamo, es otro negocio.

El margen, en la misma posición:

| Precio | Valor de la posición | Equity (`C + P_venta·N − P·N`) | Margen exigido (30 %) | Situación |
| --- | --- | --- | --- | --- |
| 50,00 | 5.000 | 2.500 | 1.500 | Holgado |
| 60,00 | 6.000 | 1.500 | 1.800 | Margin call |
| 65,00 | 6.500 | 1.000 | 1.950 | Liquidez forzosa |

Con 2.500 EUR de garantía, una subida del 20 % ya deja la cuenta por debajo del margen. La
pérdida en ese punto es de 1.000 EUR sobre 5.000 EUR de posición, un 20 % del notional y un 40 %
de la garantía. Y eso con una subida modesta: un corto no se arruina por bajar poco, se arruina
por subir mucho.

## Código

```python verificable
# Cuanto aguanta una posicion corta antes de que el alquiler se coma la ventaja
precio = 50.0
acciones = 100
ventaja_diaria = 0.02      # EUR por accion y dia que aporta la tesis

for alquiler, rebate in ((0.03, 0.01), (0.12, 0.01), (0.40, 0.0)):
    coste_dia = (alquiler - rebate) * precio / 365
    neto_dia = ventaja_diaria - coste_dia
    dias = ventaja_diaria / coste_dia if coste_dia > 0 else float("inf")
    print(f"alquiler {alquiler:>4.0%}, rebate {rebate:>4.0%}: coste {coste_dia:.5f} EUR/accion/dia, "
          f"neto {neto_dia * acciones:+.2f} EUR/dia, techo {dias:.1f} dias")
# -> alquiler  3%, rebate  1%: coste 0.00274 EUR/accion/dia, neto +1.73 EUR/dia, techo 7.3 dias
# -> alquiler 12%, rebate  1%: coste 0.01507 EUR/accion/dia, neto +0.49 EUR/dia, techo 1.3 dias
# -> alquiler 40%, rebate  0%: coste 0.05479 EUR/accion/dia, neto -3.48 EUR/dia, techo 0.4 dias
```

:::claves
- `alquiler / 365` convierte una tasa anual en coste diario; el 40 % anual son 0,0548 EUR por
  acción y día, no un 40 % «de una vez». Esa división es la que hace que el coste parezca pequeño
  y la que hace que se acumule sin que lo notes.
- Con el tercer caso el resultado neto sale **negativo**: la posición pierde dinero cada día que
  la mantienes abierta, incluso sin que el precio se mueva. Ese caso no se arregla esperando.
- `float("inf")` se usa para el caso en que el coste es cero o negativo. Si divides por cero sin
  protegerlo, el programa revienta justo cuando el préstamo es bueno.
- `{alquiler:>4.0%}` formatea un tanto por uno como porcentaje sin decimales: `0.12` se imprime
  como `12%`. Cambiar `0.12` por `12` en el cálculo multiplicaría el coste por cien.
- El bucle recorre una **tupla de tuplas**: no hay nada que ordenar ni que calcular antes, y el
  número de escenarios es exactamente el número de elementos.
:::

```python verificable
# Margen y liquidez forzosa: cuando el broker compra por ti
precio_venta = 50.0
acciones = 100
garantia = 0.50 * precio_venta * acciones   # el 50 % del valor, como pide la Regulacion T
mantenimiento = 0.30                        # margen exigido sobre el valor actual

print(f"garantia aportada: {garantia:.2f} EUR")
# -> garantia aportada: 2500.00 EUR
for precio in (50.0, 60.0, 65.0):
    equity = garantia + precio_venta * acciones - precio * acciones
    exigido = mantenimiento * precio * acciones
    estado = "ok" if equity >= exigido else "MARGIN CALL"
    print(f"precio {precio:>5.2f}: equity {equity:>8.2f} EUR, exigido {exigido:>8.2f} EUR -> {estado}")
# -> precio 50.00: equity  2500.00 EUR, exigido  1500.00 EUR -> ok
# -> precio 60.00: equity  1500.00 EUR, exigido  1800.00 EUR -> MARGIN CALL
# -> precio 65.00: equity  1000.00 EUR, exigido  1950.00 EUR -> MARGIN CALL
```

```text
El corto, en orden de decisiones
paso                 | que se comprueba                        | quien decide
disponibilidad       | hay papel prestable y a que tipo        | el broker, no tu
apertura             | garantia (150 % del valor en EE. UU.)   | tu cuenta
mantenimiento diario | equity mayor o igual que el margen      | el broker
recall               | el prestamista reclama sus acciones     | el prestamista
cierre               | recompras al ask, no al bid             | el mercado
```

## Errores típicos

- **Mirar solo el movimiento del precio.** Un corto de tres meses con alquiler del 12 % paga un
  3 % del valor por el camino. Si la tesis valía un 4 %, el préstamo se lleva tres cuartas partes
  de la operación y tú creías que habías acertado.
- **Suponer que el préstamo sigue ahí.** Un recall no avisa con antelación: el prestamista
  necesita sus acciones y el bróker las consigue como puede. Si el valor está en máximos, la
  recompra forzosa llega en el peor momento posible, y no es una decisión tuya.
- **Ignorar que la pérdida no tiene techo.** Vendes a 50 y tu ganancia máxima son 50 por acción;
  si sube a 500, pierdes 450. La asimetría no está en la probabilidad, está en el tamaño, y por
  eso el tamaño de posición de un corto se calcula con la subida posible, no con la bajada
  esperada.
- **Confundir el tipo de alquiler con una comisión fija.** Se paga por día y sobre el valor de la
  posición, así que crece con el tiempo y con la subida del precio a la vez. Con un 40 % anual el
  coste diario es del 0,11 %: tres meses son un 8 % del notional.
- **Aguantar un margin call esperando la vuelta.** El bróker no espera: exige dinero o liquida.
  Si la posición se cierra a 65 y tu tesis se cumplía a 40, el acierto no te sirve de nada porque
  ya no tienes posición.
- **Vender en corto un valor con el préstamo carísimo porque la tesis es muy buena.** Si el
  alquiler es del 40 % anual y tu ventaja es del 4 % al día, el techo es de 0,4 días: la tesis
  tiene que cumplirse hoy. Si no, el préstamo se queda con todo.
- **Olvidar el diferencial y los dos lados.** Abres vendiendo al bid y cierras comprando al ask.
  En un valor con 20 puntos básicos de diferencial, el ida y vuelta cuesta 20 puntos básicos
  antes de comisiones, y eso en un corto con techo de dos días es la mitad de la ventaja.

:::practica
enunciado: Vendes en corto 200 acciones a 80,00 EUR con un alquiler del 18 % anual y sin rebate. Tu tesis espera una caída del 3 % en un mes. ¿Qué resultado neto obtienes si la tesis se cumple al final del mes y qué pasa si el precio no se mueve en absoluto?
pista: Separa el movimiento del precio del coste del préstamo. El coste se cobra sobre el valor de la posición y por día; el movimiento de precio va sobre el mismo número de acciones.
solucion: Si la acción cae un 3 %, recompras a 77,60 EUR y ganas (80,00 − 77,60) · 200 = 480 EUR. El alquiler de 30 días es 80,00 · 0,18 / 365 · 30 · 200 = 236,71 EUR, así que el neto queda en 243,29 EUR. Si el precio no se mueve, la ganancia por precio es cero y el alquiler sigue corriendo: pierdes 236,71 EUR, más de la mitad de lo que ganabas en el escenario bueno. Y si además el bróker te reclama las acciones el día 10, pagas los 78,90 EUR de alquiler de esos diez días sin haber recogido nada de la tesis.
:::

## Comprueba que lo sabes

:::quiz
p: ¿Por qué una posición corta tiene una pérdida potencial ilimitada?
o: Porque el bróker cobra intereses mientras esté abierta
o: Porque la ganancia máxima es que el precio llegue a cero, pero el precio puede subir sin límite
o: Porque las acciones prestadas se revalorizan automáticamente
a: 2
e: La ganancia está acotada por abajo: lo máximo que puedes ganar es el precio de venta, porque el precio no baja de cero. La pérdida, en cambio, crece con cada euro que sube la acción y no hay ningún tope. El coste del préstamo agrava el problema, pero la asimetría viene del precio, no del interés.
:::

:::quiz
p: ¿Qué es un recall y por qué es peligroso?
o: Que el bróker te sube el tipo de alquiler de un día para otro
o: Que el prestamista reclama sus acciones y tienes que recomprar para devolverlas, sin elegir el momento
o: Que la bolsa suspende la cotización del valor
a: 2
e: El recall lo decide el dueño de las acciones, no el precio ni tu tesis. Cuando llega, el bróker consigue papel como puede y, si no lo encuentra, cierra tu posición a mercado. El riesgo no es el coste: es que dejas de tener el control de cuándo sales, y suele coincidir con los peores momentos.
:::

:::quiz
p: Un corto con alquiler del 12 % anual y una ventaja esperada de 4 puntos básicos al día sobre una acción de 100 EUR. ¿Cuánto tiempo puedes mantenerlo antes de que el préstamo se coma la ventaja?
o: Unos 1,2 días: el coste diario del préstamo supera a la ventaja en cuanto pasa un día
o: Unos 12 días, porque el alquiler es del 12 %
o: Indefinidamente, porque el alquiler solo se paga al cerrar la posición
a: 1
e: La ventaja diaria es 100 · 0,0004 = 0,04 EUR por acción. El alquiler cuesta 100 · 0,12 / 365 = 0,0329 EUR por acción y día. El cociente da 0,04 / 0,0329 = 1,2 días. Coincidir con el número de la tasa es casualidad: lo que importa es el cociente entre la ventaja diaria y el coste diario, y el alquiler se paga por día, no al cerrar.
:::
