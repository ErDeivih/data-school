import numpy as np

p = np.array([3.0, 4.0])
print("L1   :", float(np.linalg.norm(p, 1)))       # -> 7.0
print("L2   :", float(np.linalg.norm(p, 2)))       # -> 5.0
print("Linf :", float(np.linalg.norm(p, np.inf)))  # -> 4.0

# Girar los ejes 45 grados conserva L2 (es invariante a rotaciones) pero no L1.
t = np.deg2rad(45)
R = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
q = R @ p
print("p rotado:", np.round(q, 4).tolist())                  # -> [-0.7071, 4.9497]
print("L1 rotado:", round(float(np.linalg.norm(q, 1)), 4))   # -> 5.6569
print("L2 rotado:", round(float(np.linalg.norm(q, 2)), 4))   # -> 5.0
