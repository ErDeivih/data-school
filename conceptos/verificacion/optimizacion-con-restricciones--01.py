import numpy as np

# Cartera de máximo Sharpe con restricción presupuestaria w1 + w2 = 1.
# Caso analítico: w* proporcional a Sigma^-1 mu, normalizado a suma 1.
mu = np.array([0.10, 0.20])
Sigma = np.array([[0.15**2, 0.0], [0.0, 0.25**2]])

z = np.linalg.solve(Sigma, mu)              # Sigma^-1 mu
w = z / z.sum()                             # normalizamos para que los pesos sumen 1

retorno = float(w @ mu)
riesgo = float(np.sqrt(w @ Sigma @ w))
print("pesos            ", np.round(w, 4).tolist())    # salida: [0.5814, 0.4186]
print("retorno cartera  ", round(retorno, 4))          # salida: 0.1419
print("volatilidad      ", round(riesgo, 4))           # salida: 0.1362
print("Sharpe           ", round(retorno / riesgo, 4)) # salida: 1.0414
