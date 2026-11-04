import numpy as np
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist

# Tres enlaces, tres historiales de fusion distintos con los mismos cuatro puntos.
X = np.array([0.0, 1.0, 4.0, 9.0]).reshape(-1, 1)
for metodo in ("single", "complete", "average"):
    Z = linkage(X, method=metodo)
    # Z tiene n-1 filas: (grupo A, grupo B, altura de la fusion, tamano).
    # La altura esta en la columna 2, no en la 3.
    print(f"{metodo:>9}  alturas de fusion {np.round(Z[:, 2], 3)}")
    print(f"           cortando a distancia 3 -> {[int(e) for e in fcluster(Z, t=3, criterion='distance')]}")
    print(f"           cortando a distancia 4 -> {[int(e) for e in fcluster(Z, t=4, criterion='distance')]}")
# ->    single  alturas de fusion [1. 3. 5.]
# ->            cortando a distancia 3 -> [1, 1, 1, 2]
# ->            cortando a distancia 4 -> [1, 1, 1, 2]
# ->  complete  alturas de fusion [1. 4. 9.]
# ->            cortando a distancia 3 -> [1, 1, 2, 3]
# ->            cortando a distancia 4 -> [1, 1, 1, 2]
# ->   average  alturas de fusion [1.    3.5   7.333]
# ->            cortando a distancia 3 -> [1, 1, 2, 3]
# ->            cortando a distancia 4 -> [1, 1, 1, 2]

print("distancias entre pares:", np.round(pdist(X), 3))
# -> distancias entre pares: [1. 4. 9. 3. 8. 5.]
