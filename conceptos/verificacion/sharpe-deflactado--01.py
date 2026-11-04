import numpy as np
from statistics import NormalDist

Z = NormalDist()
EULER = 0.5772156649

def sharpe_deflactado(sr, T, intentos, var_sr, sesgo, curtosis):
    """Devuelve (DSR, Sharpe esperado del mejor intento bajo la hipotesis nula)."""
    if intentos > 1:
        sr0 = np.sqrt(var_sr) * ((1 - EULER) * Z.inv_cdf(1 - 1 / intentos)
                                 + EULER * Z.inv_cdf(1 - 1 / (intentos * np.e)))
    else:
        sr0 = 0.0
    denominador = np.sqrt(1 - sesgo * sr + (curtosis - 1) / 4 * sr ** 2)
    return Z.cdf((sr - sr0) * np.sqrt(T - 1) / denominador), sr0

# Todo por periodo: Sharpe diario 0,15 y desviacion tipica de los intentos 0,05.
dsr, sr0 = sharpe_deflactado(sr=0.15, T=1200, intentos=100, var_sr=0.05 ** 2,
                             sesgo=-0.5, curtosis=6.0)
print(f"Sharpe esperado del mejor de 100 intentos: {sr0:.4f}")   # -> 0.1265
print(f"DSR: {dsr:.4f}")                                       # -> 0.7805
