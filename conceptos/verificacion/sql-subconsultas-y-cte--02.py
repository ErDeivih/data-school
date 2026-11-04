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
