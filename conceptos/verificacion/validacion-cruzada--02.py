import numpy as np
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.neighbors import KNeighborsClassifier

rng = np.random.default_rng(2)
n = 80
y = (rng.random(n) < 0.5).astype(int)
X = rng.normal(size=(n, 4)) + y[:, None] * 0.5
rejilla = {"n_neighbors": [3, 5, 9, 15, 25]}

# Lo habitual: elegir los hiperparametros y quedarse con la nota de esa misma busqueda
busqueda = GridSearchCV(KNeighborsClassifier(), rejilla, cv=5, scoring="accuracy").fit(X, y)

# Lo correcto: la busqueda va dentro de cada pliegue exterior
anidada = cross_val_score(GridSearchCV(KNeighborsClassifier(), rejilla, cv=5),
                          X, y, cv=5, scoring="accuracy")

print("mejor k %d" % busqueda.best_params_["n_neighbors"])   # -> mejor k 9
print("CV interno %.3f" % busqueda.best_score_)              # -> CV interno 0.700
print("CV anidado %.3f" % anidada.mean())                    # -> CV anidado 0.637
print("pliegues anidados", np.round(anidada, 3).tolist())
# -> pliegues anidados [0.5, 0.75, 0.688, 0.5, 0.75]
