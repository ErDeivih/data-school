import numpy as np
from sklearn.preprocessing import StandardScaler

notas = np.array([4.0, 5.5, 6.0, 6.5, 6.5, 7.0, 7.5, 8.0, 9.5]).reshape(-1, 1)
z = StandardScaler().fit_transform(notas).ravel()

# La media de las z es 0 y su desviacion 1: es el mismo dato en otras unidades
print("media notas", round(float(notas.mean()), 4))        # -> 6.7222
print("sd notas   ", round(float(notas.std()), 4))         # -> 1.4741
print("media z    ", abs(round(float(z.mean()), 12)))      # -> 0.0
print("sd z       ", round(float(z.std()), 4))             # -> 1.0
print("z de 9.5   ", round(float(z[-1]), 4))               # -> 1.8844
