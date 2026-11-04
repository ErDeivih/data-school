import numpy as np

grupos = np.array([0, 0, 1, 1, 1, 2])          # cliente codificado como entero 0..2
importes = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0])

# Suma por grupo en una sola pasada: el equivalente vectorizado de un bucle con diccionario
print(np.bincount(grupos, weights=importes).tolist())   # -> [3.0, 12.0, 6.0]
print(np.bincount(grupos).tolist())                     # -> [2, 3, 1]
