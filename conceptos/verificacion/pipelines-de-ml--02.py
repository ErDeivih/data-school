import numpy as np
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score, StratifiedKFold

# 500 columnas y solo 3 con senal: el escenario donde la fuga se ve a simple vista
# flip_y=0.15 mete ruido en la etiqueta, asi que ni el modelo perfecto pasa de ~0.85
X, y = make_classification(n_samples=60, n_features=500, n_informative=3,
                           n_redundant=0, flip_y=0.15, random_state=0)

# MAL: elegir las 20 variables "buenas" mirando TODAS las filas y luego validar
# get_support() devuelve una mascara booleana de 500 posiciones; con ella se indexan columnas
buenas = SelectKBest(f_classif, k=20).fit(X, y).get_support()
# max_iter alto por si acaso: el ajuste real es sobre las 20 columnas elegidas, no sobre las 500
print("antes de validar:", round(cross_val_score(LogisticRegression(max_iter=1000),
      X[:, buenas], y, cv=5).mean(), 3))                                   # -> 0.867

# BIEN: la seleccion vive dentro del pipeline y se reajusta en cada pliegue
limpio = make_pipeline(SelectKBest(f_classif, k=20), LogisticRegression(max_iter=1000))
print("dentro del pipe :", round(cross_val_score(limpio, X, y,
      cv=StratifiedKFold(5, shuffle=True, random_state=0)).mean(), 3))      # -> 0.417
