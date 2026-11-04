"""mql5-y-metatrader-1.py — la misma regla leida en la barra en formación y en la barra
cerrada: el repintado. Figura de la pagina de MQL5 y MetaTrader (fase 9)."""

import numpy as np

from comun import *

estilo()

ticks = np.array([100.0, 100.5, 99.5, 100.2, 100.3, 101.0, 101.2, 100.4])
umbral = ticks[3]                            # 100.2: el cierre de la barra 1
x = np.arange(ticks.size)

fig, ax = plt.subplots(figsize=(7.2, 4.4))

# Las tres barras: donde empieza y acaba cada una.
for corte in (3.5, 5.5):
    ax.axvline(corte, color=REJILLA, linewidth=1.0, linestyle=":", zorder=1)
for centro, nombre in zip((1.5, 4.5, 6.5), ("barra 1", "barra 2", "barra 3")):
    ax.text(centro, 102.42, nombre, ha="center", fontsize=8.5, color=REJILLA)

ax.axhline(umbral, color=ROJO, linewidth=1.2, linestyle="--", zorder=1)
ax.plot(x, ticks, color=AZUL, linewidth=1.8, marker="o", markersize=5, zorder=3)

# Las dos entradas posibles sobre la misma serie.
ax.plot(4, ticks[4], marker="v", markersize=9, color=VERDE, zorder=4)
ax.plot(6, ticks[6], marker="v", markersize=9, color=NARANJA, zorder=4)
ax.plot(7, ticks[7], marker="X", markersize=8, color=TEXTO, zorder=4)

ax.set_xlim(-0.8, 8.9)
ax.set_ylim(98.6, 102.75)
ax.set_xticks(x)
ax.set_xlabel("cada punto es un precio que pública el broker")
ax.set_ylabel("precio")
titulo(ax, "La misma regla leida en dos barras distintas",
       "comprar al superar 100,2 (el cierre de la barra 1) y salir al cierre de la barra 3")

ax.text(4.15, 99.72, "lee la barra en formación:\nentra en 100,3", color=VERDE, fontsize=8.5)
ax.annotate("esperar al cierre de la barra 2 obliga\na entrar en 101,2: el primer tick\nde la barra siguiente",
            xy=(6, ticks[6]), xycoords="data", xytext=(0.025, 0.83),
            textcoords="axes fraction", fontsize=8.5, color=NARANJA, va="center", ha="left",
            arrowprops=dict(arrowstyle="->", color=NARANJA, linewidth=0.9, shrinkA=2, shrinkB=2))
ax.text(7.15, 99.9, "salida: 100,4", color=TEXTO, fontsize=8.5)
ax.text(-0.6, umbral + 0.08, "umbral 100,2", color=ROJO, fontsize=8.5)

ax.text(0.02, 0.04, "leyendo la barra en formación:  +0,10 %", transform=ax.transAxes,
        color=VERDE, fontsize=9)
ax.text(0.98, 0.04, "esperando al cierre:  \u22120,79 %", transform=ax.transAxes,
        color=NARANJA, fontsize=9, ha="right")
rejilla(ax)
numeros(ax, "y")

guardar(fig, "mql5-repintado-barra-en-formación")
