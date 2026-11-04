import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

rng = np.random.default_rng(0)

# 500 filas de 20 columnas de ruido puro: ninguna senal, la exactitud real es 0.5
X = rng.normal(size=(500, 20))
y = rng.integers(0, 2, 500)

en_validacion, en_prueba = [], []
for ronda in range(10):
    Xtr, Xresto, ytr, yresto = train_test_split(X, y, test_size=0.5, random_state=ronda)
    Xva, Xte, yva, yte = train_test_split(Xresto, yresto, test_size=0.5, random_state=ronda)
    # 20 candidatos distintos: cada arbol mira 3 variables al azar en cada division
    modelos = [DecisionTreeClassifier(max_depth=5, max_features=3, random_state=s).fit(Xtr, ytr)
               for s in range(20)]
    notas = [m.score(Xva, yva) for m in modelos]
    elegido = modelos[int(np.argmax(notas))]     # el "mejor" segun validacion
    en_validacion.append(max(notas))
    en_prueba.append(elegido.score(Xte, yte))

print("elegido en validacion %.3f" % np.mean(en_validacion))   # -> elegido en validacion 0.577
print("el mismo en prueba    %.3f" % np.mean(en_prueba))       # -> el mismo en prueba    0.490
