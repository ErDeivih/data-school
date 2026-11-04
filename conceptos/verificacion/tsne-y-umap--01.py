import numpy as np

# Cuanta atencion recibe una distancia segun el ancho de banda local (sigma).
for sigma in (1.0, 5.0):
    p1 = np.exp(-(1.0 ** 2) / (2 * sigma ** 2))    # similitud sin normalizar
    p2 = np.exp(-(2.0 ** 2) / (2 * sigma ** 2))
    print(f"sigma={sigma}  d=1 {p1:.4f}  d=2 {p2:.4f}  cociente {p1 / p2:.2f}")
# -> sigma=1.0  d=1 0.6065  d=2 0.1353  cociente 4.48
# -> sigma=5.0  d=1 0.9802  d=2 0.9231  cociente 1.06

# Perplejidad: el numero efectivo de vecinos de una distribucion de similitudes.
p = np.array([0.8, 0.1, 0.1])
H = -(p * np.log(p)).sum()                         # ojo: log neperiano, no log2
print("entropia:", round(H, 4), "perplejidad:", round(2 ** H, 2))
# -> entropia: 0.639 perplejidad: 1.56
