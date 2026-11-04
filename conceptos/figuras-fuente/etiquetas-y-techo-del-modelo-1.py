"""etiquetas-y-techo-del-modelo-1.py — el techo que pone el ruido de las etiquetas y lo que
ocurre cuando se intenta compensar con capacidad. La figura de calidad de las etiquetas (f6)."""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(8.4, 3.9))

# --- Izquierda: el techo cae con el conflicto, y cae mas deprisa con muchas clases ---
ax = ejes[0]
m = np.linspace(0, 0.30, 200)
ax.plot(m, 1 - m + m / 2, color=AZUL, linewidth=1.9, label="2 clases")
ax.plot(m, 1 - m + m / 10, color=NARANJA, linewidth=1.9, label="10 clases")
ax.axvline(0.10, color=REJILLA, linewidth=1.1, linestyle=":")
ax.plot([0.10, 0.10], [0.95, 0.91], "o", color=TEXTO, markersize=5, zorder=5)
ax.set_xlim(0, 0.30)
ax.set_ylim(0.60, 1.02)
ax.set_xlabel("fracción de etiquetas en conflicto")
ax.set_ylabel("exactitud máxima alcanzable")
ax.legend(loc="lower left", fontsize=8.5)
anotar(ax, "con 2 clases, un 10 % de conflicto\ndeja el techo en 0,95",
       (0.10, 0.95), (0.97, 0.88), color=AZUL, align="right")
anotar(ax, "con 10 clases, el mismo conflicto\ncuesta casi el doble",
       (0.10, 0.91), (0.97, 0.14), color=NARANJA, align="right")
titulo(ax, "El conflicto marca el techo", "nada por encima de estas curvas es alcanzable")
numeros(ax, ejes="x")
rejilla(ax)

# --- Derecha: la capacidad extra no sube el techo, lo unico que hace es memorizar el ruido ---
ax = ejes[1]
pos = np.arange(5)
etiquetas = ["2", "4", "6", "12", "sin\nlímite"]
entrena = [0.7087, 0.7602, 0.7850, 0.9055, 1.0000]
prueba = [0.7400, 0.7863, 0.7804, 0.7250, 0.6871]

ax.plot(pos, entrena, "o-", color=ROJO, linewidth=1.8, markersize=6,
        label="sobre el entrenamiento (con ruido)")
ax.plot(pos, prueba, "o-", color=AZUL, linewidth=1.8, markersize=6,
        label="sobre datos limpios")
ax.axhline(0.7863, color=REJILLA, linewidth=1.1, linestyle="--")
ax.set_xticks(pos)
ax.set_xticklabels(etiquetas)
ax.set_xlim(-0.35, 4.35)
ax.set_ylim(0.60, 1.20)
ax.set_xlabel("profundidad del árbol de decisión")
ax.set_ylabel("exactitud")
ax.legend(loc="upper left", fontsize=8.5)
anotar(ax, "el mejor no es el más grande:\nel máximo está aquí",
       (1, 0.7863), (0.03, 0.10), color=AZUL)
anotar(ax, "sin límite: 1,0000 dentro, 0,6871 fuera",
       (4, 1.0000), (0.97, 0.56), color=ROJO, align="right", fondo=True)
titulo(ax, "Más capacidad memoriza el ruido", "15 % de etiquetas cambiadas por una moneda")
rejilla(ax)
numeros(ax, ejes="y")

guardar(fig, "etiquetas-techo-y-memorización")
