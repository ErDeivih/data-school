---
id: nubes-y-servicios-gestionados
titulo: Nubes y servicios gestionados
fase: 4
nivel: intermedio
rutas: [de]
prerequisitos: [almacenamiento-de-objetos, coste-y-optimizacion, data-warehouse]
tags: [nube, computo, coste, servidor]
resumen: Alquilar computo, almacen y bases analiticas en vez de montarlos: que se delega, quien paga el tiempo ocioso y por qué el modelo de cobro decide la factura.
fuentes: ["Reis y Housley (2022), 'Fundamentals of Data Engineering', cap. 4", "Kleppmann (2017), 'Designing Data-Intensive Applications', cap. 1"]
---

## En una frase

Un servicio gestionado es un trozo de tu plataforma que otro opera: tú pagas por lo que usas y
el proveedor se encarga del mantenimiento, los parches y la disponibilidad. Lo que decide la
factura no es el volumen de datos, sino el **modelo de cobro**.

## La idea

Montar un servidor propio es tener un coche: cómpralo, cambia el aceite, aparca, y cuando no lo
usas sigue ocupando sitio y pagando seguro. Alquilar computo es pedir taxis: pagas exactamente
el trayecto, no hay que mantener nada, y el trayecto corto sale baratísimo... hasta que lo pides
todos los días a la misma hora, y entonces te sale más caro que el coche.

Esa es toda la decisión. Y hay tres formas de pedirlo, cada una con un modelo de cobro distinto:

- **Pago por uso:** se factura por tiempo de máquina encendida o por trabajo ejecutado. Perfecto
  para una carga intermitente, malísimo para una carga estable, porque estás pagando la comodidad
  todos los meses.
- **Capacidad reservada:** se compra una cuota fija por adelantado y el precio por hora baja.
  Gana cuando el consumo sostenido supera un umbral que se calcula en dos líneas: cuota dividida
  entre el precio por uso.
- **Consumo puro, sin servidor:** el proveedor enciende y apaga por ti y factura por invocación,
  pero tiene un techo de capacidad. Con un pico de tráfico muy por encima de ese techo, el
  servicio se queda corto y hay que escalar el trabajo, lo que multiplica el coste.

Lo mismo pasa con el almacén analítico. **BigQuery**, **Snowflake** y **Redshift** hacen el
trabajo que antes te obligaba a montar un clúster con Hadoop: guardan tablas, ejecutan SQL a
escala y reparten el trabajo entre máquinas. Se separan por cómo facturan. Los que cobran por
bytes escaneados te dan la comodidad de no administrar nada y te hacen pensar antes de lanzar una
consulta cara: olvidar un filtro en una tabla de 4 TB se paga. Los que cobran por tiempo de
cómputo mantienen la máquina encendida mientras el almacén esté activo, así que la factura sigue
corriendo aunque no llegue ninguna consulta. Por eso `SELECT` sin filtros no es solo lento: es
caro, y en un almacén por bytes la diferencia entre leer 4 GB y 4 TB es de mil veces.

También hay que saber qué **se delega** y qué no. El proveedor asume el hardware, los parches,
la replicación, las copias y la disponibilidad de la infraestructura. No asume tu modelo de
datos, tus permisos de fila, tu coste de consultas mal escritas ni el compromiso de un contrato
con tu consumidor. Eso sigue siendo tuyo, y delegarlo sin pensarlo es la forma más rápida de
convertir una migración a la nube en una factura sorpresa.

## Definición formal

Solo consideramos el coste del cómputo; el almacén se calcula como en
[[almacenamiento-de-objetos|almacenamiento de objetos]]. Con tres modelos sobre la mesa:

:::formula
coste_uso = c · Q   ·   coste_reserva = R   ·   coste_consumo = u · Q  si  Q ≤ Q_max
:::

Y por encima de `Q_max`, el consumo puro deja de ser una recta: `coste_consumo = u · Q_max + k · (Q − Q_max)`,
con `k` mayor que `u`, porque el proveedor tiene que repartir el trabajo que ya no cabe.

:::parametros
| Símbolo | Qué es | Unidades | Si sube... |
| --- | --- | --- | --- |
| `Q` | Trabajo del mes: consultas, invocaciones o tiempo de máquina | miles de unidades | Sube el coste por uso de forma lineal y hace ganar a la cuota fija |
| `c` | Precio por unidad de trabajo en el modelo de pago por uso | moneda por mil unidades | Desplaza el umbral hacia abajo: reservar compensa antes |
| `R` | Cuota fija mensual de la capacidad reservada | moneda por mes | Sube el coste constante; si es alta, solo compensa con mucha carga sostenida |
| `u` | Precio por unidad en el modelo de consumo puro | moneda por unidad | Como `c`, pero el servicio no garantiza el mismo techo de capacidad |
| `k` | Precio por unidad por encima del techo del consumo puro | moneda por unidad | Restricción `k > u`: es el recargo del trabajo que ya no cabe, y si sube la reserva gana antes |
| `Q_max` | Volumen a partir del cual el servicio sin servidor deja de dar más y el trabajo se reparte | miles de unidades | Si es pequeño, el pico diario se paga multiplicado y la reserva gana antes |
| `Q_cruce` | Punto en que reservar empieza a ser más barato: `R / c` | miles de unidades | Es la cifra que hay que calcular antes de firmar nada |
:::

La decisión, entonces, no es «¿nube o servidor?» sino «¿cuál de estos tres modelos se parece a mi
curva de carga?». Si la carga es plana y predecible, el pago por uso es el más caro de los tres.

:::figura
fichero: nubes-modelos-de-cobro
pie: Fíjate en dónde se cruzan las líneas, no en su altura final. Con rachas aisladas el pago por consulta es imbatible; en cuanto la carga se vuelve diaria y estable, la cuota reservada lo aplasta: en el extremo del gráfico, 1000 miles de consultas al mes (un millón), la diferencia es de decenas de veces. Y la curva verde enseña el otro límite: el sin servidor escala solo hasta su techo, y a partir de ahí el mismo tráfico cuesta varias veces más.
fuente: figuras/nubes-y-servicios-gestionados-1.py
:::

## Ejemplo

Un equipo lanza 400 000 consultas al mes. Con un precio de 6 unidades por cada 1000 consultas y
una cuota reservada de 100 unidades al mes:

- Pago por uso: 400 · 6 = **2400** unidades.
- Reserva: **100** unidades, uses mucho o poco.
- Umbral: 100 / 6 = **17** mil consultas al mes. Por encima de esa cifra -y 400 está muy por
  encima- el pago por uso solo tiene sentido si la carga es tan irregular que la cuota se
  quedaría ociosa buena parte de los meses.

Con 10 000 consultas al mes la conclusión se invierte: 10 · 6 = 60 frente a una cuota de 100.
Ahí lo barato es no reservar nada, porque estás comprando capacidad que no usas. Y si el
servicio sin servidor tiene su techo en 700 000 consultas, los picos de campaña obligan a
repartir el trabajo, que es exactamente cuando su coste se dispara.

## Código

```python verificable
import numpy as np

# Tres formas de conseguir el mismo computo: pagar por consulta, reservar capacidad fija
# o dejar que el proveedor escale por uso (sin servidor) hasta su techo de capacidad.
consulta = 6.0        # coste de cada 1000 consultas
reserva = 100.0       # cuota mensual fija de la capacidad reservada
techo = 150.0         # coste de consumo cuando el trafico llega al techo

q = np.array([10.0, 100.0, 500.0, 1000.0])     # consultas al mes, en miles
por_consulta = consulta * q
con_reserva = np.full_like(q, reserva)
sin_servidor = np.full_like(q, techo)           # el consumo ya esta en el techo a 700 mil
sin_servidor = np.where(q > 700, techo * (1 + 2.6 * (q - 700) / 300), sin_servidor)

total = np.vstack([por_consulta, con_reserva, sin_servidor])
for i, nombre in enumerate(("por consulta", "reservada   ", "sin servidor")):
    print(f"{nombre}  " + "  ".join(f"{v:8.1f}" for v in total[i]))
mas_barato = [("por consulta", "reservada", "sin servidor")[int(j)] for j in total.argmin(axis=0)]
print("mas barato en cada caso:", mas_barato)
# -> por consulta      60.0     600.0    3000.0    6000.0
# -> reservada        100.0     100.0     100.0     100.0
# -> sin servidor     150.0     150.0     150.0     540.0
# -> mas barato en cada caso: ['por consulta', 'reservada', 'reservada', 'reservada']
print(f"reservar gana a pagar por uso a partir de {reserva / consulta:.0f} mil consultas al mes")
# -> reservar gana a pagar por uso a partir de 17 mil consultas al mes
```

:::claves
- `np.vstack` pega los tres vectores como tres **filas** de una matriz. `total.argmin(axis=0)`
  busca el mínimo **por columna**, es decir el modelo más barato en cada nivel de tráfico. Si
  pones `axis=1`, obtienes el mínimo de cada fila y la respuesta deja de tener sentido: ese
  número no significa nada.
- `np.full_like(q, reserva)` crea un vector de la misma forma y tipo que `q` relleno con la
  cuota. Sin `_like` habría que escribir la forma a mano, y con `np.full(4, reserva)` el
  resultado sería un vector de enteros que pierde los decimales.
- `np.where(q > 700, ...)` es una condición vectorizada: recorre el array y elige un valor u
  otro según el test, sin bucle. La rama de arriba multiplica por `(q - 700) / 300`, así que en
  `q = 700` el coste sigue siendo exactamente el techo y la curva es continua.
- `total.argmin(axis=0)` devuelve **índices**, no nombres. El truco de la tupla
  `("por consulta", "reservada", "sin servidor")[int(j)]` traduce el índice a texto; sin el `int`
  NumPy devuelve un entero de su propio tipo y el indexado de tuplas funciona igual, pero deja de
  ser legible al depurar.
- `f"{v:8.1f}"` reserva ocho caracteres por número y alinea a la derecha: por eso las columnas
  salen rectas. Cambiar `8.1f` por `8.2f` cambia el aspecto, no el cálculo.
:::

```python verificable
# Presupuesto antes de gastar: cuanto va a leer de verdad una consulta.
# Los almacenes que cobran por bytes escaneados hacen que esto sea dinero, no curiosidad.
bytes_totales = 4 * 1024 ** 3       # 4 GB de tabla, 4 anos de historia
dias = 4 * 365
bytes_del_mes = bytes_totales / dias * 31
print(f"tabla entera      {bytes_totales / 1024**3:.1f} GB")                    # -> 4.0 GB
print(f"un mes si esta particionada por fecha  {bytes_del_mes / 1024**3:.3f} GB")  # -> 0.085 GB
print(f"la misma consulta sin particionar cuesta ~{bytes_totales / bytes_del_mes:.0f} veces mas")
# -> la misma consulta sin particionar cuesta ~47 veces mas
```

## Errores típicos

- **Creer que gestionado significa barato.** Significa que no administras. Una consulta sin
  filtro sigue leyendo todo, y en un almacén facturado por bytes eso es mil veces más caro. La
  pereza al escribir SQL se convierte en factura.
- **Dejar el almacén encendido sin consultas.** Los modelos de cómputo facturan mientras el
  servicio está activo, no mientras hay carga. Un almacén que solo se usa de 8 a 10 de la mañana
  y sigue encendido el resto del día paga 24 horas por 2 de trabajo.
- **Suponer que el sin servidor escala sin límite.** Tiene un techo de capacidad; por encima de
  él, el proveedor reparte o encola el trabajo y el coste por unidad sube. Es la causa habitual
  del pico de factura en una campaña.
- **Reservar capacidad para toda la carga cuando solo el 30 % es estable.** La cuota cubre el
  suelo y el resto se paga por uso: reservar de más es comprar capacidad ociosa con descuento.
- **No poner un tope de gasto ni una alerta.** El proveedor no te va a parar. Sin alerta de
  presupuesto y sin límite por consulta escaneada, un `SELECT` de madrugada puede costar más que
  el mes entero, y te enteras en la factura.

:::practica
enunciado: Tu equipo analiza 3 TB al día con una cuota reservada de 800 unidades al mes, y cada consulta cuesta 5 unidades por TB escaneado en el modelo por uso. ¿Qué modelo eliges, y cuánto ahorras?
pista: Pasa el trabajo a unidades comparables y compara el coste del mes con la cuota.
solucion: 30 días por 3 TB son 90 TB al mes. Por uso: 90 · 5 = 450 unidades. La reserva cuesta 800, así que el pago por uso es el más barato y ahorra 350 unidades al mes. El cruce está en 800 / 5 = 160 TB al mes: con ese tráfico diario de 3 TB no lo alcanzas. Reservar tendría sentido a partir de unos 5,3 TB diarios.
:::

:::aviso
Antes de reservar capacidad, mide al menos tres meses de carga real. La cuota se firma por
periodos de uno o tres años y el compromiso se paga aunque el equipo se disuelva, la carga se
mueva a otro servicio o el producto se cancele. El descuento solo es descuento si el consumo
existe.
:::

## Comprueba que lo sabes

:::quiz
p: Tu carga es estable: la misma cantidad de trabajo todos los días del año. ¿Qué modelo de cobro sale más caro y por qué?
o: La capacidad reservada, porque se paga aunque no se use
o: El pago por uso, porque estás pagando la comodidad todos los meses y el consumo no baja nunca
o: El consumo sin servidor, porque factura por invocación
a: 2
e: Con carga plana el coste por uso crece linealmente sin valle que lo compense, y la reserva reparte una cuota fija entre más trabajo. El sin servidor también sufre, pero su problema es el techo de capacidad, no la facturación por invocación.
:::

:::quiz
p: Pagas 4 unidades por cada 1000 consultas y la cuota reservada es de 120 unidades al mes. ¿Cuál es el umbral a partir del cual reservar es más barato?
o: 30 000 consultas al mes
o: 120 000 consultas al mes
o: 480 consultas al mes
a: 1
e: El umbral es la cuota dividida entre el precio por unidad: 120 / 4 = 30 mil consultas, es decir 30 000. Las otras respuestas salen de multiplicar en vez de dividir o de confundir miles con unidades.
:::

:::quiz
p: Tienes el almacén gestionado encendido 24 horas y se usa dos horas al día. ¿Cuál es el arreglo correcto?
o: Contratar menos capacidad reservada para el mismo servicio encendido
o: Apagar el almacén cuando no se usa o pasar a un modelo que facture por trabajo ejecutado
o: Pasar los datos a almacenamiento de objetos, que siempre es más barato
a: 2
e: Si el cobro es por tiempo de servicio activo, la factura la fija el tiempo encendido, no la capacidad contratada. Apagarlo o pagar por trabajo ejecutado ataca la causa. Mover los datos a objetos abarata el almacén, no el cómputo ocioso.
:::
