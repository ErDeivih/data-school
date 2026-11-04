"""xgboost-lightgbm-catboost-1.py — por qué la misma formula de ganancia lleva a árboles
distintos segun como se frenen: regularización lambda/gamma y crecimiento por niveles o por
hoja. Pagina de XGBoost, LightGBM y CatBoost (fase 6)."""

import numpy as np

from comun import *

estilo()

# --- Panel izquierdo: ganancia de la formula de XGBoost con g = [-3,-1,1,3] y h = 1.
# La ganancia bruta es 1/2 * [G_L^2/(H_L+lam) + G_R^2/(H_R+lam) - G^2/(H+lam)].
cortes = [((1, 2), -3.0, 1.0, 3.0, 3.0),      # (filas, G_L, H_L, G_R, H_R)
          ((2, 4), -4.0, 2.0, 4.0, 2.0),
          ((4, 7), -3.0, 3.0, 3.0, 1.0)]
G, H = 0.0, 4.0                                # el padre: los cuatro residuos suman cero

lam = np.linspace(0, 24, 300)

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.6))

for (filas, gl, hl, gr, hr), color in zip(cortes, (AZUL, ROJO, VERDE)):
    ganancia = 0.5 * (gl**2 / (hl + lam) + gr**2 / (hr + lam) - G**2 / (H + lam))
    ejes[0].plot(lam, ganancia, color=color, linewidth=1.8,
                 label=f"corte entre {filas[0]} y {filas[1]}")
ejes[0].axhline(2.0, color=TEXTO, linewidth=1.4, linestyle="--")
anotar(ejes[0], "gamma = 2: por debajo de esta línea\nla división no se hace",
       xy=(13.0, 2.0), xytext=(0.30, 0.30), color=TEXTO)
titulo(ejes[0], "Lambda encoge la ganancia del corte",
       "la forma no cambia: la división deja de compensar antes")
ejes[0].set_xlabel("lambda: regularización L2 de las hojas")
ejes[0].set_ylabel("ganancia del corte")
ejes[0].set_xlim(0, 24)
ejes[0].set_ylim(0, 8.6)
ejes[0].legend(loc="upper right")
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="both")

# --- Panel derecho: dos formas de crecer el mismo arbol. Es un esquema, no datos medidos:
# los dos dibujos salen de las mismas cuatro filas del ejemplo de la pagina.
def dibujar(ax, eje_x, nodos, ramas, hojas, color):
    """Dibuja un árbol: ramas, hojas rellenas y la pregunta de cada nodo interno."""
    for x0, y0, x1, y1 in ramas:
        ax.plot([x0 + eje_x, x1 + eje_x], [y0, y1], color=REJILLA, linewidth=1.3, zorder=1)
    for x, y in hojas:
        ax.scatter([x + eje_x], [y], s=110, facecolor=color, edgecolor="none", zorder=3)
    for x, y, etiqueta in nodos:
        ax.scatter([x + eje_x], [y], s=45, facecolor=color, edgecolor="none", zorder=3)
        ax.text(x + eje_x, y - 0.34, etiqueta, ha="center", va="top", fontsize=8,
                color=color, zorder=4,
                bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none"))


# Por niveles: la raiz se divide y sus dos hijos se dividen a la vez (4 hojas).
dibujar(ejes[1], -2.7,
        [(0, 3, "x ≤ 3"), (-1, 2, "x ≤ 1,5"), (1, 2, "x ≤ 5")],
        [(0, 3, -1, 2), (0, 3, 1, 2)],
        [(-2, 1), (0, 1), (0.6, 1), (2, 1)], ROJO)
# Por hoja: solo se abre la hoja que mas reduce la perdida (3 hojas).
dibujar(ejes[1], 3.5,
        [(0, 3, "x ≤ 3"), (1, 2, "x ≤ 5"), (2, 1, "x ≤ 4")],
        [(0, 3, 1, 2), (1, 2, 2, 1)],
        [(-1, 1), (1, 0), (3, 0)], AZUL)
ejes[1].set_xlim(-6.8, 7.4)
ejes[1].set_ylim(0.3, 4.2)
ejes[1].axis("off")
titulo(ejes[1], "Tres formas de crecer",
       "por niveles, en rojo, contra por hoja, en azul")
anotar(ejes[1], "las dos ramas crecen a la vez",
       xy=(-3.7, 2.0), xytext=(0.01, 0.05), color=ROJO)
anotar(ejes[1], "una rama se alarga\ny la otra se queda corta",
       xy=(2.75, 4.6), xytext=(0.76, 0.97), color=AZUL)

guardar(fig, "boosting-ganancia-regularizada-y-crecimiento")
