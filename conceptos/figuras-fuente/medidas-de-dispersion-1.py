"""medidas-de-dispersion-1.py — la media no distingue nada; la desviación, si.

Arriba: dos equipos con la misma media. El A esta apilado en el centro, el B tiene los datos
en los extremos. Abajo: las mismas dos formas miradas como desviaciones respecto a la media,
que es de donde sale la desviación típica. El pie lleva el coeficiente de variación, el único
número que permite comparar la dispersión de cosas medidas en unidades distintas.
"""

import numpy as np

from comun import *

estilo()

equipo_a = np.array([48.0, 49.0, 50.0, 51.0, 52.0])
equipo_b = np.array([10.0, 30.0, 50.0, 70.0, 90.0])

sd_a = float(equipo_a.std(ddof=1))
sd_b = float(equipo_b.std(ddof=1))
cv_a = 100 * sd_a / float(equipo_a.mean())
cv_b = 100 * sd_b / float(equipo_b.mean())

fig = plt.figure(figsize=(9.4, 6.6))
rejilla_paneles = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.15])
arriba = fig.add_subplot(rejilla_paneles[0, 0])
abajo = fig.add_subplot(rejilla_paneles[1, 0])

# --- Arriba: los dos equipos en una recta, con su media comun ------------------------------
arriba.axhline(50, color=REJILLA, linewidth=1.0, linestyle="--")
arriba.scatter(equipo_a, np.full(equipo_a.size, 1.0), s=60, color=AZUL, zorder=3)
arriba.scatter(equipo_b, np.full(equipo_b.size, 0.0), s=60, color=NARANJA, zorder=3)
arriba.text(2, 1.0, "equipo A", color=AZUL, fontsize=9.5, va="center")
arriba.text(2, 0.0, "equipo B", color=NARANJA, fontsize=9.5, va="center")
arriba.set_xlim(-3, 128)
arriba.set_ylim(-0.7, 1.75)
arriba.set_yticks([])

arriba.annotate("media 50 en los dos: la media no distingue\nun grupo del otro",
                xy=(50.0, 1.0), xycoords="data", xytext=(0.34, 0.86),
                textcoords="axes fraction", fontsize=8.5, color=ROJO, va="center",
                arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9, shrinkA=2,
                                shrinkB=6))
arriba.annotate("80 horas de rango",
                xy=(50.0, 0.0), xycoords="data", xytext=(0.78, 0.30),
                textcoords="axes fraction", fontsize=8.5, color=NARANJA, va="center",
                arrowprops=dict(arrowstyle="->", color=NARANJA, linewidth=0.9, shrinkA=2,
                                shrinkB=4))
arriba.plot([10.0, 90.0], [0.0, 0.0], color=NARANJA, linewidth=0.9, alpha=0.5)

titulo(arriba, "Misma media, dos realidades opuestas",
       "horas de conexi\u00f3n semanales de dos equipos de cinco personas")
arriba.set_xlabel("horas de conexi\u00f3n semanales")
numeros(arriba, ejes="x")

# --- Abajo: la misma informacion como desviaciones respecto a la media ---------------------
abajo.axhline(0, color=TEXTO, linewidth=0.9)
abajo.axhline(sd_a, color=AZUL, linewidth=1.1, linestyle="--")
abajo.axhline(-sd_a, color=AZUL, linewidth=1.1, linestyle="--")
abajo.axhline(sd_b, color=NARANJA, linewidth=1.1, linestyle="--")
abajo.axhline(-sd_b, color=NARANJA, linewidth=1.1, linestyle="--")
abajo.vlines(np.full(equipo_a.size, 0.18), 0, equipo_a - 50.0, color=AZUL, linewidth=1.6)
abajo.scatter(np.full(equipo_a.size, 0.18), equipo_a - 50.0, s=42, color=AZUL, zorder=3)
abajo.vlines(np.full(equipo_b.size, 0.82), 0, equipo_b - 50.0, color=NARANJA, linewidth=1.6)
abajo.scatter(np.full(equipo_b.size, 0.82), equipo_b - 50.0, s=42, color=NARANJA, zorder=3)
abajo.set_xlim(0, 1.0)
abajo.set_ylim(-48, 48)
abajo.set_xticks([0.18, 0.82])
abajo.set_xticklabels(["equipo A", "equipo B"])

abajo.annotate("desviaci\u00f3n t\u00edpica 1,58",
               xy=(0.18, sd_a), xycoords="data", xytext=(0.26, 0.22),
               textcoords="axes fraction", fontsize=8.5, color=AZUL, va="center",
               arrowprops=dict(arrowstyle="->", color=AZUL, linewidth=0.9, shrinkA=2,
                               shrinkB=2))
abajo.annotate("desviaci\u00f3n t\u00edpica 31,62",
               xy=(0.82, sd_b), xycoords="data", xytext=(0.38, 0.92),
               textcoords="axes fraction", fontsize=8.5, color=NARANJA, va="center",
               arrowprops=dict(arrowstyle="->", color=NARANJA, linewidth=0.9, shrinkA=2,
                               shrinkB=2))

titulo(abajo, "La desviaci\u00f3n t\u00edpica mide esa distancia",
       "cada raya es lo que se aparta un dato de la media; las discontinuas marcan esa distancia media")
abajo.set_xlabel("equipo")
abajo.set_ylabel("desviaci\u00f3n respecto a la media (horas)")
numeros(abajo, ejes="y")
rejilla(abajo)

fig.text(0.5, -0.005,
         "Coeficiente de variaci\u00f3n:  3,2 % en el equipo A  y  63,2 % en el B  \u2014  el equipo B es veinte veces m\u00e1s disperso en t\u00e9rminos relativos",
         ha="center", va="top", fontsize=9, color=MORADO)

guardar(fig, "dispersion-misma-media-dos-equipos")
