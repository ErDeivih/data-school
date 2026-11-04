import numpy as np

m = np.arange(12).reshape(3, 4)

# El axis que se pasa es el que se pliega (el que desaparece del resultado)
print(m.sum(axis=0).tolist())   # -> [12, 15, 18, 21]  (una suma por columna)
print(m.sum(axis=1).tolist())   # -> [6, 22, 38]       (una suma por fila)
print(m.sum().tolist())         # -> 66               (sin axis se suman los 12 elementos)
