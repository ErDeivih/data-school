import numpy as np

rng = np.random.default_rng(0)          # semilla fija: el resultado se repite igual
medias = {n: rng.integers(1, 7, size=n).mean() for n in (10, 100, 1000, 100000)}
for n, m in medias.items():
    print(f"n={n:>6}  media = {m:.4f}  error = {abs(m - 3.5):.4f}")

# El error baja con el tamano de la muestra, pero no de forma garantizada en cada camino:
# la ley habla del limite, no de cada paso.
print(f"error con n = 10     = {abs(medias[10] - 3.5):.4f}")      # -> 0.7000
print(f"error con n = 100000 = {abs(medias[100000] - 3.5):.4f}")  # -> 0.0015
