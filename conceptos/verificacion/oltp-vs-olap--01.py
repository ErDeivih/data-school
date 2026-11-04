# Diferencia medida en una base por filas (SQLite) con medio millon de lineas
import sqlite3
import time

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pedidos (pedido_id INTEGER PRIMARY KEY, estado TEXT)")
con.execute("CREATE TABLE lineas (pedido_id INTEGER, unidades INTEGER, importe REAL)")
con.executemany("INSERT INTO pedidos VALUES (?, ?)",
                [(p, "pagado") for p in range(1, 100001)])
con.executemany("INSERT INTO lineas VALUES (?, ?, ?)",
                [(p, 1 + k % 3, round(10.0 + 3 * k, 2))
                 for p in range(1, 100001) for k in range(5)])
con.commit()

# Lectura por clave: el caso para el que esta disenada una base transaccional
t0 = time.perf_counter()
for p in range(1, 2001):
    con.execute("SELECT estado FROM pedidos WHERE pedido_id = ?", (p,)).fetchone()
t_clave = (time.perf_counter() - t0) / 2000

# Agregacion sobre todo: el caso analitico, en el mismo motor
t0 = time.perf_counter()
total = con.execute("SELECT count(*), round(sum(importe), 2) FROM lineas "
                    "JOIN pedidos USING (pedido_id) WHERE estado = 'pagado'").fetchone()
t_agregado = time.perf_counter() - t0

print("filas en lineas   :", total[0])                       # -> 500000
print("lectura por clave :", round(t_clave * 1e6), "microsegundos")
# La lectura por clave tarda unos pocos microsegundos; la agregacion, unas cien veces mas.
print("agregado de todo  :", round(t_agregado * 1000, 1), "milisegundos")
print("importe total     :", total[1])                       # -> 8000000.0
