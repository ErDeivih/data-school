import duckdb
import pyarrow as pa

tabla = pa.table({"x": [1, 2, 3], "y": [10.0, 20.0, 30.0]})

# DuckDB consulta el Table de Arrow directamente, sin cargarlo en su propio formato
print(duckdb.sql("SELECT sum(y) AS total FROM tabla").fetchone())   # -> (60.0,)
print(duckdb.sql("SELECT count(*) AS filas FROM tabla").fetchone()) # -> (3,)
