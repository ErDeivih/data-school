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
