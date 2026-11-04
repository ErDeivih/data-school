# El coste de atencion crece con el CUADRADO de la secuencia total. Los vectores de imagen
# no solo ocupan contexto: multiplican el trabajo de cada capa.
import numpy as np

N_TEXTO = 600
lados = np.array([224, 336, 448, 672, 1008])
parches = np.ceil(lados / 16) ** 2          # una imagen por consulta

for lado, n_vis in zip(lados, parches):
    total = N_TEXTO + int(n_vis)
    print(f"lado {lado:4d} -> {int(n_vis):5d} vectores de imagen, "
          f"secuencia {total:5d}, atencion relativa {total ** 2 / N_TEXTO ** 2:8.1f}x")
# -> lado  224 ->   196 vectores de imagen, secuencia   796, atencion relativa      1.8x
# -> lado  336 ->   441 vectores de imagen, secuencia  1041, atencion relativa      3.0x
# -> lado  448 ->   784 vectores de imagen, secuencia  1384, atencion relativa      5.3x
# -> lado  672 ->  1764 vectores de imagen, secuencia  2364, atencion relativa     15.5x
# -> lado 1008 ->  3969 vectores de imagen, secuencia  4569, atencion relativa     58.0x

# La memoria de la atencion va con la longitud, no con su cuadrado: hay que vigilar las dos.
for lado, n_vis in zip(lados, parches):
    total = N_TEXTO + int(n_vis)
    print(f"secuencia {total:5d} -> memoria de atencion relativa al texto solo: "
          f"{total / N_TEXTO:5.1f}x")
# -> secuencia   796 -> memoria de atencion relativa al texto solo:   1.3x
# -> secuencia  1041 -> memoria de atencion relativa al texto solo:   1.7x
# -> secuencia  1384 -> memoria de atencion relativa al texto solo:   2.3x
# -> secuencia  2364 -> memoria de atencion relativa al texto solo:   3.9x
# -> secuencia  4569 -> memoria de atencion relativa al texto solo:   7.6x
