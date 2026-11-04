---
id: sql-joins
titulo: "SQL: uniones"
fase: 3
nivel: básico
rutas: [de, ds, core]
prerequisitos: [sql-select-y-filtros]
tags: [sql, joins, duckdb, duplicados, claves]
resumen: INNER, LEFT, FULL y CROSS, autocombinaciones y el error clásico de duplicar filas al unir antes de agregar.
fuentes: ["ISO/IEC 9075, 'Information technology — Database languages — SQL'", "DuckDB documentation, 'Joins'"]
---

## En una frase

Una unión pega dos tablas por una condición, y su tamaño no lo decide la condición sino **cuántas
filas de cada lado la cumplen**: si un cliente tiene tres pedidos, una fila de clientes se
convierte en tres.

## La idea

Tienes dos listas. En una, tus clientes con su ciudad. En la otra, los pedidos con el
identificador del cliente. Quieres un informe por ciudad.

Un `JOIN` es lo que haces al cruzarlas: buscas cada pedido en la lista de clientes y le pegas su
ciudad al lado. La pregunta importante no es cómo se cruzan, sino **qué pasa con los que no
tienen pareja**:

- Si un pedido es de un cliente que no está en la lista, ¿lo tiras o lo dejas con la ciudad en
  blanco? Tirarlo es `INNER JOIN`; dejarlo con la ciudad vacía es `LEFT JOIN`.
- Si tienes un cliente que no ha comprado nada, ¿aparece con cero pedidos o no aparece? Con
  `LEFT JOIN` desde clientes aparece; con `INNER JOIN` desaparece.

Ese es todo el asunto de los tipos de unión: **qué haces con las filas sin pareja**. Y la trampa
que aparece después, la que de verdad rompe informes, es otra: **una unión puede multiplicar
filas**. Si un cliente tiene tres pedidos, ese cliente aparece tres veces. Si después sumas el
saldo del cliente, lo sumas tres veces y el total sale inflado sin que nada falle.

Piensa en fotocopiar una lista. Tienes 100 clientes y 300 pedidos. Cruzas las dos listas y
obtienes 300 filas: los pedidos con su cliente al lado. Si ahora sumas la columna «saldo» de esa
tabla, el saldo de un cliente con 5 pedidos se cuenta 5 veces.

La suma está mal, la consulta
funciona y nadie ve el error salvo que compare con la caja.

La regla que evita el 90 % de estos problemas: **antes de agregar, comprueba si la unión
duplica; o agrega en la tabla de hechos y une después**. Y antes de unir, confirma cuál es la
clave: si la columna por la que unes no es única en una de las dos tablas, el multiplicador es
ese número.

## Definición formal

Sean dos tablas `A` y `B` y una condición de unión `A.k = B.k`:

- **`INNER JOIN`**: devuelve las combinaciones de filas que cumplen la condición. Si una clave
  de `A` no está en `B`, esa fila desaparece. Si una clave aparece `m` veces en `A` y `n` en
  `B`, produce `m · n` filas.
- **`LEFT JOIN`** (o `LEFT OUTER JOIN`): todas las filas de `A` y, si hay varias coincidencias
  en `B`, una fila por cada una. Si no hay ninguna, se rellena con `NULL` **todas** las columnas
  de `B` (y ojo: si una columna de `B` era nula de verdad, no se distingue del relleno).
- **`RIGHT JOIN`**: simétrico, todas las de `B`. En la práctica se reescribe como `LEFT JOIN`
  cambiando el orden de las tablas, y así se lee mejor.
- **`FULL OUTER JOIN`**: todas las de `A` y todas las de `B`, con `NULL` en el lado que falte.
  Sirve para comparar dos versiones de un mismo conjunto y ver qué se ha añadido y qué se ha
  perdido.
- **`CROSS JOIN`**: producto cartesiano, todas las combinaciones sin condición. Es lo que sale
  por accidente cuando se te olvida la condición de unión: 1.000 por 1.000 son un millón de
  filas y la consulta «funciona».
- **Autocombinación (self join):** unir una tabla consigo misma con dos alias distintos. Se usa
  para jerarquías (empleado con su jefe) y para comparar una fila con otra de la misma tabla.
- **Unión por clave compuesta:** la condición lleva varios iguales, `A.a = B.a AND A.b = B.b`.
  Unirlos con un separador inventado (concatenar) es una fuente de errores: `'1' + '23'` y
  `'12' + '3'` dan lo mismo.
- **Nulos en la clave de unión:** `NULL` no es igual a `NULL`. Una fila con clave nula **no
  coincide con nada**, ni siquiera con otra fila con la clave nula, así que en un `INNER JOIN`
  desaparece y en un `LEFT JOIN` sale con `NULL` al lado.

## Ejemplo

Dos tablas pequeñas:

```text
clientes:                        pedidos:
id | nombre | ciudad             id | cliente_id | importe
1  | Ana    | Madrid             10 | 1          | 120.50
2  | Luis   | Bilbao             11 | 1          |  30.00
3  | Marta  | NULL               12 | 2          |  80.00
4  | Pablo  | Sevilla            13 | 9          |  55.00     <- cliente desconocido
```

Los cuatro resultados que importan:

- `INNER JOIN` por `clientes.id = pedidos.cliente_id` → **3 filas**: los pedidos 10, 11 y 12. El
  pedido 13 (cliente 9) y el cliente 4 (Pablo) desaparecen.
- `LEFT JOIN` desde clientes → **5 filas**: las 3 del `INNER` más **Marta** y **Pablo**, que no
  tienen pedidos y salen con `NULL` en las columnas de pedido. El cliente 9 no aporta ninguna fila,
  porque no está en `clientes`. Ana aparece **dos veces**, una por cada pedido.
- `LEFT JOIN` desde pedidos → **4 filas**: los 3 pedidos conocidos más el pedido 13 con `NULL` en
  las columnas de cliente.
- `FULL OUTER JOIN` → **6 filas**: las 5 del `LEFT JOIN` desde clientes más el pedido 13 con
  `NULL` al lado de cliente. Con esto ves de un vistazo los dos descuadres: un cliente sin
  pedidos y un pedido sin cliente.

Y el error clásico, con números. Quieres el total de pedidos por ciudad:

```text
mal:  SELECT c.ciudad, count(*), sum(p.importe)
      FROM clientes c JOIN pedidos p ON c.id = p.cliente_id
      GROUP BY c.ciudad;

bien: SELECT c.ciudad, count(p.id), sum(p.importe)
      FROM clientes c LEFT JOIN pedidos p ON c.id = p.cliente_id
      GROUP BY c.ciudad;
```

En este caso las dos dan el mismo total (la primera simplemente pierde a Pablo y al pedido 13),
pero cambian el recuento: `count(*)` cuenta **filas del resultado**, y en un `LEFT JOIN` un
cliente sin pedidos aporta una fila que no es un pedido. `count(p.id)` cuenta pedidos de verdad,
porque ignora los `NULL` que ha dejado el relleno. Ese es el motivo de que en agregaciones sobre
una unión se use `count(columna_de_la_derecha)`, no `count(*)`.

El caso de duplicación pura aparece cuando unes por una clave que no es única **en las dos**
tablas. Si `cliente_id` aparece 2 veces en `pedidos` y 3 veces en `pagos`, la unión genera
2 · 3 = 6 filas para ese cliente, y cualquier suma está mal por un factor que depende del
número de filas de cada lado.

## Código

```sql verificable
CREATE TABLE clientes (id INTEGER, nombre TEXT, ciudad TEXT);
CREATE TABLE pedidos (id INTEGER, cliente_id INTEGER, importe DOUBLE);
INSERT INTO clientes VALUES (1, 'Ana', 'Madrid'), (2, 'Luis', 'Bilbao'), (3, 'Marta', NULL);
INSERT INTO pedidos VALUES (10, 1, 120.50), (11, 1, 30.00), (12, 2, 80.00);

-- INNER: solo los que tienen pareja. Marta no ha comprado: desaparece.
SELECT p.id, c.nombre, p.importe
FROM pedidos p
JOIN clientes c ON c.id = p.cliente_id
ORDER BY p.id;
```

```sql verificable
CREATE TABLE clientes (id INTEGER, nombre TEXT, ciudad TEXT);
CREATE TABLE pedidos (id INTEGER, cliente_id INTEGER, importe DOUBLE);
INSERT INTO clientes VALUES (1, 'Ana', 'Madrid'), (2, 'Luis', 'Bilbao'), (3, 'Marta', NULL);
INSERT INTO pedidos VALUES (10, 1, 120.50), (11, 1, 30.00), (12, 2, 80.00);

-- LEFT: todos los clientes, tengan pedidos o no. Marta sale con NULL.
SELECT c.id, c.nombre, p.id AS pedido, p.importe
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id
ORDER BY c.id, p.id;
```

```sql verificable
CREATE TABLE clientes (id INTEGER, nombre TEXT, ciudad TEXT);
CREATE TABLE pedidos (id INTEGER, cliente_id INTEGER, importe DOUBLE);
INSERT INTO clientes VALUES (1, 'Ana', 'Madrid'), (2, 'Luis', 'Bilbao'), (3, 'Marta', NULL);
INSERT INTO pedidos VALUES (10, 1, 120.50), (11, 1, 30.00), (12, 2, 80.00), (13, 9, 55.00);

-- FULL: los dos descuadres a la vez, la consulta de auditoria por excelencia.
SELECT c.id AS cliente, c.nombre, p.id AS pedido, p.importe
FROM clientes c
FULL OUTER JOIN pedidos p ON p.cliente_id = c.id
ORDER BY c.id NULLS LAST, p.id NULLS LAST;
```

```sql verificable
CREATE TABLE clientes (id INTEGER, nombre TEXT, ciudad TEXT);
CREATE TABLE pedidos (id INTEGER, cliente_id INTEGER, importe DOUBLE);
INSERT INTO clientes VALUES (1, 'Ana', 'Madrid'), (2, 'Luis', 'Bilbao'), (3, 'Marta', NULL);
INSERT INTO pedidos VALUES (10, 1, 120.50), (11, 1, 30.00), (12, 2, 80.00);

-- count(*) cuenta filas del resultado (Marta aporta una sin pedido);
-- count(p.id) cuenta pedidos de verdad, porque ignora los NULL.
SELECT
  c.ciudad,
  count(*)      AS filas_del_join,
  count(p.id)   AS pedidos_reales,
  round(sum(p.importe), 2) AS total
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id
GROUP BY c.ciudad
ORDER BY c.ciudad NULLS LAST;
```

```sql verificable
CREATE TABLE clientes (id INTEGER, nombre TEXT, ciudad TEXT);
CREATE TABLE pedidos (id INTEGER, cliente_id INTEGER, importe DOUBLE);
INSERT INTO clientes VALUES (1, 'Ana', 'Madrid'), (2, 'Luis', 'Bilbao'), (3, 'Marta', NULL);
INSERT INTO pedidos VALUES (10, 1, 120.50), (11, 1, 30.00), (12, 2, 80.00), (13, 9, 55.00);

-- Autocombinacion: los pedidos de un mismo cliente, por parejas.
SELECT a.id AS pedido_a, b.id AS pedido_b, a.importe + b.importe AS suma
FROM pedidos a
JOIN pedidos b ON a.cliente_id = b.cliente_id AND a.id < b.id
ORDER BY a.id;

-- Anti-union: lo que falta en el otro lado, sin usar NOT IN (que falla con nulos).
SELECT c.id, c.nombre
FROM clientes c
LEFT JOIN pedidos p ON p.cliente_id = c.id
WHERE p.id IS NULL;
```

## Errores típicos

- **Sumar después de unir sin comprobar la cardinalidad.** Si unes pedidos con pagos por
  `cliente_id` y después sumas, cada pedido se repite tantas veces como pagos tenga el cliente.
  Antes de agregar, cuenta las filas de la unión y compáralas con las de la tabla de hechos:
  si no coinciden, hay multiplicación. Lo correcto casi siempre es agregar primero en cada tabla
  y unir los agregados.
- **Convertir un `INNER` en `LEFT` moviendo la condición al `WHERE`.** `LEFT JOIN b ON a.k = b.k
  WHERE b.x = 5` no es un `LEFT JOIN`: el `WHERE` elimina las filas con `b` nulo y el resultado
  es un `INNER`. Si el filtro es sobre la tabla de la derecha y quieres conservar las filas sin
  pareja, la condición va en el `ON`.
- **Unir por una columna que no es única.** El error no da ningún aviso: la consulta funciona y
  el número sale mal. Antes de unir, comprueba la unicidad con
  `SELECT k, count(*) FROM tabla GROUP BY k HAVING count(*) > 1`. Si hay repetidos, decide si
  agregas antes o si la duplicación es la que quieres.
- **`count(*)` en agregaciones sobre un `LEFT JOIN`.** Los clientes sin pedidos cuentan como uno.
  Usa `count(columna_de_la_derecha)`, que ignora los `NULL` del relleno.
- **`NOT IN` con una subconsulta que contiene `NULL`.** `WHERE id NOT IN (SELECT cliente_id FROM
  pedidos)` no devuelve **ninguna** fila si hay un `cliente_id` nulo, porque `x <> NULL` es
  desconocido para todas las filas. Se resuelve con `NOT EXISTS` o con el `LEFT JOIN ... IS NULL`
  del ejemplo, que además es lo que mejor entienden los planes de ejecución.
- **Olvidar la condición de unión y creerse el resultado.** Sin `ON`, el motor hace un
  `CROSS JOIN`: 1.000 clientes por 1.000 pedidos son un millón de filas. Es rápido de detectar
  (el recuento explota), pero si las dos tablas son pequeñas pasa desapercibido y los totales
  salen multiplicados.

:::truco
Para auditar dos tablas que deberían cuadrar, el `FULL OUTER JOIN` es la herramienta: las filas
con `NULL` a un lado son exactamente los descuadres. Se lee así: «cliente sin pedido» cuando el
`NULL` está en las columnas de pedidos, y «pedido huérfano» cuando está en las de cliente.
:::

## Comprueba que lo sabes

:::quiz
p: La tabla `pedidos` tiene 3 filas del cliente 1 y la tabla `pagos` tiene 2 filas del mismo cliente. ¿Cuántas filas devuelve `pedidos JOIN pagos ON pedidos.cliente_id = pagos.cliente_id` para ese cliente?
o: 3, porque se queda con el número de filas de la tabla de la izquierda
o: 5, porque se suman las filas de las dos tablas
o: 6, porque cada fila de una tabla se combina con cada fila de la otra
a: 3
e: La unión genera todas las combinaciones de filas que cumplen la condición: 3 · 2 = 6 filas. No se suman (5) ni se conserva el número de la izquierda (3). Ese es el motivo de que sumar una columna de la izquierda después de unir multiplique el resultado: hay que agregar antes de unir o comprobar la cardinalidad.
:::

:::quiz
p: `SELECT count(*) FROM clientes c LEFT JOIN pedidos p ON p.cliente_id = c.id` con 3 clientes, uno de ellos sin pedidos y dos con 2 pedidos cada uno. ¿Qué devuelve?
o: 3, porque hay 3 clientes
o: 5, porque los dos clientes con pedidos aportan dos filas cada uno y el que no compró aporta una con NULL
o: 7, porque se cuentan los 3 clientes y los 4 pedidos
a: 2
e: El `LEFT JOIN` conserva los 3 clientes; los dos que tienen pedidos aparecen dos veces cada uno (4 filas) y el que no compró aparece una vez, con `NULL` en las columnas de pedido. En total 5 filas, de las que solo 4 son pedidos de verdad. Por eso para contar pedidos se usa `count(p.id)`, que ignora el `NULL` del relleno, y no `count(*)`.
:::

:::practica
enunciado: Tienes `clientes(id, nombre)`, `pedidos(id, cliente_id, importe, fecha)` y `pagos(id, pedido_id, importe)`. Escribe mentalmente una consulta que devuelva por cliente el número de pedidos y el importe total pagado, sin inflar ninguna cifra, y explica qué comprobarías antes de ejecutarla.
pista: Piensa en qué tabla tiene la granularidad más fina y en qué pasa si unes antes de agregar.
solucion: Primero se agrega cada tabla por su clave y luego se une: `SELECT c.nombre, coalesce(pd.n_pedidos, 0) AS pedidos, coalesce(pg.total_pagado, 0) AS pagado FROM clientes c LEFT JOIN (SELECT cliente_id, count(*) AS n_pedidos FROM pedidos GROUP BY cliente_id) pd ON pd.cliente_id = c.id LEFT JOIN (SELECT p.cliente_id, sum(g.importe) AS total_pagado FROM pedidos p JOIN pagos g ON g.pedido_id = p.id GROUP BY p.cliente_id) pg ON pg.cliente_id = c.id ORDER BY c.nombre`. Lo que hay que comprobar antes: (1) que `pagos.pedido_id` es único o, si hay varios pagos por pedido, que la suma los contempla todos; (2) que no unes `pedidos` con `pagos` directamente y luego agregas por cliente, porque cada pedido con dos pagos se contaría dos veces en `count(*)`; (3) que uso `LEFT JOIN` desde clientes para no perder a los que no han comprado, y `coalesce` para que el «sin datos» salga como 0 y no como nulo; (4) que comparo el número de pedidos del informe con `SELECT count(*) FROM pedidos` para detectar cualquier pérdida o duplicación.
:::
