import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

rng = np.random.default_rng(0)
X = rng.normal(size=(300, 4))
y = (X[:, 0] + X[:, 1] > 0).astype(int)
y = np.where(rng.random(300) < 0.15, 1 - y, y)      # 15 % de etiquetas cambiadas al azar

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4, random_state=0)

for prof in (1, 3, None):
    arbol = DecisionTreeClassifier(max_depth=prof, random_state=0).fit(X_tr, y_tr)
    print(f"profundidad {str(prof):>4}  train {arbol.score(X_tr, y_tr):.3f}  test {arbol.score(X_te, y_te):.3f}")
# -> profundidad    1  train 0.678  test 0.658
# -> profundidad    3  train 0.772  test 0.717
# -> profundidad None  train 1.000  test 0.650
