import numpy as np

# Matriz 4x3 de rango 2: truncar en k=2 la reconstruye exactamente.
D = np.array([[1.0, 2.0, 3.0],
              [4.0, 5.0, 6.0],
              [7.0, 8.0, 9.0],
              [10.0, 11.0, 12.0]])
U, s, Vt = np.linalg.svd(D, full_matrices=False)

print("valores singulares:", np.round(s, 4).tolist())   # -> [25.4624, 1.2907, 0.0]
print("rango:", int(np.linalg.matrix_rank(D)))          # -> 2

D1 = U[:, :1] @ np.diag(s[:1]) @ Vt[:1, :]
D2 = U[:, :2] @ np.diag(s[:2]) @ Vt[:2, :]
print("k=1 error relativo:", round(float(np.linalg.norm(D - D1) / np.linalg.norm(D)), 4))   # -> 0.0506
print("k=2 error relativo:", round(float(np.linalg.norm(D - D2) / np.linalg.norm(D)), 4))   # -> 0.0

# Coste de guardar una matriz grande truncada frente a guardarla entera.
print("numeros con k=10 en 1000x1000:", 1000 * 10 + 10 + 1000 * 10, "de", 1000 * 1000)   # -> 20010 de 1000000
