import zlib
import numpy as np

# Comprimir ayuda cuando hay estructura; con alta entropia solo anade cabecera.
repetitivo = ("fila," * 200).encode()
alta_entropia = np.random.default_rng(0).integers(0, 256, 2048, dtype=np.uint8).tobytes()

for nombre, datos in [("repetitivo", repetitivo), ("alta entropia", alta_entropia)]:
    comprimido = zlib.compress(datos, level=6)
    print("{:<14} {:>6} -> {:>6} bytes  ({:.0%})".format(
        nombre, len(datos), len(comprimido), len(comprimido) / len(datos)))
# repetitivo:    1000 bytes de entrada,   21 comprimidos (2 %)
# alta entropia: 2048 bytes de entrada, 2059 comprimidos (101 %)
