import polars as pl

df = pl.DataFrame({
    "ciudad": ["Madrid", "Madrid", "Sevilla"],
    "importe": [10.0, 30.0, 5.0],
})

# group_by + agg: una fila por grupo, y el resultado se ordena como parte de la consulta
print(df.group_by("ciudad").agg(pl.col("importe").sum().alias("total")).sort("ciudad").to_dicts())
# -> [{'ciudad': 'Madrid', 'total': 40.0}, {'ciudad': 'Sevilla', 'total': 5.0}]
print(df["importe"].sum())   # -> 45.0
