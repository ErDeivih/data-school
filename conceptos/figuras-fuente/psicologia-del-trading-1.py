"""psicologia-del-trading-1.py — las rachas que van a llegar, y lo que cuesta doblar el tamaño.

Izquierda: probabilidad de que aparezca al menos una racha de k pérdidas seguidas, con un sistema
que pierde el 55 % de las veces, en 200 operaciones y en 1.000. Con 200 operaciones, tres de cada
cuatro series contienen una racha de 7 pérdidas: no es un fallo del sistema, es cómo se reparte el
azar.
Derecha: lo que cuesta una racha de k pérdidas con riesgo fijo de 1R y con el tamaño doblado a
partir de la cuarta. Diez pérdidas con riesgo fijo son 10R; duplicando son 257R, más de lo que el
sistema gana en 700 operaciones.
La figura de la página de psicología del trading (fase 9).
"""

import numpy as np

from comun import *

estilo()


def prob_racha(n, k, p_perder):
    """Probabilidad de que aparezca al menos una racha de k pérdidas en n operaciones.

    El estado es la racha actual (0 a k); llegar a k es absorbente.
    """
    v = np.zeros(k + 1)
    v[0] = 1.0
    for _ in range(n):
        nuevo = np.zeros(k + 1)
        nuevo[0] = (1 - p_perder) * v[:k].sum()  # no pierde: la racha vuelve a cero
        nuevo[1:k] = p_perder * v[0:k - 1]       # pierde y alarga la racha
        nuevo[k] = p_perder * v[k - 1] + v[k]    # llega a k, y de ahí ya no se sale
        v = nuevo
    return float(v[k])


fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.5))

# --- Izquierda: la racha que te va a hacer dudar -------------------------------------
ax = ejes[0]
largos = np.arange(2, 13)
corta = np.array([prob_racha(200, int(k), 0.55) for k in largos])
larga = np.array([prob_racha(1000, int(k), 0.55) for k in largos])

ax.plot(largos, corta, color=AZUL, linewidth=2.2, marker="o", markersize=5, zorder=4)
ax.plot(largos, larga, color=MORADO, linewidth=2.0, marker="s", markersize=5, zorder=3)
anotar(ax, "en 200 operaciones, el 76 % de las series\ncontiene una racha de 7 pérdidas",
       xy=(7, float(corta[5])), xytext=(0.02, 0.86), color=AZUL, flecha=False)
anotar(ax, "en 1.000, dos de cada tres series\nven 10 pérdidas seguidas",
       xy=(10, float(larga[8])), xytext=(0.98, 0.96), color=MORADO, align="right",
       flecha=False)
titulo(ax, "La racha no es un fallo: estaba en el guion",
       "sistema que pierde el 55 % de las veces; probabilidad de al menos una racha")
ax.set_xlabel("pérdidas seguidas (k)")
ax.set_ylabel("probabilidad de que ocurra")
ax.set_xticks(largos)
ax.set_yticks([0.0, 0.25, 0.5, 0.75, 1.0])
ax.set_ylim(-0.04, 1.32)
ax.set_xlim(1.6, 12.4)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{v:.0%}"))
rejilla(ax)

# --- Derecha: lo que cuesta la misma racha con y sin doblar ---------------------------
ax = ejes[1]
perdidas = np.arange(1, 13)
fijo = perdidas.astype(float)                                   # 1R cada una
doblada = np.where(perdidas <= 3, perdidas, 2.0 ** (perdidas - 2) + 1)   # dobla desde la 4ª

ax.semilogy(perdidas, fijo, color=AZUL, linewidth=2.2, marker="o", markersize=5, zorder=4)
ax.semilogy(perdidas, doblada, color=ROJO, linewidth=2.2, marker="s", markersize=5, zorder=3)
ax.axhline(70.0, color=VERDE, linewidth=1.4, linestyle="--", zorder=2)
anotar(ax, "el resultado esperado de todo el año: 70R",
       xy=(7.0, 70.0), xytext=(0.03, 0.72), color=VERDE, flecha=False)
anotar(ax, "diez pérdidas con riesgo fijo son 10R",
       xy=(10.0, 10.0), xytext=(0.52, 0.13), color=AZUL)
anotar(ax, "las mismas diez duplicando desde la cuarta: 257R",
       xy=(10.0, 257.0), xytext=(0.98, 0.95), color=ROJO, align="right", flecha=False)
titulo(ax, "Doblar tras perder convierte la racha en una escalera",
       "coste acumulado de una racha de pérdidas, en múltiplos de R")
ax.set_xlabel("pérdidas seguidas")
ax.set_ylabel("coste acumulado (R)")
ax.set_xticks([1, 2, 3, 4, 6, 8, 10, 12])
ax.set_ylim(0.7, 900)
ax.set_yticks([1, 10, 70, 257, 700])
ax.set_yticklabels(["1", "10", "70", "257", "700"])
ax.set_xlim(0.4, 12.6)
rejilla(ax)
numeros(ax, ejes="x")

guardar(fig, "psicologia-rachas-y-doblar")
