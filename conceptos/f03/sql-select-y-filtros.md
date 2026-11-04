---
id: sql-select-y-filtros
titulo: "SQL: consultas y filtros"
fase: 3
nivel: básico
rutas: [de, ds, core]
prerequisitos: [ficheros-y-encoding, tipos-y-estructuras-python]
tags: [sql, select, where, duckdb, null]
resumen: SELECT, WHERE, ORDER BY y LIMIT con su orden de evaluación real, la lógica de tres valores de NULL y lo que cambia entre dialectos.
fuentes: ["ISO/IEC 9075, 'Information technology — Database languages — SQL'", "DuckDB documentation, 'SQL Introduction'"]
---

## En una frase

Una consulta `SELECT` describe **qué filas y qué columnas quieres**, no cómo llegar a ellas: el
motor decide el cómo, y por eso el orden en que escribes las cláusulas no es el orden en que se
ejecutan.

## La idea

Piensa en una biblioteca. El bibliotecario no lee todos los libros para responderte: primero
elige la **sección** (qué tabla), luego va descartando estanterías (el filtro), ordena lo que
queda y al final te entrega solo los primeros tomos. Tú describes el resultado que quieres y él
decide el camino.

SQL hace lo mismo, y el orden de lectura de una consulta no coincide con el orden de ejecución:

```text
se escribe:   SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY ... LIMIT
se ejecuta:   FROM -> WHERE -> GROUP BY -> HAVING -> SELECT -> ORDER BY -> LIMIT
```

De ahí salen dos consecuencias que explican casi todos los errores de principiante:

1. **No puedes usar en `WHERE` un alias definido en `SELECT`**, porque el alias todavía no
   existe. `WHERE total > 100` falla si `total` es `importe * cantidad`; hay que repetir la
   expresión o envolver la consulta en una subconsulta.
2. **`LIMIT` se aplica al final**, después de ordenar. `SELECT ... LIMIT 10` sin `ORDER BY` te
   devuelve diez filas cualesquiera, y cualesquiera significa «las que el motor encuentre antes
   esta vez». La consulta parece funcionar y cambia de resultado entre ejecuciones.

La segunda pieza que hay que entender bien es `NULL`. No es «cero» ni «cadena vacía»: es «valor
desconocido». Cualquier comparación con `NULL` (`precio = NULL`, `precio <> NULL`) no da
verdadero ni falso, da **desconocido**, y `WHERE` solo deja pasar lo que es verdadero. Por eso
se usan `IS NULL` y `IS NOT NULL`, y por eso `NULL` se lleva por delante sumas, medias y
comparaciones sin avisar.

## Definición formal

Las cláusulas, con lo que hace cada una:

- **`SELECT`**: qué columnas salen. `*` es todas; mejor nombrarlas siempre, porque el esquema
  cambia y una consulta con `*` devuelve columnas distintas cada mes.
- **`FROM`**: la tabla de origen. Es lo primero que se evalúa.
- **`WHERE`**: el filtro, fila a fila. Solo pasan las filas para las que la condición es
  verdadera.
- **`GROUP BY`**: agrupa las filas que quedan y reduce cada grupo a una fila.
- **`HAVING`**: filtra **grupos** después de agregar, no filas.
- **`ORDER BY`**: el orden final. `ASC` (por defecto) o `DESC`; con varias columnas se ordena
  por la primera y, a igualdad, por la siguiente.
- **`LIMIT n`**: como mucho `n` filas. `OFFSET m` salta las `m` primeras.

Lógica de tres valores. Sea `t` el valor de una comparación:

- `t` puede ser verdadero, falso o **desconocido**. `NULL` en cualquier operación aritmética o
  comparación produce desconocido, salvo en `IS NULL`, `IS NOT NULL` y `COALESCE`.
- `WHERE` descarta las filas con resultado falso **y** con resultado desconocido. Este es el
  comportamiento que más sorpresas causa.
- `NOT (desconocido)` sigue siendo desconocido: `WHERE NOT (precio > 100)` **no** devuelve las
  filas con `precio` nulo.

Tipos y dialectos, lo que cambia de un motor a otro:

- **Tipos**: `INTEGER`/`BIGINT`, `NUMERIC(p, s)` o `DECIMAL(p, s)` para dinero (`p` dígitos
  totales, `s` decimales), `DOUBLE`, `VARCHAR(n)` o `TEXT`, `DATE`, `TIMESTAMP`,
  `TIMESTAMPTZ` (con zona horaria) y `BOOLEAN`.
- **Comillas**: los literales de texto van entre comillas **simples** (`'Madrid'`); las dobles
  son para identificadores en el estándar. En MySQL, con las dobles puedes escribir un texto, y
  de ahí salen consultas que no funcionan en otro motor.
- **Fechas**: el estándar es `DATE '2024-01-05'`. SQLite espera `'2024-01-05'`, SQL Server
  `'2024-01-05'` o `CAST(... AS date)`, y Oracle `DATE '2024-01-05'`. Es la diferencia que más
  rompe consultas al cambiar de motor.
- **Concatenación**: `'a' || 'b'` en el estándar, PostgreSQL y DuckDB; `CONCAT('a', 'b')` en
  MySQL y SQL Server. En MySQL, `||` significa «o lógico» si no está activado el modo
  `PIPES_AS_CONCAT`.
- **Límite de filas**: `LIMIT n` en PostgreSQL, MySQL, SQLite y DuckDB; `TOP n` en SQL Server;
  `FETCH FIRST n ROWS ONLY` en Oracle y en el estándar.
- **Comillas para identificadores**: PostgreSQL y Oracle pliegan a minúsculas o mayúsculas sin
  comillas; MySQL usa acentos graves (`` `tabla` ``) y SQL Server corchetes (`[tabla]`).
- **Cadenas**: `LIKE` distingue mayúsculas y minúsculas en PostgreSQL y **no** las distingue en
  MySQL con la intercalación por defecto (`ILIKE` es la variante de PostgreSQL que las ignora).

## Ejemplo

Una tabla `pedidos` con cinco filas:

```text
id | cliente | importe | fecha      | ciudad
1  | Ana     |  120.50 | 2024-01-05 | Madrid
2  | Luis    |   80.00 | 2024-01-06 | NULL
3  | Ana     |  200.00 | 2024-01-06 | Madrid
4  | Marta   |    NULL | 2024-01-07 | Sevilla
5  | Luis    |   45.25 | 2024-01-08 | NULL
```

Consultas de una en una:

- `WHERE importe > 100` → filas 1 y 3. **La fila 4 no entra**, porque `NULL > 100` es
  desconocido, no verdadero.
- `WHERE importe <= 100` → filas 2 y 5. La fila 4 tampoco entra: desconocido no es falso, pero
  `WHERE` solo deja pasar lo verdadero. La fila 4 es invisible para las dos consultas.
- `WHERE ciudad IS NULL` → filas 2 y 5.
- `ORDER BY importe DESC` → 3 (200,00), 1 (120,50), 2 (80,00) y 5 (45,25). Y aquí está el
  detalle que cambia entre motores: **dónde cae la fila 4**. En PostgreSQL, un `NULL` es «más
  grande» que cualquier valor, así que con `ASC` aparece al final y con `DESC` al principio. En
  SQLite y en DuckDB es al revés: los nulos se colocan al final también en `DESC`. No lo dejes a
  la suerte: escribe `NULLS LAST` y el resultado será el mismo en todos los motores.
- `SELECT count(*) FROM pedidos` → 5. `SELECT count(importe) FROM pedidos` → **4**, porque
  `count(columna)` no cuenta los nulos.
- `SELECT sum(importe) FROM pedidos` → 445,75. La fila nula no suma cero: simplemente no cuenta,
  y la media (`avg`) divide entre 4, no entre 5.

Ese último detalle es el error de cálculo más común en informes: la media de una columna con
nulos es la media de los que hay, no la de todos. Si de verdad quieres contar el nulo como cero,
se escribe `avg(coalesce(importe, 0))` **a propósito y sabiendo qué significa**.

## Código

Los bloques de abajo crean sus propias tablas y se ejecutan con DuckDB.

```sql verificable
CREATE TABLE pedidos (id INTEGER, cliente TEXT, importe DOUBLE, fecha DATE, ciudad TEXT);
INSERT INTO pedidos VALUES
  (1, 'Ana',   120.50, DATE '2024-01-05', 'Madrid'),
  (2, 'Luis',   80.00, DATE '2024-01-06', NULL),
  (3, 'Ana',   200.00, DATE '2024-01-06', 'Madrid'),
  (4, 'Marta',   NULL, DATE '2024-01-07', 'Sevilla'),
  (5, 'Luis',    45.25, DATE '2024-01-08', NULL);

-- El filtro deja fuera los nulos: desconocido no es verdadero.
SELECT id, cliente, importe
FROM pedidos
WHERE importe > 100
ORDER BY importe DESC;
```

```sql verificable
CREATE TABLE pedidos (id INTEGER, importe DOUBLE, ciudad TEXT);
INSERT INTO pedidos VALUES
  (1, 120.50, 'Madrid'), (2, 80.00, NULL), (3, 200.00, 'Madrid'),
  (4, NULL, 'Sevilla'), (5, 45.25, NULL);

-- count(*) cuenta filas; count(columna) ignora los nulos. No son lo mismo.
SELECT
  count(*)                     AS filas,
  count(importe)               AS importes_no_nulos,
  count(*) - count(importe)    AS nulos,
  round(sum(importe), 2)       AS suma,
  round(avg(importe), 2)       AS media_sin_nulos,
  round(avg(coalesce(importe, 0)), 2) AS media_contando_cero
FROM pedidos;
```

```sql verificable
CREATE TABLE pedidos (id INTEGER, cliente TEXT, importe DOUBLE, fecha DATE, ciudad TEXT);
INSERT INTO pedidos VALUES
  (1, 'Ana',   120.50, DATE '2024-01-05', 'Madrid'),
  (2, 'Luis',   80.00, DATE '2024-01-06', NULL),
  (3, 'Ana',   200.00, DATE '2024-01-06', 'Madrid'),
  (4, 'Marta',   NULL, DATE '2024-01-07', 'Sevilla'),
  (5, 'Luis',    45.25, DATE '2024-01-08', NULL);

-- Varias condiciones: el parentesis cambia el resultado, no es decorativo.
SELECT id, ciudad, importe
FROM pedidos
WHERE (ciudad = 'Madrid' OR ciudad = 'Sevilla')
  AND fecha >= DATE '2024-01-06'
ORDER BY fecha, id;

-- Los nulos se ordenan siempre al final, y ademas lo decimos explicitamente.
SELECT id, importe
FROM pedidos
ORDER BY importe ASC NULLS LAST
LIMIT 3;
```

```sql verificable
CREATE TABLE pedidos (id INTEGER, importe DOUBLE);
INSERT INTO pedidos VALUES (1, 10.0), (2, NULL), (3, 30.0);

-- Donde cae el nulo al ordenar: en DuckDB, NULLS LAST es el comportamiento
-- por defecto en ASC y en DESC. Escribirlo evita depender del motor.
SELECT id, importe FROM pedidos ORDER BY importe DESC NULLS LAST;
```

```sql verificable
CREATE TABLE pedidos (id INTEGER, fecha DATE, importe DOUBLE);
INSERT INTO pedidos VALUES
  (1, DATE '2024-01-05', 120.50), (2, DATE '2024-01-06', 80.00),
  (3, DATE '2024-01-06', 200.00), (4, DATE '2024-01-07', NULL),
  (5, DATE '2024-01-08', 45.25);

-- Fechas y tipos: se comparan con el tipo correcto, no con una cadena.
SELECT fecha, count(*) AS pedidos, round(sum(importe), 2) AS total
FROM pedidos
WHERE fecha >= DATE '2024-01-06' AND importe IS NOT NULL
GROUP BY fecha
ORDER BY fecha;

-- CAST explicito: si el importe llega como texto, se convierte antes de sumar.
SELECT sum(CAST('150.25' AS DOUBLE)) AS suma_convertida;
```

## Errores típicos

- **Escribir `= NULL` en vez de `IS NULL`.** `WHERE importe = NULL` no devuelve ninguna fila, ni
  siquiera las que tienen el importe nulo, porque la comparación da desconocido. Siempre
  `IS NULL` o `IS NOT NULL`.
- **Suponer que `NOT` recupera los nulos.** `WHERE NOT (ciudad = 'Madrid')` no incluye las filas
  con `ciudad` nula: `NOT desconocido` sigue siendo desconocido. Si las quieres, hay que decirlo:
  `WHERE ciudad IS NULL OR ciudad <> 'Madrid'`.
- **Usar la media o la suma sin mirar cuántos nulos hay.** `avg(importe)` divide entre los
  importes no nulos, no entre las filas. Un informe con un 30 % de nulos da una media que no
  representa al conjunto. Comprueba siempre `count(*)` contra `count(columna)`.
- **`LIMIT` sin `ORDER BY`.** «Dame los 10 más caros» y «dame 10 filas» son consultas distintas.
  Sin `ORDER BY`, qué diez filas salen es cosa del motor y del plan de ejecución, y cambia
  cuando cambia el plan.
- **Filtrar por una fecha escrita como texto.** `WHERE fecha = '2024-01-05'` funciona si la
  columna es `DATE` (el motor convierte el literal) y falla de forma silenciosa si la columna es
  `VARCHAR`: compara cadenas y `'2024-1-5'` deja de coincidir. Usa el literal tipado
  `DATE '2024-01-05'` y comprueba el tipo de la columna.
- **Usar `SELECT *` en una consulta que va a producción.** El esquema cambia, el orden de las
  columnas cambia y alguien que lee por posición se rompe. Nombra las columnas, sobre todo si el
  resultado alimenta otro programa.

:::nota
En un `WHERE` con varias condiciones, `AND` se evalúa antes que `OR`, como en aritmética se hace
antes la multiplicación que la suma. Por eso `a OR b AND c` se lee `a OR (b AND c)`. Escribe los
paréntesis siempre, aunque la precedencia te dé la razón: quien lea la consulta mañana no
tendrá que recordarla.
:::

## Comprueba que lo sabes

:::quiz
p: Una tabla tiene 10 filas y la columna `importe` es nula en 3 de ellas. ¿Qué devuelve `SELECT count(importe), avg(importe) FROM t`?
o: 10 y la media de los 10 valores contando los nulos como cero
o: 7 y la media de los 7 valores no nulos
o: 10 y la media de los 7 valores no nulos
a: 2
e: `count(columna)` ignora los nulos y cuenta 7, mientras que `count(*)` contaría las 10 filas. `avg` también ignora los nulos, así que divide la suma entre 7. Si quieres tratar el nulo como cero hay que decirlo: `avg(coalesce(importe, 0))`, y entonces la media baja porque el denominador pasa a ser 10.
:::

:::quiz
p: ¿Cuál es el orden real de evaluación de una consulta con todas las cláusulas?
o: SELECT, FROM, WHERE, GROUP BY, ORDER BY, LIMIT
o: FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY, LIMIT
o: FROM, SELECT, WHERE, ORDER BY, GROUP BY, LIMIT
a: 2
e: El motor empieza por la tabla de origen, filtra con `WHERE`, agrupa, filtra los grupos con `HAVING`, calcula las columnas del `SELECT`, ordena y por último recorta con `LIMIT`. De ahí que `WHERE` no pueda usar los alias del `SELECT` (aún no existen) y que `LIMIT` necesite un `ORDER BY` previo para ser determinista.
:::

:::practica
enunciado: Tienes la tabla `pedidos(id, cliente, importe, fecha, ciudad)` con nulos en `importe` y en `ciudad`. Escribe mentalmente una consulta que devuelva, para cada ciudad distinta, el número de pedidos y el importe total, sin perder de vista los pedidos con ciudad desconocida. ¿Qué cuidado hay que tener en cada columna?
pista: Piensa en qué hace `GROUP BY` con los nulos y en qué columnas pueden tener valores desconocidos.
solucion: `SELECT coalesce(ciudad, '(sin ciudad)') AS ciudad, count(*) AS pedidos, round(sum(importe), 2) AS total FROM pedidos GROUP BY coalesce(ciudad, '(sin ciudad)') ORDER BY pedidos DESC`. Los tres cuidados: (1) `GROUP BY` agrupa **todos** los nulos en un solo grupo, no los descarta, así que sin `coalesce` el informe tendría una fila con ciudad nula que en un gráfico desaparece o sale como «null»; conviene etiquetarla explícitamente. (2) `count(*)` cuenta pedidos aunque el importe sea nulo, que suele ser lo correcto para «cuántos pedidos hay»; `count(importe)` daría otra cosa. (3) `sum(importe)` ignora los nulos y da el total de lo conocido; si un pedido sin importe debe contar como cero, hay que decidirlo y escribirlo (`sum(coalesce(importe, 0))`), porque el total del informe y el total de la caja no coincidirán hasta que ese criterio esté claro.
:::
