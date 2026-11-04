import numpy as np

# Ceros inflados: dos procesos mezclados, no una sola distribucion con muchos ceros.
rng = np.random.default_rng(2)
visitas = np.where(rng.random(10_000) < 0.62, 0, rng.poisson(3.5, size=10_000))

print("media global:", round(float(visitas.mean()), 3))                    # -> 1.352
print("media de los que visitan:", round(float(visitas[visitas > 0].mean()), 3))  # -> 3.621
print("proporcion de ceros:", round(float((visitas == 0).mean()), 3))      # -> 0.627
print("varianza:", round(float(visitas.var()), 3))                         # -> 4.311
