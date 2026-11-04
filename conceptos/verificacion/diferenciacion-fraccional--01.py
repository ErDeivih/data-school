import numpy as np

def pesos_fracd(d, umbral=1e-3):
    """Pesos w_k de (1-B)^d, truncados cuando el valor absoluto baja del umbral."""
    w, k = [1.0], 1
    while True:
        siguiente = -w[-1] * (d - k + 1) / k
        if abs(siguiente) < umbral:
            break
        w.append(siguiente)
        k += 1
    return np.array(w)

for d in (0.0, 0.4, 1.0):
    w = pesos_fracd(d)
    print(f"d={d:.1f}  pesos {w.size:>3}  primeros {np.round(w[:5], 4).tolist()}")
# d=0.4 -> 55 pesos, los cinco primeros son [1.0, -0.4, -0.12, -0.064, -0.0416]
# d=1.0 -> 2 pesos, [1.0, -1.0]
