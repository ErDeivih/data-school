import numpy as np
from scipy import stats

x = np.arange(1, 9, dtype=float)
lineal = x.copy()                                   # y = x
con_atipico = np.array([1, 2, 3, 4, 5, 6, 7, 20], dtype=float)
curva = x ** 2                                      # monotona, pero no lineal

for nombre, y in (("lineal", lineal), ("atipico", con_atipico), ("curva", curva)):
    r = stats.pearsonr(x, y)[0]
    rho = stats.spearmanr(x, y)[0]
    print(f"{nombre:>8}  Pearson {r:+.4f}  Spearman {rho:+.4f}")
# ->   lineal  Pearson +1.0000  Spearman +1.0000
# ->  atipico  Pearson +0.8165  Spearman +1.0000
# ->    curva  Pearson +0.9762  Spearman +1.0000
