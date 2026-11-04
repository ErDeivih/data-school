import numpy as np
from scipy import stats

# Ocho piezas medidas; la tolerancia nominal es 5,5 mm
piezas = np.array([5.2, 4.8, 6.1, 5.5, 4.9, 5.8, 5.0, 6.3])
mu0 = 5.5

# t de Student para una media: compara x_barra con mu0 usando el error tipico
t, p = stats.ttest_1samp(piezas, popmean=mu0)

print(f"media muestral    {piezas.mean():.3f}")       # -> 5.450
print(f"desv muestral     {piezas.std(ddof=1):.3f}")  # -> 0.568
print(f"estadistico t     {t:.3f}")                   # -> -0.249
print(f"p-valor           {p:.3f}")                   # -> 0.811
print("decision:", "rechazar" if p <= 0.05 else "no rechazar")  # -> no rechazar
