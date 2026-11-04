import io
import pandas as pd

# Los datos van escritos aqui, pero el patron es el mismo con un CSV de 2 GB: antes
# de analizar nada, mira tipos, duplicados, nulos y rangos.
crudo = """ciudad,anyo,precio_m2,operaciones
Madrid,2023,4200,185
Madrid,2024,4380,171
Valencia,2023,1980,96
Valencia,2024,,88
Sevilla,2023,1750,54
Sevilla,2023,1750,54
"""
df = pd.read_csv(io.StringIO(crudo))

print(df.dtypes.to_string())
print("filas:", len(df), "| duplicadas:", int(df.duplicated().sum()))   # -> 6 | 1
print("nulos:", df.isna().sum().to_dict())        # -> solo precio_m2, con 1 nulo
print(df.groupby("ciudad")["precio_m2"].median().to_string())   # -> Madrid 4290, Sevilla 1750, Valencia 1980
