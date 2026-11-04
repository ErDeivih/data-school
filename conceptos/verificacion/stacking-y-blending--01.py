import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.neighbors import KNeighborsClassifier

X, y = make_classification(n_samples=600, n_features=12, n_informative=6,
                           class_sep=0.8, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)

base = {"bosque": RandomForestClassifier(n_estimators=60, random_state=0),
        "knn": KNeighborsClassifier(n_neighbors=9),
        "logit": LogisticRegression(max_iter=2000)}

# 1) Predicciones FUERA DE MUESTRA: la columna que el metamodelo debe ver.
Z_oof = np.zeros((len(y_tr), len(base)))
for m, (nombre, modelo) in enumerate(base.items()):
    for itr, iva in StratifiedKFold(5, shuffle=True, random_state=0).split(X_tr, y_tr):
        modelo.fit(X_tr[itr], y_tr[itr])
        Z_oof[iva, m] = modelo.predict_proba(X_tr[iva])[:, 1]

# 2) La version tramposa: predicciones del modelo ya entrenado con esas mismas filas.
Z_insample = np.column_stack([m.fit(X_tr, y_tr).predict_proba(X_tr)[:, 1] for m in base.values()])

meta_oof = LogisticRegression(max_iter=2000).fit(Z_oof, y_tr)
meta_ins = LogisticRegression(max_iter=2000).fit(Z_insample, y_tr)

print(f"AUC del metamodelo sobre Z fuera de muestra {roc_auc_score(y_tr, meta_oof.predict_proba(Z_oof)[:, 1]):.3f}")
print(f"AUC del metamodelo sobre Z en muestra      {roc_auc_score(y_tr, meta_ins.predict_proba(Z_insample)[:, 1]):.3f}")
