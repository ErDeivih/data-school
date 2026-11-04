"""intervalos-de-confianza-1.py — qué significa exactamente el 95 % y de dónde sale la
anchura del intervalo. Figura de la página intervalos-de-confianza."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(8)      # semilla elegida para que fallen 5 de 100 estudios

media_real, desv, n, estudios = 170.0, 8.0, 20, 100
semiancho = 1.96 * desv / np.sqrt(n)

fig, ejes = plt.subplots(1, 2, figsize=(7.9, 3.9))

# --- Izquierda: 100 estudios, la misma receta, la cobertura como frecuencia --------
eje = ejes[0]
centros = np.array([azar.normal(media_real, desv, size=n).mean() for _ in range(estudios)])
cubre = np.abs(centros - media_real) <= semiancho
eje.vlines(np.arange(estudios), centros - semiancho, centros + semiancho,
           colors=[VERDE if c else ROJO for c in cubre], linewidth=1.7)
eje.axhline(media_real, color=TEXTO, linewidth=1.1, linestyle="--")
eje.set_xlim(-2, estudios + 1)
eje.set_ylim(158, 188)
eje.text(-1, 186, "en rojo, los %d que no cubren μ" % int((~cubre).sum()),
         color=ROJO, fontsize=8, ha="left")
eje.annotate("μ = 170 cm: fijo y desconocido", xy=(99.5, 170.3), xytext=(estudios + 1, 182),
             color=TEXTO, fontsize=8, ha="right",
             arrowprops=dict(arrowstyle="->", color=TEXTO, linewidth=0.9))
titulo(eje, "El 95 % es la frecuencia de acierto de la receta",
       "100 estudios distintos, la misma receta")
eje.set_xlabel("estudio")
eje.set_ylabel("altura media (cm)")
rejilla(eje)
numeros(eje, "y")

# --- Derecha: la anchura va con 1/√n, no con 1/n -----------------------------------
eje = ejes[1]
ns = np.arange(10, 1001)
eje.plot(ns, 2 * 1.96 * desv / np.sqrt(ns), color=AZUL, linewidth=1.9)
for tam, color in ((25, VERDE), (100, NARANJA), (400, MORADO)):
    anchura = 2 * 1.96 * desv / np.sqrt(tam)
    eje.plot([tam], [anchura], marker="o", color=color, markersize=6, zorder=4)
    eje.text(tam + 20, anchura + 0.35, "n = %d: %.1f cm" % (tam, anchura), color=color,
             fontsize=8, ha="left", va="center")
eje.set_xlim(0, 1000)
eje.set_ylim(0, 11)
eje.text(600, 8.4, "el doble de datos solo reduce\nla anchura un 29 %", color=TEXTO, fontsize=8)
eje.annotate("", xy=(400, 1.57), xytext=(100, 3.14),
             arrowprops=dict(arrowstyle="<->", color=TEXTO, linewidth=1.0))
titulo(eje, "La anchura va con 1/√n: la precisión se paga caro",
       "σ = 8 cm: doblar la muestra reduce un 29 %")
eje.set_xlabel("tamaño de la muestra, n")
eje.set_ylabel("anchura del intervalo del 95 % (cm)")
rejilla(eje)
numeros(eje)

guardar(fig, "intervalos-cobertura-y-anchura")
