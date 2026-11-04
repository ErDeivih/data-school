import numpy as np

mu = np.array([0.08, 0.12])                # rentabilidad esperada anual
sigma = np.array([0.15, 0.25])             # volatilidad anual
rho = 0.30
cov = np.array([[sigma[0] ** 2, rho * sigma[0] * sigma[1]],
                [rho * sigma[0] * sigma[1], sigma[1] ** 2]])

# Peso de varianza minima en el primer activo (formula cerrada de dos activos).
w1 = (sigma[1] ** 2 - rho * sigma[0] * sigma[1]) / (
    sigma[0] ** 2 + sigma[1] ** 2 - 2 * rho * sigma[0] * sigma[1])

def resumen(pesos):
    return float(pesos @ mu), float(np.sqrt(pesos @ cov @ pesos))

mu_min, sigma_min = resumen(np.array([w1, 1 - w1]))
print(f"varianza minima pesos {w1:.3f} y {1 - w1:.3f}  mu {mu_min:.2%}  sigma {sigma_min:.2%}")
# -> varianza minima pesos 0.820 y 0.180  mu 8.72%  sigma 14.31%

# Cartera tangente con tipo sin riesgo del 2 %: maximiza el Sharpe.
rf = 0.02
w_tan = np.linalg.solve(cov, mu - rf)
w_tan = w_tan / w_tan.sum()
mu_tan, sigma_tan = resumen(w_tan)
print(f"tangente pesos {w_tan[0]:.3f} y {w_tan[1]:.3f}  mu {mu_tan:.2%}  sigma {sigma_tan:.2%}")
# -> tangente pesos 0.625 y 0.375  mu 9.50%  sigma 15.12%
print(f"Sharpe tangente {((mu_tan - rf) / sigma_tan):.3f}")     # -> 0.496
print(f"Sharpe de A {((mu[0] - rf) / sigma[0]):.3f} y de B {((mu[1] - rf) / sigma[1]):.3f}")
# -> Sharpe de A 0.400 y de B 0.400
