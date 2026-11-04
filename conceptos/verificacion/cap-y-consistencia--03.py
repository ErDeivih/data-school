import numpy as np

rng = np.random.default_rng(0)
# Latencia de un nodo: lognormal con mediana 10 ms, una distribucion con cola como la real.
# size=(filas, columnas): cada FILA es una peticion y cada columna uno de los 5 nodos.
muestras = rng.lognormal(mean=np.log(10.0), sigma=0.6, size=(200_000, 5))
# sort con axis=1 ordena DENTRO de cada fila: asi la columna 0 es el nodo mas rapido de cada
# peticion y la 4 el mas lento. Sin axis, NumPy aplanaria la matriz y ordenaria todo junto.
ordenadas = np.sort(muestras, axis=1)

un_nodo = muestras[:, 0]         # leer de una sola replica, elegida al azar
mas_rapido = ordenadas[:, 0]     # W=1: termina cuando contesta el primero
tres_de_cinco = ordenadas[:, 2]  # cuorum: hay que esperar al tercero de cinco
los_cinco = ordenadas[:, 4]      # W=N: hay que esperar al mas lento

for nombre, serie in (("una replica al azar", un_nodo),
                      ("el mas rapido W=1 ", mas_rapido),
                      ("3 de 5 (cuorum)  ", tres_de_cinco),
                      ("los 5 (W=N)      ", los_cinco)):
    # np.median y np.percentile devuelven un escalar; el formato de la f-string lo redondea.
    print(f"{nombre}  mediana {np.median(serie):5.1f} ms   "
          f"p99 {np.percentile(serie, 99):6.1f} ms")
