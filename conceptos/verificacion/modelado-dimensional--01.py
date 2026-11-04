# El grano decide que puedes responder: la misma tabla, cuatro preguntas
LINEAS = [
    {"pedido": 5001, "producto": 1, "tienda": 10, "unidades": 2, "importe": 59.90},
    {"pedido": 5001, "producto": 2, "tienda": 10, "unidades": 1, "importe": 12.50},
    {"pedido": 5002, "producto": 1, "tienda": 20, "unidades": 3, "importe": 89.85},
]

total = sum(l["importe"] for l in LINEAS)
por_pedido = {}
for l in LINEAS:
    por_pedido[l["pedido"]] = por_pedido.get(l["pedido"], 0) + l["importe"]

print("importe total      :", round(total, 2))                                # -> 162.25
print("pedidos distintos  :", len(por_pedido))                                 # -> 2
print("ticket medio       :", round(sum(por_pedido.values()) / len(por_pedido), 2))   # -> 81.12
print("media de la columna:", round(total / len(LINEAS), 2))                   # -> 54.08
print("precio por unidad  :", round(total / sum(l["unidades"] for l in LINEAS), 2))   # -> 27.04
