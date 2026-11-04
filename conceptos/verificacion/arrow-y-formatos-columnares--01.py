import pyarrow as pa

tabla = pa.table({"pais": ["ES", "FR", None], "importe": [1.5, 2.5, None]})

print([(c, str(tabla.schema.field(c).type)) for c in tabla.column_names])
# -> [('pais', 'string'), ('importe', 'double')]
print(tabla.num_rows, tabla.num_columns)            # -> 3 2
print(tabla.column("importe").to_pylist())          # -> [1.5, 2.5, None]
print(tabla.column("importe").null_count)           # -> 1  (la mascara de validez lo sabe sin recorrer)
