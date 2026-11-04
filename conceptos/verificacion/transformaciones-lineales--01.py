import numpy as np

p = np.array([3.0, 1.0])
R = np.array([[0.0, -1.0], [1.0, 0.0]])   # rotar 90 grados en sentido antihorario
S = np.array([[2.0, 0.0], [0.0, 3.0]])    # estirar cada eje de forma distinta

print("R @ p      :", (R @ p).tolist())          # -> [-1.0, 3.0]
print("S @ (R @ p):", (S @ (R @ p)).tolist())    # -> [-2.0, 9.0]
print("R @ (S @ p):", (R @ (S @ p)).tolist())    # -> [-3.0, 6.0]
print("mismo punto:", bool(np.array_equal(S @ (R @ p), R @ (S @ p))))   # -> False
print("norma antes y despues de rotar:", round(float(np.linalg.norm(p)), 4),
      round(float(np.linalg.norm(R @ p)), 4))    # -> 3.1623 3.1623
