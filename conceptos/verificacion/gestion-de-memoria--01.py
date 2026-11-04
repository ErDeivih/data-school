import sys

import numpy as np
import pandas as pd

n = 200_000
lista = list(range(n))                    # cada entero es un objeto con su cabecera
array = np.arange(n, dtype=np.int64)      # memoria continua: 8 bytes por numero
serie = pd.Series(array)                  # pandas COPIA el array: la Serie ocupa otros 1,5 MiB

# getsizeof(lista) solo cuenta los punteros; hay que sumar cada entero por separado.
bytes_lista = sys.getsizeof(lista) + sum(map(sys.getsizeof, lista))

print(f"lista de enteros   {bytes_lista / 1024 / 1024:5.1f} MiB")   # ->   6.9 MiB
print(f"array de numpy     {array.nbytes / 1024 / 1024:5.1f} MiB")  # ->   1.5 MiB
# deep=True cuenta el contenido de las columnas de objetos; con el dtype de texto nuevo
# (pandas 3) las dos formas dan lo mismo porque los textos ya se guardan en un buffer.
print(f"serie de pandas    {serie.memory_usage(deep=True) / 1024 / 1024:5.1f} MiB")  # ->   1.5 MiB
print(f"factor lista/array {bytes_lista / array.nbytes:.1f} x")     # -> 4.5 x
