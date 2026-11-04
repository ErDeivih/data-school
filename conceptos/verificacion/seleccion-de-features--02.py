import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score

rng = np.random.default_rng(0)
n = 60
X_real = rng.normal(size=(n, 5))
# Solo las 3 primeras tienen efecto; las otras 2 y las 45 de ruido no aportan nada.
y = X_real @ np.array([2.0, -1.0, 0.5, 0.0, 0.0]) + rng.normal(0, 1.0, n)
ruido = rng.normal(size=(n, 45))

solo_real = cross_val_score(LinearRegression(), X_real, y, cv=5, scoring="r2").mean()
con_ruido = cross_val_score(LinearRegression(), np.hstack([X_real, ruido]), y, cv=5, scoring="r2").mean()

print(f"R2 con 5 variables reales {solo_real:.2f}")   # -> 0.63
print(f"R2 con 45 ruido anadido   {con_ruido:.2f}")   # -> -7.53
