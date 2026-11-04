# Medidas aditivas y cuentas de claves: el mismo hecho, cuatro respuestas distintas
HECHOS = [
    {"fecha_id": 20250131, "producto_id": 1, "pedido_id": 5001, "unidades": 2, "importe": 59.90},
    {"fecha_id": 20250131, "producto_id": 2, "pedido_id": 5001, "unidades": 1, "importe": 12.50},
    {"fecha_id": 20250201, "producto_id": 1, "pedido_id": 5002, "unidades": 3, "importe": 89.85},
]

unidades = sum(h["unidades"] for h in HECHOS)
importe = sum(h["importe"] for h in HECHOS)
pedidos = len({h["pedido_id"] for h in HECHOS})

print("unidades totales  :", unidades)                       # -> 6
print("importe total     :", round(importe, 2))             # -> 162.25
print("pedidos distintos :", pedidos)                       # -> 2
print("ticket medio      :", round(importe / pedidos, 2))   # -> 81.12
print("precio por unidad :", round(importe / unidades, 2))  # -> 27.04
print("filas contadas    :", len(HECHOS), "no son pedidos") # -> 3
