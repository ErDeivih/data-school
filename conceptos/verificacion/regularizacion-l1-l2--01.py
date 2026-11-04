import numpy as np
from sklearn.linear_model import Lasso, LinearRegression, Ridge

rng = np.random.default_rng(0)
n = 100
x1 = rng.normal(size=n)
x2 = 0.95 * x1 + rng.normal(scale=0.1, size=n)   # casi colineal con x1
x3 = rng.normal(size=n)                          # ruido puro
X = np.column_stack([x1, x2, x3])
y = 3 * x1 + rng.normal(scale=0.5, size=n)

# Penalizar sin estandarizar castiga mas a la variable con menos escala.
X = (X - X.mean(axis=0)) / X.std(axis=0)   # axis=0: una media por columna, no por fila

for nombre, modelo in (("OLS  ", LinearRegression()),
                       ("Lasso", Lasso(alpha=0.1, max_iter=10000)),   # L1: anula coeficientes
                       ("Ridge", Ridge(alpha=1.0))):                  # L2: solo los encoge
    modelo.fit(X, y)
    coef = " ".join(f"{c:6.3f}" for c in modelo.coef_)   # coef_ es un array, no un numero
    print(f"{nombre} {coef}")
# -> OLS    3.386 -0.530  0.012
# -> Lasso  2.758  0.000  0.000
# -> Ridge  2.102  0.739  0.007
