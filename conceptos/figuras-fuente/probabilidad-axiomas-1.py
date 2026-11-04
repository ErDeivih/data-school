"""probabilidad-axiomas-1.py — la regla de la suma: sumar sin restar la intersección cuenta
dos veces a quien esta en los dos. Figura de la pagina de los axiomas de probabilidad.

Los dos sucesos se construyen con las proporciones exactas del ejemplo de la pagina
(P(E) = 0,50, P(P) = 0,40, P(E y P) = 0,20), no con números aleatorios.
"""

import numpy as np

from comun import *

estilo()
# Suceso E: aprueba Estadistica, por columnas (5 de 10). Suceso P: aprueba Programacion,
# por filas (4 de 10). La esquina comun son 2 x 2 = 20 de las 100 celdas.
E = np.zeros((10, 10), dtype=bool)
E[:, :5] = True
P = np.zeros((10, 10), dtype=bool)
P[:4, :] = True

p_E = float(E.mean())
p_P = float(P.mean())
p_interseccion = float((E & P).mean())
p_union = float((E | P).mean())
suma_ingenua = p_E + p_P

# Cada region con su color propio, para que el solape se vea oscuro y no se confunda.
color_solo_E = (0.145, 0.388, 0.921)      # azul
color_solo_P = (0.851, 0.467, 0.024)      # naranja
color_ambos = (0.022, 0.588, 0.412)       # verde
color_ninguno = (0.78, 0.80, 0.83)        # gris claro
lienzo = np.ones((10, 10, 3))
lienzo[E & ~P] = color_solo_E
lienzo[P & ~E] = color_solo_P
lienzo[E & P] = color_ambos
lienzo[~E & ~P] = color_ninguno

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.3))

# --- Panel 1: los dos sucesos como conjuntos de casos, a escala.
ejes[0].imshow(lienzo, extent=(0, 10, 0, 10))
for k in range(11):
    ejes[0].plot([0, 10], [k, k], color=TEXTO, linewidth=0.4, alpha=0.5)
    ejes[0].plot([k, k], [0, 10], color=TEXTO, linewidth=0.4, alpha=0.5)
ejes[0].set_xticks([])
ejes[0].set_yticks([])
for sp in ejes[0].spines.values():
    sp.set_visible(True)
    sp.set_color(TEXTO)
ejes[0].annotate("0,20 en los dos", xy=(0.35, 2.0), color="white", fontsize=9)
ejes[0].annotate("0,30 solo E", xy=(6.0, 4.6), color=AZUL, fontsize=9)
ejes[0].annotate("0,20 solo P", xy=(0.35, 7.6), color=NARANJA, fontsize=9)
ejes[0].annotate("0,30 en ninguno", xy=(6.0, 9.3), color=TEXTO, fontsize=9)
ejes[0].annotate("cada celda pesa 0,01 y las 100 suman 1", xy=(0.1, 10.4), color=TEXTO,
                 fontsize=8.5)
ejes[0].set_title("P(E) = 0,50 y P(P) = 0,40, celda a celda")

# --- Panel 2: el error de sumar sin mirar el solape.
ejes[1].barh([1.0], [suma_ingenua], height=0.42, color=ROJO, alpha=0.22)
ejes[1].barh([1.0], [suma_ingenua], height=0.42, color=ROJO, fill=False, linewidth=2.0)
ejes[1].barh([0.0], [p_union], height=0.42, color=VERDE, alpha=0.22)
ejes[1].barh([0.0], [p_union], height=0.42, color=VERDE, fill=False, linewidth=2.0)
ejes[1].annotate("sumar sin restar", xy=(-0.44, 1.0), color=ROJO, fontsize=9.5, va="center")
ejes[1].annotate("regla de la suma", xy=(-0.44, 0.0), color=VERDE, fontsize=9.5, va="center")
ejes[1].annotate(coma(round(suma_ingenua, 2)) + " = 0,50 + 0,40", xy=(0.95, 1.0),
                 color=ROJO, fontsize=9, va="center", ha="right")
ejes[1].annotate(coma(round(p_union, 2)) + "  = 0,50 + 0,40 - 0,20", xy=(p_union + 0.03, 0.0),
                 color=VERDE, fontsize=9, va="center")
ejes[1].axvline(1.0, color=TEXTO, linewidth=1.0, linestyle=":")
ejes[1].annotate("1: el techo de\ncualquier probabilidad", xy=(1.02, -0.55), color=TEXTO,
                 fontsize=8.5)
ejes[1].annotate("la diferencia, 0,20, es justo la\nintersección contada dos veces",
                 xy=(0.0, -1.0), color=TEXTO, fontsize=8.5)
ejes[1].set_yticks([])
ejes[1].set_xlim(-0.5, 1.6)
ejes[1].set_ylim(-1.35, 1.5)
ejes[1].set_xlabel("probabilidad")
ejes[1].set_title("La intersección se estaba contando dos veces")
rejilla(ejes[1], "x")
numeros(ejes[1], "x")

guardar(fig, "axiomas-suma-con-solape")
