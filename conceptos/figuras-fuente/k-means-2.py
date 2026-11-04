"""k-means-2.py — los dos límites de K-means que no se arreglan con más datos: corta por
rectas (dos anillos) y el resultado depende del arranque. Página de K-means (fase 6)."""

import numpy as np
from sklearn.cluster import KMeans

from comun import *

estilo()
azar = np.random.default_rng(7)

# Anillo alrededor de un núcleo: la estructura natural son dos grupos, pero la frontera
# entre ellos tendría que ser un círculo y K-means solo sabe poner rectas.
angulos = azar.uniform(0, 2 * np.pi, 300)
anillo = np.column_stack([2.5 * np.cos(angulos), 2.5 * np.sin(angulos)])
anillo = anillo + azar.normal(0, 0.18, anillo.shape)
nucleo = azar.normal(0, 0.35, (110, 2))
X_anillo = np.vstack([nucleo, anillo])

fig, ejes = plt.subplots(2, 2, figsize=(10.4, 7.8))

# --- Arriba: el mismo anillo con k = 2 y con k = 4.
for eje, k in zip(ejes[0], (2, 4)):
    modelo = KMeans(n_clusters=k, n_init=10, random_state=0).fit(X_anillo)
    colores = [AZUL, NARANJA, MORADO, CIAN]
    for grupo in range(k):
        eje.scatter(X_anillo[modelo.labels_ == grupo, 0], X_anillo[modelo.labels_ == grupo, 1],
                    s=16, color=colores[grupo], alpha=0.75)
    eje.scatter(modelo.cluster_centers_[:, 0], modelo.cluster_centers_[:, 1],
                s=170, color=ROJO, marker="X", zorder=5)
    titulo(eje, f"k = {k}: los grupos salen por trozos de ángulo",
           "cada color es un trozo de anillo, no un anillo entero")
    eje.set_xlabel("variable 1")
    eje.set_ylabel("variable 2")
    eje.set_aspect("equal")
    eje.set_ylim(-3.9, 3.0)
    rejilla(eje, eje="both")
    numeros(eje, ejes="both")

anotar(ejes[0][0], "núcleo y anillo: dos grupos evidentes\nque K-means no puede separar",
       xy=(0.0, 0.0), xytext=(0.06, 0.05), color=ROJO, flecha=False)
anotar(ejes[0][1], "subir k no arregla la forma:\nsolo reparte el anillo en más trozos",
       xy=(2.5, 0.0), xytext=(0.06, 0.05), color=ROJO, flecha=False)

# --- Abajo: el mismo dato y el mismo k, con cuarenta arranques al azar.
# n_init=1 obliga a una sola tirada por semilla: así se ve la lotería del arranque. En
# producción no se hace esto, se sube n_init (o init="k-means++") y se elige la mejor.
nube_a = azar.normal([0, 0], 1.7, (120, 2))
nube_b = azar.normal([8, 0], 0.55, (60, 2))
X_arranque = np.vstack([nube_a, nube_b])

inercia, centroides, etiquetas = [], [], []
for semilla in range(40):
    modelo = KMeans(n_clusters=3, init="random", n_init=1, random_state=semilla).fit(X_arranque)
    inercia.append(modelo.inertia_)
    centroides.append(modelo.cluster_centers_)
    etiquetas.append(modelo.labels_)
inercia = np.array(inercia)

peor, mejor = int(np.argmax(inercia)), int(np.argmin(inercia))
colores = [AZUL, NARANJA, MORADO]

ejes[1][0].hist(inercia, bins=12, color=CIAN, alpha=0.85, edgecolor=TEXTO, linewidth=0.5)
ejes[1][0].axvline(inercia[mejor], color=VERDE, linewidth=2.0)
ejes[1][0].axvline(inercia[peor], color=ROJO, linewidth=2.0)
anotar(ejes[1][0], "mejor arranque", xy=(float(inercia[mejor]), 6.0),
       xytext=(0.06, 0.97), color=VERDE, flecha=False)
anotar(ejes[1][0], "peor arranque", xy=(float(inercia[peor]), 6.0),
       xytext=(0.42, 0.72), color=ROJO)
titulo(ejes[1][0], "Cuarenta arranques, cuarenta inercias",
       f"mismo dato y mismo k = 3: la peor es un {inercia[peor] / inercia[mejor] * 100 - 100:.0f} % mayor que la mejor")
ejes[1][0].set_xlabel("inercia final de cada ejecución")
ejes[1][0].set_ylabel("número de ejecuciones")
ejes[1][0].set_xlim(float(inercia.min()) - 12, float(inercia.max()) + 12)
rejilla(ejes[1][0], eje="y")
numeros(ejes[1][0], ejes="x")

# La peor y la mejor partición, una encima de otra: se ve dónde decide el arranque.
etiquetas_malas = etiquetas[peor]
for grupo in range(3):
    ejes[1][1].scatter(X_arranque[etiquetas_malas == grupo, 0], X_arranque[etiquetas_malas == grupo, 1],
                       s=16, color=colores[grupo], alpha=0.7)
ejes[1][1].scatter(centroides[peor][:, 0], centroides[peor][:, 1], s=170, color=ROJO,
                   marker="X", zorder=5, label="centroides del peor arranque")
ejes[1][1].scatter(centroides[mejor][:, 0], centroides[mejor][:, 1], s=170, facecolor="none",
                   edgecolor=TEXTO, linewidth=1.5, zorder=6, label="centroides del mejor")
anotar(ejes[1][1], "la nube grande se queda con un solo centro\ny la pequeña se reparte entre dos",
       xy=(8.0, 0.0), xytext=(0.30, 0.03), color=ROJO, flecha=False)
titulo(ejes[1][1], "El arranque decide dónde caen las fronteras",
       f"inercia {coma(round(inercia[peor], 0))} frente a {coma(round(inercia[mejor], 0))}")
ejes[1][1].set_xlabel("variable 1")
ejes[1][1].set_ylabel("variable 2")
ejes[1][1].set_ylim(-5.2, 5.0)
ejes[1][1].legend(loc="upper left", fontsize=8)
rejilla(ejes[1][1], eje="both")
numeros(ejes[1][1], ejes="both")

guardar(fig, "k-means-anillos-y-arranque")
