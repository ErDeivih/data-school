import numpy as np
from sklearn import metrics

# Cuatro puntos en las esquinas de un rectangulo: dos particiones posibles.
X = np.array([[0.0, 0.0], [0.0, 2.0], [10.0, 0.0], [10.0, 2.0]])
por_x = np.array([0, 0, 1, 1])          # {(0,0),(0,2)} y {(10,0),(10,2)}
por_y = np.array([0, 1, 0, 1])          # {(0,0),(10,0)} y {(0,2),(10,2)}

for nombre, et in (("cortando por x", por_x), ("cortando por y", por_y)):
    print(nombre,
          "silueta", round(metrics.silhouette_score(X, et), 3),
          "davies", round(metrics.davies_bouldin_score(X, et), 3),
          "calinski", round(metrics.calinski_harabasz_score(X, et), 3))
# -> cortando por x silueta 0.802 davies 0.2 calinski 50.0
# -> cortando por y silueta -0.39 davies 5.0 calinski 0.08
print("silueta punto a punto:", np.round(metrics.silhouette_samples(X, por_y), 4))
# -> silueta punto a punto: [-0.3901 -0.3901 -0.3901 -0.3901]
