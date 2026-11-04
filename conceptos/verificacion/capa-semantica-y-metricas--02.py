import pandas as pd

pedidos = pd.DataFrame({"pedido_id": [1, 2], "total": [100.0, 50.0]})
lineas = pd.DataFrame({"pedido_id": [1, 1, 2], "importe": [60.0, 40.0, 50.0]})

# La medida 'total' vive en pedidos: su valor correcto es la suma sin unir
correcto = pedidos["total"].sum()
# Al unir el detalle, cada pedido se repite una vez por linea y su total se cuenta de mas
unido = pedidos.merge(lineas, on="pedido_id")
print("filas antes", len(pedidos), "filas despues", len(unido))
print(f"suma correcta {correcto:.1f}")
print(f"suma tras unir {unido['total'].sum():.1f}")
# -> filas antes 2 filas despues 3
# -> suma correcta 150.0
# -> suma tras unir 250.0
