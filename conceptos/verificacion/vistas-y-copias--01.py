import numpy as np

a = np.arange(10)
vista = a[3:6]          # rebanada basica: comparte el buffer de a
copia = a[[3, 4, 5]]    # indexado avanzado: memoria nueva

vista[0] = 99           # escribe dentro del buffer de a
copia[1] = -1           # escribe en memoria propia, a no se entera

print(a.tolist())                    # -> [0, 1, 2, 99, 4, 5, 6, 7, 8, 9]
print(vista.tolist())                # -> [99, 4, 5]
print(copia.tolist())                # -> [3, -1, 5]
print(vista.base is a, copia.base is None)        # -> True True
print(np.shares_memory(a, vista), np.shares_memory(a, copia))   # -> True False
