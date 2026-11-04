"""grafos-computacionales-y-autograd-1.py — el grafo de un cálculo diminuto y lo que pasa
cuando se olvida limpiar el gradiente.

Izquierda: el grafo de y = (x·w + b)² con x = 2, w = 3 y b = 1. Las flechas rojas son la vuelta:
cada nodo multiplica la derivada que le llega por su derivada local, y esa vuelta cuesta una
sola pasada para todos los parámetros.
Derecha: `.grad` es un acumulador. Sin `zero_grad()`, el paso que da el optimizador en el lote
t lleva la suma de los gradientes de los t lotes anteriores y crece sin control.
La figura de la página de grafos computacionales y autograd (fase 7).
"""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.4))

# --- Izquierda: el grafo, recorrido hacia atrás ---------------------------------------
ax = ejes[0]
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")                                   # es un diagrama: ni ejes ni rejilla

# Cada nodo: posición y texto. Azul para las hojas (las entradas) y morado para las operaciones.
nodos = {
    "x": (0.12, 0.84, "x = 2", AZUL),
    "w": (0.12, 0.46, "w = 3", AZUL),
    "b": (0.12, 0.13, "b = 1", AZUL),
    "m": (0.36, 0.65, "m = x·w = 6", MORADO),
    "z": (0.64, 0.42, "z = m + b = 7", MORADO),
    "y": (0.88, 0.42, "y = z² = 49", MORADO),
}
for x0, y0, texto, color in nodos.values():
    ax.text(x0, y0, texto, ha="center", va="center", fontsize=10, color=color,
            bbox=dict(boxstyle="round,pad=0.30", facecolor="none", edgecolor=color, linewidth=1.2))


def derivada(origen, destino, factor, texto_en):
    """Flecha de la vuelta, con la derivada local del nodo que la multiplica."""
    x1, y1 = nodos[origen][0], nodos[origen][1]
    x2, y2 = nodos[destino][0], nodos[destino][1]
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), zorder=1,
                arrowprops=dict(arrowstyle="-|>", color=ROJO, linewidth=1.4, linestyle="--",
                                shrinkA=26, shrinkB=26))
    ax.text(texto_en[0], texto_en[1], factor, fontsize=9, color=ROJO, ha="center", va="center")


derivada("y", "z", "×2z", (0.75, 0.50))
derivada("z", "m", "×1", (0.50, 0.60))
derivada("z", "b", "×1", (0.32, 0.32))
derivada("m", "x", "×w", (0.215, 0.70))
derivada("m", "w", "×x", (0.215, 0.575))

ax.text(0.52, 0.055, "∂y/∂b = ∂y/∂z · 1 = 14      ∂y/∂w = ∂y/∂z · x = 28\n"
                     "∂y/∂x = ∂y/∂z · w = 42", fontsize=8.5, color=TEXTO, ha="center",
        linespacing=1.6)
titulo(ax, "Una pasada hacia atrás da los tres gradientes",
       "cada nodo multiplica por su derivada local, de derecha a izquierda")

# --- Derecha: sin zero_grad el gradiente acumulado crece sin freno ---------------------
ax = ejes[1]
azar = np.random.default_rng(7)
lotes = np.arange(1, 61)
gradiente = 0.5 + 0.2 * azar.normal(size=lotes.size)    # el gradiente de cada lote
acumulado = np.cumsum(gradiente)                        # lo que queda en .grad sin limpiarlo
ax.semilogy(lotes, gradiente, color=AZUL, linewidth=1.6, marker="o", markersize=3.5,
            label="con zero_grad()")
ax.semilogy(lotes, acumulado, color=ROJO, linewidth=1.9, label="sin zero_grad()")
anotar(ax, "sin limpiar, el paso lleva la suma\nde todos los gradientes anteriores",
       xy=(60.0, acumulado[-1]), xytext=(0.34, 0.86), color=ROJO)
anotar(ax, "limpiando, el paso mide siempre\nlo que mide el lote actual",
       xy=(36.0, gradiente[35]), xytext=(0.06, 0.06), color=AZUL)
titulo(ax, "El gradiente se acumula si nadie lo limpia",
       "norma del gradiente que usa el optimizador en cada lote")
ax.set_xlabel("lote")
ax.set_ylabel("norma del gradiente")
ax.set_ylim(1e-2, 1e3)
ax.legend(loc="upper left")
rejilla(ax)
numeros(ax, ejes="x")

guardar(fig, "grafos-computacionales-y-autograd-grafo-y-acumulación")
