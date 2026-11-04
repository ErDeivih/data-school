import pandas as pd

# Un duplicado no cambia la mediana y si infla las sumas: comprueba el grano antes
# de agregar. Aqui hay dos filas identicas de Sevilla.
df = pd.DataFrame({"ciudad": ["Sevilla"] * 3 + ["Madrid"],
                   "operaciones": [54, 54, 61, 185]})
limpio = df.drop_duplicates()

print("suma con duplicado :", int(df["operaciones"].sum()))         # -> 354
print("suma tras deduplicar:", int(limpio["operaciones"].sum()))    # -> 300
print(limpio.groupby("ciudad")["operaciones"].sum().to_dict())      # -> Madrid 185, Sevilla 115
