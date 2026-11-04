import numpy as np
from scipy import stats

# Tres grupos SIN ninguna diferencia real: cuantas veces "sale algo" haciendo 3 t-tests.
rng = np.random.default_rng(1)
reps, n = 20000, 20
x = rng.normal(0, 1, (reps, 3, n))
media, var = x.mean(axis=2), x.var(axis=2, ddof=1)

def p_valor(i, j):
    ee2 = var[:, i] / n + var[:, j] / n                     # version de Welch
    t = (media[:, i] - media[:, j]) / np.sqrt(ee2)
    gl = ee2**2 / ((var[:, i] / n)**2 / (n - 1) + (var[:, j] / n)**2 / (n - 1))
    return 2 * stats.t.sf(np.abs(t), gl)

pares = [p_valor(0, 1), p_valor(0, 2), p_valor(1, 2)]
print(f"falso positivo con 3 t-tests: {(np.minimum.reduce(pares) < 0.05).mean():.3f}")
# -> falso positivo con 3 t-tests: 0.124
print(f"cota si los tests fueran independientes: {1 - 0.95**3:.3f}")
# -> cota si los tests fueran independientes: 0.143
