import numpy as np

# Datos casi sobre una recta: la direccion principal explica casi toda la varianza.
X = np.array([[1.0, 2.1], [2.0, 3.9], [3.0, 6.2], [4.0, 7.8], [5.0, 10.1]])
C = np.cov(X, rowvar=False)
w, V = np.linalg.eigh(C)

print("covarianza:", np.round(C, 4).tolist())              # -> [[2.5, 4.975], [4.975, 9.927]]
print("autovalores:", np.round(w, 4).tolist())             # -> [0.0054, 12.4216]
print("suma de autovalores:", round(float(w.sum()), 4))    # -> 12.427
print("varianza total (traza):", round(float(np.trace(C)), 4))   # -> 12.427
print("varianza del primero:", round(float(w[-1] / w.sum()), 4))   # -> 0.9996
