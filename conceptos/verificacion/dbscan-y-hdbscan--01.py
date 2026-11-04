import numpy as np
from sklearn.cluster import DBSCAN

# Nueve puntos en una recta: el mismo dato, tres valores de eps, tres respuestas.
# reshape(-1, 1): nueve puntos en una recta, como matriz de 9 filas y 1 columna.
X = np.array([0, 1, 2, 7, 8, 9, 20, 21, 22.0]).reshape(-1, 1)
for eps in (0.5, 1.5, 6.0):
    d = DBSCAN(eps=eps, min_samples=3).fit(X)
    # labels_ es un array de enteros; -1 significa ruido, no "sin clasificar".
    etiquetas = [int(e) for e in d.labels_]
    n_ruido = int((d.labels_ == -1).sum())
    print(f"eps={eps:<4} etiquetas {etiquetas}  ruido {n_ruido}")
# -> eps=0.5  etiquetas [-1, -1, -1, -1, -1, -1, -1, -1, -1]  ruido 9
# -> eps=1.5  etiquetas [0, 0, 0, 1, 1, 1, 2, 2, 2]  ruido 0
# -> eps=6.0  etiquetas [0, 0, 0, 0, 0, 0, 1, 1, 1]  ruido 0

# Cuales son puntos centrales con eps=1.5: los que tienen 3 vecinos o mas.
d = DBSCAN(eps=1.5, min_samples=3).fit(X)
# X es (9,1) y X.T es (1,9): la resta da una matriz 9x9 de distancias, y se
# cuentan las que no pasan de 1.5. Incluye el propio punto, d(p,p)=0.
vecinos = (np.abs(X - X.T) <= 1.5).sum(axis=1)
print("vecinos por punto (incluyendo el propio):", [int(v) for v in vecinos])
# -> vecinos por punto (incluyendo el propio): [2, 3, 2, 2, 3, 2, 2, 3, 2]
