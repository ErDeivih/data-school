import numpy as np

# Sobre-suavizado: al apilar capas, todos los nodos acaban pareciendose.
n = 6
# np.eye(n, k=1) es la diagonal desplazada una posicion: sumando la identidad y las dos
# diagonales vecinas sale la matriz de adyacencia de un camino, con autoenlaces incluidos.
A = np.eye(n) + np.eye(n, k=1) + np.eye(n, k=-1)     # camino de 6 nodos
d = A.sum(axis=1)
A_hat = A / np.sqrt(np.outer(d, d))
rng = np.random.default_rng(0)
H = rng.normal(size=(n, 3))

for capas in (1, 2, 4, 8, 32):
    Hk = np.linalg.matrix_power(A_hat, capas) @ H
    Hn = Hk / np.linalg.norm(Hk, axis=1, keepdims=True)   # normalizamos para medir direccion
    # Hn @ Hn.T es la matriz de productos escalares entre todos los pares de nodos: con las
    # filas normalizadas, cada entrada ES el coseno del angulo entre esos dos nodos.
    S = Hn @ Hn.T
    iu = np.triu_indices(n, 1)                            # solo pares distintos
    print(f"capas={capas:>3}  coseno medio entre pares de nodos={S[iu].mean():.4f}")
# -> capas=  1  coseno medio entre pares de nodos=-0.0625
# -> capas=  2  coseno medio entre pares de nodos=-0.0415
# -> capas=  4  coseno medio entre pares de nodos=0.0979
# -> capas=  8  coseno medio entre pares de nodos=0.7973
# -> capas= 32  coseno medio entre pares de nodos=0.9999
