import numpy as np
from sklearn.svm import SVC

# El truco del nucleo: XOR no es separable con una recta, con un polinomio de grado 2 si.
rng = np.random.default_rng(0)
X = rng.normal(size=(200, 2))
y = np.where(X[:, 0] * X[:, 1] > 0, 1, -1)   # dos cuadrantes opuestos

for nombre, params in (("linear", {}),
                       ("poly", {"degree": 2, "gamma": 1.0, "coef0": 1.0}),
                       ("rbf", {"gamma": 1.0})):
    m = SVC(kernel=nombre, C=1.0, **params).fit(X, y)
    print(f"{nombre:>6}  exactitud {m.score(X, y):.3f}  vectores de soporte {len(m.support_)} de {X.shape[0]}")
# -> linear  exactitud 0.540  vectores de soporte 192 de 200
# ->   poly  exactitud 0.965  vectores de soporte 52 de 200
# ->    rbf  exactitud 0.980  vectores de soporte 82 de 200
