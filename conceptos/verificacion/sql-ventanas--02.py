import duckdb

con = duckdb.connect()
con.sql("""
    CREATE TABLE estados (cliente VARCHAR, fecha DATE, plan VARCHAR);
    INSERT INTO estados VALUES
        ('Ana',   DATE '2024-01-10', 'basico'),
        ('Ana',   DATE '2024-02-01', 'pro'),
        ('Luis',  DATE '2024-01-05', 'pro'),
        ('Luis',  DATE '2024-01-20', 'basico'),
        ('Marta', DATE '2024-03-02', 'pro');
""")

# ROW_NUMBER numera dentro de cada particion y no colapsa nada: se filtra fuera.
# Es el idioma estandar para quedarse con la ultima fila de cada clave.
ultimo = con.sql("""
    SELECT cliente, plan FROM (
        SELECT cliente, plan,
               ROW_NUMBER() OVER (PARTITION BY cliente ORDER BY fecha DESC) AS rn
        FROM estados
    )
    WHERE rn = 1
    ORDER BY cliente
""").fetchall()

print(" ".join(f"{cliente}:{plan}" for cliente, plan in ultimo))
# -> Ana:pro Luis:basico Marta:pro
