import numpy as np

A = np.array([[1.0, 2.0], [2.0, 4.0]])   # la 2.a columna es el doble de la 1.a

print("det(A):", round(float(np.linalg.det(A)), 6))   # -> 0.0
print("rango(A):", np.linalg.matrix_rank(A))          # -> 1

try:
    np.linalg.inv(A)
except np.linalg.LinAlgError:
    print("inv(A): singular, no existe")              # -> inv(A): singular, no existe

# Un determinante diminuto no es cero: invertible, pero numericamente inestable.
C = np.array([[1.0, 2.0], [2.0, 4.0001]])
print("det(C):", round(float(np.linalg.det(C)), 6))   # -> 0.0001
print("cond(C):", f"{np.linalg.cond(C):.3e}")         # -> 2.500e+05
