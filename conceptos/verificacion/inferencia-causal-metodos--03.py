import numpy as np

rng = np.random.default_rng(1)
n = 4000
u = rng.normal(0, 1, n)                                  # confusor, no observado
z = rng.normal(0, 1, n)                                  # instrumento: sorteo
t = (0.8 * z + u + rng.normal(0, 0.5, n) > 0).astype(float)
y = 2.0 * t + 3.0 * u + rng.normal(0, 0.5, n)            # efecto causal real: 2,0

# Wald: covarianza del instrumento con el resultado partido por la primera etapa.
# No hace falta observar u, solo que z no afecte a y por otra via.
iv = np.cov(z, y)[0, 1] / np.cov(z, t)[0, 1]
print(f"primera etapa   {np.cov(z, t)[0, 1] / z.var():.3f}")   # -> 0.226
print(f"estimacion IV   {iv:.2f}")                            # -> 1.87
