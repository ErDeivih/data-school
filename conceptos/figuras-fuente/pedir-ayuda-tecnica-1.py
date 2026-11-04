"""pedir-ayuda-tecnica-1.py — como se reduce un script al ejemplo mínimo.

Dos formas de recortar 5.000 líneas hasta las 3 que reproducen el fallo: quitando una
línea cada vez (4.997 intentos) o partiendo el ejemplo por la mitad y quedándote con la
mitad que sigue fallando (11 cortes). Es la misma diferencia que hay entre buscar una
palabra en un diccionario página a página y por bisección.
"""

import numpy as np

from comun import *

estilo()

original = 5000          # líneas del script que falla
objetivo = 3             # líneas del ejemplo mínimo que todavía falla
cortes = np.arange(0, 13)

por_mitades = original / 2.0 ** cortes          # cada corte tira la mitad que no falla
de_una_en_una = np.maximum(original - cortes, 0)  # una línea por intento

fig, ax = plt.subplots(figsize=(8.2, 4.4))
ax.set_yscale("log")

ax.plot(cortes, de_una_en_una, color=NARANJA, marker="o", markersize=4, linewidth=1.4,
        label="quitando una línea cada vez")
ax.plot(cortes, por_mitades, color=AZUL, marker="o", markersize=4, linewidth=1.6,
        label="partiendo el ejemplo por la mitad")
ax.axhline(objetivo, color=VERDE, linewidth=1.2, linestyle="--")

ax.set_xlim(-0.3, 12.3)
ax.set_ylim(1, 9000)
ax.set_xticks(cortes)
ax.set_xlabel("cortes hechos al ejemplo")
ax.set_ylabel("líneas que quedan (escala logarítmica)")
ax.legend(loc="center right")

anotar(ax, "11 cortes y quedan 3 líneas:\nel fallo sigue reproduciéndose",
       xy=(11, por_mitades[11]), xytext=(0.06, 0.24), color=AZUL)
anotar(ax, "de una en una harían falta 4.997",
       xy=(12, de_una_en_una[12]), xytext=(0.42, 0.80), color=NARANJA)

titulo(ax, "El ejemplo mínimo se busca por mitades",
       "partir por la mitad cuesta 11 intentos; recortar de línea en línea, 4.997")
numeros(ax)
rejilla(ax)

guardar(fig, "pedir-ayuda-recortar-por-mitades")
