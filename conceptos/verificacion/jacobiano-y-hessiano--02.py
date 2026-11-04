import numpy as np

# Punto de silla: el hessiano indefinido lo delata aunque el gradiente sea cero.
g = lambda x, y: x**2 - y**2          # silla clásica en el origen
H_silla = np.array([[2.0, 0.0], [0.0, -2.0]])

print("gradiente en (0,0):", [0.0, 0.0])                       # salida: [0.0, 0.0]
print("autovalores silla :", np.linalg.eigvalsh(H_silla))      # salida: [-2.  2.]
print("signos distintos  :", bool(np.any(np.linalg.eigvalsh(H_silla) > 0) and np.any(np.linalg.eigvalsh(H_silla) < 0)))  # salida: True

# La misma silla vista en los valores de la función alrededor del origen
print("punto", (0.1, 0.0), "-> f =", round(g(0.1, 0.0), 4))   # salida: punto (0.1, 0.0) -> f = 0.01
print("punto", (0.0, 0.1), "-> f =", round(g(0.0, 0.1), 4))   # salida: punto (0.0, 0.1) -> f = -0.01
