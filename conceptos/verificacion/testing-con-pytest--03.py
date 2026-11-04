# Regla de unicidad sobre los datos: el test de contrato mas barato que existe.
import pandas as pd

pedidos = pd.DataFrame({
    "pedido_id": [10, 11, 11, 12],
    "cliente_id": [1, 2, 2, 3],
    "importe": [10.0, 20.0, 20.0, 5.0],
})

duplicados = int(pedidos["pedido_id"].duplicated().sum())
nulos_clave = int(pedidos["pedido_id"].isna().sum())

print("filas:", len(pedidos))
print("pedido_id duplicados:", duplicados)
print("claves nulas:", nulos_clave)

if duplicados or nulos_clave:
    print("el pipeline debe parar aqui antes de agregar nada")
