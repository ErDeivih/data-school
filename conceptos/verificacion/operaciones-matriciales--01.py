import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[0, 1], [1, 0]])

print("A @ B :", (A @ B).tolist())   # -> [[2, 1], [4, 3]]
print("B @ A :", (B @ A).tolist())   # -> [[3, 4], [1, 2]]
print("A * B :", (A * B).tolist())   # -> [[0, 2], [3, 0]]

# La identidad no cambia nada: es el "1" del producto matricial.
print("A @ I = A:", bool(np.array_equal(A @ np.eye(2), A)))   # -> True
