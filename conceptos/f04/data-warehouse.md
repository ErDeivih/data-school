---
id: data-warehouse
titulo: Data warehouse
fase: 4
nivel: intermedio
rutas: [de, ds]
prerequisitos: [oltp-vs-olap, modelado-dimensional, etl-vs-elt]
tags: [almacenamiento, bi, gobierno, historico]
resumen: El almacén curado donde los datos de muchos sistemas se limpian, se integran y se modelan una sola vez para que toda la empresa use las mismas cifras.
fuentes: ["Kimball y Ross (2013), 'The Data Warehouse Toolkit'", "Inmon (2005), 'Building the Data Warehouse'"]
---

## En una frase

Un **data warehouse** es la base de datos analítica donde los datos de todos los sistemas de la
empresa se integran, se limpian y se modelan una sola vez, de forma que «cliente», «venta» o
«país» signifiquen exactamente lo mismo para todo el mundo y las cifras de dos informes
distintos cuadren.

## La idea

El problema que resuelve no es la velocidad, es la **contradicción**. Cinco sistemas, cada uno
con su idea de lo que es un cliente:

- El CRM identifica al cliente con el código `4471`, el país como `ES` y la ciudad en texto
  libre.
- Facturación lo identifica con `C-004471`, el país como `España` y guarda los importes en
  céntimos.
- El e-commerce lo identifica por el correo electrónico y guarda las fechas en UTC.
- Soporte tiene clientes que en los otros tres no existen, porque son prospectos.

Cuando el director pide «ventas por país del último trimestre», cada departamento da un número
distinto y todos tienen razón **en su sistema**. La reunión se convierte en una discusión sobre
quién cuenta bien en lugar de sobre el negocio. El almacén existe para que esa discusión no
ocurra: se define una única tabla de dimensiones de cliente, con una única lista de códigos de
país, y todo lo demás cuelga de ahí.

Inmon resumió las propiedades de un almacén en cuatro palabras, y siguen siendo la mejor
prueba de si lo que tienes merece ese nombre:

- **Orientado a temas**, no a aplicaciones. Se organiza por cliente, producto o venta, no por
  «lo que necesita el módulo de facturación».
- **Integrado.** Un solo código de país, una sola moneda, una sola definición de «cliente
  activo», aunque los orígenes usen cinco.
- **No volátil.** Se carga y se consulta; no se actualiza fila a fila mientras alguien lee. Los
  cambios llegan como cargas nuevas, con su fecha.
- **Variable en el tiempo.** Guarda el histórico con su horizonte temporal, no solo la foto de
  ahora.

La diferencia con una copia de la base de producción es justo esa palabra: **integrado**. Una
copia tiene los mismos datos mal normalizados y las mismas trampas, solo que en otro servidor.

Hay dos escuelas clásicas de cómo construirlo. La de Inmon propone un núcleo normalizado en
tercera forma normal del que se derivan los data marts; la de Kimball propone directamente
modelos dimensionales ([[esquema-estrella-y-copo|esquema en estrella]]) con dimensiones
conformadas y una matriz de bus que dice qué procesos comparten qué dimensiones. En la práctica
casi todo lo que verás es una mezcla por capas: *staging* (copia cruda del origen), núcleo
integrado, marts por dominio y una capa semántica encima con las métricas ya definidas.

Y conviene tener claro lo que **no** es: no es el lago ([[data-lake]]), que guarda el crudo; no
es la base de la aplicación ([[oltp-vs-olap]]); y no es un sitio donde volcar todo «por si
acaso». Un almacén sin grano declarado y sin gobierno es un conjunto de tablas grandes.

## Definición formal

Los elementos del modelo y sus invariantes:

- **Grano**: la frase que dice qué representa **una fila** de la tabla de hechos. «Una fila es
  una línea de pedido», «una fila es el stock de un producto en un almacén al cierre del día».
  Si no puedes escribirla en una frase, la tabla tiene dos granos mezclados.
- **Hecho**: la tabla de eventos o medidas, con claves foráneas a las dimensiones y las medidas
  numéricas. Suele ser mucho más alta que ancha.
- **Dimensión**: el contexto descriptivo (cliente, producto, tiempo, geografía). Es ancha y
  relativamente corta, y puede tener historia ([[scd-dimensiones-cambiantes]]).
- **Dimensión conformada**: una dimensión compartida por varios procesos, con la misma clave y
  el mismo significado. Es lo que permite comparar dos marts sin reconciliar a mano.

Las dos comprobaciones que un almacén debe pasar siempre:

:::formula
sum(hechos) = sum(origen) · toda fila del hecho apunta a una dimensión existente
:::

La primera es la **reconciliación**: el total del almacén tiene que coincidir con el de los
orígenes, al céntimo, para el mismo periodo. La segunda es la **integridad referencial**: sin
filas huérfanas y sin claves nulas en los hechos. Un almacén que no se reconcilia no es un
almacén, es una opinión.

## Ejemplo

Dos orígenes que hablan de los mismos dos clientes con vocabularios distintos:

| Origen | Cliente | País | Importe |
| --- | --- | --- | --- |
| CRM | 4471 | ES | 1.205,00 EUR |
| Facturación | C-004471 | España | 120500 céntimos |

Sin integrar, un `GROUP BY` por país produce dos grupos (`ES` y `España`) y una misma venta
aparece dos veces si además se une por el cliente. Después de la carga integrada:

- `dim_pais` tiene una fila por código ISO: `ES` con nombre `España`.
- `hechos_ventas` guarda una fila por línea de factura, con el importe convertido a euros y la
  clave de país, no el texto.
- El informe por país devuelve **un solo grupo**: `ES`, 2 ventas, 200,50 EUR.

Ese «un solo grupo» es todo el valor del almacén. Si al terminar la carga el total del almacén
no coincide con la suma de los orígenes, la carga se marca como fallida y no se publica: mejor
una tabla de ayer que una de hoy equivocada.

## Código

```sql verificable
-- Dos origenes con vocabularios distintos: el almacen los integra en una sola verdad
CREATE TABLE crm AS
SELECT * FROM (VALUES
    ('4471', 'ES', 'Barcelona'),
    ('8890', 'ES', 'Sevilla')
) AS t(id_cliente, codigo_pais, ciudad);

CREATE TABLE facturacion AS
SELECT * FROM (VALUES
    ('4471', 'España', 12050),   -- importe en centimos de euro
    ('8890', 'España',  8000)
) AS t(customer_id, pais, importe_centimos);

CREATE TABLE dim_pais AS
SELECT * FROM (VALUES ('ES', 'España'), ('FR', 'Francia')) AS t(codigo_pais, pais);

-- Hecho integrado: una fila por factura, pais con codigo ISO e importe en euros
CREATE TABLE hechos_ventas AS
SELECT f.customer_id AS nk_cliente, p.codigo_pais, f.importe_centimos / 100.0 AS importe_eur
FROM facturacion f
JOIN dim_pais p ON p.pais = f.pais;

-- Un unico grupo (ES) con las dos ventas: 2 y 200.5
SELECT codigo_pais, count(*) AS ventas, sum(importe_eur) AS total_eur
FROM hechos_ventas
GROUP BY codigo_pais
ORDER BY codigo_pais;
```

```python verificable
import pandas as pd

# Dos origenes en monedas distintas: sin convertir no se pueden sumar
crm = pd.DataFrame({"pais": ["ES", "FR"], "importe": [1200.0, 800.0], "moneda": ["EUR", "USD"]})
facturacion = pd.DataFrame({"pais": ["ES"], "importe": [300.0], "moneda": ["EUR"]})
todos = pd.concat([crm, facturacion], ignore_index=True)

# El tipo de cambio se guarda con la carga: sin el, el numero de manana no se puede reproducir
fx = {"EUR": 1.0, "USD": 0.92}
en_euros = todos.assign(eur=todos.importe * todos.moneda.map(fx))

print("suma sin convertir:", round(todos.importe.sum(), 2))        # -> suma sin convertir: 2300.0
print("suma integrada en euros:", round(en_euros.eur.sum(), 2))    # -> suma integrada en euros: 2236.0
print("filas del hecho:", len(en_euros))                          # -> filas del hecho: 3
```

## Errores típicos

- **Confundir el almacén con el sistema transaccional.** Una copia con los mismos códigos, los
  mismos textos libres y las mismas tres definiciones de cliente no ha integrado nada: ha movido
  el problema de servidor. Y consultar el almacén desde la aplicación que da de alta pedidos
  mezcla cargas analíticas pesadas con usuarios esperando un formulario ([[oltp-vs-olap]]).
- **No declarar el grano de la tabla de hechos.** Sin grano no se sabe qué suma un `SUM`, y
  cualquier informe que agregue dos tablas de grano distinto duplicará filas. Escríbelo en la
  documentación y en el nombre de la tabla.
- **Confundir el almacén con el lago.** El crudo y el curado tienen dueños, precios y garantías
  distintos. Si mezclas ambos en la misma capa, nadie sabe qué se puede consultar y qué no
  ([[data-lake]], [[arquitectura-medallion]]).
- **Reconstruir todo cada noche.** Un *full refresh* diario de una tabla de 800 millones de
  filas es caro y frágil: usa [[ingesta-incremental-y-cdc|carga incremental]] y reprocesa solo
  lo que cambió, con un proceso idempotente ([[idempotencia-y-reintentos]]).
- **Marts de dominios sin dimensiones conformadas.** Si ventas y marketing calculan «cliente
  activo» con criterios distintos, los dos cuadros de mando se contradicen y el almacén pierde
  su única promesa. La dimensión se define una vez, en el núcleo.
- **Cargar sin reconciliar.** Si el proceso no compara el total cargado con el del origen y no
  falla cuando no cuadra, los errores llegan al comité de dirección sin avisar.

## Comprueba que lo sabes

:::quiz
p: ¿Qué distingue a un data warehouse de una copia de la base de datos de producción?
o: Que el almacén guarda los mismos datos pero en otro servidor con más disco
o: Que el almacén está integrado: unifica códigos, monedas y definiciones de todos los orígenes
o: Que el almacén solo guarda datos agregados y nunca el detalle
a: 2
e: La copia arrastra los vocabularios y las contradicciones del origen. Lo que aporta el almacén es la integración: un código de país, una moneda, una definición de cliente. Guardar el detalle es perfectamente normal, y a menudo necesario, para poder auditar las cifras.
:::

:::quiz
p: Una tabla de hechos no tiene documentado su grano. ¿Cuál es la consecuencia más probable?
o: Que las consultas van más lentas
o: Que al agregar esa tabla junto con otra de grano distinto se dupliquen o se pierdan filas sin que nadie lo note
o: Que no se puede particionar por fecha
a: 2
e: El grano es lo que dice qué cuenta cada fila. Sin él, dos tablas que parecen compatibles se unen y el resultado multiplica filas (o promedia granularidades distintas). El rendimiento y el particionado son problemas independientes.
:::

:::quiz
p: El proceso de carga termina sin errores pero el total del hecho no coincide con la suma de los orígenes para el mismo periodo. ¿Qué corresponde hacer?
o: Publicar igualmente: la diferencia será redondeo
o: Marcar la carga como fallida, no publicar esa partición y avisar, dejando disponible la anterior
o: Sumar la diferencia a la partición más reciente para cuadrar el total
a: 2
e: La reconciliación es la garantía básica del almacén: si no cuadra, hay filas perdidas o duplicadas y las cifras que se publiquen serán falsas. Repartir el descuadre a mano destruye la trazabilidad y esconde el fallo de origen.
:::

:::trampa
Un almacén que solo guarda el estado actual es cómodo hasta el primer informe comparativo. Si
no conservas la historia (dimensiones versionadas y hechos con su fecha de evento), no podrás
responder «cómo era esto en marzo» y volver a construir el pasado costará meses de reproceso.
:::
