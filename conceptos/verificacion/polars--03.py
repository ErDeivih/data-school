import polars as pl
import pyarrow as pa

tabla = pa.table({"x": [1, 2, 3]})
df = pl.from_arrow(tabla)          # comparte los buffers de Arrow, sin convertirlos
print(df["x"].to_list())           # -> [1, 2, 3]
print(df.to_arrow().equals(tabla)) # -> True

# Convertir a pandas es una operacion explicita: util para pasar el resultado a otra libreria
print(df.to_pandas()["x"].tolist())   # -> [1, 2, 3]
