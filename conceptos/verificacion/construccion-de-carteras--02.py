import numpy as np

# Reparto del riesgo: mitad de capital no es mitad de riesgo.
w = np.array([0.5, 0.5])
sigmas = np.array([0.20, 0.10])
rho = 0.2
cov = np.outer(sigmas, sigmas) * np.array([[1.0, rho], [rho, 1.0]])

sigma_p = float(np.sqrt(w @ cov @ w))
rc = w * (cov @ w) / sigma_p          # contribucion de cada estrategia al riesgo
print(f"sigma cartera {sigma_p:.2%}")                       # -> sigma cartera 12.04%
print(f"reparto del riesgo {rc[0] / sigma_p:.1%} y {rc[1] / sigma_p:.1%}")   # -> 75.9% y 24.1%

# Numero efectivo de apuestas con los autovalores de la correlacion.
for n in (3, 10):
    corr = np.full((n, n), 0.2)
    np.fill_diagonal(corr, 1.0)
    autovalores = np.linalg.eigvalsh(corr)
    print(f"N={n:>2}  apuestas efectivas {autovalores.sum() ** 2 / (autovalores ** 2).sum():.2f}")
# -> N= 3  apuestas efectivas 2.78
# -> N=10  apuestas efectivas 7.35
