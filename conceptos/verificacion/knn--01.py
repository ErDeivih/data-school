import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# n_informative=4: solo 4 de las 8 columnas llevan senal; de las otras 4, dos son
# combinaciones de las informativas y dos son ruido, asi que la distancia se calcula
# en 8 dimensiones y esas 4 no aportan informacion nueva.
X, y = make_classification(n_samples=400, n_features=8, n_informative=4,
                           class_sep=1.0, random_state=0)
# Devuelve cuatro arrays en este orden fijo: X e y de entrenamiento y de prueba.
# stratify=y reparte las clases en la misma proporcion en las dos partes.
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=0)

# k=1 memoriza: acierta el 100 % del entrenamiento y generaliza peor.
print(f"{'k':>3}  {'exactitud train':>15}  {'exactitud test':>15}")
for k in (1, 3, 15, 45):
    m = KNeighborsClassifier(n_neighbors=k).fit(X_tr, y_tr)
    print(f"{k:>3}  {m.score(X_tr, y_tr):>15.3f}  {m.score(X_te, y_te):>15.3f}")
# ->   k  exactitud train   exactitud test
# ->   1            1.000            0.825
# ->   3            0.896            0.833
# ->  15            0.879            0.842
# ->  45            0.886            0.850
