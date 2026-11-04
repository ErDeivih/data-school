import io

import pyarrow as pa
import pyarrow.parquet as pq

n = 200_000
ciudades = ["Madrid", "Barcelona", "Sevilla", "Bilbao", "Valencia"]

# Datos deterministas y desordenados: alta cardinalidad en cliente e importe
tabla = pa.table({
    "cliente": pa.array([(i * 7919) % 1000 for i in range(n)], pa.int64()),
    "ciudad": pa.array([ciudades[(i * 3) % 5] for i in range(n)], pa.string()),
    "importe": pa.array([round(((i * 104729) % 100_000) / 100, 2) for i in range(n)], pa.float64()),
})

def serializar(t):
    buffer = io.BytesIO()
    pq.write_table(t, buffer, compression="zstd", row_group_size=50_000)
    return buffer.getvalue()

bytes_sin_orden = serializar(tabla)
bytes_ordenada = serializar(tabla.sort_by("importe"))

print("ordenar por importe reduce el fichero:", len(bytes_ordenada) < len(bytes_sin_orden))  # -> ordenar por importe reduce el fichero: True
print("la mejora pasa del 20 %:", len(bytes_ordenada) < 0.8 * len(bytes_sin_orden))          # -> la mejora pasa del 20 %: True

f = pq.ParquetFile(io.BytesIO(bytes_sin_orden))
print("grupos de filas:", f.metadata.num_row_groups)             # -> grupos de filas: 4
print("columnas del fichero:", f.metadata.num_columns)           # -> columnas del fichero: 3
print("filas al leer solo una columna:", f.read(columns=["ciudad"]).num_rows)  # -> filas al leer solo una columna: 200000

tam_ciudad = sum(f.metadata.row_group(g).column(1).total_compressed_size
                 for g in range(f.metadata.num_row_groups))
tam_total = sum(f.metadata.row_group(g).column(c).total_compressed_size
                for g in range(f.metadata.num_row_groups) for c in range(f.metadata.num_columns))
print("una columna de tres ocupa menos de la mitad:", tam_ciudad < tam_total / 2)  # -> una columna de tres ocupa menos de la mitad: True
