import numpy as np

X = np.array([[1.0, 2.0, 3.0],
              [4.0, 6.0, 8.0],
              [7.0, 10.0, 13.0]])   # 3 muestras (filas) x 3 variables (columnas)

por_columna = X.mean(axis=0)        # forma (3,): se alinea con las columnas
print(por_columna.tolist())         # -> [4.0, 6.0, 8.0]
print((X - por_columna).tolist())   # -> [[-3.0, -4.0, -5.0], [0.0, 0.0, 0.0], [3.0, 4.0, 5.0]]

# keepdims conserva el eje de tamano 1: la misma linea vale para 2 o para 5 dimensiones
print(X.mean(axis=0, keepdims=True).shape)   # -> (1, 3)
print(X.mean(axis=1, keepdims=True).shape)   # -> (3, 1)
