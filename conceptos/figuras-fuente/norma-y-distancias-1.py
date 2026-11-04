"""norma-y-distancias-1.py — elegir norma es elegir la forma del vecindario, y Mahalanobis
no ordena los puntos como la euclídea. Figura de la pagina norma-y-distancias."""

import numpy as np

from comun import *

estilo()

# Nube de puntos correlacionados: semilla fija para que la figura salga siempre igual.
azar = np.random.default_rng(7)
S = np.array([[1.0, 0.9], [0.9, 1.0]])
nube = azar.multivariate_normal([0.0, 0.0], S, size=160)
S_inv = np.linalg.inv(S)

dif = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
euclidea = np.linalg.norm(dif, axis=1)
maha = np.sqrt(np.einsum("ij,jk,ik->i", dif, S_inv, dif))


def coma(v, dec=2):
    return ("%.*f" % (dec, v)).replace(".", ",")


# Tres paneles no caben en una fila: cada uno quedaba tan estrecho que el titulo se salia
# por los lados y se solapaba con los ejes. Dos arriba y el de barras abajo, a todo el ancho.
fig = plt.figure(figsize=(9.8, 7.4))
rejilla_paneles = fig.add_gridspec(2, 2)
bolas = fig.add_subplot(rejilla_paneles[0, 0])
maha_eje = fig.add_subplot(rejilla_paneles[0, 1])
barras = fig.add_subplot(rejilla_paneles[1, :])

# ------------------------------------ arriba a la izquierda: la forma del vecindario
t = np.linspace(0, 2 * np.pi, 400)
bolas.set_aspect("equal")
bolas.set_xlim(-1.55, 1.55)
bolas.set_ylim(-1.45, 1.45)

bolas.plot(np.cos(t), np.sin(t), color=AZUL, linewidth=2.0)
bolas.plot([1, 0, -1, 0, 1], [0, 1, 0, -1, 0], color=ROJO, linewidth=2.0)
bolas.plot([1, 1, -1, -1, 1], [1, -1, -1, 1, 1], color=VERDE, linewidth=2.0)
bolas.text(0.04, 1.08, "L2", fontsize=10, color=AZUL)
bolas.text(1.08, 0.0, "L1", fontsize=10, color=ROJO)
bolas.text(1.06, 1.04, "L∞", fontsize=10, color=VERDE)

bolas.plot([0.6], [0.8], marker="o", markersize=7, color=MORADO, zorder=5)
# El rotulo se escribe en coordenadas del eje (0-1) para caer dentro del rombo, en el hueco
# que queda a la izquierda del punto.
anotar(bolas, "(0,6; 0,8)", xy=(0.58, 0.78), xytext=(0.40, 0.56), color=MORADO)
titulo(bolas, "El mismo radio, tres vecindarios",
       "(0,6; 0,8) está a 1 en L2, a 1,4 en L1 y a 0,8 en L∞")
numeros(bolas)
rejilla(bolas, "both")

# ----------------------------- arriba a la derecha: Mahalanobis con variables correlacionadas
maha_eje.set_aspect("equal")
maha_eje.set_xlim(-2.8, 2.8)
maha_eje.set_ylim(-2.9, 2.6)

maha_eje.plot(nube[:, 0], nube[:, 1], marker="o", linestyle="none", markersize=3,
              color=REJILLA, alpha=0.75)

L = np.linalg.cholesky(S)
radio = float(maha[0])
elipse = radio * (L @ np.vstack([np.cos(t), np.sin(t)]))
maha_eje.plot(elipse[0], elipse[1], color=CIAN, linewidth=1.8)

maha_eje.plot([1.0, 0.0], [0.0, 1.0], marker="o", linestyle="none", markersize=8,
              color=ROJO, label="(1, 0) y (0, 1): a 2,29")
maha_eje.plot([1.0], [1.0], marker="o", markersize=8, color=VERDE,
              label="(1, 1): a 1,03")
# La nota del contorno cian se va a la esquina de arriba a la izquierda, que es la unica
# zona sin nube, y la flecha senala el arco de la elipse.
anotar(maha_eje, "el contorno cian: la misma\ndistancia de Mahalanobis",
       xy=(1.86, 2.29), xytext=(0.03, 0.90), color=CIAN)
titulo(maha_eje, "Con correlación 0,9, (1, 1) no es lo raro",
       "las dos variables suben juntas; ese contorno mide 2,29")
maha_eje.legend(loc="lower right", fontsize=8)
numeros(maha_eje)
rejilla(maha_eje, "both")

# -------------------- abajo, a todo el ancho: el orden de cercanía se invierte
pos = np.arange(3)
ancho = 0.38
barras.bar(pos - ancho / 2, euclidea, ancho, color=AZUL, label="distancia euclídea")
barras.bar(pos + ancho / 2, maha, ancho, color=NARANJA, label="distancia de Mahalanobis")
barras.set_xticks(pos)
barras.set_xticklabels(["(1, 0)", "(0, 1)", "(1, 1)"], fontsize=9)
barras.set_ylim(0, 3.6)
for k in range(3):
    barras.text(k - ancho / 2, euclidea[k] + 0.06, coma(euclidea[k]),
                ha="center", fontsize=8, color=TEXTO)
    barras.text(k + ancho / 2, maha[k] + 0.06, coma(maha[k]),
                ha="center", fontsize=8, color=TEXTO)
barras.set_ylabel("distancia al origen")
titulo(barras, "Las dos distancias no ordenan igual",
       "en Euclídea gana (1, 1); en Mahalanobis gana (1, 0)")
barras.legend(loc="upper right", fontsize=8)
numeros(barras)
rejilla(barras)

guardar(fig, "normas-y-mahalanobis")
