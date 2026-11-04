import numpy as np

# Filtro grueso de universo: liquidez, no precio.
simbolos = np.array(["AAA", "BBB", "CCC", "DDD", "EEE"])
precio = np.array([12.5, 340.0, 8.2, 95.0, 45.0])
volumen = np.array([4_000_000, 120_000, 25_000_000, 900_000, 3_100_000], dtype=float)

dolares = precio * volumen
umbral = 60_000_000
pasa = dolares > umbral
orden = np.argsort(-dolares)

for s, d, ok in zip(simbolos, dolares, pasa):
    print(f"  {s}  {d / 1e6:>6.1f} millones  {'pasa' if ok else 'fuera'}")
# ->   AAA    50.0 millones  fuera
# ->   BBB    40.8 millones  fuera
# ->   CCC   205.0 millones  pasa
# ->   DDD    85.5 millones  pasa
# ->   EEE   139.5 millones  pasa

print("elegidos para el universo:", simbolos[orden[:2]].tolist())
# -> elegidos para el universo: ['CCC', 'EEE']
