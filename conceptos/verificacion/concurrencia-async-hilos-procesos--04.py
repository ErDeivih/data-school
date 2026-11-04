import pickle
import tracemalloc

import numpy as np

datos = np.arange(1_000_000, dtype=np.float64)      # 8 MB

tracemalloc.start()
serializado = pickle.dumps(datos)                   # lo que viaja por la tuberia al hijo
copia = pickle.loads(serializado)                   # y lo que el hijo reconstruye en su memoria
actual, pico = tracemalloc.get_traced_memory()
tracemalloc.stop()

print("bytes del array original:", datos.nbytes)                        # -> 8000000
print("bytes del array reconstruido:", copia.nbytes)                    # -> 8000000
print(f"pico medido durante la copia {pico / 1024 / 1024:.1f} MiB")
print("el hijo no ve el array del padre: lo reconstruye entero")
