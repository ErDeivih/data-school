import numpy as np

A = np.array([[1, 2, 3], [4, 5, 6]])      # forma (2, 3)
B = np.array([[1, 0], [0, 1], [2, 2]])    # forma (3, 2)

print("A @ B  :", (A @ B).tolist())        # -> [[7, 8], [16, 17]]
print("(A@B).T:", (A @ B).T.tolist())      # -> [[7, 16], [8, 17]]
print("B.T@A.T:", (B.T @ A.T).tolist())    # -> [[7, 16], [8, 17]]

# Producto matriz-vector: cada componente es un producto punto con una fila.
v = np.array([1, 1, 1])
print("A @ v  :", (A @ v).tolist())        # -> [6, 15]

# Si las dimensiones interiores no coinciden, el producto no existe.
try:
    A @ A
except ValueError:
    print("A @ A: dimensiones interiores incompatibles")   # -> A @ A: dimensiones interiores incompatibles
