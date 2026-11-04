import numpy as np

# Censura por la derecha: el sensor corta en 10 y la media observada baja.
rng = np.random.default_rng(4)
real = rng.lognormal(mean=1.0, sigma=0.8, size=50_000)
registrado = np.minimum(real, 10.0)

print("media real:      ", round(float(real.mean()), 3))        # -> 3.741
print("media registrada:", round(float(registrado.mean()), 3))  # -> 3.506
print("proporcion censurada:", round(float((real > 10).mean()), 4))  # -> 0.0515
print("media de los censurados:", round(float(real[real > 10].mean()), 3))  # -> 14.553
