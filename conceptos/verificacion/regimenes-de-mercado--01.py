import numpy as np

# Filas: estado en t. Columnas: estado en t+1. Estado 0 = calma, 1 = tension.
P = np.array([[0.95, 0.05],
              [0.10, 0.90]])

vals, vecs = np.linalg.eig(P.T)
est = np.real(vecs[:, np.argmin(np.abs(vals - 1))])
est = est / est.sum()
print("probabilidad estacionaria  calma %.3f  tension %.3f" % (est[0], est[1]))
print("duracion esperada  calma %.1f  tension %.1f periodos" % (1 / 0.05, 1 / 0.10))

rng = np.random.default_rng(4)
n, estado, actual = 20000, 0, 0
duraciones = {0: [], 1: []}
for t in range(n):
    actual += 1
    if rng.random() < P[estado, 1 - estado]:
        duraciones[estado].append(actual)
        actual = 0
        estado = 1 - estado
print("duracion simulada  calma %.1f  tension %.1f periodos"
      % (np.mean(duraciones[0]), np.mean(duraciones[1])))
# -> probabilidad estacionaria  calma 0.667  tension 0.333
# -> duracion esperada  calma 20.0  tension 10.0 periodos
# -> duracion simulada  calma 20.0  tension 9.9 periodos
