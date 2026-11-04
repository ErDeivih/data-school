import numpy as np
from scipy import stats

# Lognormal: log(X) es normal, pero la media de X no es exp(mu).
mu, sigma = 0.0, 0.5
print(f"mediana = {np.exp(mu):.4f}")                                           # -> 1.0000
print(f"media   = {np.exp(mu + sigma ** 2 / 2):.4f}")                          # -> 1.1331
print(f"P95     = {stats.lognorm.ppf(0.95, s=sigma, scale=np.exp(mu)):.4f}")   # -> 2.2760

# Otras familias: la beta vive en [0, 1] y la gamma generaliza la exponencial.
print(f"uniforme(0,4) varianza  = {(4 - 0) ** 2 / 12:.4f}")       # -> 1.3333
print(f"beta(2,5) media         = {stats.beta.mean(2, 5):.4f}")   # -> 0.2857
print(f"gamma(3, escala 2) media = {stats.gamma.mean(3, scale=2):.4f}")  # -> 6.0000
