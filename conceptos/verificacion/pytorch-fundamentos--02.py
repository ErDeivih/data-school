import numpy as np

# Lo que hace el DataLoader: barajar una vez por epoca y cortar en lotes.
datos = np.arange(10.0)                     # 10 muestras
rng = np.random.default_rng(0)
for epoca in range(2):
    orden = rng.permutation(datos.size)     # barajado distinto en cada epoca
    for inicio in range(0, datos.size, 4):
        idx = orden[inicio:inicio + 4]      # el ultimo lote es mas pequeno
        # inicio // 4 numera el lote: division entera, no la posicion de la muestra
        print(f"epoca {epoca}  lote {inicio // 4}  indices {idx}")
# -> epoca 0  lote 0  indices [4 6 2 7]
# -> epoca 0  lote 1  indices [3 5 9 0]
# -> epoca 0  lote 2  indices [8 1]
# -> epoca 1  lote 0  indices [2 9 3 6]
# -> epoca 1  lote 1  indices [0 4 8 7]
# -> epoca 1  lote 2  indices [5 1]
