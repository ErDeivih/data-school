import numpy as np
from scipy import stats

# Dos series independientes que solo suben: correlacion alta sin ninguna relacion
rng = np.random.default_rng(0)
n = 50
t = np.arange(n)
a = 0.5 * t + rng.normal(0, 1, n)
b = 0.2 * t + rng.normal(0, 1, n)

print("en niveles", round(float(stats.pearsonr(a, b)[0]), 2))          # -> 0.93
print("en cambios", round(float(stats.pearsonr(np.diff(a), np.diff(b))[0]), 2))  # -> 0.02
