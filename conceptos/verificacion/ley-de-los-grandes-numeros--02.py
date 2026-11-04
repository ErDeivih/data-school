import numpy as np

# Cota de Chebyshev para la media de 100 tiradas de un dado: sigma^2 / (n * eps^2)
sigma2, eps, n = 35 / 12, 0.5, 100
print(f"cota de Chebyshev = {sigma2 / (n * eps ** 2):.4f}")   # -> 0.1167

# Frecuencia real de alejarse 0,5 o mas, con 2000 muestras de tamano 100
rng = np.random.default_rng(1)
medias = rng.integers(1, 7, size=(2000, n)).mean(axis=1)
print(f"frecuencia real   = {(np.abs(medias - 3.5) >= eps).mean():.4f}")  # -> 0.0030

# El error tipico baja como 1/sqrt(n): 10 veces menos error cuesta 100 veces mas datos
print(f"sd de las medias  = {medias.std(ddof=1):.4f}")     # -> 0.1750
print(f"teorico sqrt(s2/n) = {np.sqrt(sigma2 / n):.4f}")   # -> 0.1708
