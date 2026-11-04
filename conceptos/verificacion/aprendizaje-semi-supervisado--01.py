import numpy as np
from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression
from sklearn.semi_supervised import SelfTrainingClassifier, LabelSpreading
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

# Dos lunas: la geometria de los puntos SIN etiquetar tambien informa
X, y = make_moons(n_samples=200, noise=0.2, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=0)

y_parcial = np.full_like(y_tr, -1)                 # -1 significa "sin etiquetar"
etiquetados = np.array([0, 1, 2, 3, 40, 41, 42, 43, 80, 81, 82, 83])
y_parcial[etiquetados] = y_tr[etiquetados]         # 12 etiquetas de 150 filas

def evalua(modelo, objetivo):
    # Se ajusta con las 150 filas: las marcadas con -1 son candidatas y no cuentan en la perdida
    modelo.fit(X_tr, objetivo)
    # score devuelve np.float64; float() lo deja en un numero de Python corriente
    return round(float(modelo.score(X_te, y_te)), 3)

base = LogisticRegression(max_iter=1000).fit(X_tr[etiquetados], y_tr[etiquetados])
print("solo con las 12 etiquetas:", round(float(base.score(X_te, y_te)), 3))              # -> 0.72
print("pseudoetiquetado         :", evalua(SelfTrainingClassifier(
      LogisticRegression(max_iter=1000), threshold=0.75, max_iter=10), y_parcial))        # -> 0.44
print("propagacion de etiquetas :", evalua(LabelSpreading(
      kernel="knn", n_neighbors=7), y_parcial))                                           # -> 0.84
print("MLP con las 150 etiquetas:", evalua(MLPClassifier(hidden_layer_sizes=(16,),
      max_iter=2000, early_stopping=False, random_state=0), y_tr))                        # -> 0.84
