import copy

import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.neighbors import KNeighborsClassifier

# Por que el metamodelo debe ser simple: con 600 filas y 2 columnas,
# un metamodelo muy flexible se ajusta al ruido de las predicciones.
X, y = make_classification(n_samples=600, n_features=12, n_informative=6,
                           class_sep=0.8, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)

Z_tr = np.zeros((len(y_tr), 2))
Z_te = np.zeros((len(y_te), 2))
for m, modelo in enumerate([LogisticRegression(max_iter=2000), KNeighborsClassifier(n_neighbors=9)]):
    for itr, iva in StratifiedKFold(5, shuffle=True, random_state=0).split(X_tr, y_tr):
        mod = copy.deepcopy(modelo).fit(X_tr[itr], y_tr[itr])
        Z_tr[iva, m] = mod.predict_proba(X_tr[iva])[:, 1]
    mod = copy.deepcopy(modelo).fit(X_tr, y_tr)
    Z_te[:, m] = mod.predict_proba(X_te)[:, 1]

# Un metamodelo que memoriza la matriz Z saca 1.000 en entrenamiento y pierde en prueba.
for nombre, meta in (("logistica L2", LogisticRegression(max_iter=2000)),
                     ("knn k=1", KNeighborsClassifier(n_neighbors=1)),
                     ("knn k=3", KNeighborsClassifier(n_neighbors=3))):
    meta.fit(Z_tr, y_tr)
    auc_tr = roc_auc_score(y_tr, meta.predict_proba(Z_tr)[:, 1])
    auc_te = roc_auc_score(y_te, meta.predict_proba(Z_te)[:, 1])
    print(f"{nombre:<14} AUC entrenamiento {auc_tr:.3f}   AUC prueba {auc_te:.3f}   diferencia {auc_tr - auc_te:+.3f}")
# -> logistica L2   AUC entrenamiento 0.886   AUC prueba 0.900   diferencia -0.015
# -> knn k=1        AUC entrenamiento 1.000   AUC prueba 0.750   diferencia +0.250
# -> knn k=3        AUC entrenamiento 0.936   AUC prueba 0.836   diferencia +0.100
