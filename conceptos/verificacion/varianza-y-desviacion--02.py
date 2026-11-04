import numpy as np
from itertools import product

alturas = np.array([1.62, 1.71, 1.68, 1.75, 1.80, 1.66])

# ddof=1 divide por n-1: estimamos la media y gastamos un grado de libertad.
print(f"media          = {alturas.mean():.4f} m")        # -> 1.7033 m
print(f"varianza ddof0 = {alturas.var(ddof=0):.5f} m^2")  # -> 0.00349 m^2
print(f"varianza ddof1 = {alturas.var(ddof=1):.5f} m^2")  # -> 0.00419 m^2
print(f"desv. tipica   = {alturas.std(ddof=1):.4f} m")    # -> 0.0647 m

# Dos dados independientes: las varianzas se suman, las desviaciones no.
suma = np.array([a + b for a, b in product(range(1, 7), repeat=2)], dtype=float)
dado = np.arange(1, 7, dtype=float)
print(f"Var(suma) = {suma.var():.4f}  = 2 * {dado.var():.4f}")   # -> 5.8333  = 2 * 2.9167
