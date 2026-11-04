import numpy as np

mu = np.array([0.10, 0.10])        # rentabilidad esperada anual de cada estrategia
sigma = np.array([0.20, 0.20])     # volatilidad anual de cada una
w = np.array([0.5, 0.5])           # mitad de capital en cada una

for rho in (0.0, 0.2, 0.6, 1.0):
    cov = np.array([[sigma[0] ** 2, rho * sigma[0] * sigma[1]],
                    [rho * sigma[0] * sigma[1], sigma[1] ** 2]])
    sigma_p = float(np.sqrt(w @ cov @ w))
    print(f"rho {rho:.1f}  sigma {sigma_p:.2%}  Sharpe {float(w @ mu) / sigma_p:.3f}")
# -> rho 0.2  sigma 15.49%  Sharpe 0.645
# -> rho 0.0  sigma 14.14%  Sharpe 0.707

# Tres estrategias iguales con la misma correlacion media: menos de tres apuestas.
n, rho = 3, 0.2
sigma_p3 = 0.20 * np.sqrt(1 / n + rho * (n - 1) / n)
print(f"tres estrategias sigma {sigma_p3:.2%}  Sharpe {0.10 / sigma_p3:.3f}")
# -> tres estrategias sigma 13.66%  Sharpe 0.732
