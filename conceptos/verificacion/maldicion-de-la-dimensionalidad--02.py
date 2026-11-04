import numpy as np

# 200 puntos uniformes en un cubo de lado 1, para varias dimensiones
rng = np.random.default_rng(0)
for d in (2, 10, 100, 1000):
    P = rng.random((200, d))
    dist = np.sqrt(((P[:, None, :] - P[None, :, :]) ** 2).sum(axis=2))
    np.fill_diagonal(dist, np.nan)                  # fuera la distancia de cada punto a si mismo
    minima, maxima = np.nanmin(dist, axis=1), np.nanmax(dist, axis=1)
    print("d=%4d  cercano %.3f  lejano %.3f  cociente min/max %.4f"
          % (d, minima.mean(), maxima.mean(), (minima / maxima).mean()))
# -> d=   2  cercano 0.035  lejano 1.023  cociente min/max 0.0351
# -> d=  10  cercano 0.633  lejano 1.841  cociente min/max 0.3442
# -> d= 100  cercano 3.437  lejano 4.647  cociente min/max 0.7397
# -> d=1000  cercano 12.260  lejano 13.506  cociente min/max 0.9078
