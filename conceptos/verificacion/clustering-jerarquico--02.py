import numpy as np
from scipy.cluster.hierarchy import linkage
from sklearn.datasets import make_blobs

# Ward sobre tres grupos bien separados: el salto de altura marca donde cortar.
X, verdad = make_blobs(n_samples=150, centers=3, cluster_std=0.5, random_state=0)
Z = linkage(X, method="ward")
print("tamano real de cada grupo:", np.bincount(verdad))
print("alturas de las 3 ultimas fusiones:", np.round(Z[-3:, 2], 3))
print("salto entre la 2.a y la 3.a por la cola:", round(Z[-2, 2] / Z[-3, 2], 2))
