import numpy as np

rng = np.random.default_rng(0)
# 200.000 muestras de 5 valores de una normal con varianza real 4
muestras = rng.normal(loc=10.0, scale=2.0, size=(200_000, 5))

# Con ddof=0 dividimos entre n y la varianza sale sistematicamente baja:
# la varianza real de la normal es 4, asi que falta un 20 %
print(f"media con n   {muestras.var(axis=1, ddof=0).mean():.1f}")   # -> 3.2
print(f"media con n-1 {muestras.var(axis=1, ddof=1).mean():.1f}")   # -> 4.0
