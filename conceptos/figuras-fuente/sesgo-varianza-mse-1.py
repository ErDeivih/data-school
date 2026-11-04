"""sesgo-varianza-mse-1.py — el error esperado como suma de sesgo y varianza, y la imagen
del tirador. Figura de la página sesgo-varianza-mse."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

fig = plt.figure(figsize=(7.9, 5.0))
gs = fig.add_gridspec(2, 4, height_ratios=[1.0, 1.45])

# --- Arriba: las cuatro dianas. La cruz roja es la media de los tiros; el centro
#     de la diana es el valor verdadero, que no se ve en los datos.
casos = [
    (0.0, 0.0, 0.22, "Centrado y firme:\nerror pequeño"),
    (0.0, 0.0, 0.60, "Centrado, pero\ntiembla: varianza"),
    (1.45, 0.85, 0.22, "Firme, pero\ndescentrado: sesgo"),
    (1.45, 0.85, 0.60, "Descentrado y\ntembloroso: lo peor"),
]
for j, (dx, dy, desv, texto) in enumerate(casos):
    eje = fig.add_subplot(gs[0, j])
    eje.add_patch(plt.Circle((0, 0), 1.0, fill=False, color=REJILLA, linewidth=1.0))
    eje.add_patch(plt.Circle((0, 0), 0.30, fill=False, color=REJILLA, linewidth=1.0))
    tiros = azar.normal((dx, dy), desv, size=(14, 2))
    eje.scatter(tiros[:, 0], tiros[:, 1], color=AZUL, s=13, zorder=3)
    eje.plot([dx], [dy], marker="+", color=ROJO, markersize=10, markeredgewidth=1.6, zorder=4)
    eje.set_xlim(-3.0, 3.0)
    eje.set_ylim(-3.0, 3.0)
    eje.set_aspect("equal")
    eje.axis("off")
    eje.set_title(texto, fontsize=8)

# --- Abajo: la descomposición medida en el ejemplo de k-NN de la página ------------
eje = fig.add_subplot(gs[1, :])
ks = np.array([1, 5, 20, 60, 200])
sesgo2 = np.array([0.0004, 0.0000, 0.0000, 0.0000, 0.0622])
varianza = np.array([0.0956, 0.0176, 0.0047, 0.0014, 0.0004])
error = sesgo2 + varianza
x = np.arange(ks.size)

eje.bar(x, sesgo2, width=0.6, color=NARANJA, label="sesgo²")
eje.bar(x, varianza, width=0.6, bottom=sesgo2, color=MORADO, label="varianza")
eje.plot(x, 0.09 / ks, color=ROJO, linewidth=1.2, linestyle="--", marker="o", markersize=4,
         label="suelo del ruido σ²/k")
for xi, e in zip(x, error):
    eje.text(xi, e + 0.007, ("%.4f" % e).replace(".", ","), ha="center", fontsize=8)
eje.annotate("el mínimo no está en el más flexible", xy=(3, 0.0014), xytext=(2.45, 0.062),
             color=TEXTO, fontsize=8,
             arrowprops=dict(arrowstyle="->", color=TEXTO, linewidth=0.9))
eje.set_xticks(x, ["k = %d" % k for k in ks])
eje.set_ylabel("error cuadrático medio")
eje.set_ylim(0, 0.145)
titulo(eje, "El mejor modelo no es el más flexible ni el más rígido",
       "en las dianas, la cruz roja es la media de los tiros y el centro es la verdad")
eje.legend(loc="upper center", ncol=3, fontsize=8.5)
rejilla(eje)
numeros(eje, "y")

guardar(fig, "sesgo-varianza-diana-y-descomposición")
