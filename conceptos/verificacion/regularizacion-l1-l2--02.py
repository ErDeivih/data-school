import numpy as np
from sklearn.linear_model import Ridge

rng = np.random.default_rng(0)
n = 100
x1 = rng.normal(size=n)
x2 = 0.95 * x1 + rng.normal(scale=0.1, size=n)
x3 = rng.normal(size=n)
X = np.column_stack([x1, x2, x3])
y = 3 * x1 + rng.normal(scale=0.5, size=n)
X = (X - X.mean(axis=0)) / X.std(axis=0)      # centrada: el intercepto no se penaliza

X2 = X[:, :2]                                 # x1 y x2, las dos colineales
for lam in (0.0, 1.0, 10.0, 100.0):
    # Formula cerrada: sumar lam a la diagonal es lo unico que cambia respecto a OLS.
    manual = np.linalg.solve(X2.T @ X2 + lam * np.eye(2), X2.T @ y)
    # fit_intercept=False no cambia los coeficientes: la X ya esta centrada, asi que
    # sklearn obtendria el mismo resultado y solo sacaria aparte la media de y.
    sk = Ridge(alpha=lam, fit_intercept=False).fit(X2, y).coef_
    print(f"lambda {lam:>5.1f}  manual [{manual[0]:6.3f} {manual[1]:6.3f}]"
          f"  sklearn [{sk[0]:6.3f} {sk[1]:6.3f}]")
# -> lambda   0.0  manual [ 3.382 -0.527]  sklearn [ 3.382 -0.527]
# -> lambda   1.0  manual [ 2.101  0.740]  sklearn [ 2.101  0.740]
# -> lambda  10.0  manual [ 1.458  1.260]  sklearn [ 1.458  1.260]
# -> lambda 100.0  manual [ 0.961  0.940]  sklearn [ 0.961  0.940]
