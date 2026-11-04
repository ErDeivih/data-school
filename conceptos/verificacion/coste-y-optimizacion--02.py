import io
import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

rng = np.random.default_rng(7)
filas = 200_000
tabla = pa.table({
    "pais": pa.array(rng.choice(["ES", "FR", "DE", "IT"], filas)),
    "importe": pa.array(np.round(rng.lognormal(3.0, 0.8, filas), 2)),
    "unidades": pa.array(rng.integers(1, 20, filas)),
})

def tamano(t, **kw):
    destino = io.BytesIO()          # medimos en memoria: nada de ficheros externos
    pq.write_table(t, destino, **kw)
    return destino.tell()

print("todo, sin comprimir:", tamano(tabla, compression="none") // 1024, "KiB")  # -> 615 KiB
print("todo, gzip:         ", tamano(tabla, compression="gzip") // 1024, "KiB")  # -> 546 KiB
print("solo pais (gzip):   ", tamano(tabla.select(["pais"]), compression="gzip") // 1024, "KiB")     # -> 50 KiB
print("solo importe (gzip):", tamano(tabla.select(["importe"]), compression="gzip") // 1024, "KiB")  # -> 376 KiB
