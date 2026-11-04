# El mismo trabajo con la misma cuenta de operaciones: solo cambia el orden de los datos
import numpy as np

filas, columnas = 512, 512
m = np.arange(filas * columnas, dtype=np.float64).reshape(filas, columnas)
t = m.T                                   # vista traspuesta: NO copia nada

print("m es C-contigua:", m.flags["C_CONTIGUOUS"], "-> recorre memoria en orden")
# -> m es C-contigua: True -> recorre memoria en orden
print("t es C-contigua:", t.flags["C_CONTIGUOUS"], "-> salta de fila en fila")
# -> t es C-contigua: False -> salta de fila en fila
print("bytes de una fila:", m.strides[0], "bytes de la linea de cache tipica: 64")
# -> bytes de una fila: 4096 bytes de la linea de cache tipica: 64
