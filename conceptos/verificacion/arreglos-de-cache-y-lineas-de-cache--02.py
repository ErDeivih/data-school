# Cuantos bytes de memoria hay que traer por cada elemento, segun el salto
import numpy as np

LINEA = 64                        # bytes por linea de cache en x86-64

for salto in (1, 16, 64, 4096):
    # Un recorrido con paso fijo no repite linea: el numero de lineas distintas que se tocan
    # es como mucho el total del buffer, y el coste util de cada una depende de cuantos de sus
    # elementos se llegan a usar.
    elementos_por_linea = max(1, LINEA // salto)
    print(f"salto {salto:>5} B: {elementos_por_linea:>3} elementos por linea, "
          f"{LINEA / elementos_por_linea:>7.1f} bytes traidos por elemento")
# -> salto     1 B:  64 elementos por linea,     1.0 bytes traidos por elemento
# -> salto    16 B:   4 elementos por linea,    16.0 bytes traidos por elemento
# -> salto    64 B:   1 elementos por linea,    64.0 bytes traidos por elemento
# -> salto  4096 B:   1 elementos por linea,    64.0 bytes traidos por elemento
