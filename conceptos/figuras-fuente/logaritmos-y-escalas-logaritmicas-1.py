"""logaritmos-y-escalas-logaritmicas-1.py — que hace de verdad una escala logaritmica.

Arriba, la misma serie de casos (crece multiplicandose) dibujada dos veces: a la izquierda con
el eje en escala lineal, donde los primeros pasos no se ven y el final se lleva todo el alto;
a la derecha con el eje en escala logaritmica, donde la serie sale recta porque multiplicar por
lo mismo siempre ocupa lo mismo. Abajo, la curva de log10: cada vez que x se multiplica por 10,
la altura sube exactamente 1, y en x = 0 la curva no existe y se escapa hacia abajo.
"""

import numpy as np

from comun import *

estilo()

azar = np.random.default_rng(7)

# Crecimiento multiplicativo: cada paso multiplica por algo parecido a 2 (con su ruido).
pasos = np.arange(13)
factores = azar.normal(2.0, 0.12, pasos.size)
casos = np.round(np.cumprod(np.concatenate([[10.0], factores[1:]]))).astype(int)

# El alto del eje logaritmico va de 8 al maximo mas un margen. La mitad VISUAL de ese tramo no
# es la media de los extremos, es su raiz: la escala mide factores, no cantidades.
tope = casos.max() * 1.6
mitad_visual = float(np.sqrt(8.0 * tope))
mitad_aritmetica = float((8.0 + tope) / 2.0)


def millar(v):
    """Numeros grandes con punto de millar, como se escriben en el portal."""
    return "{:,.0f}".format(v).replace(",", ".")

fig = plt.figure(figsize=(10.4, 6.4))
rejilla_paneles = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.05], hspace=0.34)

lineal = fig.add_subplot(rejilla_paneles[0, 0])
logaritmica = fig.add_subplot(rejilla_paneles[0, 1])
curva = fig.add_subplot(rejilla_paneles[1, :])

# --- Arriba izquierda: eje lineal, el primer tramo desaparece -------------------------------
lineal.plot(pasos, casos, color=AZUL, marker="o", markersize=4, linewidth=1.6)
lineal.set_ylim(0, casos.max() * 1.12)
lineal.set_xticks([0, 3, 6, 9, 12])

lineal.annotate("aqu\u00ed los valores son 10, 20 y 40:\npegados al suelo, invisibles",
                xy=(2.0, 40.0), xycoords="data", xytext=(0.06, 0.26),
                textcoords="axes fraction", fontsize=8.5, color=ROJO, va="center",
                arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9, shrinkA=2,
                                shrinkB=4))
lineal.annotate("el \u00faltimo paso se lleva\ncasi todo el alto del eje",
                xy=(11.0, casos[-1] * 0.96), xycoords="data", xytext=(0.40, 0.80),
                textcoords="axes fraction", fontsize=8.5, color=AZUL, va="center",
                arrowprops=dict(arrowstyle="->", color=AZUL, linewidth=0.9, shrinkA=2,
                                shrinkB=6))

titulo(lineal, "Escala lineal: el principio no se ve",
       "la misma serie de casos, con el eje en la escala de todos los d\u00edas")
lineal.set_xlabel("paso (meses desde el primero)")
lineal.set_ylabel("casos acumulados")
numeros(lineal, ejes="y")
rejilla(lineal)

# --- Arriba derecha: la misma serie en escala logaritmica -----------------------------------
logaritmica.plot(pasos, casos, color=VERDE, marker="o", markersize=4, linewidth=1.6)
logaritmica.set_yscale("log")
logaritmica.set_ylim(8, tope)
logaritmica.set_xticks([0, 3, 6, 9, 12])

anotar(logaritmica, "multiplicar por 2 en cada paso\nocupa siempre lo mismo: sale recta",
       xy=(7.0, casos[7]), xytext=(0.05, 0.88), color=VERDE)
logaritmica.annotate("la mitad de este eje es %s,\nno %s" % (millar(mitad_visual), millar(mitad_aritmetica)),
                     xy=(0.0, mitad_visual), xycoords="data", xytext=(0.46, 0.20),
                     textcoords="axes fraction", fontsize=8.5, color=MORADO, va="center",
                     arrowprops=dict(arrowstyle="->", color=MORADO, linewidth=0.9, shrinkA=2,
                                     shrinkB=4))

titulo(logaritmica, "Escala logar\u00edtmica: sale una recta",
       "los mismos casos, con el eje midiendo factores y no cantidades")
logaritmica.set_xlabel("paso (meses desde el primero)")
logaritmica.set_ylabel("casos acumulados (escala log)")
numeros(logaritmica, ejes="y")
rejilla(logaritmica)

# --- Abajo: la curva de log10 y su escalon --------------------------------------------------
x = np.logspace(np.log10(0.05), 3.0, 400)
curva.plot(x, np.log10(x), color=AZUL, linewidth=1.8)
curva.axhline(0.0, color=REJILLA, linewidth=0.9)
curva.axvline(1.0, color=REJILLA, linewidth=0.9)
curva.set_xscale("log")
curva.set_xlim(0.05, 1000)
curva.set_ylim(-1.6, 3.5)
curva.set_xticks([0.1, 1, 10, 100, 1000])
curva.set_yticks([-1, 0, 1, 2, 3])

for valor, altura in ((10.0, 1.0), (100.0, 2.0), (1000.0, 3.0)):
    curva.plot([valor, valor], [0.0, altura], color=NARANJA, linewidth=1.1, linestyle=":")
    curva.plot([valor], [altura], color=NARANJA, marker="o", markersize=5)

curva.annotate("cada x10 sube exactamente 1:\n10 -> 1,  100 -> 2,  1000 -> 3",
               xy=(100.0, 2.0), xycoords="data", xytext=(0.28, 0.74),
               textcoords="axes fraction", fontsize=8.5, color=NARANJA, va="center",
               arrowprops=dict(arrowstyle="->", color=NARANJA, linewidth=0.9, shrinkA=2,
                               shrinkB=6))
curva.annotate("en 0 no existe: la curva se escapa\nhacia abajo sin llegar a tocarlo",
               xy=(0.07, -1.25), xycoords="data", xytext=(0.03, 0.44),
               textcoords="axes fraction", fontsize=8.5, color=ROJO, va="center",
               arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9, shrinkA=2,
                               shrinkB=4))
curva.annotate("y=0 en x=1: el logaritmo de 1 es 0\npara cualquier base",
               xy=(1.0, 0.0), xycoords="data", xytext=(0.44, 0.09),
               textcoords="axes fraction", fontsize=8.5, color=TEXTO, va="center",
               arrowprops=dict(arrowstyle="->", color=TEXTO, linewidth=0.9, shrinkA=2,
                               shrinkB=4))

titulo(curva, "Multiplicar por 10 es subir un escal\u00f3n",
       "log10 de x: la escala convierte productos en sumas, y por eso se lee en factores")
curva.set_xlabel("x (escala logar\u00edtmica)")
curva.set_ylabel("log10 de x")
numeros(curva)
rejilla(curva, eje="both")

guardar(fig, "logaritmos-escala-lineal-y-logaritmica")

print("máximo de la serie: %d   mitad visual del eje: %s   media de los extremos: %s"
      % (casos.max(), millar(mitad_visual), millar(mitad_aritmetica)))
