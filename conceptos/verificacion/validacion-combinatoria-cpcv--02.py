import numpy as np
from itertools import combinations

rng = np.random.default_rng(0)
n_grupos, k, T = 6, 2, 120
ret = rng.normal(0.0005, 0.01, size=n_grupos * T)   # una sola estrategia, sin cambios
bloques = [ret[g * T:(g + 1) * T] for g in range(n_grupos)]

def sharpe_anual(x):
    return x.mean() / x.std(ddof=1) * np.sqrt(252)

# Cada camino es la concatenacion de los k bloques de prueba de esa combinacion.
srs = np.array([sharpe_anual(np.concatenate([bloques[g] for g in c]))
                for c in combinations(range(n_grupos), k)])
print(f"serie completa: Sharpe {sharpe_anual(ret):.2f}")      # -> 0.49
print(f"caminos {srs.size}  media {srs.mean():.2f}")          # -> 0.50
print(f"minimo {srs.min():.2f}  maximo {srs.max():.2f}")      # -> -0.60 y 1.47
print(f"p5 {np.percentile(srs, 5):.2f}  p95 {np.percentile(srs, 95):.2f}")  # -> -0.43 y 1.45
