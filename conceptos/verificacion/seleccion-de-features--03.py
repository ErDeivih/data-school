import numpy as np
from sklearn.linear_model import Lasso

rng = np.random.default_rng(0)
X = rng.normal(size=(100, 6))
y = 3.0 * X[:, 0] - 2.0 * X[:, 3] + rng.normal(0, 0.5, 100)

# La penalizacion L1 lleva a cero las variables que no aportan: seleccion embebida.
lasso = Lasso(alpha=0.1).fit(X, y)
print("coeficientes:", [round(float(c), 2) if abs(c) > 0.005 else 0.0 for c in lasso.coef_])
# -> coeficientes: [2.91, 0.0, 0.0, -1.81, 0.0, 0.02]
print(f"variables anuladas {int((np.abs(lasso.coef_) < 0.005).sum())} de {lasso.coef_.size}")
# -> variables anuladas 3 de 6
