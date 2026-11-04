import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

rng = np.random.default_rng(1)
n = 8_000
X = rng.normal(0, 1, (n, 8))
senal = 1.2 * X[:, 0] + 0.8 * X[:, 1]
y = (senal + rng.normal(0, 1.0, n) > 0).astype(int)

# Se parte primero y se ensucia despues: la prueba queda limpia y el techo lo pone el ruido de entrenamiento
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)
ruido = rng.random(len(y_tr)) < 0.15
y_tr[ruido] = rng.integers(0, 2, len(y_tr))[ruido]

for prof in (2, 4, 6, 12, None):
    arbol = DecisionTreeClassifier(max_depth=prof, random_state=0).fit(X_tr, y_tr)
    print(f"profundidad {str(prof):>4}  entrenamiento {arbol.score(X_tr, y_tr):.4f}"
          f"  prueba {arbol.score(X_te, y_te):.4f}")
# -> profundidad    4  entrenamiento 0.7602  prueba 0.7863   (el mejor)
# -> profundidad None  entrenamiento 1.0000  prueba 0.6871   (memoriza el ruido)
