import numpy as np
from statistics import NormalDist

Z = NormalDist()
EULER = 0.5772156649

def dsr(sr, T, intentos, var_sr, sesgo, curtosis):
    if intentos > 1:
        sr0 = np.sqrt(var_sr) * ((1 - EULER) * Z.inv_cdf(1 - 1 / intentos)
                                 + EULER * Z.inv_cdf(1 - 1 / (intentos * np.e)))
    else:
        sr0 = 0.0
    den = np.sqrt(1 - sesgo * sr + (curtosis - 1) / 4 * sr ** 2)
    return Z.cdf((sr - sr0) * np.sqrt(T - 1) / den), sr0

# El mismo backtest, el mismo Sharpe, distinto numero de intentos.
print("intentos  Sharpe del ruido  DSR")
for intentos in (1, 10, 100, 1000, 10000):
    valor, sr0 = dsr(0.15, 1200, intentos, 0.05 ** 2, -0.5, 6.0)
    print(f"{intentos:>8}  {sr0:>16.4f}  {valor:.4f}")
# con 1 intento el DSR es 1.0000; con 10000 baja a 0.0780
