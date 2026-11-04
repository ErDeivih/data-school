import sqlite3

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE pedidos (id INTEGER PRIMARY KEY, cliente_id INTEGER, fecha TEXT, importe REAL)")
con.executemany("INSERT INTO pedidos VALUES (?, ?, ?, ?)",
                [(i, i % 500, f"2024-01-{i % 28 + 1:02d}", 10.0 + i % 90) for i in range(20000)])

def plan(sql):
    return [fila[-1] for fila in con.execute("EXPLAIN QUERY PLAN " + sql)][0]

consulta = "SELECT SUM(importe) FROM pedidos WHERE cliente_id = 123"
print("sin indice  :", plan(consulta))   # -> sin indice  : SCAN pedidos

con.execute("CREATE INDEX idx_pedidos_cliente ON pedidos(cliente_id)")
print("con indice  :", plan(consulta))
# -> con indice  : SEARCH pedidos USING INDEX idx_pedidos_cliente (cliente_id=?)

# La operacion sobre la columna y el comodin inicial devuelven el plan a un recorrido completo.
print("con funcion :", plan("SELECT SUM(importe) FROM pedidos WHERE cliente_id + 0 = 123"))
# -> con funcion : SCAN pedidos
print("comodin     :", plan("SELECT SUM(importe) FROM pedidos WHERE fecha LIKE '%01-15'"))
# -> comodin     : SCAN pedidos
