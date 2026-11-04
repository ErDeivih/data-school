import numpy as np

A = np.array([[2.0, 1.0], [1.0, 2.0]])   # simetrica: autovalores reales y autovectores ortogonales

w, V = np.linalg.eigh(A)     # eigh para simetricas; eig no ordena y devuelve complejos si toca
print("autovalores:", np.round(w, 4).tolist())            # -> [1.0, 3.0]
print("autovectores:", np.round(V, 4).tolist())           # -> [[-0.7071, 0.7071], [0.7071, 0.7071]]
print("traza y determinante:", float(np.trace(A)), round(float(np.linalg.det(A)), 1))   # -> 4.0 3.0

# Comprobacion directa de Av = lambda v para el autovalor dominante.
v2 = V[:, 1]
print("A @ v - 3v:", np.round(A @ v2 - w[1] * v2, 10).tolist())   # -> [0.0, 0.0]
