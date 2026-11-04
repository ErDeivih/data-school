import numpy as np

# Camino de 4 nodos con autoenlaces y normalizacion simetrica D^-1/2 A D^-1/2.
A = np.array([[1, 1, 0, 0],
              [1, 1, 1, 0],
              [0, 1, 1, 1],
              [0, 0, 1, 1]], float)
d = A.sum(axis=1)                # grado de cada nodo, contando el autoenlace de la diagonal
# np.outer(d, d) es la matriz d_u * d_v de todos los pares; la raiz de eso divide cada arista
# por la raiz del grado de sus dos extremos, que es la normalizacion simetrica.
A_hat = A / np.sqrt(np.outer(d, d))

H = np.array([[1.0, 0.0],
              [0.0, 1.0],
              [1.0, 1.0],
              [2.0, 0.0]])

print("capa 0:")
print(H)
print("capa 1 (cada nodo agrega los mensajes de sus vecinos):")
# @ es el producto matricial: una capa entera de paso de mensajes en una sola operacion.
print(np.round(A_hat @ H, 3))
