---
id: slippage-y-comisiones
titulo: Deslizamiento y comisiones
fase: 9
nivel: intermedio
rutas: [quant]
prerequisitos: [microestructura-de-mercado, order-book-y-spread]
tags: [costes, ejecucion, backtest, comisiones]
resumen: Comisiones, diferencial e impacto: los tres costes que se pagan en cada operación y que convierten una estrategia ganadora en papel en una perdedora en real.
fuentes: ["Harris (2003), 'Trading and Exchanges: Market Microstructure for Practitioners'", "Bouchaud et al. (2018), 'Trades, Quotes and Prices'"]
---

## En una frase

Operar cuesta dinero cada vez que entras y cada vez que sales, y ese coste no es un detalle
administrativo: es una resta que se aplica a la ventaja bruta de cada operación, así que una
estrategia con poco margen puede pasar de ganar a perder solo por el precio de ejecutar.

## La idea

Piensa en cambiar dinero de moneda en un aeropuerto. El cartel dice un precio, pero cuando
llegas a la ventanilla te dan menos de lo que esperabas: hay una comisión y, además, el precio
de compra y el de venta no son el mismo. Si cambias 100 euros pierdes poco; si cambias 100.000,
la diferencia es un viaje entero. Y si intentas cambiar un millón de golpe en una ventanilla
pequeña, el propio mostrador se queda sin billetes y te aplica un precio peor para el resto.

En el mercado pasa exactamente lo mismo, con tres costes que conviene separar porque se
comportan de forma distinta:

1. **Comisiones y tasas.** Lo que te cobra el bróker y, en su caso, la bolsa y la cámara. Es
   explícito, fijo y fácil de meter en un backtest. Se paga por operación, no por resultado.
2. **Diferencial (*spread*).** Si cruzas a mercado, compras al *ask* y vendes al *bid*. Esa
   distancia la pagas en cada vuelta y es la parte que más se olvida. Un valor con 5 puntos
   básicos de diferencial te cuesta 10 pb por ida y vuelta aunque la comisión sea cero.
3. **Impacto y deslizamiento (*slippage*).** Tu propia orden mueve el precio: consume niveles
   del libro y, si eres grande, empuja el precio en tu contra. Además, entre el momento en que
   decides y el momento en que se ejecuta, el precio puede haberse movido. El resultado es que
   la ejecución acaba peor que el precio que tenías en pantalla cuando decidiste.

El deslizamiento se define como la diferencia entre el precio que esperabas y el precio al que
acabas ejecutado. No es un fallo técnico: es la consecuencia de que el precio es una cola de
órdenes que cambia, y tú no eres el único que la usa.

:::figura
fichero: slippage-coste-y-tamano
pie: Arriba, los tres costes apilados frente a una ventaja bruta que no se mueve: la comisión y el diferencial son una banda de altura fija y solo el impacto engorda con el tamaño. Abajo, la resta: con 225.000 EUR de nominal la ventaja neta toca cero y la estrategia deja de existir aunque la señal siga acertando. Mira dónde cruza la curva el cero, porque ese punto es la capacidad real de la estrategia, no su calidad.
fuente: figuras/slippage-y-comisiones-1.py
:::

Lo que hace que este tema sea el más importante de la fase es la asimetría: **la ganancia de una
operación es incierta y el coste es seguro**. Da igual si aciertas o fallas la dirección; la
comisión, el diferencial y el impacto los pagas siempre. Por eso el coste no reduce el
resultado: decide qué estrategias existen y cuáles no.

:::trampa
Un backtest con coste cero no está midiendo una estrategia, está midiendo una idea. Añade
después el coste y verás cuántas ideas sobreviven. La mayoría de las estrategias de alta
frecuencia mueren exactamente aquí.
:::

## Definición formal

El coste de una operación de ida y vuelta, en puntos básicos sobre el nominal, se descompone
así:

:::formula
coste_pb = 2 · c + diferencial_pb + impacto_pb
:::

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `coste_pb` | Coste total de una ida y vuelta | pb (1 pb = 0,01 %) | Es la cifra que se resta a la ventaja bruta: por encima de ella la estrategia pierde dinero |
| `c` | Comisión y tasas de una punta | pb sobre el nominal | El coste sube al doble de ritmo, porque se paga al entrar y al salir: es lo que más castiga operar mucho |
| `diferencial_pb` | Distancia entre el bid y el ask | pb | Se paga entero en cada vuelta. Por encima de la ventaja bruta no hay señal que lo salve: compruébalo antes de programar nada |
| `impacto_pb` | Lo que tu propia orden mueve el precio | pb | Es el único de los tres que empeora al asignar más capital a la misma idea; los otros dos no cambian con el tamaño |
| `slippage` | Precio ejecutado menos precio esperado | unidades de precio | Positivo significa que has perdido, tanto si compras como si vendes: no hay un signo bueno |
| `ventaja_bruta` | Lo que gana la señal antes de costes | pb | Con la misma señal, decide cuánto tamaño aguanta la estrategia antes de quedarse en cero |
| `Q` | Tamaño de la orden | acciones o EUR | El impacto crece con su raíz: cuadruplicar el nominal multiplica el impacto por 2, no por 4 |
| `V` | Volumen negociado en el periodo de referencia | acciones o EUR, el mismo día | Cuanto más se negocia, menos pesa tu orden: es la diferencia entre un valor líquido y uno que no lo es |
| `σ` | Volatilidad del activo en ese periodo | tanto por uno o % | Con más volatilidad tu orden mueve antes el precio y el impacto sube en la misma proporción |
| `k` | Constante de proporcionalidad del modelo de impacto | adimensional | No es universal: se estima con datos propios. Si la copias de un artículo, el resultado no será el tuyo |
:::

- `c` — comisión más tasas de una punta, en puntos básicos sobre el nominal (pb, una
  diezmilésima: 1 pb = 0,01 %).
- `2 · c` — se paga en la entrada y en la salida; por eso se duplica.
- `diferencial_pb` — el diferencial del libro, en pb. Si cruzas a mercado, lo pagas una vez
  por vuelta (compras al ask y vendes al bid).
- `impacto_pb` — lo que tu orden mueve el precio, en pb. Depende del tamaño de la orden
  respecto a la liquidez disponible.

El deslizamiento de una ejecución concreta, en unidades de precio:

:::formula
slippage = precio_ejecutado − precio_esperado      (con signo: positivo si compras más caro)
:::

- `precio_esperado` — el precio que había en el libro (o el de la señal) cuando decidiste.
- `precio_ejecutado` — el precio medio real de tu orden.
- **signo** — si compras, el deslizamiento es positivo cuando pagas más; si vendes, cuando
  cobras menos. En los dos casos, positivo significa que has perdido.

Y la condición de viabilidad de una estrategia, que es la que hay que comprobar antes de
escribir una línea de código más:

:::formula
ventaja_neta_por_operacion = ventaja_bruta − coste_pb > 0
:::

- `ventaja_bruta` — lo que gana la señal antes de costes, en pb, medido con datos reales.
- `coste_pb` — el coste total de la ida y vuelta.

**Cómo crece el coste con el tamaño.** El impacto crece siempre con el tamaño, pero cada vez
menos: doblar la orden más que dobla el impacto, y cuadruplicarla lo multiplica por dos. Esa
relación cóncava se describe habitualmente con una raíz cuadrada:

:::formula
impacto ≈ k · σ · √( Q / V )
:::

- `Q` — el tamaño de tu orden (acciones o importe).
- `V` — el volumen negociado en el periodo de referencia (el mismo día, por ejemplo).
- `σ` — la volatilidad del activo en ese periodo: a más volatilidad, más impacto.
- `k` — constante de proporcionalidad que depende del mercado y del activo; **no es un número
  universal** y hay que estimarla con datos propios.

La consecuencia práctica de esa raíz: dividir una orden en trozos reduce el impacto (la raíz
de la suma es menor que la suma de raíces), pero alarga el tiempo de ejecución y con él el
riesgo de que el precio se mueva.

## Ejemplo

Una estrategia intradía que opera un valor liquido con órdenes de 25.000 EUR y una ventaja
bruta medida de 15 pb por operación. El valor tiene un diferencial de 4 pb y el bróker cobra
4 pb por punta.

- Comisiones, ida y vuelta: 2 · 4 = **8 pb**.
- Diferencial: **4 pb**.
- Impacto estimado para ese tamaño frente a la liquidez del valor: **1 pb**.
- `coste_pb` = 8 + 4 + 1 = **13 pb**.
- `ventaja_neta_por_operacion` = 15 − 13 = **+2 pb**.

Cinco veces menos de lo que parecía. Sobre un nominal de 25.000 EUR, 2 pb son 5 EUR por
operación. Con 4 operaciones al día y 250 días, son 1.000 operaciones y 5.000 EUR al año;
sobre el capital necesario para operar, el resultado depende de cada cuenta, pero el margen es
tan fino que cualquier empeoramiento lo borra:

- Si el impacto sube a 3 pb porque el mercado está revuelto, la ventaja neta baja a **0 pb**.
- Si la ventaja bruta real es 11 pb en vez de 15 (bastante habitual al medirla fuera de muestra),
  la ventaja neta es **−2 pb**: la estrategia pierde dinero con una señal que "acierta".

Ahora cambia el tamaño. Con órdenes de 250.000 EUR, diez veces mayores, el impacto crece con
la raíz del tamaño: si con 25.000 era 1 pb, con 250.000 ronda los 3 pb (raíz de 10 es 3,16).
El coste pasa a 8 + 4 + 3 = **15 pb**, exactamente la ventaja bruta: la estrategia se queda en
cero **sin haber cambiado la señal ni el modelo**, solo por operar más grande.

Ese es el motivo de que muchas estrategias funcionen en un backtest con nominales pequeños y no
funcionen cuando se les asigna capital: la capacidad de una estrategia no la fija la señal, la
fija el coste.

## Código

```python verificable
# Los tres costes y la ventaja neta, en puntos basicos sobre el nominal.
comision_pb = 4.0        # por punta: se paga al entrar y al salir
diferencial_pb = 4.0     # cruzar a mercado una vez por vuelta
impacto_pb = 1.0
ventaja_bruta_pb = 15.0

coste_pb = 2 * comision_pb + diferencial_pb + impacto_pb
neta_pb = ventaja_bruta_pb - coste_pb

print("coste ida y vuelta:", round(coste_pb, 1), "pb")     # -> 13.0 pb
print("ventaja neta      :", round(neta_pb, 1), "pb")      # -> 2.0 pb

nominal = 25_000
print("coste en euros    :", round(nominal * coste_pb / 10_000, 2))    # -> 32.5
print("neto en euros     :", round(nominal * neta_pb / 10_000, 2))      # -> 5.0

# La ventaja bruta minima para no perder con estos costes.
print("ventaja de equilibrio:", round(coste_pb, 1), "pb")  # -> 13.0 pb
```

:::claves
- Las cuatro primeras líneas no son código, son **parámetros**: cambiarlas cambia la conclusión del ejemplo entero. Prueba a poner `diferencial_pb = 6.0` y verás que la ventaja neta pasa de +2 pb a 0 pb: la misma señal, otro mercado.
- `2 * comision_pb` se escribe con el `2` delante porque la comisión se paga **dos veces**, al entrar y al salir. Si alguien "arregla" esa línea quitando el 2, la ventaja neta se duplica en pantalla y no en la cuenta.
- `25_000` es el mismo número que `25000`: el guion bajo es solo un separador para leerlo de un vistazo. Python lo ignora, y funciona igual con `1_000_000`.
- `round(x, 1)` **no cambia** la variable: devuelve un número nuevo y el original sigue con todos sus decimales. Si en vez de eso escribieras `coste_pb = round(coste_pb, 1)` redondearías de verdad y el coste en euros saldría con el error arrastrado.
- `nominal * coste_pb / 10_000` convierte puntos básicos a euros: 1 pb es una diezmilésima, así que se divide entre 10.000. Si te sale un número mil veces mayor, casi siempre es que has dividido entre 100 y no entre 10.000.
- El último `print` imprime otra vez `coste_pb` y lo llama «ventaja de equilibrio». No es una cuenta nueva: es el mismo número leído al revés, porque la ventaja bruta mínima para no perder **es** exactamente el coste.
:::

```python verificable
# Cuanto empeora el resultado al operar mas grande: el impacto no es lineal.
def impacto_pb(tamano, tamano_base=25_000, impacto_base=1.0):
    """Modelo de raiz cuadrada: el impacto crece con la raiz del tamano relativo."""
    return impacto_base * (tamano / tamano_base) ** 0.5

for tamano in (25_000, 100_000, 250_000, 1_000_000):
    coste = 2 * 4.0 + 4.0 + impacto_pb(tamano)
    print(f"nominal {tamano:>9,}  impacto {impacto_pb(tamano):5.2f} pb  coste {coste:5.2f} pb")
# -> nominal    25,000  impacto  1.00 pb  coste 13.00 pb
# -> nominal   100,000  impacto  2.00 pb  coste 14.00 pb
# -> nominal   250,000  impacto  3.16 pb  coste 15.16 pb
# -> nominal 1,000,000  impacto  6.32 pb  coste 18.32 pb
```

```python ilustrativo
# Simulacion de una ejecucion contra el libro, con la cola y el retardo reales.
# Necesita datos de libro con marcas de tiempo, que no estan en este bloque:
# por eso es ilustrativo y no verificable.
def ejecutar_orden(libro, cantidad, retardo_ms, tipo="mercado"):
    """Recorre el libro tras aplicar el retardo y devuelve el precio medio real."""
    libro_enviado = aplicar_retardo(libro, retardo_ms)
    if tipo == "mercado":
        return consumir_niveles(libro_enviado["asks"], cantidad)
    return colocar_limite(libro_enviado, cantidad)
```

## Errores típicos

- **Backtestear con coste cero o con un coste inventado.** Un 0,1 % "porque suena razonable" no
  es una estimación. Mide el diferencial real del activo en tus horas de operación y pon la
  comisión de tu tarifa: la diferencia entre las dos cifras decide el signo del resultado.
- **Olvidar que la comisión se paga dos veces.** Se entra y se sale. El error típico es meter
  la comisión una sola vez por operación completa, lo que duplica la ventaja aparente.
- **Ignorar el diferencial en valores poco líquidos.** Con 20 pb de diferencial, una estrategia
  que gana 15 pb brutos pierde dinero siempre, por muy buena que sea la señal. Comprueba el
  diferencial **antes** de desarrollar la estrategia, no después.
- **Modelar el impacto como lineal.** Duplicar el tamaño no duplica el impacto para órdenes
  grandes, pero tampoco lo mantiene: crece. Si tu backtest usa un coste fijo por operación y
  luego aumentas el capital, el resultado de la simulación no se parecerá al real.
- **Suponer que una orden límite se ejecuta siempre y al precio exacto.** Ya lo viste en
  [[microestructura-de-mercado|la microestructura]]: hay cola. Modelar ejecución inmediata en
  cada nivel tocado regala resultado.
- **Operar más por bajar el coste medio.** Es la trampa final: si cada operación pierde 2 pb y
  haces más operaciones, pierdes más, más rápido. El coste se suma, no se diluye.

:::practica
enunciado: Una señal gana 22 pb brutos. Comisión 2,5 pb por punta, diferencial 5 pb e impacto, con órdenes de 40.000 EUR, 1,2 pb. Calcula la ventaja neta con 40.000 y con 160.000 EUR, y el beneficio en euros por operación en el segundo caso.
pista: El impacto crece con la raíz del tamaño: al cuadruplicar el nominal se multiplica por dos. La comisión se paga dos veces y el diferencial una por vuelta.
solucion: Coste = 2 · 2,5 + 5 + impacto. Con 40.000 EUR: 5 + 5 + 1,2 = 11,2 pb, ventaja neta 22 − 11,2 = 10,8 pb. Con 160.000 EUR el impacto es 1,2 · √4 = 2,4 pb, el coste 12,4 pb y la ventaja neta 9,6 pb. En euros, 160.000 · 9,6 / 10.000 = 153,60 EUR por operación.
:::

## Comprueba que lo sabes

:::quiz
p: Una señal gana 12 pb brutos por operación. El bróker cobra 3 pb por punta, el diferencial del valor es de 6 pb y el impacto estimado 1 pb. ¿Qué pasa?
o: La ventaja neta es 5 pb, así que la estrategia es viable
o: La ventaja neta es −1 pb: 12 − (2·3 + 6 + 1) = −1, así que pierde dinero
o: La ventaja neta es 2 pb, porque el diferencial se paga una vez por cada punta
a: 2
e: El coste es 2·3 de comisiones más 6 de diferencial más 1 de impacto, es decir 13 pb, por encima de los 12 pb de ventaja bruta. La comisión se paga al entrar y al salir, y el diferencial se cruza una vez por vuelta: con estos números la señal acierta y la cuenta baja.
:::

:::quiz
p: ¿Por qué el impacto de mercado no crece de forma lineal con el tamaño de la orden?
o: Porque los brókers aplican descuentos a las órdenes grandes
o: Porque el libro tiene niveles con distinta profundidad y, al repartir la orden, el efecto crece aproximadamente con la raíz del tamaño
o: Porque el impacto solo depende de la volatilidad, no del tamaño
a: 2
e: El impacto depende de cuánta liquidez consumes y de cómo reacciona el mercado, y se describe habitualmente con una raíz cuadrada del tamaño relativo al volumen. No es lineal: dividir una orden en trozos reduce el impacto total, aunque alarga la ejecución y añade riesgo. La volatilidad influye, pero no es el único factor.
:::

:::quiz
p: Un backtest con coste cero da un resultado espectacular. ¿Cuál es la forma correcta de comprobarlo?
o: Añadir comisiones reales, el diferencial del activo en las horas de operación y una estimación de impacto, y volver a medir la ventaja neta por operación
o: Restar un 0,1 % por operación y dar el resultado por bueno
o: Dejarlo sin costes y señalar que en producción será algo peor
a: 1
e: El coste se compone de comisiones, diferencial e impacto, y cada uno se mide con datos del mercado concreto y de tus horas de operación. Un porcentaje genérico no sirve, y presentar el resultado sin costes no informa de nada: la única cifra relevante es la ventaja neta por operación.
:::

:::aviso
El coste de ejecución es la razón por la que muchas estrategias buenas en investigación no se
llevan a producción, y no se arregla con un modelo más complicado: se arregla operando menos,
más despacio o en activos más líquidos. Antes de optimizar la señal, comprueba que la ventaja
bruta supera el coste por un margen cómodo.
:::
