import pandas as pd

ventas = pd.DataFrame({
    "ciudad": ["Madrid", "Madrid", "Sevilla", "Sevilla", "Sevilla"],
    "importe": [10.0, 30.0, 5.0, 15.0, 25.0],
})

print(ventas.groupby("ciudad")["importe"].sum().to_dict())    # -> {'Madrid': 40.0, 'Sevilla': 45.0}
print(ventas.groupby("ciudad")["importe"].size().to_dict())   # -> {'Madrid': 2, 'Sevilla': 3}

# transform devuelve una fila por fila original: sirve para comparar cada venta con su grupo
ventas["media_ciudad"] = ventas.groupby("ciudad")["importe"].transform("mean")
print(ventas["media_ciudad"].tolist())   # -> [20.0, 20.0, 15.0, 15.0, 15.0]
