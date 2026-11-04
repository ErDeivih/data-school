---
id: modelado-dimensional
titulo: Modelado dimensional
fase: 4
nivel: intermedio
rutas: [de]
prerequisitos: [oltp-vs-olap, sql-modelado-y-normalizacion, sql-joins]
tags: [modelado, dwh, kimball, granularidad]
resumen: Organizar los datos analíticos en hechos y dimensiones alrededor de un grano claro: el modelo que entienden las herramientas de BI y que sobrevive a los años.
fuentes: ["Kimball y Ross (2013), 'The Data Warehouse Toolkit', caps. 1-2"]
---

## En una frase

El modelado dimensional separa lo que se mide (hechos, en tablas largas y estrechas) de lo que
describe la medición (dimensiones, en tablas anchas y cortas), y empieza siempre por decidir qué
representa una fila.

## La idea

Piensa en una hoja de cálculo llena de ventas. Tiene la fecha, la tienda, el cliente, el
producto, las unidades y el importe. Es cómoda hasta que quieres contar cosas: ¿cuántos clientes
distintos compraron en Madrid en 2025 sin repetir? ¿cuántos productos se vendieron en tiendas
que abrieron ese año? Con texto repetido en cada fila, cada pregunta se convierte en una
trampa de duplicados.

El modelado dimensional resuelve eso con una idea sencilla: **cada tabla guarda una sola cosa**.
Unas tablas guardan **lo que ocurre** (hechos: una venta, un clic, un envío) con números
medibles y referencias a todo lo demás. Otras guardan **el contexto** (dimensiones: producto,
tienda, cliente, fecha) con texto descriptivo y atributos para filtrar y agrupar.

La forma que resulta tiene el hecho en el centro y las dimensiones alrededor, y por eso se llama
esquema en estrella. La diferencia con la base de la aplicación es deliberada: allí se normaliza
para no repetir nada al escribir; aquí se **desnormaliza** para que una consulta se resuelva con
una unión por dimensión y nada más.

Antes de dibujar nada hay que declarar el **grano**: qué representa exactamente una fila de la
tabla de hechos. «Una fila por línea de pedido», «una fila por producto y día», «una fila por
suscripción y mes». Este paso se hace antes que los demás y no se puede saltar, porque decide
todo lo que viene después:

- Si el grano es la línea de pedido, la tabla tiene muchos millones de filas y permite analizar
  por producto; el ticket medio hay que calcularlo sumando.
- Si el grano es el pedido, hay diez veces menos filas, pero pierdes el detalle de producto: el
  análisis por familia ya no es posible.
- Si mezclas los dos granos en la misma tabla, las sumas de importe cuentan doble y ningún
  informe cuadra con otro. Este es el error que más tiempo cuesta en un almacén de datos.

Dos tipos de hechos que conviene distinguir desde el principio: **transaccionales** (una fila
por evento, crecen sin parar) y **periódicos** (una fila por entidad y periodo, con una foto del
estado: saldo a fin de mes, stock a cierre). Los segundos se usan para preguntar «cuánto había»
en vez de «cuánto pasó», y no se suman igual: sumar el stock de doce meses no significa nada.

## Definición formal

Un modelo dimensional se define por una tupla `(G, F, D, M)`:

- **Grano `G`**: la frase que dice qué representa una fila de la tabla de hechos. Toda la
  validez del modelo depende de que sea única y constante.
- **Tabla de hechos `F`**: contiene la **clave** de cada dimensión (clave ajena) y las
  **medidas** (columnas numéricas aditivas o semaditivas). Ejemplo: `ventas(fecha_id,
  producto_id, tienda_id, unidades, importe)`.
- **Dimensiones `D₁ … Dₙ`**: tablas con una **clave sustituta** (un entero propio del almacén,
  no el identificador del sistema de origen) y los **atributos** descriptivos.
  Ejemplo: `dim_producto(producto_id, codigo, nombre, familia, marca)`.
- **Medidas `M`**: las columnas numéricas de `F`. Se clasifican así:
  - **Aditivas**: se pueden sumar por cualquier dimensión (importe, unidades).
  - **Semaditivas**: se pueden sumar por unas dimensiones y no por otras (saldo, stock: sumables
    entre tiendas, no a lo largo del tiempo).
  - **No aditivas**: no se suman nunca (margen porcentual, precio unitario, ratio). Se guardan
    como numerador y denominador y se dividen al consultar.

Reglas de diseño que resumen la práctica:

1. **Claves sustitutas**, no claves naturales. Un `producto_id` entero propio del almacén
   permite versionar un producto (cambió de familia) sin tocar el hecho y sin depender de que
   el ERP no reutilice códigos.
2. **Dimensiones conformadas**: las mismas dimensiones se reutilizan en varios procesos de
   negocio. `dim_fecha` y `dim_producto` son iguales para ventas y para devoluciones, y eso es
   lo que permite compararlas entre sí.
3. **La dimensión de fecha es una tabla, no una función.** Con columnas como `anio`, `mes`,
   `dia_semana`, `es_festivo`, `trimestre`. Así el filtro es una unión y todas las herramientas
   agrupan igual.
4. **Un atributo va donde vive.** Si un atributo cambia con el tiempo (la familia de un
   producto, la ciudad de un cliente), hay que decidir si se guarda el valor de hoy o el de
   entonces. Eso es exactamente lo que resuelven las dimensiones que cambian.

El esquema tiene una propiedad que se busca a propósito: **la consulta más frecuente es una
unión de `F` con una o dos dimensiones y una agregación**. Cualquier cosa que obligue a unir
seis tablas para un informe básico es una señal de que el modelo está mal.

## Ejemplo

Comercio con ventas de tres líneas. Primero el grano, después las tablas.

**Grano**: una fila por línea de pedido (producto vendido en una operación concreta).

`dim_producto`:

| producto_id | código | nombre | familia |
| --- | --- | --- | --- |
| 1 | TEC-01 | teclado | periféricos |
| 2 | RAT-02 | ratón | periféricos |
| 3 | MON-03 | monitor | pantallas |

`dim_tienda`:

| tienda_id | nombre | ciudad | comunidad |
| --- | --- | --- | --- |
| 10 | Centro | Madrid | Madrid |
| 20 | Norte | Bilbao | País Vasco |

`hechos_ventas` (grano: una línea de pedido):

| fecha_id | producto_id | tienda_id | pedido_id | unidades | importe |
| --- | --- | --- | --- | --- | --- |
| 20250131 | 1 | 10 | 5001 | 2 | 59,90 |
| 20250131 | 2 | 10 | 5001 | 1 | 12,50 |
| 20250201 | 1 | 20 | 5002 | 3 | 89,85 |

Lecturas que salen directas:

- **Importe por familia**: unir `hechos_ventas` con `dim_producto` y agregar: periféricos
  59,90 + 12,50 + 89,85 = 162,25; pantallas 0.
- **Ticket medio por pedido**: como el grano es la línea, hay dos filas del pedido 5001. El
  ticket no es la media de `importe` (que daría (59,90 + 12,50 + 89,85) / 3 = 54,08), sino la
  suma por pedido dividida entre pedidos: 162,25 / 2 = 81,12.
- **Unidades por ciudad**: unir con `dim_tienda`: Madrid 3, Bilbao 3.

El ejemplo del ticket medio es el que enseña por qué el grano manda: **la medida aditiva es el
importe, no el ticket**. El ticket se calcula, no se guarda.

## Código

```python verificable
# El grano decide que puedes responder: la misma tabla, cuatro preguntas
LINEAS = [
    {"pedido": 5001, "producto": 1, "tienda": 10, "unidades": 2, "importe": 59.90},
    {"pedido": 5001, "producto": 2, "tienda": 10, "unidades": 1, "importe": 12.50},
    {"pedido": 5002, "producto": 1, "tienda": 20, "unidades": 3, "importe": 89.85},
]

total = sum(l["importe"] for l in LINEAS)
por_pedido = {}
for l in LINEAS:
    por_pedido[l["pedido"]] = por_pedido.get(l["pedido"], 0) + l["importe"]

print("importe total      :", round(total, 2))                                # -> 162.25
print("pedidos distintos  :", len(por_pedido))                                 # -> 2
print("ticket medio       :", round(sum(por_pedido.values()) / len(por_pedido), 2))   # -> 81.12
print("media de la columna:", round(total / len(LINEAS), 2))                   # -> 54.08
print("precio por unidad  :", round(total / sum(l["unidades"] for l in LINEAS), 2))   # -> 27.04
```

```python verificable
# Dimensiones conformadas: la misma dim_tienda sirve para ventas y para devoluciones
PRODUCTO = {1: ("TEC-01", "teclado", "perifericos"), 2: ("RAT-02", "raton", "perifericos")}
TIENDA = {10: ("Centro", "Madrid"), 20: ("Norte", "Bilbao")}

VENTAS = [(1, 10, 59.90), (2, 10, 12.50), (1, 20, 89.85)]
DEVOLUCIONES = [(2, 10, 12.50), (2, 20, 9.99)]

def por_ciudad(filas):
    acumulado = {}
    for producto, tienda, importe in filas:
        ciudad = TIENDA[tienda][1]
        acumulado[ciudad] = round(acumulado.get(ciudad, 0) + importe, 2)
    return acumulado

ventas_ciudad = por_ciudad(VENTAS)
devoluciones_ciudad = por_ciudad(DEVOLUCIONES)

print("ventas por ciudad      :", ventas_ciudad)          # -> {'Madrid': 72.4, 'Bilbao': 89.85}
print("devoluciones por ciudad:", devoluciones_ciudad)    # -> {'Madrid': 12.5, 'Bilbao': 9.99}
print("tasa de devolucion     :", round(sum(devoluciones_ciudad.values())
                                         / sum(ventas_ciudad.values()), 4))   # -> 0.1386
```

```python verificable
# Medidas no aditivas: el margen no se suma, se recalcula sobre los totales
LINEAS = [
    {"producto": "teclado", "ingreso": 59.90, "coste": 36.00},
    {"producto": "raton", "ingreso": 12.50, "coste": 6.00},
    {"producto": "monitor", "ingreso": 179.00, "coste": 140.00},
    {"producto": "teclado", "ingreso": 29.95, "coste": 18.00},
]

suma_de_margenes = sum((l["ingreso"] - l["coste"]) / l["ingreso"] for l in LINEAS)
ingreso_total = sum(l["ingreso"] for l in LINEAS)
coste_total = sum(l["coste"] for l in LINEAS)

print("suma de margenes fila a fila:", round(suma_de_margenes, 3))
print("margen real                 :", round((ingreso_total - coste_total) / ingreso_total, 3))
print("ingreso total:", round(ingreso_total, 2), "coste total:", round(coste_total, 2))
# -> suma de margenes fila a fila: 1.536
# -> margen real                 : 0.289
# -> ingreso total: 281.35 coste total: 200.0
# Ese 1.536 es la suma de cuatro porcentajes, no el margen de nada: el margen real es 0.289.
```

```sql ilustrativo
-- El esquema en estrella se consulta asi: una union por dimension usada
SELECT p.familia,
       t.comunidad,
       sum(h.importe) AS importe,
       sum(h.unidades) AS unidades
FROM hechos_ventas h
JOIN dim_producto p ON p.producto_id = h.producto_id
JOIN dim_tienda   t ON t.tienda_id = h.tienda_id
JOIN dim_fecha    f ON f.fecha_id = h.fecha_id
WHERE f.anio = 2025
GROUP BY p.familia, t.comunidad
ORDER BY importe DESC;
```

## Errores típicos

- **No declarar el grano.** Sin la frase «una fila por…», cada desarrollador asume uno distinto
  y las sumas dejan de cuadrar entre informes. Escríbelo en la documentación de la tabla, no en
  la cabeza de quien la creó.
- **Mezclar granos en una tabla de hechos.** Si unas filas son líneas de pedido y otras son
  resúmenes de pedido, sumar `importe` cuenta doble una parte de la realidad. Es el error más
  caro y el más difícil de detectar, porque los números siguen siendo plausibles.
- **Usar claves naturales del sistema de origen.** El día que el ERP reutiliza un código de
  producto o el cliente cambia de identificador, el histórico se corrompe. La clave sustituta
  es tuya y no cambia nunca.
- **Guardar ratios como medida.** El margen, el precio medio o el porcentaje de conversión no
  se suman. Guarda numerador y denominador (ingreso y coste) y divídelos al consultar; si no,
  el total de un mes será la suma de doce porcentajes, que no significa nada.
- **Una tabla de hechos sin contexto.** Si el hecho no tiene dimensiones por las que filtrar ni
  medidas que sumar, probablemente deba ser una columna más de otra tabla.
- **Confundir dimensión con catálogo vivo.** La dimensión del almacén es una copia con historia,
  no una vista del sistema de origen. Si la lees en vivo, los informes del pasado cambian de
  significado cuando alguien edita un producto hoy.
- **Nombres de atributo que no significan nada.** `campo1`, `tipo`, `flag`: nadie sabe qué
  filtrar con ellos. Un nombre de dimensión debe leerse como una frase (`familia_producto`,
  `es_cliente_nuevo`).

## Comprueba que lo sabes

:::quiz
p: La tabla de hechos tiene grano «una línea de pedido» y quieres el ticket medio. ¿Cómo se calcula?
o: Con la media de la columna importe
o: Sumando el importe por pedido y dividiendo entre el número de pedidos
o: Sumando el importe y dividiendo entre el número de líneas
a: 2
e: Con grano de línea, cada pedido pesa lo que pesan sus líneas, así que la media directa de importe mezcla pedidos grandes y pequeños. Hay que agregar primero a nivel de pedido y promediar después. Dividir entre el número de líneas da el importe medio por línea, no por pedido.
:::

:::quiz
p: ¿Por qué una medida como el margen porcentual no debe guardarse como columna de la tabla de hechos?
o: Porque ocupa demasiado espacio
o: Porque no es aditiva: sumarla por meses daría la suma de porcentajes, que no significa nada
o: Porque las tablas de hechos solo admiten números enteros
a: 2
e: Las medidas aditivas se suman por cualquier dimensión, y el margen no. Guarda numerador y denominador (ingreso y coste) y calcula el ratio al final, sobre los totales. El espacio no es el problema.
:::

:::quiz
p: ¿Para qué sirve una clave sustituta en una dimensión?
o: Para que la dimensión ocupe menos y sea más rápida
o: Para tener un identificador propio del almacén, estable, que permita versionar atributos sin tocar los hechos
o: Para cifrar los identificadores del sistema de origen
a: 2
e: La clave sustituta es un entero que genera el almacén: no cambia nunca, no depende de que el origen reutilice códigos y permite tener dos versiones del mismo producto (antes y después de cambiar de familia). No es una medida de rendimiento ni de seguridad.
:::

:::practica
enunciado: Un periódico registra lecturas de artículos. Cada fila actual es un artículo con sus visitas totales del mes. Quieres poder analizar visitas por sección, por dispositivo y por día. ¿Cuál es el grano adecuado y qué tablas necesitas?
pista: Pregúntate qué combinación de cosas hace única una fila y qué atributos cambian en el tiempo.
solucion: El grano correcto es «una fila por artículo, día y dispositivo»: es la combinación más fina que permite responder las tres preguntas. La tabla de hechos tendría fecha_id, articulo_id, dispositivo_id y las medidas visitas y segundos_leidos. Las dimensiones serían dim_articulo (con la sección, el autor y la fecha de publicación), dim_fecha (con día de la semana y festivos) y dim_dispositivo. Si guardas solo el total del mes por artículo, pierdes el detalle de día y de dispositivo para siempre, y para recuperarlo habría que reprocesar los datos en crudo.
:::
