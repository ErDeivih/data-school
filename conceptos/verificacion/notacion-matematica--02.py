import numpy as np

# X ~ N(10, 4) usa la VARIANZA como segundo parámetro; np.random.normal pide la
# desviación típica (scale). Es el error de lectura más caro de esta página.
rng = np.random.default_rng(0)
media, varianza = 10.0, 4.0

muestra = rng.normal(loc=media, scale=np.sqrt(varianza), size=1_000_000)
print(f"E[X] = {media:.1f}   media muestral = {muestra.mean():.3f}")        # -> 10.0 y 10.002
print(f"sigma = {np.sqrt(varianza):.1f}   s = {muestra.std(ddof=1):.3f}")   # -> 2.0 y 2.001
