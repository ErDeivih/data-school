import numpy as np

lado = np.array([1, 1, -1, 1, -1, -1, 1, 1, -1, 1, -1, -1])
y    = np.array([1, -1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1])
p    = np.array([0.78, 0.72, 0.66, 0.58, 0.55, 0.71, 0.83, 0.33, 0.62, 0.69, 0.44, 0.30])

z = ((lado * y) > 0).astype(int)
toma = p >= 0.5

r_multiple = np.where(z == 1, 1.6, -1.0)     # 1,6R si acierta, -1R si falla
print(f"sin filtro  E[R] {r_multiple.mean():+.3f}  operaciones {z.size}")       # -> +0.733
print(f"sin filtro  total {r_multiple.sum():+.1f}R")                          # -> +8.8R
print(f"con filtro  E[R] {r_multiple[toma].mean():+.3f}  operaciones {toma.sum()}")  # -> +1.022
print(f"con filtro  total {r_multiple[toma].sum():+.1f}R")                    # -> +9.2R
