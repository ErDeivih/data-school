import numpy as np

x = np.array([1.0, 2.0, 2.0])
y = np.array([2.0, 1.0, 0.0])
y10 = 10 * y            # el mismo usuario puntuando en otra escala

cos = float(x @ y / (np.linalg.norm(x) * np.linalg.norm(y)))
cos10 = float(x @ y10 / (np.linalg.norm(x) * np.linalg.norm(y10)))

print("producto con y y con 10y:", float(x @ y), float(x @ y10))   # -> 4.0 40.0
print("coseno con y y con 10y:", round(cos, 4), round(cos10, 4))   # -> 0.5963 0.5963

# Producto punto cero: direcciones perpendiculares.
z = np.array([2.0, -1.0, 0.0])
print("x . z:", float(x @ z))                                      # -> 0.0
