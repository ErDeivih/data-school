import pandas as pd

ventas = pd.DataFrame({
    "ciudad": ["Madrid", "Sevilla", "Madrid", "Bilbao"],
    "unidades": [3, 5, 2, 7],
    "precio": [10.0, 4.0, 10.0, 2.5],
})

# Ordenar NO renumera las etiquetas: el indice conserva su valor original
ordenado = ventas.sort_values("unidades", ascending=False)
print(ordenado.index.tolist())              # -> [3, 1, 0, 2]
print(ordenado["unidades"].iloc[0])         # -> 7   (primera fila de la tabla ordenada)
print(ordenado["unidades"].loc[0])          # -> 3   (fila con etiqueta 0 = tercera posicion)
print(ordenado["unidades"].tolist())        # -> [7, 5, 3, 2]
