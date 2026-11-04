"""indices-y-busqueda-en-texto-1.py — por qué BM25 ordena mejor que contar apariciones.

Izquierda: cuánto aporta repetir el término, con el factor f·(k₁+1)/(f + k₁·normalización).
Crece rápido al principio y se aplana en un techo: con k₁ = 1,2 ese techo es 2,2, así que
pasar de 1 a 20 apariciones no multiplica la puntuación por 20.
Derecha: el ejemplo de la página. El documento que repite «gato» dos veces gana al breve
mientras es corto, pero la normalización por longitud lo hunde: a partir de 14 tokens el
documento breve (que lo menciona una sola vez) pasa por delante.
La figura de la página de índices y búsqueda en texto (fase 10).

Los dos paneles salen de la fórmula de BM25 y del ejemplo de la página, no de una
simulación: por eso no hay semilla aleatoria que fijar.
"""

import math

import numpy as np

from comun import *

estilo()

K1, B = 1.2, 0.75          # valores habituales: el 1,2 del ejemplo y el 0,75 de la página
L_MEDIA = 6.0              # longitud media de los tres documentos del ejemplo
N, DF = 3, 2               # 3 documentos, «gato» aparece en 2: IDF(gato) = 0,4700
IDF = math.log(1 + (N - DF + 0.5) / (DF + 0.5))


def num(x, dec=2):
    """Números con coma decimal, como se escriben en el portal."""
    return ("%.*f" % (dec, x)).replace(".", ",")


fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.4))

# --- Izquierda: la saturación de la frecuencia ---------------------------------------
f = np.linspace(0.0, 25.0, 500)
ax = ejes[0]
for k1, color in [(0.5, NARANJA), (1.2, AZUL), (2.0, VERDE)]:
    ax.plot(f, f * (k1 + 1) / (f + k1), color=color, linewidth=1.9,
            label="k₁ = " + num(k1, 1))
    # El techo no se alcanza nunca: es la asíntota, y se dibuja para verlo.
    ax.axhline(k1 + 1, color=color, linewidth=0.9, linestyle=":", alpha=0.65)
ax.set_ylim(0.0, 3.4)
anotar(ax, "el techo es k₁ + 1: con k₁ = 1,2 repetir 20 veces\nda {} frente al 1,00 de repetir una"
       .format(num(20 * (K1 + 1) / (20 + K1))),
       xy=(20.0, 20 * (K1 + 1) / (20 + K1)), xytext=(0.28, 0.30), color=AZUL)
anotar(ax, "de 1 a 2 apariciones se gana un {} %;\nde 20 a 21, un {} %"
       .format(num(100 * ((2 * (K1 + 1) / (2 + K1)) / 1.0 - 1), 0),
               num(100 * ((21 * (K1 + 1) / (21 + K1)) / (20 * (K1 + 1) / (20 + K1)) - 1), 1)),
       xy=(2.0, 2 * (K1 + 1) / (2 + K1)), xytext=(0.12, 0.10), color=VERDE)
titulo(ax, "La frecuencia se satura: tiene techo",
       "lo que aporta repetir el término, con un documento de longitud media")
ax.set_xlabel("f: veces que aparece el término en el documento")
ax.set_ylabel("factor de frecuencia")
ax.legend(loc="lower right", fontsize=8)
rejilla(ax)
numeros(ax)

# --- Derecha: el documento largo pierde aunque repita el término ---------------------
largos = np.linspace(3.0, 30.0, 500)


def bm25(f_t, largo, k1=K1, b=B):
    """Puntuación BM25 de un término, con el IDF del ejemplo de la página."""
    return IDF * (f_t * (k1 + 1)) / (f_t + k1 * (1 - b + b * largo / L_MEDIA))


breve = bm25(1, 6.0)                      # d3: «gato» una vez en 6 tokens
repite = bm25(2, largos)                  # d1: «gato» dos veces, con la longitud variando
cruce = float(largos[np.argmin(np.abs(repite - breve))])

ax = ejes[1]
ax.axhline(breve, color=VERDE, linewidth=1.9)
ax.plot(largos, repite, color=AZUL, linewidth=2.0)
ax.axvline(cruce, color=REJILLA, linewidth=1.1, linestyle=":")
ax.scatter([6.0, 8.0], [bm25(1, 6.0), bm25(2, 8.0)], s=28, color=TEXTO, zorder=5)
ax.set_ylim(0.10, 0.85)
anotar(ax, "el documento que repite «gato» dos veces:\n{} con 8 tokens, {} si tiene 20"
       .format(num(bm25(2, 8.0), 3), num(bm25(2, 20.0), 3)),
       xy=(8.0, bm25(2, 8.0)), xytext=(0.03, 0.94), color=AZUL)
anotar(ax, "el breve, con «gato» una vez y 6 tokens: {}".format(num(breve, 3)),
       xy=(28.0, breve), xytext=(0.97, 0.60), color=VERDE, align="right")
anotar(ax, "a partir de {} tokens el largo pierde".format(num(cruce, 0)),
       xy=(cruce, bm25(1, 6.0) * 0.55), xytext=(0.42, 0.12), color=TEXTO)
titulo(ax, "Un documento largo pierde aunque repita",
       "puntuación BM25 de «gato» frente a la longitud del documento, con b = " + num(B, 2))
ax.set_xlabel("tokens del documento")
ax.set_ylabel("puntuación BM25 de «gato»")
rejilla(ax)
numeros(ax)

guardar(fig, "bm25-saturacion-y-longitud")
