import numpy as np

A = np.array([[1.0, 2.0], [2.0, 4.0]])   # rango 1: la 2.a fila es el doble de la 1.a
U, s, Vt = np.linalg.svd(A)

print("valores singulares:", np.round(s, 6).tolist())                  # -> [5.0, 0.0]
print("rango:", int(np.linalg.matrix_rank(A)))                         # -> 1
print("reconstruccion:", np.round(U @ np.diag(s) @ Vt, 6).tolist())    # -> [[1.0, 2.0], [2.0, 4.0]]

# La aproximacion de rango 1 es exacta: sigma1 * u1 * v1^T reconstruye toda la matriz.
print("aproximacion rango 1:", np.round(s[0] * np.outer(U[:, 0], Vt[0, :]), 6).tolist())   # -> [[1.0, 2.0], [2.0, 4.0]]
