"""z-score-y-estandarizacion-1.py — por qué un 7,5 puede ser mejor resultado que un 8,9.

Arriba, cada examen con su propia regla: la marca corta es su media, los tramos son medias
desviaciones y el punto es la nota del alumno. Las dos reglas miden cosas distintas y a ojo no
se comparan. Abajo, las mismas dos notas pasadas a desviaciones tipicas: el único eje es el
mismo para los dos examenes y se ve de un golpe que el 7,5 estaba más lejos de su clase.
"""

import numpy as np

from comun import *

estilo()

facil_media, facil_sd = 6.5, 1.2
dificil_media, dificil_sd = 5.0, 0.8
nota_facil, nota_dificil = 8.9, 7.5
z_facil = (nota_facil - facil_media) / facil_sd          # 2,000
z_dificil = (nota_dificil - dificil_media) / dificil_sd  # 3,125

fig = plt.figure(figsize=(9.6, 6.4))
rejilla_paneles = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.0])
arriba = fig.add_subplot(rejilla_paneles[0, 0])
abajo = fig.add_subplot(rejilla_paneles[1, 0])

# --- Arriba: dos escalas distintas en el mismo eje ----------------------------------------
for y, media, desv, color in ((1.0, facil_media, facil_sd, VERDE),
                              (0.0, dificil_media, dificil_sd, MORADO)):
    arriba.plot([media - 3 * desv, media + 3 * desv], [y, y], color=color, linewidth=2.0,
                solid_capstyle="butt")
    for k in (-2, -1, 1, 2):
        arriba.plot([media + k * desv, media + k * desv], [y - 0.07, y + 0.07], color=color,
                    linewidth=1.2)
    arriba.plot([media], [y + 0.10], marker="v", markersize=7, color=color)

arriba.plot([nota_facil], [1.0], marker="o", markersize=9, color=VERDE, zorder=3)
arriba.plot([nota_dificil], [0.0], marker="o", markersize=9, color=MORADO, zorder=3)

# Las etiquetas van centradas DEBAJO de cada regla, no a su lado: a la derecha se salian del
# panel y encima de la linea se cruzaban con las marcas.
arriba.text(facil_media, 0.78, "examen f\u00e1cil: media 6,5 y desviaci\u00f3n 1,2",
            color=VERDE, fontsize=9, ha="center", va="top")
arriba.text(dificil_media, -0.22, "examen dif\u00edcil: media 5,0 y desviaci\u00f3n 0,8",
            color=MORADO, fontsize=9, ha="center", va="top")
arriba.text(nota_facil + 0.15, 1.06, "8,9", color=VERDE, fontsize=9.5, va="bottom")
arriba.text(nota_dificil + 0.15, 0.06, "7,5", color=MORADO, fontsize=9.5, va="bottom")
arriba.set_xlim(2.4, 10.4)
arriba.set_ylim(-0.62, 1.62)
arriba.set_yticks([])

titulo(arriba, "Dos ex\u00e1menes, dos reglas distintas",
       "la marca corta es la media y los tramos las desviaciones: las dos reglas miden cosas distintas")
arriba.set_xlabel("nota")
numeros(arriba, ejes="x")

# --- Abajo: los dos pasados a z, un unico eje para los dos --------------------------------
abajo.axvspan(-0.4, 1, color=REJILLA, alpha=0.15)
abajo.axvspan(1, 2, color=CIAN, alpha=0.10)
abajo.axvspan(2, 4, color=ROJO, alpha=0.10)
abajo.axvline(0, color=TEXTO, linewidth=1.0)
for z in (-3, -2, -1, 1, 2, 3):
    abajo.axvline(z, color=REJILLA, linewidth=0.7, linestyle=":")
abajo.plot([z_facil], [1.0], marker="o", markersize=9, color=VERDE, zorder=3)
abajo.plot([z_dificil], [0.0], marker="o", markersize=9, color=MORADO, zorder=3)
abajo.set_xlim(-0.4, 4.05)
abajo.set_ylim(-0.62, 1.62)
abajo.set_yticks([])

abajo.text(z_facil, 1.10, "z = 2,00: dos desviaciones por encima de su clase", color=VERDE,
           fontsize=9, ha="center", va="bottom")
abajo.text(z_dificil, 0.10, "z = 3,12: fuera de donde llega casi nadie de su clase",
           color=MORADO, fontsize=9, ha="center", va="bottom")

titulo(abajo, "El z-score pone los dos ex\u00e1menes en el mismo eje",
       "el 7,5 estaba m\u00e1s lejos de su grupo que el 8,9 del suyo, y ahora se ve")
abajo.set_xlabel("z: cu\u00e1ntas desviaciones t\u00edpicas por encima de la media de su examen")
numeros(abajo, ejes="x")
rejilla(abajo, eje="x")

guardar(fig, "z-score-dos-examenes-en-un-eje")
