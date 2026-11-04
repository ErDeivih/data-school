import numpy as np

# Talento y suerte son independientes; el exito ocurre si se da al menos uno.
# El exito es un colisionador (T -> E <- L) y condicionar en el crea la asociacion.
rng = np.random.default_rng(0)
talento = rng.integers(0, 2, 100_000)
suerte = rng.integers(0, 2, 100_000)
exito = (talento + suerte) >= 1

print(f"poblacion completa {np.corrcoef(talento, suerte)[0, 1]:+.3f}")
# -> poblacion completa -0.001
print(f"solo los exitosos  {np.corrcoef(talento[exito], suerte[exito])[0, 1]:+.3f}")
# -> solo los exitosos  -0.501
