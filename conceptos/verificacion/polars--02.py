import polars as pl

lf = pl.LazyFrame({"x": [1, 2, 3, 4], "y": [10.0, 20.0, 30.0, 40.0]})

# Esto NO ha ejecutado nada: es un plan con filtro, columna calculada y seleccion
plan = (lf.filter(pl.col("x") > 1)
          .with_columns((pl.col("y") / pl.col("x")).alias("ratio"))
          .select("x", "ratio"))

print(plan.collect().to_dict(as_series=False))
# -> {'x': [2, 3, 4], 'ratio': [10.0, 10.0, 10.0]}

# El if/else de las expresiones, sin bucles ni apply
print(pl.LazyFrame({"v": [-1, 0, 2]})
      .select(pl.when(pl.col("v") > 0).then(pl.lit("pos")).otherwise(pl.lit("no")).alias("s"))
      .collect()["s"].to_list())
# -> ['no', 'no', 'pos']
