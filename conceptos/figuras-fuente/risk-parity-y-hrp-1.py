"""risk-parity-y-hrp-1.py — quién se lleva el riesgo en cada cartera, y el orden que sale del árbol.

Izquierda: la aportación relativa al riesgo de cada activo en cuatro carteras construidas con la
misma matriz de covarianzas. Repartir el capital a partes iguales no reparte el riesgo: el activo
más volátil y más correlacionado se lleva más de la mitad. ERC lo iguala exactamente, y la
mínima varianza lo baja todavía más a costa de concentrarlo casi todo en uno.
Derecha: la matriz de correlaciones de cuatro activos en el orden que deja la agrupación
jerárquica de HRP. Los dos bloques de correlación alta quedan pegados a la diagonal; en el orden
original estaban separados.
La figura de la página de risk parity y HRP (fase 9).
"""

import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.optimize import minimize
from scipy.spatial.distance import squareform

from comun import *

estilo()

# --- Tres activos con volatilidades muy distintas y correlaciones moderadas -----------
vol = np.array([0.10, 0.20, 0.30])
corr = np.array([[1.0, 0.2, 0.1],
                 [0.2, 1.0, 0.6],
                 [0.1, 0.6, 1.0]])
cov = np.outer(vol, vol) * corr


def aportes(w):
    """Aportación relativa al riesgo de cada activo: RCᵢ / σ(w), que suma 1."""
    rc = w * (cov @ w) / np.sqrt(w @ cov @ w)
    return rc / rc.sum()


# ERC: los pesos que igualan las aportaciones. No hay fórmula cerrada, se resuelve a mano.
# Con la barrera logarítmica el problema es convexo y sale siempre el mismo resultado.
barrera = lambda y: float(0.5 * y @ cov @ y - np.log(y).sum())
erc = minimize(barrera, 1 / np.sqrt(np.diag(cov)), method="BFGS").x
erc = erc / erc.sum()
inversa = (1 / vol) / (1 / vol).sum()
min_var = np.linalg.solve(cov, np.ones(3))
min_var = min_var / min_var.sum()

metodos = [("partes\niguales", np.full(3, 1 / 3)), ("inversa de\nvolatilidad", inversa),
           ("ERC: riesgo\nigual", erc), ("mínima\nvarianza", min_var)]
colores = [AZUL, NARANJA, MORADO]
aportes_todos = np.array([aportes(w) for _, w in metodos])

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.6))

# --- Izquierda: aportación al riesgo de cada método -----------------------------------
ax = ejes[0]
x = np.arange(len(metodos))
base = np.zeros(len(metodos))
for i in range(3):
    alturas = aportes_todos[:, i]
    ax.bar(x, alturas, bottom=base, width=0.62, color=colores[i], alpha=0.42, zorder=3,
           label=f"activo {i + 1}: volatilidad {vol[i]:.0%}")
    # El número va dentro del tramo: así se lee la aportación sin mirar la leyenda.
    for xi, (b, h) in enumerate(zip(base, alturas)):
        if h >= 0.06:
            ax.text(xi, b + h / 2, f"{h:.0%}", ha="center", va="center", fontsize=9.5,
                    color=TEXTO, zorder=5)
    base += alturas
ax.axhline(1 / 3, color=ROJO, linewidth=1.4, linestyle="--", zorder=6)
anotar(ax, "con un tercio del dinero, el activo 3\nse lleva más de la mitad del riesgo",
       xy=(0.0, 0.95), xytext=(0.03, 0.965), color=ROJO)
anotar(ax, "en mínima varianza el activo 3 se queda en el 2 %",
       xy=(3.0, 0.99), xytext=(0.98, 0.895), color=MORADO, align="right")
titulo(ax, "Repartir capital no es repartir riesgo",
       "aportación de cada activo al riesgo total; la línea roja es 1/3")
ax.set_xticks(x)
ax.set_xticklabels([nombre for nombre, _ in metodos], fontsize=8.5)
ax.set_ylabel("aportación al riesgo")
ax.set_ylim(0.0, 1.28)
ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{v:.0%}"))
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.15), ncol=3, fontsize=8)
rejilla(ax)

# --- Derecha: el orden que deja la jerarquía de correlaciones -------------------------
ax = ejes[1]
corr4 = np.array([[1.0, 0.7, 0.2, 0.1],
                  [0.7, 1.0, 0.2, 0.1],
                  [0.2, 0.2, 1.0, 0.8],
                  [0.1, 0.1, 0.8, 1.0]])
# Distancia d = √((1 − ρ)/2) y agrupación por enlace simple: el dendrograma da el orden.
distancia = np.sqrt(np.clip(0.5 * (1 - corr4), 0.0, None))
np.fill_diagonal(distancia, 0.0)
Z = linkage(squareform(distancia, checks=False), method="single")
orden = list(dendrogram(Z, no_plot=True)["leaves"])
reordenada = corr4[np.ix_(orden, orden)]

for i in range(4):
    for j in range(4):
        valor = float(reordenada[i, j])
        if i == j:
            color, alfa = REJILLA, 0.18
        elif valor >= 0:
            color, alfa = ROJO, 0.06 + 0.64 * valor
        else:
            color, alfa = CIAN, 0.06 + 0.64 * abs(valor)
        ax.add_patch(plt.Rectangle((j, 3 - i), 1, 1, facecolor=color, alpha=alfa,
                                   edgecolor="white", linewidth=1.6))
        ax.text(j + 0.5, 3 - i + 0.5, f"{valor:.1f}".replace(".", ","), ha="center",
                va="center", fontsize=10, color=TEXTO)
for k, indice in enumerate(orden):
    ax.text(k + 0.5, 4.10, f"activo {indice + 1}", ha="center", va="bottom", fontsize=9)
    ax.text(-0.10, 3 - k + 0.5, f"activo {indice + 1}", ha="right", va="center", fontsize=9)
# Los dos bloques que encuentra el árbol, marcados donde están.
for desde, hasta in ((0, 2), (2, 4)):
    ax.plot([desde + 0.06, hasta - 0.06, hasta - 0.06, desde + 0.06, desde + 0.06],
            [-0.12, -0.12, -0.46, -0.46, -0.12], color=MORADO, linewidth=1.5, clip_on=False)
ax.text(1.0, -0.62, "bloque que se mueve junto", ha="center", va="top", fontsize=8.5,
        color=MORADO)
ax.text(3.0, -0.62, "el otro bloque", ha="center", va="top", fontsize=8.5, color=MORADO)
titulo(ax, "Ordenar por jerarquía junta lo que se parece",
       "correlaciones de cuatro activos, en el orden que deja el dendrograma")
ax.set_xlim(0, 4)
ax.set_ylim(-0.95, 4.60)
ax.set_xticks([])
ax.set_yticks([])
for lado in ax.spines.values():
    lado.set_visible(False)

guardar(fig, "risk-parity-aportes-y-jerarquia")
