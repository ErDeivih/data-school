import numpy as np
from scipy import stats

# Cumulantes teoricos: la normal solo tiene los dos primeros.
print(f"normal  curtosis de exceso = {stats.norm.stats(moments='k'):.4f}")    # -> 0.0000
print(f"t(5)    curtosis de exceso = {stats.t.stats(5, moments='k'):.4f}")    # -> 6.0000
print(f"t(4)    curtosis de exceso = {stats.t.stats(4, moments='k'):.4f}")    # -> inf
print(f"t(30)   curtosis de exceso = {stats.t.stats(30, moments='k'):.4f}")   # -> 0.2308
print(f"lognormal(s=1) exceso     = {stats.lognorm.stats(s=1.0, moments='k'):.4f}")  # -> 110.9364

# La varianza de una cartera mezcla varianzas y covarianza.
x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
y = np.array([2.0, 1.0, 4.0, 3.0, 6.0])
a, b = 0.6, 0.4
directa = np.var(a * x + b * y, ddof=1)
formula = a**2 * x.var(ddof=1) + b**2 * y.var(ddof=1) + 2 * a * b * np.cov(x, y, ddof=1)[0, 1]
print(f"varianza directa = {directa:.6f}")   # -> 2.692000
print(f"varianza formula = {formula:.6f}")   # -> 2.692000
print(f"cov = {np.cov(x, y, ddof=1)[0, 1]:.4f}  corr = {np.corrcoef(x, y)[0, 1]:.4f}")  # -> cov = 2.5000  corr = 0.8220
