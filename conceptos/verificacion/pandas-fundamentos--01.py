import pandas as pd

ventas = pd.DataFrame({
    "ciudad": ["Madrid", "Sevilla", "Madrid", "Bilbao"],
    "unidades": [3, 5, 2, 7],
    "precio": [10.0, 4.0, 10.0, 2.5],
})

print(ventas.shape)                      # -> (4, 3)
print(ventas["unidades"].dtype)          # -> int64
print(ventas["precio"].dtype)            # -> float64
print(ventas.loc[2, "ciudad"])           # -> Madrid
print(ventas.iloc[2, 0])                 # -> Madrid
print((ventas["unidades"] * ventas["precio"]).sum())   # -> 87.5
