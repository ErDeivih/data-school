"""correlacion-pearson-spearman-1.py — Pearson mira las distancias, Spearman solo el orden.

Arriba a la izquierda, una recta perfecta: las dos correlaciones valen 1.
Arriba a la derecha, la misma recta con el último valor disparado a 20: Pearson cae a 0,8165
porque mira cuanto se separa ese punto de la recta, y Spearman sigue en 1 porque el 20 sigue
siendo el mayor de la lista.
Abajo, una relación monotona pero no lineal (y = x al cuadrado en el tramo positivo): Spearman
la ve perfecta y Pearson la infravalora, porque solo premia las rectas.
"""

import numpy as np
from scipy import stats

from comun import *

estilo()

x = np.arange(1, 9, dtype=float)
lineal = x.copy()
con_atipico = np.array([1, 2, 3, 4, 5, 6, 7, 20], dtype=float)
curva = x ** 2

r_lineal = float(stats.pearsonr(x, lineal)[0])
rho_lineal = float(stats.spearmanr(x, lineal)[0])
r_atipico = float(stats.pearsonr(x, con_atipico)[0])
rho_atipico = float(stats.spearmanr(x, con_atipico)[0])
r_curva = float(stats.pearsonr(x, curva)[0])
rho_curva = float(stats.spearmanr(x, curva)[0])

fig = plt.figure(figsize=(10.4, 7.4))
rejilla_paneles = fig.add_gridspec(2, 2)
arriba_izq = fig.add_subplot(rejilla_paneles[0, 0])
arriba_der = fig.add_subplot(rejilla_paneles[0, 1])
abajo = fig.add_subplot(rejilla_paneles[1, :])


def etiquetas(eje, r, rho):
    """Las dos correlaciones, escritas en la esquina libre del panel."""
    eje.text(0.04, 0.95, "Pearson  %+.4f" % r, transform=eje.transAxes, va="top",
             fontsize=9.5, color=AZUL)
    eje.text(0.04, 0.86, "Spearman %+.4f" % rho, transform=eje.transAxes, va="top",
             fontsize=9.5, color=VERDE)


# --- Arriba izquierda: la recta perfecta ---------------------------------------------------
arriba_izq.scatter(x, lineal, s=38, color=AZUL, zorder=3)
arriba_izq.plot(x, lineal, color=AZUL, linewidth=1.0, alpha=0.6)
etiquetas(arriba_izq, r_lineal, rho_lineal)
arriba_izq.set_ylim(0, 23)
titulo(arriba_izq, "Recta perfecta: las dos valen 1",
       "una recta tambi\u00e9n es una relaci\u00f3n mon\u00f3tona")
arriba_izq.set_xlabel("x")
arriba_izq.set_ylabel("y")
numeros(arriba_izq)
rejilla(arriba_izq)

# --- Arriba derecha: un solo punto lo cambia todo -------------------------------------------
arriba_der.scatter(x[:-1], con_atipico[:-1], s=38, color=AZUL, zorder=3)
arriba_der.scatter([x[-1]], [con_atipico[-1]], s=70, facecolor="none", edgecolor=ROJO,
                   linewidth=1.8, zorder=4)
arriba_der.plot(x, x, color=REJILLA, linewidth=1.2, linestyle="--")
etiquetas(arriba_der, r_atipico, rho_atipico)
arriba_der.set_ylim(0, 23)
arriba_der.annotate("el 20 sigue siendo el mayor:\nel orden no cambia",
                    xy=(8.0, 19.0), xycoords="data", xytext=(0.30, 0.62),
                    textcoords="axes fraction", fontsize=8.5, color=ROJO, va="center",
                    arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9, shrinkA=2,
                                    shrinkB=6))
titulo(arriba_der, "Un solo punto hunde a Pearson y no a Spearman",
       "la recta gris es la que seguir\u00eda el resto de los puntos")
arriba_der.set_xlabel("x")
arriba_der.set_ylabel("y")
numeros(arriba_der)
rejilla(arriba_der)

# --- Abajo: monotona pero no lineal ---------------------------------------------------------
abajo.scatter(x, curva, s=38, color=MORADO, zorder=3)
abajo.plot(x, curva, color=MORADO, linewidth=1.4, alpha=0.7)
etiquetas(abajo, r_curva, rho_curva)
abajo.annotate("crece siempre, pero al final\nmucho m\u00e1s deprisa que al principio",
               xy=(4.0, 16.0), xycoords="data", xytext=(0.58, 0.30),
               textcoords="axes fraction", fontsize=8.5, color=MORADO, va="center",
               arrowprops=dict(arrowstyle="->", color=MORADO, linewidth=0.9, shrinkA=2,
                               shrinkB=6))
titulo(abajo, "y = x al cuadrado: mon\u00f3tona y nada lineal",
       "Spearman mide el orden y da 1; Pearson mide la recta y se queda en 0,9762")
abajo.set_xlabel("x")
abajo.set_ylabel("y = x^2")
numeros(abajo)
rejilla(abajo)

guardar(fig, "correlacion-pearson-frente-a-spearman")
