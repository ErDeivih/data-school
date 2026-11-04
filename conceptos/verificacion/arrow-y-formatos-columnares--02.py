import io

import pyarrow as pa
import pyarrow.parquet as pq

n = 20_000
tabla = pa.table({"pais": ["ES", "FR"] * (n // 2), "importe": list(range(n))})

memoria = io.BytesIO()
pq.write_table(tabla, memoria, compression="zstd")

# El fichero comprimido ocupa menos que los datos en memoria
print(memoria.getbuffer().nbytes < tabla.nbytes)     # -> True

# Se lee SOLO la columna pedida: el resto no se descomprime
leida = pq.read_table(io.BytesIO(memoria.getvalue()), columns=["importe"])
print(leida.column_names, leida.num_rows)            # -> ['importe'] 20000
print(leida.equals(tabla.select(["importe"])))       # -> True
