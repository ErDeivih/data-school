import numpy as np

rng = np.random.default_rng(0)
normal = rng.normal(0, 1, size=(300, 2))
angulos = np.linspace(0, 2 * np.pi, 15, endpoint=False)
anomalos = 7 * np.column_stack([np.cos(angulos), np.sin(angulos)])   # 15 puntos en un anillo lejano
X = np.vstack([normal, anomalos])
es_anomalia = np.r_[np.zeros(300), np.ones(15)]

# Puntuacion sin modelo: la distancia al quinto vecino mas cercano. Cuanto mayor, mas raro.
D = np.linalg.norm(X[:, None, :] - X[None, :, :], axis=2)   # matriz 315x315 de distancias
D.sort(axis=1)                       # ordena cada fila en el sitio: devuelve None
puntuacion = D[:, 5]                 # la columna 0 es el propio punto; esta es el 5.o vecino
for k in (10, 20):
    elegidos = np.argsort(puntuacion)[::-1][:k]
    print(f"top{k}: {int(es_anomalia[elegidos].sum())} anomalias reales de {k}")
# -> top10: 10 anomalias reales de 10
# -> top20: 15 anomalias reales de 20
print("puntuacion media normal:", round(float(puntuacion[:300].mean()), 3),
      "anomala:", round(float(puntuacion[300:].mean()), 3))
# -> puntuacion media normal: 0.326 anomala: 4.68
