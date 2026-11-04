import numpy as np
from scipy import stats

# Ocho retornos mensuales de un fondo, en %.
r = np.array([2.1, -0.4, 1.3, -3.2, 0.8, 5.6, -1.1, 0.2])

print(f"media        = {r.mean():.4f}")                                    # -> 0.6625
print(f"varianza     = {r.var(ddof=1):.4f}")                               # -> 6.6055
print(f"asimetria    = {stats.skew(r, bias=False):.4f}")                   # -> 0.6643
print(f"curtosis ex. = {stats.kurtosis(r, fisher=True, bias=False):.4f}")  # -> 1.6401

# Los k-estadisticos estiman los cumulantes; k2 es la varianza muestral.
print(f"k1 = {stats.kstat(r, 1):.4f}")   # -> 0.6625
print(f"k2 = {stats.kstat(r, 2):.4f}")   # -> 6.6055
print(f"k3 = {stats.kstat(r, 3):.4f}")   # -> 11.2772
print(f"k4 = {stats.kstat(r, 4):.4f}")   # -> 71.5613
