import numpy as np

R = np.array([[0.0, -1.0], [1.0, 0.0]])
S = np.array([[2.0, 0.0], [0.0, 3.0]])
P = np.array([[1.0, 0.0], [0.0, 0.0]])

# Las columnas de la matriz son las imagenes de los vectores de la base.
print("columnas de R:", (R @ np.eye(2)).tolist())    # -> [[0.0, -1.0], [1.0, 0.0]]

# El determinante es el factor de area: S multiplica por 6 y P aplasta a cero.
print("det(S) y det(P):", round(float(np.linalg.det(S)), 1),
      round(float(np.linalg.det(P)), 1))             # -> 6.0 0.0

# Proyectar dos veces es proyectar una vez: P es idempotente.
print("P @ P == P:", bool(np.array_equal(P @ P, P)))      # -> True
print("P @ (3,1):", (P @ np.array([3.0, 1.0])).tolist())  # -> [3.0, 0.0]

# Cizallar conserva el area aunque mueva los puntos.
H = np.array([[1.0, 1.0], [0.0, 1.0]])
print("H @ (2,1):", (H @ np.array([2.0, 1.0])).tolist(),
      "det:", round(float(np.linalg.det(H)), 1))         # -> [3.0, 1.0] det: 1.0
