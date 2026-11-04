import io

import pyarrow as pa
import pyarrow.parquet as pq

# 40.000 importes entre 1,00 y 1.000,99 en orden arbitrario pero reproducible
n = 40_000
tabla = pa.table({"importe": pa.array(
    [round(1 + ((i * 7919) % 100_000) / 100, 2) for i in range(n)], pa.float64())})

def rango_primer_grupo(t):
    """Minimo y maximo del primer grupo de filas: lo que el motor usa para podar."""
    buffer = io.BytesIO()
    pq.write_table(t, buffer, compression="none", row_group_size=8_000)
    meta = pq.ParquetFile(io.BytesIO(buffer.getvalue())).metadata
    est = meta.row_group(0).column(0).statistics
    return f"{est.min:.1f} a {est.max:.1f} en {meta.num_row_groups} grupos"

print("sin ordenar:", rango_primer_grupo(tabla))                 # -> sin ordenar: 1.0 a 1000.9 en 5 grupos
print("ordenado por importe:", rango_primer_grupo(tabla.sort_by("importe")))  # -> ordenado por importe: 1.0 a 200.9 en 5 grupos
