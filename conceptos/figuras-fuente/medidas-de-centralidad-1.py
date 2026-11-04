"""medidas-de-centralidad-1.py — por qué la media no representa a la mayoria.

Arriba: 9 vecinos y el sueldo de un jugador de futbol. La media se va detras del único valor
grande; la mediana se queda donde esta la gente. Abajo: la escalera de valores ordenados, que
deja ver de un golpe que nueve de los diez cobran menos que la media.

Las tres notas de la izquierda van DENTRO de su propio panel, con coordenadas de la figura:
anotadas contra el borde del eje se salian por abajo o se cruzaban con el titulo del panel
siguiente (visto al revisar el PNG del 2026-10-15).
"""

import numpy as np

from comun import *

estilo()

vecinos = np.array([1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0])   # miles de euros
con_futbolista = np.append(vecinos, 40.0)

media_sin = float(vecinos.mean())
media = float(con_futbolista.mean())
mediana = float(np.median(con_futbolista))

fig = plt.figure(figsize=(9.2, 6.6))
rejilla_paneles = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.15])
arriba = fig.add_subplot(rejilla_paneles[0, 0])
abajo = fig.add_subplot(rejilla_paneles[1, 0])

# --- Arriba: los diez sueldos en escala logaritmica (si no, el de 40.000 aplasta al resto) ---
bordes = np.logspace(np.log10(1.05), np.log10(52.0), 30)
arriba.hist(con_futbolista, bins=bordes, color=CIAN, alpha=0.30)
arriba.axvline(media_sin, color=NARANJA, linewidth=1.4, linestyle=":")
arriba.axvline(mediana, color=VERDE, linewidth=1.6)
arriba.axvline(media, color=ROJO, linewidth=1.6, linestyle="--")
arriba.set_xscale("log")
arriba.set_xlim(1.05, 52.0)
arriba.set_ylim(0, 3.2)
arriba.set_yticks([])

arriba.annotate("9 de los 10 vecinos\ncobran menos que la media",
                xy=(mediana, 1.65), xycoords="data", xytext=(0.05, 0.82),
                textcoords="axes fraction", fontsize=8.5, color=ROJO, va="center",
                arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9, shrinkA=2,
                                shrinkB=4))
arriba.annotate("la mediana sube solo a 1.650 \u20ac",
                xy=(mediana, 0.75), xycoords="data", xytext=(0.13, 0.38),
                textcoords="axes fraction", fontsize=8.5, color=VERDE, va="center",
                arrowprops=dict(arrowstyle="->", color=VERDE, linewidth=0.9, shrinkA=8,
                                shrinkB=4))
arriba.annotate("sin \u00e9l la media de los nueve\nvuelve a 1.600 \u20ac",
                xy=(media_sin, 0.62), xycoords="data", xytext=(0.05, 0.10),
                textcoords="axes fraction", fontsize=8.5, color=NARANJA, va="center",
                arrowprops=dict(arrowstyle="->", color=NARANJA, linewidth=0.9, shrinkA=2,
                                shrinkB=4))

titulo(arriba, "Un solo sueldo mueve la media y no la mediana",
       "los mismos nueve vecinos; el jugador de 40.000 \u20ac es la barra de la derecha")
arriba.set_xlabel("sueldo mensual (euros, escala logar\u00edtmica)")
numeros(arriba, ejes="x")

# --- Abajo: la escalera de valores ordenados y donde caen las tres medidas -----------------
ordenados = np.sort(con_futbolista)
posiciones = np.arange(1, ordenados.size + 1)
abajo.plot(posiciones, ordenados, color=AZUL, marker="o", linewidth=1.4, markersize=5)
abajo.axhline(mediana, color=VERDE, linewidth=1.4)
abajo.axhline(media, color=ROJO, linewidth=1.6, linestyle="--")
abajo.set_yscale("log")
abajo.set_ylim(1.0, 60.0)
abajo.set_xlim(0.4, 9.9)
abajo.set_xticks(posiciones)

# Las dos notas van a la derecha de la escalera, que ahi esta vacia. El limite del eje llega
# hasta 9,9 para que quepa el texto: con el limite en 10,6 se salia del panel.
abajo.annotate("media 5.440 \u20ac: un punto de equilibrio,\nno un vecino",
               xy=(7.4, media), xycoords="data", xytext=(0.62, 0.88),
               textcoords="axes fraction", fontsize=8.5, color=ROJO, va="center",
               arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9, shrinkA=12,
                               shrinkB=2))
abajo.annotate("mediana 1.650 \u20ac: la mitad por debajo",
               xy=(7.4, mediana), xycoords="data", xytext=(0.62, 0.72),
               textcoords="axes fraction", fontsize=8.5, color=VERDE, va="center",
               arrowprops=dict(arrowstyle="->", color=VERDE, linewidth=0.9, shrinkA=12,
                               shrinkB=2))
anotar(abajo, "la mediana cae entre el 5.\u00ba y el 6.\u00ba;\nla media no cae sobre nadie",
       xy=(5.5, mediana), xytext=(0.04, 0.90), color=MORADO)

titulo(abajo, "Nueve de diez quedan por debajo de la media",
       "la media iguala lo que sobra arriba con lo que falta abajo: no se parece a nadie")
abajo.set_xlabel("puesto que ocupa al ordenar los sueldos (de menor a mayor)")
abajo.set_ylabel("sueldo (euros)")
numeros(abajo, ejes="y")
rejilla(abajo)

guardar(fig, "centralidad-media-fragil-mediana-robusta")
