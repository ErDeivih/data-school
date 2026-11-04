import hashlib
import numpy as np

# Count-min sketch: 4 filas x 64 columnas. Solo puede sobreestimar.
d, w = 4, 64
rng = np.random.default_rng(7)
mult = rng.integers(1, 10**6, size=d).tolist()   # listas de int de Python: sin desbordar
suma = rng.integers(0, 10**6, size=d).tolist()
tabla = np.zeros((d, w), dtype=int)


def _hash(clave):
    return int.from_bytes(hashlib.blake2b(clave.encode(), digest_size=8).digest(), "big")


def anadir(clave, veces=1):
    h = _hash(clave)
    for fila in range(d):
        tabla[fila, (mult[fila] * h + suma[fila]) % w] += veces


def estimar(clave):
    h = _hash(clave)
    return min(tabla[fila, (mult[fila] * h + suma[fila]) % w] for fila in range(d))


for clave, veces in [("a", 50), ("b", 300), ("c", 7)]:
    anadir(clave, veces)
for i in range(1000):
    anadir("ruido-{}".format(i))          # otras claves del flujo, colisionan

print("real b=300  estimado b={}".format(estimar("b")))   # -> 323
print("real c=7    estimado c={}".format(estimar("c")))   # -> 19
print("real a=50   estimado a={}".format(estimar("a")))   # -> 64
print("contadores usados: {}".format(d * w))              # -> 256
