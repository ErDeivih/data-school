"""pruebas-de-equivalencia-y-no-inferioridad-1.py - cuatro estudios, una zona de equivalencia.

Cada barra es el intervalo de confianza del 90 % de la diferencia entre dos tratamientos (el
intervalo que decide un TOST con alpha = 0,05), sobre la misma zona de equivalencia de mas-menos
0,5 marcada en verde.
A: el intervalo cae entero dentro del margen -> equivalencia declarada.
B: también cae dentro, pero el intervalo es ancho: con un margen de 0,3 no lo seria.
C: el intervalo es ancho y cruza el margen por los dos lados -> ni equivalencia ni superioridad.
D: el intervalo esta fuera por arriba -> la equivalencia no se sostiene, y hay evidencia de
diferencia.
"""

import numpy as np
from scipy import stats

from comun import *

estilo()

# (etiqueta, diferencia observada, semianchura del IC del 90 %, color)
estudios = [
    ("A  n = 400 por grupo", 0.15, 0.16, VERDE),
    ("B  n = 40 por grupo", 0.15, 0.46, AZUL),
    ("C  n = 25 por grupo", 0.30, 0.72, NARANJA),
    ("D  n = 400 por grupo", 1.10, 0.20, ROJO),
]
margen = 0.5

fig, ax = plt.subplots(figsize=(9.2, 4.4))
ax.axvspan(-margen, margen, color=VERDE, alpha=0.12, zorder=0)
for limite in (-margen, margen):
    ax.axvline(limite, color=VERDE, linewidth=1.6, linestyle="--", zorder=1)
ax.axvline(0.0, color=REJILLA, linewidth=1.2, zorder=1)

for pos, (etiqueta, d, semi, color) in enumerate(estudios):
    ax.errorbar(d, pos, xerr=semi, fmt="o", color=color, ecolor=color, elinewidth=2.0,
                capsize=6, markersize=7, zorder=3)

ax.set_yticks(range(len(estudios)), labels=[e[0] for e in estudios])
ax.set_xlabel("diferencia entre los dos tratamientos (el nuevo menos el de referencia)")
ax.set_xlim(-1.05, 1.45)
ax.set_ylim(-0.6, len(estudios) - 0.35)
ax.text(margen + 0.03, len(estudios) - 0.55, "margen +0,5", color=VERDE, fontsize=8.5)
ax.text(-margen - 0.03, len(estudios) - 0.55, "margen −0,5", color=VERDE, fontsize=8.5, ha="right")
anotar(ax, "A: el intervalo entero dentro\ndel margen (equivalencia)", (0.15, 0.0), (0.72, 0.14),
       color=VERDE)
anotar(ax, "D: fuera del margen por arriba:\nla equivalencia no se sostiene", (1.10, 3.0),
       (0.98, 0.80), color=ROJO, align="right")
titulo(ax, "Quién demuestra equivalencia y quién no",
       "intervalos del 90 % sobre la misma zona de equivalencia de ±0,5")
rejilla(ax, eje="x")
numeros(ax, ejes="x")

guardar(fig, "equivalencia-tost-y-su-intervalo")
