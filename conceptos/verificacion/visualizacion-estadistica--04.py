import numpy as np

# Matriz de correlacion: covarianza estandarizada, diagonal 1 y simetrica.
rng = np.random.default_rng(7)
altura = rng.normal(170, 9, size=400)
peso = 0.8 * altura + rng.normal(20, 4, size=400)   # correlacion fuerte y positiva
horas_sueno = rng.normal(7, 1.2, size=400)          # independiente de las otras dos

datos = np.column_stack([altura, peso, horas_sueno])
r = np.corrcoef(datos, rowvar=False)

print("forma de la matriz:", r.shape)
print("simetrica:", bool(np.allclose(r, r.T)))
print("diagonal:", np.round(np.diag(r), 6).tolist())
print("r(altura, peso):", round(r[0, 1], 3))
print("r(altura, sueno):", round(r[0, 2], 3))
