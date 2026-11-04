import numpy as np
from scipy import stats

# Relacion determinista y perfecta que ninguna de las dos correlaciones detecta
x = np.arange(-4, 5, dtype=float)
y = x ** 2

print("Pearson ", round(float(stats.pearsonr(x, y)[0]), 4))    # -> 0.0
print("Spearman", round(float(stats.spearmanr(x, y)[0]), 4))   # -> 0.0
