import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score
from sklearn.model_selection import train_test_split

# Dos nubes de puntos solapadas: la clase rara son 200 filas de 4.000.
rng = np.random.default_rng(0)
n_may, n_min = 3800, 200
X = np.vstack([rng.normal(0.0, 1.0, (n_may, 2)), rng.normal(1.2, 1.0, (n_min, 2))])
y = np.array([0] * n_may + [1] * n_min)

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0, stratify=y)
sin_peso = LogisticRegression(max_iter=1000).fit(X_tr, y_tr)
con_peso = LogisticRegression(max_iter=1000, class_weight="balanced").fit(X_tr, y_tr)

print(f"positivos en prueba {int(y_te.sum())} de {y_te.size}")   # -> 60 de 1200
print(f"recall sin pesos                 {recall_score(y_te, sin_peso.predict(X_te)):.2f}")   # -> 0.18
print(f"recall con class_weight balanced {recall_score(y_te, con_peso.predict(X_te)):.2f}")   # -> 0.68
