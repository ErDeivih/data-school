---
id: que-es-un-mercado
titulo: Qué es un mercado
fase: 9
nivel: básico
rutas: [quant]
prerequisitos: []
tags: [mercado, activos, órdenes, costes]
resumen: Quien compra, quién vende, quién pone el precio y quién cobra: el mapa del mercado antes de tocar una estrategia.
fuentes: ["Harris (2003), 'Trading and Exchanges: Market Microstructure for Practitioners'"]
---

## En una frase

Un mercado es un mecanismo que junta a gente que quiere comprar con gente que quiere vender,
decide a qué precio se cruzan y deja un rastro de lo ocurrido; todo lo demás (plataformas,
brókers, cámaras) existe para que ese cruce sea fiable y para cobrar por ello.

## La idea

Piensa en el mercadillo del domingo. Hay quien trae naranjas, quien las busca, y un espacio común
donde se encuentran. El precio no lo fija nadie desde arriba: sale de la negociación, y si hay
mucha gente buscando naranjas y pocas vendiéndolas, sube. Además de los dos bandos hay figuras de
servicio: el que pesa la fruta, el que cobra el puesto y el que vigila que nadie venda arena por
azúcar.

Un mercado financiero es lo mismo con tres diferencias importantes. Primera, lo que se
intercambia son activos estandarizados: una acción de una empresa es idéntica a otra acción de la
misma empresa, así que no hay que discutir por la calidad de cada unidad. Segunda, no hace falta
estar presente: se participa a través de un bróker, que es tu intermediario y quien te exige
garantías. Tercera, el mercado recuerda: cada operación queda registrada con hora, precio y
volumen.

Quien participa, y con qué interés:

- **Inversores particulares.** Compran y venden para ahorrar o especular. Aportan poco volumen
  relativo, pero son la razón de que el mercado exista.
- **Institucionales.** Fondos, aseguradoras, tesorerías de empresas. Mueven volúmenes grandes y su
  problema no es acertar la dirección, sino ejecutar sin mover el precio en su contra.
- **Creadores de mercado (market makers).** Cotizan a la vez un precio de compra y uno de venta y
  ganan, en teoría, la diferencia. Asumen dos riesgos concretos: quedarse con inventario que se
  mueve en su contra y cruzarse con alguien mejor informado que ellos.
- **Brókers.** Canalizan tus órdenes y, en muchos casos, las ejecutan. No son el mercado: son tu
  puerta a él. Cobran comisión o viven del diferencial.
- **Centros de negociación.** Bolsas y sistemas alternativos donde las órdenes se cruzan. Hay
  varios compitiendo por el mismo activo, y eso fragmenta el libro.
- **Cámara de compensación (clearing house).** Se interpone entre comprador y vendedor y garantiza
  que la operación se líquida aunque una parte quiebre. Por eso exige garantías y ajustes diarios.
- **Regulador.** Fija las reglas de transparencia, abuso de mercado y protección del inversor.

Los activos que verás en las fases siguientes: **renta variable** (acciones, participación en una
empresa), **renta fija** (bonos, préstamos con cupón), **divisas** (pares de monedas), **materias
primas** (energía, metales, agrícolas), **derivados** (futuros y opciones, cuyo valor depende de
otro activo) y **criptoactivos**. Cada uno tiene horarios, garantías y microestructura distintos, y
una estrategia que funciona en uno puede ser inviable en otro solo por el coste de negociar.

Hay un papel que conviene entender desde el principio, porque es donde vive el dinero de verdad:
el **creador de mercado**. Si alguien quiere comprar tu acción ahora mismo, no espera a que
aparezca otro particular con la idea contraria. Le vende el creador de mercado, que ya tenía la
acción en su inventario, y te la cobra un poco más cara de lo que la compró. Ese pequeño margen es
su beneficio por darte inmediatez, y para ti es un coste en cada operación.

:::figura
fichero: mercado-notional-coste-y-tamano
pie: A la izquierda, la ganancia que da el precio (en verde) frente a lo que se lleva el intermediario (en rojo), en los dos recorridos del ejemplo: con 200 acciones el bróker se queda el 8,2 % del beneficio bruto, y con 2.000 —el mismo movimiento por acción— el 14,8 %. A la derecha, el porcentaje que sobrevive: el precio no ha cambiado, ha cambiado tu tamaño. Conclusión: el coste no es un detalle administrativo que se resta al final; en cuanto la posición crece, el diferencial y el impacto son parte del resultado.
fuente: figuras/que-es-un-mercado-1.py
:::

:::nota
Hay dos formas de cruzar órdenes. En una **subasta de apertura o cierre** todas las órdenes se
acumulan y se calcula un único precio que maximiza el volumen cruzado. Durante la sesión, el
régimen normal es la **negociación continua**: las órdenes se cruzan en cuanto coinciden, por
orden de precio y luego de llegada.
:::

## Definición formal

Un mercado continuo se describe con tres objetos: el libro de órdenes, la regla de cruce y el
resultado de cada cruce.

:::formula
libro = ( B, A )    con B = { (p_i, q_i) } y A = { (p_j, q_j) }
:::

- `B` — el lado de compra (*bid*): órdenes que esperan a que alguien venda.
- `A` — el lado de venta (*ask*): órdenes que esperan a que alguien compre.
- `p_i`, `q_i` — precio y cantidad de la orden i. En un libro, `max(B) < min(A)` siempre que no
  haya cruzado todavía; a esa separación se le llama **diferencial** o *spread*.

La regla de prioridad es doble: primero el mejor precio, y a igual precio, quien llegó antes
(*price-time priority*). Cada cruce define tres números:

:::formula
notional = p · q        comisión = p · q · f        coste_total = comisión + coste_implicito
:::

- `p` — precio de la operación.
- `q` — cantidad de títulos intercambiados.
- `notional` — el importe en dinero de la operación, también llamado nominal negociado.
- `f` — la comisión por unidad de nominal que cobra tu bróker o el centro de negociación.
- **coste implícito** — lo que pierdes por el diferencial y por el impacto de tu propia orden,
  aunque la comisión sea cero.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `p` | El precio de la operación, que es el del último cruce, no el del gráfico | EUR por título | Sube el nominal y, con la misma comisión porcentual, también la comisión en euros. Si tu orden es grande, el precio que consigues es peor que el que ves |
| `q` | La cantidad de títulos intercambiados | títulos | Es la palanca que casi nadie mira: multiplica el nominal y, con él, la comisión; y por encima de lo que hay en el mejor nivel, también el diferencial y el impacto. A partir de cierto tamaño, el coste crece más deprisa que la ganancia |
| `notional = p · q` | El importe en dinero de la operación | EUR | No cambia el precio de tu operación, pero decide qué tarifa te aplican: los mínimos de comisión dejan de importar y los descuentos por volumen empiezan a notarse |
| `f` | La comisión por unidad de nominal que cobra el bróker | tanto por uno (0,001 = 0,10 %) | Con `f` alta manda la comisión; con `f` casi cero (brókers sin comisión) el coste real se muda al diferencial, que no desaparece |
| `coste_implícito` | Lo que pagas por cruzar el diferencial y por mover el precio con tu orden | EUR | Crece con la raíz del tamaño y con la prisa, no con el nominal: doblar la posición cuesta bastante más del doble en un libro fino. Es el que hace inviable una estrategia pequeña que parece buena en papel |
| `coste_total = comisión + coste_implícito` | Lo que se descuenta del resultado bruto | EUR | Es el número que decide si la estrategia vive: con 2.500 operaciones al año, unos pocos puntos básicos de más convierten una ventaja en una pérdida (`(edge − coste) · operaciones`) |
:::

## Ejemplo

Compras 200 acciones de un valor español a 24,50 EUR. El bróker cobra 0,10 % de comisión con un
mínimo de 3 EUR. Más tarde vendes a 25,10 EUR, con la misma tarifa.

- Compra: nominal = 200 · 24,50 = **4.900 EUR**; comisión = 4.900 · 0,001 = 4,90 EUR.
- Venta: nominal = 200 · 25,10 = **5.020 EUR**; comisión = 5.020 · 0,001 = 5,02 EUR.
- Beneficio bruto: 5.020 − 4.900 = **120 EUR**.
- Beneficio neto: 120 − 4,90 − 5,02 = **110,08 EUR**.
- Lo que se ha quedado el intermediario: 9,92 EUR, un **8,3 %** del beneficio bruto.
- En porcentaje sobre el nominal de compra: 110,08 / 4.900 = **2,25 %**.

Ahora el mismo recorrido con una posición diez veces mayor, 2.000 acciones, y una orden a mercado
en un valor con un diferencial de 2 céntimos. La comisión con mínimo de 3 EUR pasa a 49,00 EUR en
la compra, pero además el diferencial cuesta 2.000 · 0,02 = **40 EUR** por entrar, y probablemente
otros tantos por salir si el libro está fino. Con el mismo movimiento de precio (120 EUR por cada
200 acciones, es decir 1.200 EUR brutos), el coste total ronda los 178 EUR: casi el **15 %** del
beneficio. El precio de la acción no ha cambiado; lo que ha cambiado es tu tamaño.

Esa es la lección económica de esta fase: en un mercado, el precio que ves en el gráfico es el
precio de la última operación, no el precio al que tú podrías operar. La distancia entre ambos es
el negocio de alguien.

## Código

```python verificable
# El coste de operar: comision con minimo y diferencia de precios, en una ida y vuelta.
nominal_compra = 200 * 24.50
nominal_venta = 200 * 25.10

def comision(nominal, porcentaje=0.001, minimo=3.0):
    """La tarifa del broker: un porcentaje, pero nunca menos que el minimo."""
    return max(nominal * porcentaje, minimo)

c_compra = comision(nominal_compra)
c_venta = comision(nominal_venta)
bruto = nominal_venta - nominal_compra

print("nominal compra :", round(nominal_compra, 2))   # -> 4900.0
print("comision compra:", round(c_compra, 2))         # -> 4.9
print("comision venta :", round(c_venta, 2))          # -> 5.02
print("beneficio bruto:", round(bruto, 2))            # -> 120.0
print("beneficio neto :", round(bruto - c_compra - c_venta, 2))   # -> 110.08
print("coste sobre bruto:", round((c_compra + c_venta) / bruto * 100, 1), "%")   # -> 8.3 %
```

:::claves
- `def comision(nominal, porcentaje=0.001, minimo=3.0)` lleva los valores por defecto en la propia definición, no en una variable global: cambiarlos ahí los cambia para todas las llamadas, y llamar `comision(1000, 0.002)` solo pisa el segundo. Y `max(nominal * porcentaje, minimo)` no redondea nada: devuelve el mayor de los dos, así que con nominales pequeños la comisión se queda clavada en 3,00 y deja de ser proporcional.
- `round(5.0200000000000005, 2)` no «recorta decimales»: busca el número de coma flotante más cercano con dos decimales, y por eso `round(4.9, 2)` te devuelve `4.9` (no `4.90`). El resultado del portal sale exacto porque `120 - 4.9 - 5.02` es, en coma flotante, exactamente `110.08`; con otros importes verás colas de `...0000001` y no es un error del mercado, es de la representación.
- La comisión se paga **en cada punta**: `c_compra + c_venta`, no una vez por la operación completa. Sobre un bruto de 120 EUR y una tarifa del 0,10 %, el intermediario se lleva el 8,3 %, y ese porcentaje crece cuando el nominal baja porque el mínimo de 3 EUR pasa a mandar.
- `nominal_compra = 200 * 24.50` son `float`, no `Decimal`. En un sistema que cuadre cuentas con céntimos, sumar miles de comisiones así acumula un desajuste visible: para eso se usa `decimal.Decimal` con redondeo explícito, o se trabaja en céntimos enteros.
- `print("coste sobre bruto:", ..., "%")` es una llamada con cuatro argumentos: `print` los pega con un espacio y no aplica ningún formato. `"%.1f %%" % valor` sería otra cosa, pero aquí `round(..., 1)` ya devuelve un número y el `%` es solo texto decorativo que se añade a mano.
- El factor `100` de `round(..., 1)` es conversión de tanto por uno a porcentaje, y no está en la fórmula: `0.001` es `0,1 %`. Si copias esa expresión a otro sitio y te olvidas del `100`, reportarás 0,1 como si fuera un 0,1 % cuando en realidad es un 10 %.
:::

```python ilustrativo
# Por que una estrategia rentable en papel puede no serlo en un mercado real:
# el coste se paga en cada operacion, la ganancia solo cuando aciertas.
edge_por_operacion = 0.0008      # 8 puntos basicos de ventaja media
coste_ida_vuelta = 0.0006        # 6 puntos basicos entre comision y diferencial
operaciones_al_ano = 2500

resultado_neto = (edge_por_operacion - coste_ida_vuelta) * operaciones_al_ano
print("resultado neto anual:", round(resultado_neto, 3))

# Sube el coste a 10 pb y la misma estrategia cambia de signo.
print("con coste de 10 pb  :", round((edge_por_operacion - 0.0010) * operaciones_al_ano, 3))
```

## Errores típicos

- **Creer que el precio del gráfico es el precio al que puedes operar.** El gráfico muestra
  operaciones ya cerradas. Tú operas contra el libro: compras al *ask* y vendes al *bid*, y esa
  diferencia se paga en cada vuelta.
- **Mirar solo la comisión.** En muchos mercados la comisión es pequeña y el coste real es el
  diferencial y el impacto de tu orden. Un bróker barato con mala ejecución sale más caro que uno
  caro que ejecuta bien.
- **Ignorar el tamaño de la posición.** Un movimiento de 200 acciones y el mismo movimiento con
  20.000 no se ejecutan al mismo precio. El impacto crece con el tamaño y no es lineal.
- **Operar activos sin liquidez porque el gráfico se ve bonito.** Con un diferencial del 1 %,
  necesitas ganar un 2 % solo para empatar. Muchos valores pequeños tienen ese diferencial de
  forma permanente.
- **Olvidar que el bróker es un intermediario con reglas.** Márgenes, garantías, horarios,
  liquidación en dos días y posibilidad de que te cierren la posición. Todo eso forma parte del
  mercado, no es un detalle administrativo.
- **Suponer que el mercado te debe un precio justo.** El mercado no tiene precio justo: tiene el
  precio al que alguien está dispuesto a cruzarse contigo en ese instante.

:::practica
enunciado: Compras 500 acciones a 12,00 EUR (al ask) y las vendes a 12,10 EUR (al bid). El bróker cobra 0,15 % por punta, con un mínimo de 4 EUR. ¿Cuál es el beneficio neto y cuántos céntimos tiene que moverse el precio solo para no perder?
pista: Cada punta paga comisión sobre su propio nominal, y el movimiento de equilibrio sale de dividir el coste total entre los títulos.
solucion: Compra: 500 · 12,00 = 6.000 EUR, comisión 9,00. Venta: 500 · 12,10 = 6.050 EUR, comisión 9,08. Bruto 50 EUR; el intermediario se lleva 18,08 y quedan 31,92 EUR netos, un 0,53 % sobre la compra. Para empatar hacen falta 18,08 / 500 = 0,0362 EUR por acción, 3,6 céntimos o un 0,30 %: el movimiento debe superar con holgura el diferencial que pagas al entrar.
:::

## Comprueba que lo sabes

:::quiz
p: Compras 200 acciones a 24,50 EUR con una comisión del 0,10 % y las vendes a 25,10 EUR con la misma tarifa. ¿Cuál es el beneficio neto aproximado?
o: 120,00 EUR, porque el beneficio es la diferencia de precios por el número de acciones
o: 110,08 EUR, porque hay que descontar 4,90 EUR de compra y 5,02 EUR de venta
o: 116,00 EUR, porque la comisión se paga una sola vez por operación completa
a: 2
e: El beneficio bruto es 120 EUR, pero la comisión se paga en las dos puntas: 4,90 al comprar y 5,02 al vender. Quedan 110,08 EUR, y el 8,3 % del beneficio bruto se lo ha llevado el intermediario.
:::

:::quiz
p: ¿Qué hace un creador de mercado y por qué gana dinero?
o: Predice la dirección del precio y compra antes de que suba
o: Cotiza a la vez un precio de compra y otro de venta, y cobra esa diferencia por dar inmediatez
o: Garantiza la liquidación de las operaciones ante la cámara de compensación
a: 2
e: El creador de mercado no adivina la dirección: ofrece comprar y vender a la vez y vive del diferencial. Su riesgo es quedarse con inventario que se mueve en su contra o cruzarse con alguien mejor informado. Garantizar la liquidación es el papel de la cámara de compensación.
:::

:::trampa
Un backtest que opera en valores con poco volumen y no modela el diferencial puede dar un
resultado excelente y ser imposible de ejecutar. Antes de creerte cualquier curva, mira el volumen
diario del activo y compara el tamaño de tus órdenes con él. Si tu orden es una parte apreciable
de lo que se negocia en un día, el coste no es un detalle: es el resultado.
:::
