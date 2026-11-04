"""tests-no-parametricos-1.py - por qué mirar el orden salva el analisis que la media destroza.

Izquierda: los dos grupos del ejemplo del portal. El 100 del grupo A es un único dato, pero la
media y la desviación del grupo lo absorben todo: el test t no ve nada.
Derecha: los mismos 16 datos reetiquetados con su rango. El 100 pasa a ser «el mayor» y da igual
que este a 100 o a 1.000.000: con los rangos el grupo B domina claramente.
"""

import numpy as np
from scipy import stats

from comun import *

estilo()

a = np.array([1., 2, 3, 4, 5, 6, 7, 100])
b = np.array([20., 21, 22, 23, 24, 25, 26, 27])

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.4))

# ═══ Izquierda: el valor extremo secuestra la media y la desviacion ═══
ax = ejes[0]
ax.scatter(np.zeros(a.size), a, s=30, color=AZUL, zorder=3)
ax.scatter(np.ones(b.size), b, s=30, color=NARANJA, zorder=3)
ax.hlines(a.mean(), -0.22, 0.34, color=AZUL, linewidth=2.2, zorder=4)
ax.hlines(b.mean(), 0.66, 1.22, color=NARANJA, linewidth=2.2, zorder=4)
ax.text(0.36, a.mean(), f"media {coma(a.mean())}", color=AZUL, fontsize=9, va="bottom")
ax.text(0.64, b.mean(), f"media {coma(b.mean())}", color=NARANJA, fontsize=9,
        va="bottom", ha="right")
ax.set_xticks([0, 1], labels=["grupo A", "grupo B"])
ax.set_xlim(-0.5, 1.5)
ax.set_ylabel("valor observado")
t_w, p_w = stats.ttest_ind(a, b, equal_var=False)
_, p_mw = stats.mannwhitneyu(a, b, alternative="two-sided")
anotar(ax, "desviación del grupo A: " + coma(a.std(ddof=1)) + "\npor un solo dato. El test t\n"
           "de Welch da p = " + coma(round(p_w, 2)),
       (0.0, 100), (0.06, 0.55), color=ROJO)
titulo(ax, "Un solo valor extremo hace desaparecer la diferencia",
       "siete de los ocho valores de A están por debajo de todos los de B")

# ═══ Derecha: los mismos datos, ordenados ═══
ax = ejes[1]
juntos = np.concatenate([a, b])
etiqueta = np.array(["A"] * a.size + ["B"] * b.size)
rangos = stats.rankdata(juntos)
for grupo, color in (("A", AZUL), ("B", NARANJA)):
    es = etiqueta == grupo
    ax.scatter(rangos[es], juntos[es], s=30, color=color, zorder=3)
ax.set_xlabel("rango que le toca dentro de los 16 datos")
ax.set_ylabel("valor observado")
ax.set_xlim(0, 17)
ax.set_ylim(0, 128)
ax.text(0.02, 0.95, "rango 16: da igual que valga 100\no un millón, el test no lo mira",
        transform=ax.transAxes, fontsize=8.5, va="top", color=ROJO)
anotar(ax, "los rangos 1 a 7 son de A y los 8 a 15 de B:\n"
           "R₁ = 44, U = 8 y p = 0,0104. Con los rangos,\nla conclusión cambia por completo",
       (14.0, 34), (0.03, 0.35), flecha=False, color=TEXTO)
titulo(ax, "Con rangos, lo que cuenta es el orden, no la distancia",
       "el test de Mann-Whitney solo mira quién va por delante de quién")

guardar(fig, "tests-no-parametricos-media-rota-y-rangos")
