---
id: hechos-y-dimensiones
titulo: Tablas de hechos y dimensiones
fase: 4
nivel: intermedio
rutas: [de]
prerequisitos: [modelado-dimensional, esquema-estrella-y-copo, sql-agregaciones-y-group-by]
tags: [modelado, hechos, dimensiones, claves, grano]
resumen: La tabla de hechos guarda lo que se mide y las dimensiones lo que describe; las claves sustitutas y el grano son lo que impide que las sumas cuenten doble.
fuentes: ["Kimball y Ross (2013), 'The Data Warehouse Toolkit', cap. 2", "Kimball Group, 'Dimensionally Modeled Fact Tables' (documentación técnica)"]
---

## En una frase

Una tabla de hechos es una lista de eventos con números y referencias (claves ajenas) a las
dimensiones, y cada dimensión es el catálogo de atributos por los que quieres filtrar y agrupar
esos eventos.

## La idea

Vuelve a la hoja de cálculo de ventas, pero ahora piensa en qué harías con ella si tuvieras diez
millones de filas y cien preguntas distintas. La tentación es meter todo en una tabla: fecha,
tienda, ciudad de la tienda, producto, familia del producto, cliente, edad del cliente, unidades,
precio, importe. Funciona hasta que el nombre de la ciudad cambia, o hasta que quieres contar
clientes sin repetir y el texto está copiado en cada fila.

El modelado dimensional hace una separación tajante:

- **Tablas de hechos**: lo que **ocurre o se mide**. Muchas filas, pocas columnas, casi todo
  números y claves. Aquí viven las medidas (`unidades`, `importe`, `segundos`, `stock`) y el
  grano. Crecen deprisa: una fila por línea de pedido, por clic, por envío.
- **Tablas de dimensiones**: lo que **describe**. Pocas filas, muchas columnas, casi todo texto
  y atributos. Aquí viven los nombres, las jerarquías y las banderas (`familia`, `ciudad`,
  `es_cliente_nuevo`, `dia_semana`). Crecen despacio: un producto nuevo es una fila.

Dos propiedades hacen que esta separación funcione:

1. **La tabla de hechos es estrecha y larga; la dimensión, ancha y corta.** Esa forma es la que
   el almacenamiento columnar aprovecha: agregar `importe` recorre una sola columna de miles de
   millones de valores, y filtrar por `familia` recorre una dimensión de miles.
2. **Las claves ajenas de la tabla de hechos son claves sustitutas de las dimensiones.** No el
   código del ERP, sino el entero que genera tu almacén. Como son enteros pequeños y
   consecutivos, ocupan poco y se comprimen bien. Y son estables: si el origen renumera, tu
   histórico no se rompe.

Las medidas merecen una clasificación explícita porque decide qué puedes hacer con ellas:
**aditivas** (se suman por cualquier dimensión: `importe`, `unidades`), **semaditivas** (se
suman por unas dimensiones y no por otras: `stock` o `saldo` se suman entre tiendas, pero no a
lo largo del tiempo) y **no aditivas** (`margen_porcentual`, `precio_unitario`: se guardan como
numerador y denominador y se dividen al consultar).

Hay un tipo de tabla que se confunde a menudo con una dimensión y no lo es: la **tabla de
hechos sin hechos** (o *factless fact table*). Guarda solo claves, y sirve para responder
preguntas de existencia: «¿qué productos estuvieron en promoción ese día?». No hay nada que
sumar, pero el hecho de que una fila exista es la información.

Y otro concepto que sostiene todo el edificio: las **dimensiones conformadas**. La misma
`dim_fecha` y la misma `dim_producto` se usan en el proceso de ventas y en el de devoluciones.
Eso es lo que permite compararlos. Si cada proceso tiene su propia dimensión de producto con
criterios distintos, ninguna comparación es fiable.

## Definición formal

Sea `F` la tabla de hechos y `D₁ … Dₙ` las dimensiones.

```
F( k₁, k₂, …, kₙ, m₁, m₂, …, mₚ )
Dᵢ( kᵢ, a₁, a₂, …, a_q )
```

donde:

- **`kᵢ`** — clave sustituta de la dimensión `i` en `Dᵢ`, y clave ajena en `F`. Es un entero
  generado por el almacén: no tiene significado de negocio y **nunca se reutiliza**.
- **`mⱼ`** — medida de `F`. Numérica y, siempre que se pueda, aditiva.
- **`a`** — atributo descriptivo de la dimensión: texto, fecha, booleano o una jerarquía
  aplanada.
- **`n`** — número de dimensiones de `F` (el número de referencias).
- **`p`** — número de medidas.

Tres reglas que definen la tabla de hechos:

1. **El grano es único y se declara.** Todos los registros de `F` representan lo mismo. Mezclar
   dos granos en una tabla rompe la aditividad y ninguna cifra cuadra.
2. **Solo medidas y claves.** Nada de texto descriptivo en `F` (ocupa espacio y se repite) ni de
   atributos calculables a partir de otras medidas.
3. **La clave primaria es la combinación de claves de dimensión** que define el grano. Si dos
   dimensiones no bastan para identificar la fila de forma única, falta una dimensión (por
   ejemplo, la línea del pedido) o el grano está mal declarado.

Sobre las claves sustitutas, dos precisiones:

- **Clave natural**: el identificador del sistema de origen (`TEC-01`). Sirve para rastrear el
  dato, no para unir tablas del almacén.
- **Clave sustituta**: el entero propio (`1`, `2`, `3`…). Es lo que se une. Guardar además la
  natural como atributo de la dimensión permite auditar de dónde salió cada fila.
- **Miembro desconocido**: una fila reservada (habitualmente `-1`, «desconocido») para cuando
  una clave ajena no se puede resolver en la carga. Sin ella, un hecho huérfano rompe la unión
  y desaparece del informe, que es peor que aparecer como «desconocido».

## Ejemplo

Grano: **una fila por línea de pedido**. Tres líneas, dos pedidos, dos productos, dos tiendas.
(el `tienda_id` 10 y el 20 son claves de `dim_tienda`, que aquí no se despliega.)

`dim_fecha` (extracto):

| fecha_id | fecha | anio | mes | dia_semana | es_festivo |
| --- | --- | --- | --- | --- | --- |
| 20250131 | 2025-01-31 | 2025 | 1 | viernes | falso |

`dim_producto`:

| producto_id | codigo_natural | nombre | familia |
| --- | --- | --- | --- |
| 1 | TEC-01 | teclado | periféricos |
| 2 | RAT-02 | ratón | periféricos |

`hechos_ventas`:

| fecha_id | producto_id | tienda_id | pedido_id | unidades | importe |
| --- | --- | --- | --- | --- | --- |
| 20250131 | 1 | 10 | 5001 | 2 | 59,90 |
| 20250131 | 2 | 10 | 5001 | 1 | 12,50 |
| 20250201 | 1 | 20 | 5002 | 3 | 89,85 |

Consecuencias de este grano, con números:

- **Unidades vendidas** (aditiva): 2 + 1 + 3 = 6. Por familia: periféricos 6.
- **Importe** (aditiva): 59,90 + 12,50 + 89,85 = 162,25.
- **Número de pedidos**: no se suma `pedido_id`, se cuentan valores distintos: 5001 y 5002 son
  **2**. Contar filas daría 3, y ese 3 no es «pedidos».
- **Ticket medio**: 162,25 / 2 = 81,12. No es la media de la columna `importe`, que da 54,08,
  porque cada línea pesa igual y el pedido 5001 tiene dos líneas.
- **Precio medio por unidad**: 162,25 / 6 = 27,04. Es un cociente, no una medida aditiva.

Fíjate en la consecuencia práctica: **el mismo `importe` responde a tres preguntas distintas
según con qué lo combines**. Eso es lo que compra el modelo dimensional: medidas neutras y
contexto en las dimensiones.

## Código

```python verificable
# Medidas aditivas y cuentas de claves: el mismo hecho, cuatro respuestas distintas
HECHOS = [
    {"fecha_id": 20250131, "producto_id": 1, "pedido_id": 5001, "unidades": 2, "importe": 59.90},
    {"fecha_id": 20250131, "producto_id": 2, "pedido_id": 5001, "unidades": 1, "importe": 12.50},
    {"fecha_id": 20250201, "producto_id": 1, "pedido_id": 5002, "unidades": 3, "importe": 89.85},
]

unidades = sum(h["unidades"] for h in HECHOS)
importe = sum(h["importe"] for h in HECHOS)
pedidos = len({h["pedido_id"] for h in HECHOS})

print("unidades totales  :", unidades)                       # -> 6
print("importe total     :", round(importe, 2))             # -> 162.25
print("pedidos distintos :", pedidos)                       # -> 2
print("ticket medio      :", round(importe / pedidos, 2))   # -> 81.12
print("precio por unidad :", round(importe / unidades, 2))  # -> 27.04
print("filas contadas    :", len(HECHOS), "no son pedidos") # -> 3
```

```python verificable
# Clave sustituta frente a clave natural, y el miembro desconocido
ORIGEN = [{"codigo": "TEC-01", "unidades": 2},
          {"codigo": "RAT-02", "unidades": 1},
          {"codigo": "MON-03", "unidades": 5}]       # este producto no esta en la dimension

DIM_PRODUCTO = [(-1, "DESCONOCIDO", "Desconocido"),
                (1, "TEC-01", "teclado"),
                (2, "RAT-02", "raton")]

por_codigo = {natural: (sustituta, nombre) for sustituta, natural, nombre in DIM_PRODUCTO}
hechos = []
for fila in ORIGEN:
    sustituta, nombre = por_codigo.get(fila["codigo"], (-1, "Desconocido"))
    hechos.append({"codigo_natural": fila["codigo"], "producto_id": sustituta,
                   "nombre": nombre, "unidades": fila["unidades"]})

print("codigo_natural  producto_id      nombre  unidades")
for h in hechos:
    print(f"{h['codigo_natural']:>14}  {h['producto_id']:>11}  {h['nombre']:>11}  {h['unidades']:>8}")

huerfanas = sum(h["unidades"] for h in hechos if h["producto_id"] == -1)
print("filas sin resolver:", sum(1 for h in hechos if h["producto_id"] == -1))   # -> 1
print("unidades huerfanas:", huerfanas)                                        # -> 5
```

```sql ilustrativo
-- Dimensiones conformadas: la misma dim_producto sirve para ventas y para devoluciones.
-- Cada hecho se agrega ANTES de unir: uniendo las dos tablas de hechos directamente, cada venta
-- se multiplica por las devoluciones del producto (y al reves) y las dos cifras salen infladas.
WITH v AS (
    SELECT producto_id, sum(importe) AS ventas
    FROM hechos_ventas GROUP BY producto_id
),
d AS (
    SELECT producto_id, sum(importe) AS devoluciones
    FROM hechos_devoluciones GROUP BY producto_id
)
SELECT p.familia,
       coalesce(sum(v.ventas), 0) AS ventas,
       coalesce(sum(d.devoluciones), 0) AS devoluciones
FROM dim_producto p
LEFT JOIN v ON v.producto_id = p.producto_id
LEFT JOIN d ON d.producto_id = p.producto_id
GROUP BY p.familia;

-- Contar pedidos con grano de linea: valores distintos, nunca filas
SELECT count(*) AS lineas,
       count(DISTINCT pedido_id) AS pedidos
FROM hechos_ventas;
```

## Errores típicos

- **Meter atributos descriptivos en la tabla de hechos.** Guardar el nombre del producto en cada
  línea ocupa espacio, se desactualiza y hace imposible cambiar el nombre sin reescribir el
  histórico. El nombre va en la dimensión; el hecho lleva la clave.
- **Guardar medidas calculadas.** `ticket_medio`, `margen_porcentual` o `precio_unitario` como
  columnas del hecho no se pueden sumar y además se quedan obsoletos si cambia la regla de
  cálculo. Guarda `importe` y `unidades`; divide al consultar.
- **Usar la clave natural del origen para unir.** Un `codigo` de producto reutilizado o con
  espacios distintos rompe las uniones y deja hechos huérfanos. La clave sustituta es lo que se
  une; la natural se guarda como atributo para trazar.
- **No tener miembro desconocido.** Sin la fila `-1`, una clave ajena que no se resuelve hace
  que la fila desaparezca de los informes con `INNER JOIN`, y el total del mes baja sin que
  nadie sepa por qué. Con miembro desconocido, aparece como «Desconocido» y se ve.
- **Contar filas donde hay que contar valores distintos.** «Número de pedidos» con grano de
  línea es `COUNT(DISTINCT pedido_id)`, no `COUNT(*)`. Confundirlo infla la cifra y no hay
  forma de detectarlo mirando el resultado.
- **Sumar medidas semaditivas a lo largo del tiempo.** El stock de enero más el de febrero no es
  el stock de dos meses: o tomas la última foto, o promedias, pero no sumas. Lo mismo con saldos
  y con inventarios.
- **Dimensiones no conformadas con el mismo nombre.** Dos `dim_producto` distintas (una de
  ventas y otra de devoluciones) con criterios diferentes hacen que las comparaciones entre
  procesos sean falsas. Si se llaman igual, tienen que ser la misma.

## Comprueba que lo sabes

:::quiz
p: Con grano «una línea de pedido», ¿cómo se obtiene el número de pedidos?
o: Contando las filas de la tabla de hechos
o: Contando los valores distintos de la clave de pedido
o: Sumando la columna pedido_id
a: 2
e: Cada pedido puede tener varias líneas, así que las filas no son pedidos. Se cuentan valores distintos de pedido_id. Sumar una clave no tiene sentido (son identificadores, no cantidades) y contar filas da el número de líneas.
:::

:::quiz
p: Llega una venta cuyo producto no existe en dim_producto. ¿Qué conviene que pase?
o: Que la fila se descarte, porque un hecho sin dimensión no es válido
o: Que la clave ajena apunte a un miembro «Desconocido» reservado, para que la venta siga contando
o: Que se cree automáticamente un producto nuevo con el código recibido
a: 2
e: Descartarla hace que los totales no cuadren sin dejar rastro; crearla automáticamente llena la dimensión de duplicados y errores. El miembro desconocido mantiene el hecho y lo hace visible para corregirlo después.
:::

:::quiz
p: ¿Por qué el ticket medio no debe guardarse como medida de la tabla de hechos?
o: Porque no es aditivo: hay que calcularlo dividiendo el importe total entre el número de pedidos
o: Porque ocupa mucho espacio
o: Porque los identificadores de pedido no se pueden sumar, y el ticket tampoco
a: 1
e: El ticket medio es un cociente entre dos medidas. Si lo guardas por fila y luego lo promedias o lo sumas, obtienes un número que no corresponde a ningún total real. Se guarda importe y se cuentan pedidos, y el cociente se hace al final, sobre los agregados.
:::

:::practica
enunciado: Una cadena de gimnasios quiere analizar el uso de sus instalaciones. Registra cada entrada con el socio, la fecha y hora, la sede y el tipo de actividad. Quiere responder cuántas entradas por sede y mes, cuántos socios distintos por actividad y cuánto tiempo medio por visita. Define el grano, las medidas y las dimensiones.
pista: Distingue lo que se mide (números que sumas) de lo que describe (atributos por los que filtras), y decide qué combinación hace única una fila.
solucion: El grano es «una fila por entrada de un socio en una sede»: la combinación socio, instante de entrada y sede identifica la visita. Las medidas son duracion_minutos (aditiva) y un contador de entradas (aditiva, valor 1). Las dimensiones son dim_socio (con alta, tipo de abono, edad), dim_sede (ciudad, aforo), dim_fecha (con hora, día de la semana, festivo) y dim_actividad (nombre, tipo, monitor). Las preguntas se responden así: entradas por sede y mes con sum(entradas); socios distintos por actividad con count(distinct socio_id); duración media por visita con sum(duracion_minutos) / count(*), nunca con la media de una columna de medias. Ojo con la edad del socio: es un atributo que cambia, así que hay que decidir si se guarda la edad en el momento de la visita o la fecha de nacimiento en la dimensión.
:::
