import numpy as np
from scipy.optimize import minimize

# El mismo problema resuelto con un optimizador numérico: comprobación cruzada.
def sharpe_negativo(w):
    mu = np.array([0.10, 0.20])
    Sigma = np.array([[0.15**2, 0.0], [0.0, 0.25**2]])
    return -float(w @ mu) / float(np.sqrt(w @ Sigma @ w))

restricciones = [{"type": "eq", "fun": lambda w: w.sum() - 1.0}]
limites = [(0.0, 1.0), (0.0, 1.0)]
resultado = minimize(sharpe_negativo, x0=np.array([0.5, 0.5]),
                     constraints=restricciones, bounds=limites, method="SLSQP")

print("convergio        ", bool(resultado.success))       # salida: True
print("pesos SLSQP      ", np.round(resultado.x, 4).tolist())  # salida: [0.5814, 0.4186]
print("Sharpe SLSQP     ", round(-float(resultado.fun), 4))    # salida: 1.0414
