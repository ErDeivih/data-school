"""reversion-a-la-media-1.py — la farola y el borracho, con la misma regla encima.

Izquierda: dos series indistinguibles a ojo, las dos lejos de su media reciente. La azul tiene a
donde volver; la roja no, porque su nivel se ha ido y la media de la ventana va detras. Derecha:
la misma regla de z-score aplicada a las dos. En la que revierte, el resultado sube y se mantiene;
en la que pasea, lo que se gana es la suerte de una racha concreta.
"""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)
n = 2000
ventana, entrada = 60, 2.0

rev = np.zeros(n)                            # tiene farola: AR(1) con rho 0,95
for t in range(1, n):
    rev[t] = 0.95 * rev[t - 1] + azar.normal(0, 0.01)
paseo = np.cumsum(azar.normal(0, 0.01, n))   # no tiene farola: raiz unitaria


def pnl_reversion(x, ventana=60, entrada=2.0):
    """Compra con z muy negativo y vende con z muy positivo; sale cuando z vuelve a cero."""
    pos, pnl, ops = 0, 0.0, 0
    curva = np.zeros(len(x))
    for t in range(ventana, len(x) - 1):
        v = x[t - ventana:t]
        z = (x[t] - v.mean()) / v.std(ddof=1)
        if pos == 0:
            if z > entrada:
                pos, ops = -1, ops + 1
            elif z < -entrada:
                pos, ops = 1, ops + 1
        elif pos == 1 and z >= 0:
            pos = 0
        elif pos == -1 and z <= 0:
            pos = 0
        pnl += pos * (x[t + 1] - x[t])
        curva[t] = pnl
    return curva, ops


curva_rev, ops_rev = pnl_reversion(rev)
curva_pas, ops_pas = pnl_reversion(paseo)

fig, ejes = plt.subplots(1, 2, figsize=(9.8, 4.3), width_ratios=[1.2, 1.0])

# --- Izquierda: las dos series con la media movil que la regla usa como referencia -----------
inicio = 900
tramo = slice(inicio, inicio + 400)
eje_x = np.arange(inicio, inicio + 400)
media_rev = np.array([rev[t - ventana:t].mean() for t in range(inicio, inicio + 400)])
media_pas = np.array([paseo[t - ventana:t].mean() for t in range(inicio, inicio + 400)])

ejes[0].plot(eje_x, rev[tramo], color=AZUL, linewidth=1.5)
ejes[0].plot(eje_x, media_rev, color=AZUL, linewidth=1.1, linestyle="--", alpha=0.85)
ejes[0].plot(eje_x, paseo[tramo], color=ROJO, linewidth=1.5)
ejes[0].plot(eje_x, media_pas, color=ROJO, linewidth=1.1, linestyle="--", alpha=0.85)
anotar(ejes[0], "aquí la media es una farola:\nla serie se aleja y vuelve",
       xy=(inicio + 100, rev[inicio + 100]), xytext=(0.35, 0.96), color=AZUL)
anotar(ejes[0], "aquí la «media» es solo el sitio\npor donde pasó hace poco",
       xy=(inicio + 390, paseo[inicio + 390]), xytext=(0.97, 0.30), color=ROJO, align="right")
titulo(ejes[0], "Dos series que bajan, dos significados",
       "la línea discontinua es la media de los 60 días anteriores: la referencia de la regla")
ejes[0].set_xlabel("día")
ejes[0].set_ylabel("nivel")
rejilla(ejes[0])
numeros(ejes[0])

# --- Derecha: la misma regla, dos resultados -------------------------------------------------
ejes[1].axhline(0, color=TEXTO, linewidth=0.9)
ejes[1].plot(curva_rev, color=AZUL, linewidth=1.7)
ejes[1].plot(curva_pas, color=ROJO, linewidth=1.7)
anotar(ejes[1], f"revierte: {curva_rev[-2]:+.2f} en {ops_rev} operaciones",
       xy=(1500, curva_rev[1500]), xytext=(0.05, 0.94), color=AZUL)
anotar(ejes[1], f"pasea: {curva_pas[-2]:+.2f} en {ops_pas} operaciones.\nLo ganado es una racha, no una vuelta",
       xy=(1100, curva_pas[1100]), xytext=(0.97, 0.55), color=ROJO, align="right")
titulo(ejes[1], "La misma regla, dos series",
       "resultado acumulado en unidades de la serie, antes de comisiones y diferencial")
ejes[1].set_xlabel("día")
ejes[1].set_ylabel("resultado acumulado")
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "reversion-farola-y-paseo")
