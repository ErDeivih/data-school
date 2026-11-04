import numpy as np

A = np.array([[2.0, 1.0], [1.0, 3.0]])
b = np.array([5.0, 10.0])

print("det(A):", round(float(np.linalg.det(A)), 1))   # -> 5.0
print("rango(A):", np.linalg.matrix_rank(A))          # -> 2

# Resolver el sistema es mas estable que invertir la matriz y multiplicar.
x = np.linalg.solve(A, b)
print("solucion:", np.round(x, 6).tolist())           # -> [1.0, 3.0]
print("A @ x   :", (A @ x).tolist())                  # -> [5.0, 10.0]

# Duplicar una columna deja rango 1: el sistema pierde la solucion unica.
B = np.array([[2.0, 4.0], [1.0, 2.0]])
print("rango(B):", np.linalg.matrix_rank(B))          # -> 1
