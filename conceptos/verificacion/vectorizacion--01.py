import numpy as np

precios = np.array([100.0, 102.0, 98.0, 105.0, 103.0])
retornos = np.diff(precios) / precios[:-1]     # el bucle real ocurre en C

print(np.round(retornos, 4).tolist())          # -> [0.02, -0.0392, 0.0714, -0.019]
print(int((retornos > 0).sum()), "subidas de", retornos.size)   # -> 2 subidas de 4
print(np.round(retornos[retornos > 0].mean(), 4))               # -> 0.0457

senal = np.where(retornos > 0, 1, -1)          # sin if dentro de un bucle
print(senal.tolist())                          # -> [1, -1, 1, -1]
