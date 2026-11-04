"""pilas-y-colas-1.py — la estructura decide el orden y, de paso, el coste.

Izquierda: vaciar una cola entera. Con una lista y `pop(0)` cada extracción desplaza todo lo
que queda, así que el total crece como n²/2; con un deque son n actualizaciones de puntero.
Derecha: el mismo grafo recorrido con una pila y con una cola. Mismos nodos, mismo número de
pasos, orden de visita opuesto: en profundidad contra por niveles.
La figura de la página de pilas, colas y deques (fase 10).
"""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.6))

# --- Izquierda: vaciar la cola, con lista y con deque ---------------------------
ax = ejes[0]
n = np.logspace(2, 5, 60)
ax.loglog(n, n * (n - 1) / 2, color=ROJO, linewidth=2.0)     # pop(0) sobre una lista
ax.loglog(n, n, color=VERDE, linewidth=2.0)                  # popleft sobre un deque
anotar(ax, "lista con pop(0): O(n²)\ncada extracción mueve los que quedan",
       xy=(5e3, 1.25e7), xytext=(0.42, 0.08), color=ROJO)
anotar(ax, "deque con popleft: O(n)\nsolo se actualiza un puntero",
       xy=(1e5, 1e5), xytext=(0.16, 0.80), color=VERDE)
anotar(ax, "con 10.000 elementos:\n49.995.000 frente a 10.000",
       xy=(1e4, 5e7), xytext=(0.14, 0.38), color=MORADO, flecha=False)
titulo(ax, "Sacar por delante con una lista cuesta n²/2",
       "elementos desplazados al vaciar una cola de n elementos")
ax.set_ylim(60, 3e10)
ax.set_xlabel("elementos en la cola")
ax.set_ylabel("desplazamientos acumulados")
rejilla(ax, eje="both")
numeros(ax)

# --- Derecha: el mismo grafo con pila y con cola --------------------------------
ax = ejes[1]
# Un grafo pequeño y dirigido: las capas ya se ven en el dibujo (A arriba, F abajo).
vecinos = {"A": ["B", "C"], "B": ["D"], "C": ["D", "E"], "D": ["F"], "E": ["F"], "F": []}
pos = {"A": (0.0, 1.30), "B": (-1.30, 0.25), "C": (1.30, 0.25),
       "D": (-1.30, -0.85), "E": (1.30, -0.85), "F": (0.0, -1.85)}


def bfs(inicio):
    """Recorrido por niveles: cola, y el nodo se marca al ENCOLAR, no al desencolar."""
    visitados, cola, orden = {inicio}, [inicio], []
    while cola:
        nodo = cola.pop(0)
        orden.append(nodo)
        for v in vecinos[nodo]:
            if v not in visitados:
                visitados.add(v)
                cola.append(v)
    return orden


def dfs(inicio):
    """Recorrido en profundidad: pila, apilando los vecinos al revés para respetar el orden."""
    visitados, pila, orden = set(), [inicio], []
    while pila:
        nodo = pila.pop()
        if nodo in visitados:
            continue
        visitados.add(nodo)
        orden.append(nodo)
        for v in reversed(vecinos[nodo]):
            if v not in visitados:
                pila.append(v)
    return orden


orden_bfs, orden_dfs = bfs("A"), dfs("A")

# Las aristas primero, para que los nodos queden por encima.
for origen, destinos in vecinos.items():
    for destino in destinos:
        x0, y0 = pos[origen]
        x1, y1 = pos[destino]
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color=REJILLA, linewidth=1.3,
                                    shrinkA=15, shrinkB=15))
for nodo, (x, y) in pos.items():
    # El color dice en qué nivel está: es lo que la cola respeta y la pila no.
    nivel = orden_bfs.index(nodo)
    color = [AZUL, VERDE, NARANJA, MORADO][min(nivel, 3)]
    ax.scatter([x], [y], s=520, color=color, zorder=3, alpha=0.9)
    ax.text(x, y, nodo, ha="center", va="center", color="white", fontsize=11, zorder=4,
            fontweight="bold")
ax.text(-2.05, 1.72, "cola (BFS):  " + " → ".join(orden_bfs), fontsize=9, color=VERDE)
ax.text(-2.05, 1.47, "pila (DFS):  " + " → ".join(orden_dfs), fontsize=9, color=ROJO)
anotar(ax, "la pila baja hasta el fondo antes\nde mirar al siguiente hermano",
       xy=(0.0, -1.85), xytext=(0.06, 0.20), color=ROJO)
titulo(ax, "Cambiar la estructura cambia el orden",
       "el mismo grafo y los mismos seis nodos, visitados de dos maneras")
ax.set_xlim(-2.15, 2.05)
ax.set_ylim(-2.25, 1.95)
ax.set_axis_off()

guardar(fig, "pilas-y-colas-vaciar-y-recorrido")
