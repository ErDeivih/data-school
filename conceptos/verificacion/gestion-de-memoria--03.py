import numpy as np

base = np.arange(5, dtype=np.int64)
vista = base[1:4]                        # vista: comparte el mismo bloque de memoria
vista[0] = 99                            # escribir en la vista cambia el array original
print("base tras escribir en la vista:", base.tolist())     # -> [0, 99, 2, 3, 4]

copia = base[1:4].copy()                 # copy() reserva memoria nueva: ya es independiente
copia[0] = -1
print("base tras escribir en la copia:", base.tolist())     # -> [0, 99, 2, 3, 4]

print("la vista comparte el buffer:", vista.base is base)   # -> True
print("bytes afectados:", vista.nbytes, "de", base.nbytes)  # -> 24 de 40
