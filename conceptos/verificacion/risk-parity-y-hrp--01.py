import numpy as np
from scipy.optimize import minimize

# Tres activos con volatilidad anual del 10 %, 20 % y 30 %.
vol = np.array([0.10, 0.20, 0.30])
corr = np.array([[1.0, 0.2, 0.1],
                 [0.2, 1.0, 0.6],
                 [0.1, 0.6, 1.0]])
cov = np.outer(vol, vol) * corr          # Sigma = D * C * D

def contribuciones(w):
    sigma = np.sqrt(w @ cov @ w)         # volatilidad de la cartera
    return w * (cov @ w) / sigma         # RC_i = w_i * (Sigma w)_i / sigma

def dispersion(w):
    rc = contribuciones(w)               # ERC = contribuciones iguales
    return float(((rc - rc.mean()) ** 2).sum() * 1e6)   # escala para el optimizador

inicio = np.array([1 / 3, 1 / 3, 1 / 3])
erc = minimize(dispersion, inicio, method="SLSQP", bounds=[(0, 1)] * 3,
               constraints=[{"type": "eq", "fun": lambda w: w.sum() - 1}]).x
inversa = (1 / vol) / (1 / vol).sum()

print("pesos ERC:", np.round(erc, 4).tolist())              # -> pesos ERC: [0.5901, 0.2406, 0.1694]
print("aportes ERC:", np.round(contribuciones(erc) / contribuciones(erc).sum(), 4).tolist())  # -> aportes ERC: [0.3333, 0.3333, 0.3333]
print("volatilidad ERC:", round(float(np.sqrt(erc @ cov @ erc)), 4))   # -> volatilidad ERC: 0.1142
print("pesos inversa de volatilidad:", np.round(inversa, 4).tolist())  # -> pesos inversa de volatilidad: [0.5455, 0.2727, 0.1818]
print("aportes inversa de volatilidad:", np.round(contribuciones(inversa) / contribuciones(inversa).sum(), 4).tolist())  # -> aportes inversa de volatilidad: [0.2708, 0.375, 0.3542]
print("aportes a partes iguales:", np.round(contribuciones(inicio) / contribuciones(inicio).sum(), 4).tolist())  # -> aportes a partes iguales: [0.0752, 0.354, 0.5708]
