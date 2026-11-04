import numpy as np
import pandas as pd

# 4.000 locales en una region de 100 x 100 km. Buscamos parejas a menos de 1 km.
rng = np.random.default_rng(0)
df = pd.DataFrame(rng.uniform(0.0, 100.0, (4000, 2)), columns=["x", "y"])
df["i"] = np.arange(len(df))
df["cx"] = (df.x // 5).astype(int)      # rejilla de 5 km: la clave de un geohash
df["cy"] = (df.y // 5).astype(int)

calculadas, pares = 0, 0
izq = df.rename(columns={"cx": "kx", "cy": "ky"})
for dx in (-1, 0, 1):                    # la celda y sus ocho vecinas
    for dy in (-1, 0, 1):
        der = df.assign(kx=df.cx + dx, ky=df.cy + dy)[["kx", "ky", "x", "y", "i"]]
        m = izq.merge(der, on=["kx", "ky"], suffixes=("_a", "_b"))
        calculadas += len(m)             # solo estos pares llegan a medir una distancia
        d = np.hypot(m.x_a - m.x_b, m.y_a - m.y_b)
        pares += int(((d <= 1.0) & (m.i_a != m.i_b)).sum())

print(f"pares posibles         {df.shape[0] ** 2}")     # -> 16000000
print(f"distancias calculadas  {calculadas}")           # -> 342032
print(f"parejas a menos de 1 km {pares // 2}")          # -> 2507
