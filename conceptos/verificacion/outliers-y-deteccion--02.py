import numpy as np

# Enmascaramiento: al crecer el extremo, la desviacion tipica crece con el y el
# z-score se queda clavado, mientras el z modificado (robusto) se dispara.
for extremo in (45.0, 200.0, 1000.0):
    v = np.array([8, 9, 10, 10, 11, 12, 12, 13, 14, 15, 16, extremo])
    mediana = np.median(v)
    mad = np.median(np.abs(v - mediana))
    z = (extremo - v.mean()) / v.std(ddof=1)
    z_mod = 0.6745 * (extremo - mediana) / mad
    print(f"extremo {extremo:>6.0f}  sd {v.std(ddof=1):>7.2f}  z {z:.2f}  z_mod {z_mod:>7.2f}")
