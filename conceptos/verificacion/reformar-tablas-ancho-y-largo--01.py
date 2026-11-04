import pandas as pd

ancho = pd.DataFrame({
    "cliente": ["A", "B", "C"],
    "ene": [10, 20, 30],
    "feb": [40, 50, 60],
    "mar": [70, 80, 90],
})
largo = ancho.melt(id_vars="cliente", var_name="mes", value_name="ventas")

print(ancho.shape, largo.shape)          # -> (3, 4) (9, 3)
print(largo["mes"].tolist())             # -> ['ene', 'ene', 'ene', 'feb', 'feb', 'feb', 'mar', 'mar', 'mar']
print(largo["ventas"].sum())             # -> 450  la misma suma que en la tabla ancha
print(ancho[["ene", "feb", "mar"]].to_numpy().sum())   # -> 450
print(largo.dtypes["ventas"])            # -> int64  el tipo de los valores se conserva
