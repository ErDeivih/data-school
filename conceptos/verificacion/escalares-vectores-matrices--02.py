import numpy as np

datos = np.array([[34, 171, 68], [51, 165, 71], [28, 180, 84], [45, 158, 57]])

# axis=0 recorre las filas y resume cada columna (cada variable).
# Si te equivocas y usas axis=1, resumes personas: numeros sin sentido.
print("media por columna:", np.round(datos.mean(axis=0), 1))   # -> [ 39.5 168.5  70. ]
print("suma por fila:    ", datos.sum(axis=1))                 # -> [273 287 292 260]

# La traspuesta cambia el significado: ahora cada fila es una variable.
print("forma traspuesta:", datos.T.shape)                      # -> (3, 4)
print("fila 1 de la traspuesta:", datos.T[0])                  # -> [34 51 28 45]

# Un vector 1D de numpy no distingue fila de columna: su forma es (3,)
v = np.array([1, 2, 3])
print("forma de un vector 1D:", v.shape)                       # -> (3,)
print("como columna:", v.reshape(-1, 1).shape)                 # -> (3, 1)
