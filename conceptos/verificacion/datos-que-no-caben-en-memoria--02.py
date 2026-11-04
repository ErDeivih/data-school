import io
import tracemalloc

import numpy as np
import pandas as pd

# Un CSV de 200.000 filas y 3 columnas numericas, construido en memoria
rng = np.random.default_rng(0)
partes = ["a,b,c"]
for i in range(200_000):
    partes.append(f"{i},{rng.random():.6f},{i % 7}")
texto = "\n".join(partes) + "\n"

# tracemalloc mide lo que pide Python, no lo que ocupa el fichero en disco
tracemalloc.start()
completo = pd.read_csv(io.StringIO(texto))
pico_completo, _ = tracemalloc.get_traced_memory()
tracemalloc.stop()

tracemalloc.start()
suma = 0.0
for bloque in pd.read_csv(io.StringIO(texto), chunksize=10_000):
    suma += float(bloque["b"].sum())
    memoria_bloque = bloque.memory_usage(deep=True).sum()
pico_bloques, _ = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(len(completo), round(completo.memory_usage(deep=True).sum() / 1e6, 1))  # -> 200000 4.8
print(round(memoria_bloque / 1e6, 2))          # -> 0.24  un bloque, siempre igual
print(pico_completo > 10 * pico_bloques)       # -> True  el pico del bloque es minimo
