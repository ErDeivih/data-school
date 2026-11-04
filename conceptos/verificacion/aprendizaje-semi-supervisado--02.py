import numpy as np
from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression
from sklearn.semi_supervised import SelfTrainingClassifier
from sklearn.model_selection import train_test_split

# Dos lunas con muy pocas etiquetas: aqui el pseudoetiquetado hace dano
X, y = make_moons(n_samples=200, noise=0.2, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=0)
y_parcial = np.full_like(y_tr, -1)                 # -1 significa "sin etiquetar"
etiquetados = np.array([0, 1, 2, 3, 40, 41, 42, 43, 80, 81, 82, 83])
y_parcial[etiquetados] = y_tr[etiquetados]

base = LogisticRegression(max_iter=1000).fit(X_tr[etiquetados], y_tr[etiquetados])
print("base con 12 etiquetas:", round(float(base.score(X_te, y_te)), 3))        # -> 0.72

auto = SelfTrainingClassifier(LogisticRegression(max_iter=1000), threshold=0.75, max_iter=10)
auto.fit(X_tr, y_parcial)        # las 150 filas: las de etiqueta -1 son las candidatas
print("tras el pseudoetiquetado:", round(float(auto.score(X_te, y_te)), 3))     # -> 0.44
print("pseudoetiquetas anadidas:", int((auto.transduction_ >= 0).sum()) - len(etiquetados))  # -> 138
# transduction_ trae la etiqueta final de cada fila; compararla con y_tr mide cuantas acerto
print("acuerdo (sobre 150 filas):", round(float((auto.transduction_ == y_tr).mean()), 3))   # -> 0.56
