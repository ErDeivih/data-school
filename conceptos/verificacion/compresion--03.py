import io
import pyarrow as pa
import pyarrow.parquet as pq

# Una columna categorica: el diccionario sustituye cadenas por indices enteros.
ciudades = ["Madrid", "Barcelona", "Valencia", "Sevilla"] * 2500
tabla = pa.table({"ciudad": ciudades, "importe": list(range(10000))})

for nombre, dicc, codec in [("sin diccionario", False, "none"),
                            ("con diccionario", True, "none"),
                            ("diccionario + zstd", True, "zstd")]:
    buffer = io.BytesIO()
    pq.write_table(tabla, buffer, use_dictionary=dicc, compression=codec)
    print("{:<20} {:>7} bytes".format(nombre, buffer.tell()))
# sin diccionario:      195721 bytes
# con diccionario:      100861 bytes
# diccionario + zstd:    28759 bytes
