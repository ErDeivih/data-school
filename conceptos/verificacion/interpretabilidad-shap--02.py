import numpy as np
from sklearn.tree import DecisionTreeRegressor

rng = np.random.default_rng(0)
X = rng.uniform(0, 1, size=(300, 2))
y = 3 * X[:, 0] + 2 * (X[:, 1] > 0.5)

arbol = DecisionTreeRegressor(max_depth=3, random_state=0).fit(X, y)

# PDP de x1: prediccion media al fijar x1 = t y dejar x2 tal como esta en la muestra.
for t in (0.0, 0.25, 0.5, 0.75, 1.0):
    Xm = X.copy()        # copia, no vista: si no, machacarias la columna de X
    Xm[:, 0] = t
    print(f"x1={t:.2f}  PDP={arbol.predict(Xm).mean():.3f}")

# ICE del individuo 0: su curva sola, de x1=0 a x1=1.
Xm = X.copy()
Xm[:, 0] = 0.0
# El extremo izquierdo de SU curva es su prediccion con x1 forzado a 0, no su x1 real.
izq = arbol.predict(Xm)[0]
Xm[:, 0] = 1.0
print(f"ICE obs 0: {izq:.3f} -> {arbol.predict(Xm)[0]:.3f}")
# -> x1=0.00  PDP=1.436
# -> x1=0.25  PDP=1.436
# -> x1=0.50  PDP=2.593
# -> x1=0.75  PDP=2.934
# -> x1=1.00  PDP=3.688
# -> ICE obs 0: 0.395 -> 2.645
