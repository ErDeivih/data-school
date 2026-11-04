import numpy as np

A = np.array([[2.0, 1.0], [1.0, 2.0]])
x0 = np.array([1.0, 0.0])

# Con autovalores 3 y 1, el termino dominante multiplica por 3 en cada paso.
print("A @ x0   :", (A @ x0).tolist())                            # -> [2.0, 1.0]
print("A^2 @ x0 :", (np.linalg.matrix_power(A, 2) @ x0).tolist())  # -> [5.0, 4.0]
print("A^10 @ x0:", (np.linalg.matrix_power(A, 10) @ x0).tolist()) # -> [29525.0, 29524.0]
print("3**10:", 3 ** 10)                                           # -> 59049

# Iteracion de potencias: multiplicar y normalizar acaba dando la direccion dominante.
v = x0.copy()
for _ in range(20):
    v = A @ v
    v = v / np.linalg.norm(v)
print("direccion tras 20 pasos:", np.round(v, 4).tolist())         # -> [0.7071, 0.7071]
