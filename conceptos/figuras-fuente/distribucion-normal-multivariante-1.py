"""distribucion-normal-multivariante-1.py - la correlación redibuja la nube, no las campanas.

Izquierda: los contornos de una normal bivariante con varianzas 4 y 9 y correlación 0,70, con el
centro en (0,0). Los tres puntos del ejemplo del portal caen sobre la misma elipse: los tres
están a la misma distancia de Mahalanobis, y por eso la densidad en (2,3) y en (-2,-3) es
idéntica. La línea roja marca la dirección principal de la nube y el rombo, el cuadrado y el
triángulo son los tres puntos.
Derecha: con las MISMAS marginales (desviaciones 2 y 3), la probabilidad de que las dos variables
se queden por debajo de 2 sube del 62,9 % al 74,1 % solo por cambiar la correlación de 0 a 0,95.
Las marginales no se mueven: lo que se mueve es la probabilidad conjunta.
"""

import numpy as np
from scipy import stats

from comun import *

estilo()

mu = np.array([0.0, 0.0])
S = np.array([[4.0, 4.2], [4.2, 9.0]])
rho = S[0, 1] / np.sqrt(S[0, 0] * S[1, 1])
Sinv = np.linalg.inv(S)

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.6))

# --- Izquierda: los contornos de la elipse.
ax = ejes[0]
malla = np.linspace(-8.0, 8.0, 261)
X1, X2 = np.meshgrid(malla, malla * 3.0 / 2.0)
Z = np.empty(X1.shape)
for i in range(X1.shape[0]):
    d = np.stack([X1[i], X2[i]], axis=-1) - mu
    Z[i] = np.einsum("ij,jk,ik->i", d, Sinv, d)
niveles = stats.chi2.ppf([0.39, 0.68, 0.86, 0.95, 0.99], df=2)
ax.contourf(X1, X2, Z, levels=np.r_[0.0, niveles], colors=[AZUL], alpha=0.13)
ax.contour(X1, X2, Z, levels=niveles, colors=[AZUL], linewidths=1.1)

# La dirección principal de la nube (autovector dominante) y los tres puntos del ejemplo.
valores, vectores = np.linalg.eigh(S)
v = vectores[:, -1]
largo = np.sqrt(valores[-1]) * 2.6
ax.plot([-largo * v[0], largo * v[0]], [-largo * v[1], largo * v[1]], color=ROJO, linewidth=1.5,
        linestyle="--", zorder=4)
for punto, marca, color in (([2.0, 3.0], "s", NARANJA), ([4.0, 6.0], "^", MORADO),
                            ([-2.0, -3.0], "D", VERDE)):
    ax.plot(punto[0], punto[1], marker=marca, color=color, markersize=7, zorder=5)
ax.plot(0.0, 0.0, marker="o", color=TEXTO, markersize=5, zorder=6)

anotar(ax, "(4, 6): Mahalanobis 4,71,\ndensidad 0,0035",
       (4.0, 6.0), (0.03, 0.92), color=MORADO)
anotar(ax, "(2, 3) y (-2, -3): la misma\nMahalanobis (1,18) y la misma\ndensidad (0,0206)",
       (2.0, 3.0), (0.03, 0.70), color=NARANJA)
ax.text(-7.6, 7.9, "ρ = 0,70", color=ROJO, fontsize=9)
ax.set_xlabel("variable 1  (σ = 2)")
ax.set_ylabel("variable 2  (σ = 3)")
titulo(ax, "La correlación inclina la elipse, no las campanas")
numeros(ax)

# --- Derecha: misma marginal, distinta probabilidad conjunta.
ax = ejes[1]
rhos = [0.0, 0.7, 0.95]
probs = []
for r in rhos:
    Sr = np.array([[4.0, 2.0 * 3.0 * r], [2.0 * 3.0 * r, 9.0]])
    probs.append(float(stats.multivariate_normal(mean=mu, cov=Sr).cdf([2.0, 2.0])))

ax.bar(rhos, probs, width=0.22, color=[CIAN, AZUL, ROJO], zorder=3)
for r, p in zip(rhos, probs):
    ax.text(r, p + 0.012, f"{p:.3f}".replace(".", ","), ha="center", fontsize=10, color=TEXTO)
ax.set_xticks(rhos, labels=["0,00", "0,70", "0,95"])
ax.set_xlabel("correlación entre las dos variables")
ax.set_ylabel("P(variable 1 < 2 y variable 2 < 2)")
ax.set_ylim(0.0, 0.90)
anotar(ax, "las marginales son idénticas\nen las tres barras: lo que cambia\nes la probabilidad conjunta",
       (0.95, probs[2]), (0.30, 0.30), color=TEXTO)
titulo(ax, "La misma campana, otra probabilidad conjunta",
       "varianzas 4 y 9 en los tres casos: solo cambia la covarianza")
rejilla(ax)
numeros(ax, ejes="y")

guardar(fig, "normal-multivariante-elipse-y-conjunta")
