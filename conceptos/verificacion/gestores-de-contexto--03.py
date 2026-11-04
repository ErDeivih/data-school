import sqlite3

# with conexion: es una TRANSACCION, no un cierre. La conexion sigue viva al salir.
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pedidos (id INTEGER)")

with con:                                   # confirma al salir sin excepcion
    con.execute("INSERT INTO pedidos VALUES (1)")

try:
    with con:                               # deshace al salir con excepcion
        con.execute("INSERT INTO pedidos VALUES (2)")
        raise ValueError("el lote venia mal")
except ValueError:
    pass

print("filas confirmadas:", con.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0])
# -> 1
print("la conexion sigue abierta:", con.execute("SELECT 1").fetchone()[0])
# -> 1
con.close()                                 # cerrar es cosa tuya, no del with
