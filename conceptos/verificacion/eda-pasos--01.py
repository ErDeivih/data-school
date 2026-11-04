import pandas as pd

# Ocho pedidos: el dataset minimo para recorrer los cuatro primeros pasos del metodo
pedidos = pd.DataFrame({
    "pedido_id": [1, 2, 3, 4, 5, 6, 7, 8],
    "cliente_id": [10, 10, 11, 12, 12, 12, 13, 13],
    "importe": [19.9, 45.0, 12.5, None, 78.2, 33.0, 9.99, 120.0],
    "canal": ["web", "app", "web", "web", "app", "web", "tienda", "web"],
    "fecha": ["2024-01-02", "2024-01-02", "2024-01-03", "2024-01-03",
              "2024-01-04", "2024-01-05", "2024-01-05", "2024-01-09"],
})

print("filas, columnas:", pedidos.shape)                       # -> (8, 5)
print("pedidos distintos:", pedidos["pedido_id"].nunique())    # -> 8
print("nulos en importe:", int(pedidos["importe"].isna().sum()))  # -> 1
print("canales distintos:", pedidos["canal"].nunique())        # -> 3
print("importe minimo:", pedidos["importe"].min())             # -> 9.99
