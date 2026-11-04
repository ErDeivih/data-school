"""funciones-y-modulos-1.py - por qué un argumento por defecto mutable se comparte entre
llamadas y que cambia al usar None. La figura de la pagina de funciones y modulos (fase 3)."""

import numpy as np

from comun import *

estilo()
fig, ax = plt.subplots(figsize=(7.6, 4.4))

llamadas = np.arange(1, 9)


def acumula_trampa(x, caja=[]):
    """El [] se crea una sola vez, al definir la función."""
    caja.append(x)
    return caja


def acumula_bien(x, caja=None):
    """La caja se crea nueva en cada llamada que no la recibe."""
    if caja is None:
        caja = []
    caja.append(x)
    return caja


largo_trampa = [len(acumula_trampa(1)) for _ in llamadas]
largo_bien = [len(acumula_bien(1)) for _ in llamadas]

ax.plot(llamadas, largo_trampa, color=ROJO, linewidth=2.0, marker="o", markersize=4)
ax.plot(llamadas, largo_bien, color=VERDE, linewidth=2.0, marker="o", markersize=4)
titulo(ax, "El defecto mutable se comparte entre llamadas",
       "la caja con [] se creó una sola vez; la de None, en cada llamada")
ax.set_xlabel("número de llamada a la función")
ax.set_ylabel("elementos que devuelve la función")
ax.set_xlim(0.4, 8.6)
ax.set_ylim(0, 9.8)
# La roja se explica arriba a la izquierda, por encima de su recta; la verde, en el hueco de
# abajo a la derecha, que queda libre porque su recta va pegada al uno.
ax.text(0.04, 0.93, "caja=[]: la misma lista en todas las llamadas",
        transform=ax.transAxes, color=ROJO, fontsize=9, va="center", ha="left")
ax.annotate("", xy=(5, 5.75), xytext=(4.6, 8.5), textcoords="data",
            arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9))
ax.text(0.40, 0.30, "caja=None: una lista nueva cada vez",
        transform=ax.transAxes, color=VERDE, fontsize=9, va="center", ha="left")
ax.annotate("", xy=(6, 1.55), xytext=(5.6, 3.72), textcoords="data",
            arrowprops=dict(arrowstyle="->", color=VERDE, linewidth=0.9))
rejilla(ax)
numeros(ax)
guardar(fig, "funciones-y-modulos-defecto-mutable")
