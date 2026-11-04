import pandas as pd

# La misma pregunta tiene dos respuestas si no fijas la unidad de analisis:
# una fila puede ser un pedido o un cliente, y no son lo mismo.
pedidos = pd.DataFrame({
    "cliente": ["A", "A", "A", "B", "C"],
    "importe": [10.0, 12.0, 8.0, 90.0, 25.0],
})

print("media por pedido :", round(pedidos["importe"].mean(), 2))                           # -> 29.0
print("media por cliente:", round(pedidos.groupby("cliente")["importe"].sum().mean(), 2))   # -> 48.33
print("pedidos por cliente:", pedidos.groupby("cliente").size().to_dict())                  # -> A:3, B:1, C:1
