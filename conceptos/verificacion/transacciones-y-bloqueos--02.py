import sqlite3

# Una sola base en memoria compartida y dos conexiones: las dos cajas del ejemplo.
uri = "file:cuentas?mode=memory&cache=shared"
c1 = sqlite3.connect(uri, uri=True, isolation_level=None, timeout=0.05)
c2 = sqlite3.connect(uri, uri=True, isolation_level=None, timeout=0.05)
c1.execute("CREATE TABLE cuentas (id TEXT PRIMARY KEY, saldo INTEGER)")
c1.execute("INSERT INTO cuentas VALUES ('A', 500)")

# Leer, calcular en Python y escribir: entre la lectura y la escritura cabe la otra sesion.
leido1 = c1.execute("SELECT saldo FROM cuentas WHERE id = 'A'").fetchone()[0]
leido2 = c2.execute("SELECT saldo FROM cuentas WHERE id = 'A'").fetchone()[0]
c1.execute("UPDATE cuentas SET saldo = ? WHERE id = 'A'", (leido1 + 100,))
c2.execute("UPDATE cuentas SET saldo = ? WHERE id = 'A'", (leido2 + 50,))
print("tras leer-modificar-escribir:", c1.execute("SELECT saldo FROM cuentas WHERE id = 'A'").fetchone()[0])
# -> 550

# El motor hace la suma: leer y escribir son una sola operacion, no hay hueco.
c1.execute("UPDATE cuentas SET saldo = saldo + 100 WHERE id = 'A'")
c2.execute("UPDATE cuentas SET saldo = saldo + 50 WHERE id = 'A'")
print("tras sumar dentro del UPDATE:", c1.execute("SELECT saldo FROM cuentas WHERE id = 'A'").fetchone()[0])
# -> 700

# Un escritor bloquea al otro en vez de dejar que lo pise: esa es la parte de los bloqueos.
c1.execute("BEGIN IMMEDIATE")
c1.execute("UPDATE cuentas SET saldo = saldo - 10 WHERE id = 'A'")
try:
    c2.execute("BEGIN IMMEDIATE")
except sqlite3.OperationalError as e:
    print("la segunda sesion no puede escribir:", type(e).__name__)
# -> OperationalError
c1.execute("ROLLBACK")
print("tras el rollback:", c1.execute("SELECT saldo FROM cuentas WHERE id = 'A'").fetchone()[0])
# -> 700
