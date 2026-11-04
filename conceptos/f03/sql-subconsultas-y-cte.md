---
id: sql-subconsultas-y-cte
titulo: "SQL: subconsultas y CTE"
fase: 3
nivel: intermedio
rutas: [de, ds]
prerequisitos: [sql-select-y-filtros, sql-agregaciones-y-group-by]
tags: [sql, cte, subconsultas, legibilidad]
resumen: Consultas dentro de consultas y el WITH que les pone nombre; cómo se lee una consulta larga de arriba abajo sin perderse por el camino.
fuentes: ["Garcia-Molina, Ullman y Widom (2008), 'Database Systems: The Complete Book'", "Melton y Simon (2002), 'SQL: 1999 Understanding Relational Language Components'"]
---

## En una frase

Una subconsulta es una consulta metida dentro de otra, y una CTE (`WITH nombre AS (...)`) es esa
misma consulta con nombre y escrita antes de la principal, que es lo que convierte un bloque de
80 líneas anidadas en una lista de pasos que se lee de arriba abajo.

## La idea

Una consulta anidada se lee como los paréntesis en una fórmula: el `SELECT` que ves primero es
el último que se ejecuta. Para responder «¿qué clientes facturan más que el pedido medio?» el
motor primero calcula el pedido medio (consulta interna) y después compara cada cliente con él
(consulta externa). Es correcto, pero cuando hay tres o cuatro niveles, leerlo exige ir saltando
del centro hacia fuera y es donde aparecen los errores.

Las CTE dan la vuelta a ese orden. Escribes primero el cálculo intermedio, le pones un nombre y
lo usas después como si fuera una tabla. Cada paso tiene su propio grano (una fila por cliente,
una fila por día) y eso se puede comprobar de uno en uno. La regla práctica: **si necesitas
explicar una consulta en voz alta con «primero saco esto, luego lo cruzo con aquello», cada
«primero» es una CTE.**

Hay cuatro formas de subconsulta y conviene distinguirlas porque se comportan distinto:

- **Escalar:** devuelve una fila y una columna, y se usa donde iría un valor
  (`WHERE total > (SELECT AVG(importe) FROM pedidos)`).
- **De tabla:** aparece en el `FROM` y se comporta como una tabla más, aunque no tenga nombre. Es
  lo que hace una CTE, con mejor legibilidad.
- **De lista:** `x IN (SELECT ...)`. Cómoda y traicionera, por lo del nulo que se cuenta abajo.
- **Correlacionada:** menciona una columna de la consulta externa, así que conceptualmente se
  evalúa una vez por fila candidata. Es la que convierte una consulta de un segundo en una de un
  minuto.

La subconsulta estrella es `EXISTS`: pregunta si hay al menos una fila, no qué valor tiene, y por
eso el motor puede parar en la primera coincidencia y no le importa lo que pongas en el `SELECT`
(de ahí la costumbre de escribir `SELECT 1`).

Dos aclaraciones que evitan malentendidos caros:

1. **Una CTE no es una tabla temporal.** No se indexa, no se guarda entre consultas y, según el
   motor y la versión, puede recalcularse cada vez que la mencionas. En PostgreSQL anterior a la
   12 se materializaba siempre (y actuaba como barrera para el optimizador); en versiones
   modernas decide el planificador. Si necesitas el resultado dos veces y es caro, mide antes de
   suponer.
2. **El orden de escritura no es el orden de ejecución.** Si la segunda CTE usa la primera, el
   motor resuelve las dependencias; la primera de la lista puede ser la última en calcularse.

Y una tercera, la que más veces he visto romper un informe: **`NOT IN` con un nulo dentro de la
subconsulta devuelve el conjunto vacío**. No da error. Devuelve cero filas y parece que no hay
ningún caso pendiente, cuando puede haber miles.

## Definición formal

Una CTE se declara así, y puede encadenar tantas como necesites:

```
WITH primera AS (consulta_1),
     segunda  AS (consulta_2 que usa primera)
SELECT ... FROM segunda JOIN primera ON ...
```

Cada nombre del `WITH` es visible para las CTE posteriores y para la consulta final, no para las
anteriores ni para las que ya han terminado.

- **Subconsulta escalar:** `(SELECT ...)` con exactamente una fila y una columna. Si devuelve
  más de una fila, el motor lanza un error en tiempo de ejecución, no al compilar.
- **`EXISTS (subconsulta)`:** verdadero si la subconsulta devuelve al menos una fila. Las
  columnas del `SELECT` interno se ignoran por completo.
- **Correlacionada:** la subconsulta referencia una columna de la consulta externa. En SQL puro
  se evalúa por fila candidata; los optimizadores modernos la transforman a menudo en una unión.
- **CTE recursiva:**

```
WITH RECURSIVE t(n) AS (
    SELECT ancla              -- fila(s) de partida
    UNION ALL
    SELECT paso FROM t WHERE condicion_de_parada
)
SELECT * FROM t
```

El término ancla produce las filas iniciales; después se evalúa el término recursivo una y otra
vez sobre las filas nuevas hasta que no devuelve ninguna. `UNION ALL` conserva duplicados y es lo
habitual; `UNION` los elimina, y con él la condición de parada tiene que ser de igualdad, no de
recorrido.

**Lógica de tres valores.** `x NOT IN (a, b, NULL)` equivale a `x <> a AND x <> b AND x <> NULL`.
La última comparación es *desconocida* para cualquier `x`, así que el `AND` completo nunca es
verdadero y no sale ninguna fila. `NOT EXISTS` no sufre esto porque compara fila a fila y un
`NULL` no puede «coincidir» con nada.

## Ejemplo

Tabla `pedidos` con 6 filas; la sexta no tiene cliente identificado:

```
id  cliente  importe
1   Ana        100
2   Ana         50
3   Luis       200
4   Luis       300
5   Marta      400
6   NULL        80
```

- Total facturado: 1.130. Pedido medio: 1.130 / 6 = **188,33**.
- Totales por cliente: Ana 150, Luis 500, Marta 400.
- Clientes que superan el pedido medio: **Luis (500)** y **Marta (400)**. Ana se queda fuera.

Y ahora la trampa, con una tabla `clientes` que contiene Ana, Luis, Marta y Pablo:

- `SELECT COUNT(*) FROM clientes WHERE nombre NOT IN (SELECT cliente FROM pedidos)` devuelve
  **0**. Pablo no tiene pedidos, pero el nulo del pedido 6 envenena la comparación para todas las
  filas.
- `... WHERE NOT EXISTS (SELECT 1 FROM pedidos p WHERE p.cliente = c.nombre)` devuelve **1**:
  Pablo, que es la respuesta correcta.

Cero contra uno. El primero es el número que aparecería en un informe de «clientes sin compras».
Y una CTE recursiva que genera 5 días desde el 1 de enero de 2024 evita escribir el calendario a
mano, que es el otro uso clásico de la recursión junto con las jerarquías.

## Código

```sql verificable
-- Encadenar dos CTE es lo que permite leer la consulta en el orden en que se piensa.
CREATE TABLE pedidos (id INTEGER, cliente VARCHAR, importe INTEGER);

INSERT INTO pedidos VALUES
    (1, 'Ana',   100), (2, 'Ana',    50),
    (3, 'Luis',  200), (4, 'Luis',  300),
    (5, 'Marta', 400), (6, NULL,     80);

WITH por_cliente AS (
    SELECT cliente, SUM(importe) AS total, COUNT(*) AS pedidos
    FROM pedidos
    WHERE cliente IS NOT NULL
    GROUP BY cliente
),
referencia AS (
    SELECT AVG(importe) AS pedido_medio FROM pedidos
)
SELECT p.cliente, p.total, p.pedidos, ROUND(r.pedido_medio, 2) AS pedido_medio
FROM por_cliente p
CROSS JOIN referencia r
WHERE p.total > r.pedido_medio
ORDER BY p.total DESC;
```

```text
cliente | total | pedidos | pedido_medio
Luis | 500 | 2 | 188.33
Marta | 400 | 1 | 188.33
```

```python verificable
import duckdb

con = duckdb.connect()
con.sql("""
    CREATE TABLE pedidos (id INTEGER, cliente VARCHAR, importe INTEGER);
    INSERT INTO pedidos VALUES
        (1, 'Ana', 100), (2, 'Ana', 50), (3, 'Luis', 200),
        (4, 'Luis', 300), (5, 'Marta', 400), (6, NULL, 80);
    CREATE TABLE clientes (nombre VARCHAR);
    INSERT INTO clientes VALUES ('Ana'), ('Luis'), ('Marta'), ('Pablo');
""")

# El nulo de la subconsulta hace que NOT IN no devuelva ninguna fila: no falla, miente.
sin_pedidos_not_in = con.sql(
    "SELECT COUNT(*) FROM clientes WHERE nombre NOT IN (SELECT cliente FROM pedidos)"
).fetchone()[0]
sin_pedidos_not_exists = con.sql(
    "SELECT COUNT(*) FROM clientes c WHERE NOT EXISTS "
    "(SELECT 1 FROM pedidos p WHERE p.cliente = c.nombre)"
).fetchone()[0]
print(f"clientes sin pedidos  NOT IN {sin_pedidos_not_in}  NOT EXISTS {sin_pedidos_not_exists}")
# -> clientes sin pedidos  NOT IN 0  NOT EXISTS 1

# Una CTE recursiva genera el calendario en lugar de escribirlo a mano.
dias, primero, ultimo = con.sql("""
    WITH RECURSIVE calendario(fecha) AS (
        SELECT DATE '2024-01-01'
        UNION ALL
        SELECT fecha + INTERVAL 1 DAY FROM calendario WHERE fecha < DATE '2024-01-05'
    )
    SELECT COUNT(*), MIN(fecha), MAX(fecha) FROM calendario
""").fetchone()
print(f"dias {dias}  de {primero} a {ultimo}")   # -> dias 5  de 2024-01-01 a 2024-01-05
```

## Errores típicos

- **Usar `NOT IN` con una subconsulta que puede tener nulos.** Devuelve cero filas sin avisar. Si
  no controlas la subconsulta, usa `NOT EXISTS`; si la usas, añade `WHERE columna IS NOT NULL`
  dentro. Es el error que más informes falsos produce, porque «cero pendientes» parece una buena
  noticia.
- **Escribir una subconsulta escalar que devuelve más de una fila.** `(SELECT importe FROM
  pedidos)` no es escalar. Si quieres «el mayor», dilo con `MAX` o con `ORDER BY ... LIMIT 1`, y
  no confíes en que los datos actuales solo tengan una fila: el día que aparezca la segunda, la
  consulta revienta en producción.
- **Correlacionadas en el `SELECT` que se ejecutan una vez por fila.** Funcionan, pero con una
  tabla de millones de filas el coste es millones de búsquedas. Casi siempre se reescriben como
  un `JOIN` con un agregado o como una función de ventana de [[sql-ventanas|las funciones de
  ventana]]. Mira el plan antes de dar por buena la versión bonita.
- **Repetir la misma subconsulta tres veces en la misma consulta.** Además de ser ilegible, el
  motor puede calcularla tres veces. Nómbrala con `WITH` y úsala desde los tres sitios.
- **CTE recursiva sin condición de parada.** Si el paso recursivo siempre devuelve filas, la
  consulta no termina hasta agotar memoria o hasta que el motor corta por límite de recursión. La
  condición va en el `WHERE` del término recursivo, no en el `SELECT` final.
- **Creer que una CTE es una vista o una tabla temporal.** No se indexa ni se conserva, y en
  algunos motores se recalcula en cada mención. Si el cálculo es caro y lo usas dos veces, mide
  antes de darlo por hecho.

:::practica
enunciado: En `pedidos(cliente, importe)` hay: Ana 100 y 50; Luis 200 y 300; Marta 400; Pablo 60, 70 y 80. Escribe con una CTE la consulta que devuelva los clientes cuyo total supera la media de los totales por cliente, con su total y su número de pedidos.
pista: La CTE deja una fila por cliente; su media es una subconsulta escalar en la consulta final.
solucion: `WITH por_cliente AS (SELECT cliente, SUM(importe) AS total, COUNT(*) AS pedidos FROM pedidos GROUP BY cliente) SELECT cliente, total, pedidos FROM por_cliente WHERE total > (SELECT AVG(total) FROM por_cliente) ORDER BY total DESC`. Los totales son Ana 150, Luis 500, Marta 400 y Pablo 210; la media por cliente es 1.260 / 4 = 315. Superan esa media Luis (500) y Marta (400): salen dos filas y Ana y Pablo quedan fuera.
:::

## Comprueba que lo sabes

:::quiz
p: La consulta SELECT COUNT(*) FROM clientes WHERE nombre NOT IN (SELECT cliente FROM pedidos) devuelve 0 aunque exista un cliente sin pedidos. ¿Por qué?
o: Porque COUNT(*) nunca cuenta filas cuando hay un nulo en la tabla
o: Porque la subconsulta contiene un nulo y la comparación con ese nulo es desconocida para todas las filas
o: Porque NOT IN solo funciona con listas de valores escritas a mano
a: 2
e: x NOT IN (a, b, NULL) se evalúa como x <> a AND x <> b AND x <> NULL. La última comparación es desconocida para cualquier x, así que el resultado nunca es verdadero y no sale ninguna fila. NOT EXISTS compara fila a fila y devuelve el cliente que falta.
:::

:::quiz
p: ¿Cuál es la ventaja principal de una CTE frente a una subconsulta anidada equivalente?
o: Se ejecuta siempre más rápido porque el motor la guarda en disco
o: Permite leer la consulta como una secuencia de pasos con nombre, cada uno con su propio grano
o: Evita tener que escribir la cláusula GROUP BY
a: 2
e: La CTE es sobre todo una herramienta de legibilidad y de reutilización dentro de la misma consulta. No se guarda en disco, no se indexa y no garantiza mejor plan; de hecho puede ser más lenta si el motor la materializa. Y el GROUP BY sigue siendo necesario.
:::

:::truco
Para leer una consulta larga, empieza por el final: mira el `SELECT` de fuera y pregúntate **una
fila por qué**. Después ve hacia arriba comprobando el grano de cada CTE. Si dos pasos tienen
granos incompatibles (uno por pedido y otro por cliente) y los unes sin agregar antes, el `JOIN`
multiplica filas y todos los totales salen inflados.
:::
