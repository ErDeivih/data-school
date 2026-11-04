import numpy as np

# En un ndarray los elementos van seguidos: la direccion del elemento i es base + i*8.
a = np.arange(1_000_000, dtype=np.int64)
print("bytes del array:", a.nbytes)                    # -> bytes del array: 8000000
print("bytes por elemento:", a.itemsize)               # -> bytes por elemento: 8
print("desplazamiento del elemento 500000:", hex(500000 * a.itemsize))  # -> desplazamiento del elemento 500000: 0x3d0900

# Un trozo con paso 2 NO es contiguo, pero comparte memoria con el original: es una vista.
vista = a[::2]
print("stride de la vista:", vista.strides[0])         # -> stride de la vista: 16
print("comparte memoria:", np.shares_memory(a, vista)) # -> comparte memoria: True
print("elementos de la vista:", vista.size)            # -> elementos de la vista: 500000

# Lo mismo con una matriz: la traspuesta tampoco copia, solo cambia los strides.
m = np.arange(12).reshape(3, 4)
print("strides de la matriz:", m.strides)              # -> strides de la matriz: (32, 8)
print("strides de la traspuesta:", m.T.strides)        # -> strides de la traspuesta: (8, 32)
