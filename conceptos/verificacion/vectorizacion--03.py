import numpy as np

x = np.array([-5.0, -0.5, 0.5, 5.0])

# Varias condiciones en orden: la primera que se cumple manda
etiquetas = np.select([x < -1, x < 1], ["bajada fuerte", "plana"], default="subida fuerte")
print(etiquetas.tolist())   # -> ['bajada fuerte', 'plana', 'plana', 'subida fuerte']

# Recortar valores extremos sin bucles
print(np.clip(x, -1.0, 1.0).tolist())   # -> [-1.0, -0.5, 0.5, 1.0]
