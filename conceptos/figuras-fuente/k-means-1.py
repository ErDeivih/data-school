"""k-means-1.py — el método del codo, medido: la inercia siempre baja, la silueta es la que
dice dónde parar. Página de K-means (fase 6)."""

import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from comun import *

estilo()
azar = np.random.default_rng(7)

# Cuatro grupos separados, uno de ellos más pequeño: así se ve que el codo y la silueta
# pueden señalar el mismo k por motivos distintos.
centros = np.array([[-3.0, -2.5], [3.0, -2.0], [-2.5, 3.0], [3.2, 2.8]])
tamanos = np.array([60, 60, 60, 25])
X = np.vstack([azar.normal(c, 0.62, size=(n, 2)) for c, n in zip(centros, tamanos)])

valores_k = np.arange(1, 9)
inercia, siluetas, caidas = [], [], []
anterior = None
for k in valores_k:
    # n_init=10 repite el arranque k-means++ diez veces y se queda con la mejor inercia:
    # con una sola ejecución, dos semillas distintas dan particiones distintas.
    modelo = KMeans(n_clusters=int(k), n_init=10, random_state=0).fit(X)
    inercia.append(modelo.inertia_)
    # Cuánto baja la inercia al añadir este grupo, en porcentaje del valor anterior: es la
    # pendiente de la curva del codo, y es lo único que se puede leer con sentido.
    caidas.append(100 * (anterior - modelo.inertia_) / anterior if anterior else np.nan)
    anterior = modelo.inertia_
    # La silueta no está definida con un solo grupo: se calcula de k = 2 en adelante.
    siluetas.append(silhouette_score(X, modelo.labels_) if k > 1 else np.nan)

inercia = np.array(inercia)
siluetas = np.array(siluetas, dtype=float)
# Dos magnitudes con unidades distintas (inercia al cuadrado y un índice entre -1 y 1) en
# el mismo eje: cada una se lleva a su escala 0-100 y se avisa en la etiqueta.
inercia_pct = 100 * (inercia - inercia.min()) / (inercia.max() - inercia.min())
silueta_pct = 100 * siluetas / np.nanmax(siluetas)

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.5))

ejes[0].plot(valores_k, inercia_pct, color=AZUL, linewidth=2.0, marker="o", markersize=5,
             label="inercia (100 = la peor, 0 = la mejor)")
ejes[0].plot(valores_k[1:], silueta_pct[1:], color=VERDE, linewidth=2.0, marker="s",
             markersize=5, label="silueta (100 = la mejor)")
ejes[0].axvline(4, color=REJILLA, linewidth=1.1, linestyle=":")
anotar(ejes[0], f"el codo está en k = 4: la inercia baja un {caidas[3]:.0f} %\ny al añadir otro grupo solo un {caidas[4]:.0f} %", flecha=False,
       xy=(4, float(inercia_pct[3])), xytext=(0.56, 0.12), color=AZUL)
anotar(ejes[0], "la silueta también toca techo ahí", xy=(4, float(silueta_pct[3])), flecha=False,
       xytext=(0.22, 0.34), color=VERDE)
titulo(ejes[0], "La inercia engaña; la silueta opina",
       "las dos curvas llevadas a la misma escala para poder compararlas")
ejes[0].set_xlabel("k: número de grupos")
ejes[0].set_ylabel("escala 0-100 (cada curva, la suya)")
ejes[0].legend(loc="upper right", fontsize=8)
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="y")

# --- Derecha: la partición que sale con k = 4, con los centroides encima.
modelo4 = KMeans(n_clusters=4, n_init=10, random_state=0).fit(X)
colores = [AZUL, NARANJA, MORADO, CIAN]
for grupo in range(4):
    ejes[1].scatter(X[modelo4.labels_ == grupo, 0], X[modelo4.labels_ == grupo, 1],
                    s=24, color=colores[grupo], alpha=0.75, label=f"grupo {grupo}")
ejes[1].scatter(modelo4.cluster_centers_[:, 0], modelo4.cluster_centers_[:, 1],
                s=185, color=ROJO, marker="X", zorder=5, label="centroides")
# La frontera entre dos centroides es siempre la recta perpendicular al segmento que los
# une: por eso los grupos de K-means son esferas y por eso corta mal las formas alargadas.
anotar(ejes[1], "la frontera entre dos centroides\nes la recta que los separa por la mitad",
       xy=(0.0, 0.0), xytext=(0.42, 0.93), color=TEXTO)
anotar(ejes[1], "el grupo de 25 puntos: K-means no sabe\nque es pequeño, solo mide distancias",
       xy=(float(centros[3, 0]), float(centros[3, 1])), xytext=(0.42, 0.06), color=ROJO)
titulo(ejes[1], "Cada grupo es una esfera alrededor de su centro",
       "k = 4 con los centroides ya convergidos")
ejes[1].set_xlabel("variable 1")
ejes[1].set_ylabel("variable 2")
ejes[1].legend(loc="center left", fontsize=8)
rejilla(ejes[1], eje="both")
numeros(ejes[1], ejes="both")

guardar(fig, "k-means-codo-y-centroides")
