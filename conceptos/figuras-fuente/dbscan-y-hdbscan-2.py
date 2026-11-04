"""dbscan-y-hdbscan-2.py — dos lunas entrelazadas: K-means corta por el medio y DBSCAN
sigue la densidad. Pagina de DBSCAN y HDBSCAN (fase 6)."""

import numpy as np
from sklearn.cluster import DBSCAN, KMeans
from sklearn.datasets import make_moons

from comun import *

estilo()

# Dos lunas entrelazadas: no hay ninguna recta que las separe, que es justo el caso en el
# que K-means no tiene nada que hacer.
X, y_real = make_moons(n_samples=340, noise=0.085, random_state=7)

fig, ejes = plt.subplots(2, 1, figsize=(8.6, 7.4))

# --- Arriba: K-means, que solo puede poner fronteras rectas.
modelo_km = KMeans(n_clusters=2, n_init=10, random_state=0).fit(X)
etiquetas_km = modelo_km.labels_
for grupo, color in ((0, AZUL), (1, NARANJA)):
    ejes[0].scatter(X[etiquetas_km == grupo, 0], X[etiquetas_km == grupo, 1], s=18,
                    color=color, alpha=0.8)
ejes[0].scatter(modelo_km.cluster_centers_[:, 0], modelo_km.cluster_centers_[:, 1],
                s=170, color=ROJO, marker="X", zorder=5, label="centroides")
# El acierto se mide contra las lunas de verdad. Como el numero de grupo es arbitrario, se
# prueban las dos asignaciones y se toma la mejor: 0 -> luna A o 0 -> luna B.
acuerdo_km = max((etiquetas_km == y_real).mean(), (etiquetas_km == (1 - y_real)).mean())
anotar(ejes[0], f"acierta el {acuerdo_km:.0%}: cada luna se queda\npartida por la mitad",
       xy=(float(modelo_km.cluster_centers_[1, 0]), float(modelo_km.cluster_centers_[1, 1])),
       xytext=(0.98, 0.16), color=ROJO, flecha=False, align="right")
titulo(ejes[0], "K-means: dos mitades de cada luna",
       "la frontera entre centroides es una recta y las lunas no son rectas")
ejes[0].set_xlabel("variable 1")
ejes[0].set_ylabel("variable 2")
ejes[0].legend(loc="lower right", fontsize=8)
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="both")

# --- Abajo: DBSCAN con un eps razonable.
EPS, MIN_PTS = 0.16, 8
etiquetas_db = DBSCAN(eps=EPS, min_samples=MIN_PTS).fit_predict(X)
ruido = etiquetas_db == -1
for grupo, color in ((0, VERDE), (1, MORADO)):
    ejes[1].scatter(X[etiquetas_db == grupo, 0], X[etiquetas_db == grupo, 1], s=18,
                    color=color, alpha=0.8, label=f"grupo {grupo + 1}")
# La etiqueta -1 que devuelve DBSCAN son los puntos que no ha metido en ningun grupo.
ejes[1].scatter(X[ruido, 0], X[ruido, 1], s=44, color=ROJO, marker="x",
                label=f"ruido detectado ({int(ruido.sum())})")
anotar(ejes[1], f"eps = {coma(EPS)} y minPts = {MIN_PTS}:\nlos dos grupos salen enteros",
       xy=(0.0, 0.5), xytext=(0.04, 0.90), color=ROJO)
titulo(ejes[1], "DBSCAN: sigue la densidad, no el centro",
       "y además dice qué puntos no pertenecen a nada")
ejes[1].set_xlabel("variable 1")
ejes[1].set_ylabel("variable 2")
ejes[1].legend(loc="lower right", fontsize=8)
rejilla(ejes[1], eje="both")
numeros(ejes[1], ejes="both")

guardar(fig, "dbscan-lunas-frente-a-k-means")
