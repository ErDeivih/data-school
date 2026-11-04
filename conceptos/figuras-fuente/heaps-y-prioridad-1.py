"""heaps-y-prioridad-1.py — un montículo es un árbol guardado en un array.

Arriba a la izquierda: el árbol y su array. Los hijos de la posición i viven en 2i+1 y 2i+2,
así que no hacen falta punteros ni nodos: el máximo siempre está en la posición 0.
Arriba a la derecha: el mismo montículo como array, con los huecos que ocupa.
Abajo a la izquierda: la bajada de un elemento (sift-down) paso a paso, con las comparaciones
que cuesta: tres para un montículo de ocho elementos.
Abajo a la derecha: lo que cuesta sacar los k mejores de n elementos: con un montículo de
tamaño k, n log k; ordenando todo primero, n log n.
La figura de la página de montículos y colas de prioridad (fase 10).
"""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(2, 2, figsize=(11.0, 7.6))

MONTICULO = [92, 71, 88, 40, 63, 75, 30, 22]
NIVELES = [[0], [1, 2], [3, 4, 5, 6], [7]]


def posiciones(niveles=NIVELES, ancho=8.0):
    """Sitúa cada índice del montículo en su nivel: la raíz arriba y los hijos debajo."""
    pos = {}
    for nivel, indices in enumerate(niveles):
        paso = ancho / (len(indices) + 1)
        for j, i in enumerate(indices):
            pos[i] = ((j + 1) * paso, -nivel)
    return pos


def bajar(valores, raiz):
    """Sustituye la raíz y la hunde hasta su sitio. Devuelve las fotos de cada paso."""
    estado = valores[:]
    estado[raiz] = estado[-1]
    estado[-1] = None
    fotos = [(estado[:], None)]
    i = raiz
    while True:
        hijos = [h for h in (2 * i + 1, 2 * i + 2)
                 if h < len(estado) and estado[h] is not None]
        if not hijos:
            break
        mayor = max(hijos, key=lambda h: estado[h])
        if estado[mayor] <= estado[i]:
            break
        estado[i], estado[mayor] = estado[mayor], estado[i]
        i = mayor
        fotos.append((estado[:], i))
    return fotos


# --- Arriba a la izquierda: el árbol con los índices -----------------------------
ax = ejes[0, 0]
pos = posiciones()
for i in range(len(MONTICULO)):
    for hijo in (2 * i + 1, 2 * i + 2):
        if hijo < len(MONTICULO):
            ax.plot([pos[i][0], pos[hijo][0]], [pos[i][1], pos[hijo][1]], color=REJILLA,
                    linewidth=1.1, zorder=1)
for i, valor in enumerate(MONTICULO):
    x, y = pos[i]
    ax.scatter([x], [y], s=300, color=ROJO if i == 0 else AZUL, zorder=3)
    ax.text(x, y, str(valor), ha="center", va="center", color="white", fontsize=8.5, zorder=4)
    ax.text(x, y - 0.28, f"i={i}", ha="center", va="top", fontsize=7, color=REJILLA)
anotar(ax, "el 92 vive en la posición 0 porque es el máximo,\nno porque el array esté ordenado",
       xy=(pos[0][0], pos[0][1]), xytext=(0.02, 0.88), color=ROJO)
titulo(ax, "La raíz es el máximo, siempre",
       "un montículo de ocho elementos, con el índice de cada posición")
ax.set_axis_off()
ax.set_xlim(-0.4, 8.6)
ax.set_ylim(-3.9, 1.3)

# --- Arriba a la derecha: el mismo montículo como array --------------------------
ax = ejes[0, 1]
for i, valor in enumerate(MONTICULO):
    color = ROJO if i == 0 else AZUL
    ax.add_patch(plt.Rectangle((i, 0), 0.9, 0.8, color=color, alpha=0.9))
    ax.text(i + 0.45, 0.4, str(valor), ha="center", va="center", color="white", fontsize=9.5)
    ax.text(i + 0.45, -0.12, f"{i}", ha="center", va="top", fontsize=8, color=TEXTO)
ax.annotate("", xy=(1.45, 1.05), xytext=(0.45, 1.05),
            arrowprops=dict(arrowstyle="<->", color=VERDE, linewidth=1.3))
ax.text(0.95, 1.13, "hijos de i=0", ha="center", fontsize=8, color=VERDE)
anotar(ax, "los hijos de la posición i están en 2i+1 y 2i+2:\nno hay punteros ni nodos que recorrer",
       xy=(-0.30, 0.25), xytext=(0.02, 0.02), color=TEXTO)
titulo(ax, "Y el array es el árbol",
       "ocho posiciones contiguas: cero memoria para enlazar nodos")
ax.set_axis_off()
ax.set_xlim(-0.4, 8.6)
ax.set_ylim(-0.9, 1.9)

# --- Abajo a la izquierda: la bajada del elemento --------------------------------
ax = ejes[1, 0]
fotos = bajar(MONTICULO, 0)
bajando = [foto[1] for foto in fotos if foto[1] is not None]
camino = [pos[0]] + [pos[i] for i in bajando]
ax.plot([p[0] for p in camino], [p[1] for p in camino], color=MORADO, linewidth=2.4,
        linestyle="--", zorder=2)
for i in range(len(MONTICULO)):
    for hijo in (2 * i + 1, 2 * i + 2):
        if hijo < len(MONTICULO):
            ax.plot([pos[i][0], pos[hijo][0]], [pos[i][1], pos[hijo][1]], color=REJILLA,
                    linewidth=1.0, zorder=1)
for i, valor in enumerate(MONTICULO):
    x, y = pos[i]
    ax.scatter([x], [y], s=300, color=MORADO if i in camino else REJILLA, zorder=3)
    ax.text(x, y, str(valor), ha="center", va="center", color="white", fontsize=8.5, zorder=4)
# El valor que baja es el último del array: en cada paso se compara con sus dos hijos.
ax.scatter([pos[0][0]], [pos[0][1]], s=300, color=NARANJA, zorder=5)
ax.text(pos[0][0], pos[0][1], "22", ha="center", va="center", color="white", fontsize=8.5,
        zorder=6)
anotar(ax, "el 22 sube a la raíz y se hunde por el camino\nlargo: tres comparaciones dobles",
       xy=(pos[7][0], pos[7][1]), xytext=(0.30, 0.90), color=NARANJA)
titulo(ax, "Bajar un elemento cuesta log2(n)",
       "extraer el máximo: el último pasa arriba y baja hasta su sitio")
ax.set_axis_off()
ax.set_xlim(-0.4, 8.6)
ax.set_ylim(-3.9, 1.5)

# --- Abajo a la derecha: los k mejores de n --------------------------------------
ax = ejes[1, 1]
n = np.logspace(3, 7, 200)
for k, color in ((10, VERDE), (100, NARANJA), (1000, ROJO)):
    ax.loglog(n, n * np.log2(k), color=color, linewidth=2.0)
ax.loglog(n, n * np.log2(n), color=AZUL, linewidth=2.0, linestyle="--")
anotar(ax, "ordenar todo y cortar: n log n",
       xy=(1e4, 1.6e5), xytext=(0.22, 0.84), color=AZUL)
anotar(ax, "montículo de tamaño k: n log k,\ncasi lineal cuando k es pequeño",
       xy=(1e6, 6.6e4), xytext=(0.05, 0.90), color=VERDE)
anotar(ax, "con k = 1.000, veinte veces menos trabajo",
       xy=(1e7, 2e8), xytext=(0.05, 0.70), color=ROJO, flecha=False)
titulo(ax, "Los k mejores sin ordenar todo",
       "operaciones para sacar los k mayores de n elementos")
ax.set_xlabel("elementos totales (n)")
ax.set_ylabel("operaciones")
rejilla(ax, eje="both")
numeros(ax)

guardar(fig, "heaps-array-siftdown-y-los-k-mejores")
