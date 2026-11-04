import numpy as np

x = np.array([1.0, 2.0, 2.0])
y = np.array([2.0, 1.0, 0.0])

producto = float(x @ y)
cos = producto / (np.linalg.norm(x) * np.linalg.norm(y))

print("producto punto:", producto)                        # -> 4.0
print("normas:", np.round([np.linalg.norm(x), np.linalg.norm(y)], 4).tolist())   # -> [3.0, 2.2361]
print("coseno:", round(cos, 4))                           # -> 0.5963
print("angulo en grados:", round(float(np.degrees(np.arccos(cos))), 1))          # -> 53.4

# Proyeccion de y sobre x: la parte de y que va en la direccion de x.
proyeccion = (producto / float(x @ x)) * x
print("proyeccion:", np.round(proyeccion, 4).tolist())    # -> [0.4444, 0.8889, 0.8889]
