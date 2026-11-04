import numpy as np
from sklearn.datasets import make_classification
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV, StratifiedKFold, cross_val_score

# 60 muestras, 6 variables: una rejilla pequena cabe entera y se puede leer
X, y = make_classification(n_samples=60, n_features=6, n_informative=3,
                           n_redundant=0, random_state=0)
cv = StratifiedKFold(5, shuffle=True, random_state=0)   # baraja antes de partir, con semilla fija
rejilla = {"C": [0.1, 1.0, 10.0], "gamma": ["scale", 0.1, 1.0]}   # 9 combinaciones

# SVC va SIN ajustar: el buscador clona el modelo en cada pliegue y en cada combinacion
busqueda = GridSearchCV(SVC(kernel="rbf"), rejilla, cv=cv, scoring="accuracy").fit(X, y)
print("combinaciones evaluadas:", len(busqueda.cv_results_["params"]))   # -> 9
print("mejor C y gamma        :", busqueda.best_params_)                 # -> {'C': 1.0, 'gamma': 'scale'}
print("mejor accuracy en CV   :", round(busqueda.best_score_, 3))       # -> 0.85

# La aleatoria gasta 4 intentos en vez de 9 y muestrea en escala logaritmica
rng = np.random.default_rng(0)
mejores = []
for _ in range(4):
    C = float(10 ** rng.uniform(-1, 1))    # de 0,1 a 10
    g = float(10 ** rng.uniform(-2, 0))    # de 0,01 a 1
    s = cross_val_score(SVC(kernel="rbf", C=C, gamma=g), X, y, cv=cv).mean()
    mejores.append((round(float(s), 3), round(C, 2), round(g, 3)))
print("mejor de 4 aleatorias  :", max(mejores))   # -> (0.833, 1.63, 0.288)
