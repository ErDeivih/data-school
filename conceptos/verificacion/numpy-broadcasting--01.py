import numpy as np

filas = np.arange(3).reshape(3, 1)   # forma (3, 1): una columna
cols = np.arange(1, 5)               # forma (4,): una fila
print(filas.shape, cols.shape, (filas * cols).shape)   # -> (3, 1) (4,) (3, 4)

# Al estirar las dos dimensiones de tamano 1 sale la tabla de multiplicar, sin bucles
print((filas * cols).tolist())   # -> [[0, 0, 0, 0], [1, 2, 3, 4], [2, 4, 6, 8]]
