import numpy as np

a = np.array([1, 2, 3])                  # enteros: el dtype por defecto es int64
b = np.array([1.0, 2, 3])                # basta un float para que todo el array sea float64
print(a.dtype, a.shape, a.nbytes)        # -> int64 (3,) 24
print(b.dtype, b.nbytes)                 # -> float64 24
print((a / 2).dtype)                     # -> float64  (la division nunca devuelve enteros)

m = np.arange(12).reshape(3, 4)          # 3 filas x 4 columnas de int64
print(m.shape, m.ndim, m.size, m.nbytes) # -> (3, 4) 2 12 96
print(m.strides)                         # -> (32, 8)  (32 bytes por fila, 8 por columna)
print(m[2, 3])                           # -> 11
