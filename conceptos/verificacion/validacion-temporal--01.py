import numpy as np

# Serie con tendencia lineal clara y ruido: y = 0.5*t + ruido
rng = np.random.default_rng(7)
n = 400
t = np.arange(n, dtype=float)
y = 0.5 * t + rng.normal(0, 2.0, n)
idx = np.arange(n)

def vecino_mas_cercano(entrena, prueba):
    """Predice con el valor del punto de entrenamiento mas cercano en el tiempo."""
    distancias = np.abs(t[prueba][:, None] - t[entrena][None, :])
    return y[entrena[distancias.argmin(axis=1)]]

def rmse(entrena, prueba):
    return float(np.sqrt(np.mean((y[prueba] - vecino_mas_cercano(entrena, prueba)) ** 2)))

# K-fold barajado: cada punto de prueba tiene vecinos temporales en el entrenamiento
azar = rng.permutation(idx)
err_azar = [rmse(np.setdiff1d(idx, p), p) for p in np.array_split(azar, 5)]

# Walk-forward: cada bloque se predice entrenando solo con lo anterior
err_wf = [rmse(idx[idx < b[0]], b) for b in np.array_split(idx, 5)[1:]]

print("K-fold barajado  RMSE %.2f  pliegues %s"
      % (np.mean(err_azar), " ".join("%.2f" % e for e in err_azar)))
# -> K-fold barajado  RMSE 2.59  pliegues 2.62 2.28 2.60 2.56 2.91
print("walk-forward     RMSE %.2f  bloques %s"
      % (np.mean(err_wf), " ".join("%.2f" % e for e in err_wf)))
# -> walk-forward     RMSE 23.11  bloques 20.48 24.32 25.94 21.70

# La causa: pasado el ultimo punto de entrenamiento, repite siempre ese mismo valor
entrena = idx[idx < 320]
print("predice en t=320 %.1f y en t=399 %.1f; la recta real en t=399 vale 199.5"
      % (vecino_mas_cercano(entrena, np.array([320]))[0],
         vecino_mas_cercano(entrena, np.array([399]))[0]))
# -> predice en t=320 161.3 y en t=399 161.3; la recta real en t=399 vale 199.5
