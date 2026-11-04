---
id: sql-modelado-y-normalizacion
titulo: "SQL: modelado y normalización"
fase: 3
nivel: intermedio
rutas: [de, ds]
prerequisitos: [sql-joins, sql-agregaciones-y-group-by]
tags: [sql, modelado, normalizacion, claves]
resumen: Que entidades existen, con qué clave se identifican y en qué tabla vive cada hecho; por qué repetir la ciudad del cliente en cada pedido acaba rompiendo los informes.
fuentes: ["Codd (1970), 'A Relational Model of Data for Large Shared Data Banks'", "Kent (1983), 'A Simple Guide to Five Normal Forms in Relational Database Theory'"]
---

## En una frase

Modelar es decidir qué entidades existen, con qué clave se identifica cada una y en qué tabla
vive cada hecho; normalizar es la disciplina de guardar cada hecho **una sola vez**, en la tabla
que le corresponde.

## La idea

Piensa en una agenda de contactos donde, cada vez que apuntas una cena, copias también el
teléfono de cada invitado. Funciona hasta que alguien cambia de número: tienes que corregirlo en
las nueve cenas donde aparece, y si te dejas una, tu agenda dice dos cosas distintas sobre la
misma persona. Eso es exactamente lo que pasa cuando la ciudad del cliente se guarda dentro de la
tabla de pedidos.

Con una tabla plana así aparecen tres problemas clásicos, y los tres se ven con el mismo ejemplo
(Ana se muda de Valencia a Bilbao):

- **Anomalía de actualización.** Hay que cambiar la ciudad en *todos* los pedidos de Ana. Si un
  proceso se cae a mitad o alguien actualiza solo las filas de este año, la misma clienta aparece
  en dos ciudades. La base de datos no protesta: las dos filas son válidas.
- **Anomalía de inserción.** No puedes dar de alta a un cliente que todavía no ha comprado nada,
  porque no hay dónde ponerlo: la tabla es de pedidos y necesita un pedido.
- **Anomalía de borrado.** Borras el último pedido de un cliente y, con él, la única constancia
  de que ese cliente existía y de dónde es.

Y una cuarta que no es de integridad sino de negocio: si guardas el precio del producto en la
línea del pedido y luego lo sobrescribes porque subió, has reescrito la historia. La factura de
enero deja de cuadrar con lo que se cobró. Lo veremos abajo: ese precio **no** es redundancia, es
un hecho distinto del precio actual.

Normalizar es eliminar esas repeticiones hasta que cada hecho tenga un único hogar. Las formas
normales son una escala de exigencia, no un dogma:

- **1FN:** los valores son atómicos. Nada de listas metidas en una columna.
- **2FN:** ningún atributo depende de una *parte* de la clave compuesta.
- **3FN:** ningún atributo depende de otro atributo que no sea la clave.

Para un sistema transaccional, 3FN es el punto de partida razonable. Para analítica, se
desnormaliza **a propósito**: el [[modelado-dimensional|modelado dimensional]] repite atributos en
la tabla de hechos y en las dimensiones porque las consultas leen millones de filas y un `JOIN`
de menos es tiempo ganado (ver [[normalizacion-vs-desnormalizacion|normalización frente a
desnormalización]]). La diferencia entre desnormalizar y tener un modelo roto no es el resultado:
es haberlo decidido y saber qué se paga por ello.

## Definición formal

- **Superclave:** cualquier conjunto de columnas que identifica una fila de forma única.
- **Clave candidata:** superclave mínima, sin columnas sobrantes. Puede haber varias.
- **Clave primaria:** la clave candidata elegida como identificador oficial. No admite nulos.
- **Clave foránea:** columna (o conjunto) cuyos valores deben existir en la clave primaria de
  otra tabla. Es lo que la base de datos comprueba por ti.
- **Clave sustituta:** identificador sin significado de negocio, normalmente un entero generado
  (secuencia o `IDENTITY`). **Clave natural:** un dato real como el correo o el número de
  factura.
- **Dependencia funcional `X → Y`:** «conocido el valor de `X` hay como máximo un valor de `Y`».
  Es la herramienta con la que se razona todo lo demás: `cliente → ciudad` significa que un
  cliente tiene una ciudad, así que la ciudad no puede depender del pedido.

Las formas normales, en corto, con `R` una relación y `K` su clave:

- **1FN:** todos los atributos de `R` toman valores atómicos. Sin listas, sin conjuntos, sin
  campos que contengan varios valores separados por comas.
- **2FN:** está en 1FN y todo atributo no primo depende de la clave **completa**, no de una parte.
  Solo importa cuando la clave es compuesta.
- **3FN:** está en 2FN y ningún atributo no primo depende transitivamente de la clave, es decir,
  no existe `K → A → B` con `A` no primo.
- **BCNF:** para toda dependencia funcional no trivial `X → Y`, `X` es superclave. Es más estricta
  que 3FN y solo discrepa en casos con varias claves candidatas solapadas.

Y la regla práctica que resume el oficio: **una tabla, un grano**. Antes de escribir la primera
columna, di en voz alta «cada fila de esta tabla es un…» y comprueba que ninguna columna describe
algo de un grano distinto. El 90 % de los modelos rotos se detectan así, sin hablar de formas
normales.

## Ejemplo

Tabla plana de pedidos, con 4 filas:

| pedido | cliente | ciudad_cliente | producto | precio | unidades |
| --- | --- | --- | --- | --- | --- |
| 1001 | Ana | Valencia | teclado | 25,00 | 2 |
| 1002 | Ana | Valencia | ratón | 15,00 | 1 |
| 1003 | Luis | Bilbao | teclado | 25,00 | 1 |
| 1004 | Luis | Bilbao | monitor | 180,00 | 2 |

Cuatro filas para dos clientes: la ciudad se guarda dos veces por cliente y el precio del teclado
también. Con 1.000.000 de pedidos y 5.000 clientes, la columna de ciudad almacena 1.000.000 de
copias de 5.000 valores distintos cuando solo hacen falta 5.000. La redundancia aquí es del 50 %
(dos valores distintos en cuatro filas), y crece con el número de pedidos, no con el de clientes.

Descomposición en cuatro tablas, cada una con su grano:

- `clientes(cliente_id, nombre, ciudad)` — una fila por cliente.
- `pedidos(pedido_id, cliente_id, fecha)` — una fila por pedido.
- `lineas(pedido_id, producto_id, unidades, precio_unitario)` — una fila por línea de pedido.
- `productos(producto_id, nombre, precio_actual)` — una fila por producto.

Fíjate en `precio_unitario`: parece que duplica `productos.precio_actual`, pero no lo hace. El
precio de la línea es el precio **pactado en ese pedido** y no cambia nunca; el de `productos` es
el precio **vigente hoy** y cambia cuando la empresa quiere. Son dos hechos distintos, y por eso
los dos existen. Guardar solo uno de ellos es elegir entre no poder facturar dos veces lo mismo o
no poder cambiar la tarifa.

Con el modelo normalizado, la facturación por cliente es una consulta con dos uniones:

```
Luis  Bilbao    2 lineas   385,00
Ana   Valencia  2 lineas    65,00
```

## Código

```sql verificable
-- Cada hecho en un solo sitio: el nombre del cliente no se repite en pedidos,
-- y el precio de venta se guarda en la linea, donde es un hecho historico.
CREATE TABLE clientes (cliente_id INTEGER PRIMARY KEY, nombre VARCHAR, ciudad VARCHAR);
CREATE TABLE pedidos  (pedido_id INTEGER PRIMARY KEY, cliente_id INTEGER, fecha DATE);
CREATE TABLE lineas   (pedido_id INTEGER, producto_id INTEGER,
                       unidades INTEGER, precio_unitario DECIMAL(10,2));

INSERT INTO clientes VALUES (1, 'Ana', 'Valencia'), (2, 'Luis', 'Bilbao');
INSERT INTO pedidos VALUES
    (1001, 1, DATE '2024-02-01'), (1002, 1, DATE '2024-02-03'),
    (1003, 2, DATE '2024-02-05'), (1004, 2, DATE '2024-02-07');
INSERT INTO lineas VALUES
    (1001, 10, 2,  25.00), (1002, 11, 1,  15.00),
    (1003, 10, 1,  25.00), (1004, 12, 2, 180.00);

SELECT c.nombre,
       c.ciudad,
       COUNT(*) AS lineas,
       SUM(l.unidades * l.precio_unitario) AS total
FROM pedidos p
JOIN clientes c ON c.cliente_id = p.cliente_id
JOIN lineas   l ON l.pedido_id = p.pedido_id
GROUP BY c.nombre, c.ciudad
ORDER BY total DESC;
```

```text
nombre | ciudad | lineas | total
Luis | Bilbao | 2 | 385.00
Ana | Valencia | 2 | 65.00
```

```python verificable
# Tabla plana: la ciudad del cliente se copia en cada pedido que hace.
plano = [
    {"pedido": 1001, "cliente": "Ana",  "ciudad": "Valencia"},
    {"pedido": 1002, "cliente": "Ana",  "ciudad": "Valencia"},
    {"pedido": 1003, "cliente": "Luis", "ciudad": "Bilbao"},
    {"pedido": 1004, "cliente": "Luis", "ciudad": "Bilbao"},
]

# Redundancia: valores distintos frente a filas que los repiten.
ciudades = {fila["ciudad"] for fila in plano}
print(f"ciudad  distintos {len(ciudades)} en {len(plano)} filas"
      f"  redundancia {1 - len(ciudades) / len(plano):.0%}")
# -> ciudad  distintos 2 en 4 filas  redundancia 50%

# La anomalia de actualizacion, provocada a proposito: se corrige una sola fila.
plano[3]["ciudad"] = "Bilbo"
por_cliente = {}
for fila in plano:
    por_cliente.setdefault(fila["cliente"], set()).add(fila["ciudad"])
print("clientes con mas de una ciudad:", sum(1 for v in por_cliente.values() if len(v) > 1))
# -> clientes con mas de una ciudad: 1
```

## Errores típicos

- **Meter listas en una columna.** `telefonos = '600111222, 600333444'` viola la 1FN: no puedes
  buscar un teléfono sin funciones de texto, no puedes indexarlo bien y no puedes validar que cada
  número tenga el formato correcto. Una tabla `telefonos(persona_id, telefono)`.
- **Elegir una clave natural que cambia.** El correo, el teléfono o el nombre completo cambian.
  Si son la clave primaria, cada cambio obliga a actualizar todas las tablas que los referencian.
  Usa una clave sustituta y deja la natural como columna única con índice.
- **Confiar la integridad al código de la aplicación.** Sin claves foráneas declaradas, cualquier
  script de carga, cualquier `UPDATE` manual y cualquier herramienta de BI pueden dejar huérfanos.
  La base de datos es el último sitio donde se puede comprobar; que lo compruebe.
- **Normalizar hasta el absurdo.** Una tabla para provincias, otra para estados y doce uniones para
  pintar un listado. Las tablas de referencia pequeñas y estables se consultan tanto que a veces
  conviene copiar la etiqueta en la tabla principal, a sabiendas y con un proceso que la mantenga.
- **«Normalizar» el precio histórico.** Quitar `precio_unitario` de la línea y leerlo de
  `productos` hace que todas las facturas antiguas muestren el precio de hoy. Es un error de
  modelado que además destruye la trazabilidad y suele acabar en una auditoría incómoda.
- **Añadir columnas nuevas en vez de cambiar el modelo.** Cuando a la tabla de pedidos le empiezan
  a sobrar `ciudad_envio`, `ciudad_factura`, `ciudad_cliente_actual` y `ciudad_anterior`, el
  problema no es de columnas: la entidad que falta no está en el modelo.

:::practica
enunciado: Tabla plana envios(envio_id, cliente, ciudad, transportista, tarifa) con 5 filas: (1, Ana, Valencia, Seur, 4,50), (2, Ana, Valencia, Seur, 4,50), (3, Luis, Bilbao, Correos, 3,20), (4, Luis, Bilbao, Seur, 4,50), (5, Marta, Sevilla, Correos, 3,20). Di qué dependencias funcionales hay, qué forma normal se incumple y cuánta redundancia tiene la tarifa.
pista: Pregunta de qué depende cada atributo que no sea la clave, y mide la redundancia como 1 − valores distintos / filas.
solucion: Dependencias: envio_id → cliente y transportista; cliente → ciudad; transportista → tarifa. La última es transitiva (envio_id → transportista → tarifa), así que la tabla no está en 3FN. Redundancia de tarifa: 2 valores distintos en 5 filas, 1 − 2/5 = 60 %. Se descompone en clientes(cliente_id, nombre, ciudad), transportistas(transportista_id, nombre, tarifa) y envios(envio_id, cliente_id, transportista_id): si Seur sube a 5,00 se cambia una fila, no tres.
:::

## Comprueba que lo sabes

:::quiz
p: La ciudad del cliente se guarda en la tabla de pedidos. ¿Qué anomalía aparece cuando el cliente se muda?
o: La de actualización: hay que cambiar muchas filas y basta con olvidar una para tener dos verdades
o: La de inserción, porque no se pueden crear pedidos nuevos
o: Ninguna, porque el motor actualiza las columnas repetidas automáticamente
a: 1
e: Es la anomalía clásica de actualización, causada por la dependencia transitiva pedido -> cliente -> ciudad. El motor no sabe que esas columnas son «lo mismo»: para él son datos independientes en cada fila. La anomalía de inserción es otra: no poder dar de alta un cliente sin pedidos.
:::

:::quiz
p: En el modelo normalizado, la línea de pedido guarda precio_unitario y la tabla de productos guarda precio_actual. ¿Es una redundancia que haya que eliminar?
o: Sí, porque el mismo dato no puede estar en dos tablas
o: No, porque son dos hechos distintos: el precio pactado en ese pedido y el precio vigente hoy
o: Sí, y se elimina dejando solo precio_actual en productos
a: 2
e: El precio de la línea es histórico e inmutable; el de productos es el vigente y cambia. Si se guarda solo el vigente, todas las facturas antiguas mostrarían el precio de hoy; si se guarda solo el histórico, no hay forma de cambiar la tarifa. Son dos atributos con distinto significado, no una copia.
:::

:::nota
3FN no es la meta: es el punto de partida. Un almacén analítico desnormaliza a propósito
([[modelado-dimensional]], [[esquema-estrella-y-copo]]) y una tabla de hechos puede repetir
atributos de dimensión sin que el modelo esté mal. Lo que nunca es aceptable es no saber qué se
está duplicando y quién lo mantiene al día.
:::
