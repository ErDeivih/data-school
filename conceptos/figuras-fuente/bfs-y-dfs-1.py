"""bfs-y-dfs-1.py — el mismo grafo recorrido de las dos formas: BFS numera las capas y da
distancias; DFS se hunde por la primera rama. Página de recorridos BFS y DFS (fase 10)."""

from collections import deque

import numpy as np

from comun import *

estilo()

# El grafo del ejemplo de la página: 7 vértices, 7 aristas y un ciclo (2-4-5-2).
aristas = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (6, 7), (4, 5)]
grafo = {1: [2, 3], 2: [1, 4, 5], 3: [1, 6], 4: [2, 5], 5: [2, 4], 6: [3, 7], 7: [6]}

# Posiciones escritas a mano: el dibujo tiene que parecerse al árbol de recorridos, no a una
# nube de puntos. Los dos paneles usan las mismas, para poder compararlos de un vistazo.
pos = {1: (0.0, 0.0), 2: (-1.6, -1.0), 3: (1.6, -1.0),
       4: (-2.3, -2.1), 5: (-0.9, -2.2), 6: (1.6, -2.1), 7: (2.7, -3.0)}


def bfs(grafo, inicio):
    """Orden de visita y distancias en aristas. Marca al encolar, no al desencolar."""
    visitado, cola, orden, dist = {inicio}, deque([inicio]), [], {inicio: 0}
    while cola:
        u = cola.popleft()
        orden.append(u)
        for v in grafo[u]:
            if v not in visitado:
                visitado.add(v)
                dist[v] = dist[u] + 1
                cola.append(v)
    return orden, dist


def dfs_recursivo(grafo, u, visitado, orden, padre, previo):
    """DFS con recursión, guardando de qué vértice se descubrió cada uno."""
    visitado.add(u)
    orden.append(u)
    padre[u] = previo
    for v in grafo[u]:
        if v not in visitado:
            dfs_recursivo(grafo, v, visitado, orden, padre, u)


orden_bfs, dist = bfs(grafo, 1)

visitado, orden_dfs, padre_dfs = set(), [], {}
dfs_recursivo(grafo, 1, visitado, orden_dfs, padre_dfs, None)

# Aristas del árbol de cada recorrido: las que descubren un vértice. El árbol NO es el mismo:
# BFS llega al 5 desde el 2 y DFS desde el 4, así que la arista que sobra cambia de panel.
arbol_bfs = {frozenset((v, p)) for v, p in {2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 6}.items()}
arbol_dfs = {frozenset((v, p)) for v, p in padre_dfs.items() if p is not None}

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.6))
colores_capa = [ROJO, AZUL, VERDE, NARANJA]


def dibujar(eje, arbol, corto, sub):
    """Pinta las aristas: gruesas las del árbol del recorrido, punteadas las descartadas.

    Las líneas se recortan en los dos extremos (shrink) para que no atraviesen el interior de
    los círculos: si pasaran por debajo, el número del vértice quedaría ilegible."""
    for u, v in aristas:
        del_arbol = frozenset((u, v)) in arbol
        eje.annotate("", xy=pos[v], xytext=pos[u], zorder=1,
                     arrowprops=dict(arrowstyle="-", shrinkA=17, shrinkB=17,
                                     color=TEXTO if del_arbol else REJILLA,
                                     linewidth=2.3 if del_arbol else 1.3,
                                     linestyle="-" if del_arbol else "--"))
    eje.set_xlim(-3.5, 3.9)
    eje.set_ylim(-3.8, 1.0)
    eje.axis("off")                              # es un diagrama: ni ejes ni rejilla
    titulo(eje, corto, sub)


# --- Izquierda: BFS. El número de capa es la distancia mínima en aristas: rojo el origen,
# azul los de un salto, verde los de dos y naranja el de tres.
dibujar(ejes[0], arbol_bfs, "BFS explora por capas y mide distancias",
        "el aro se colorea por capa; «d» es la distancia mínima al vértice 1, en aristas")
for u in grafo:
    capa = dist[u]
    ejes[0].scatter(*pos[u], s=900, facecolor="none", edgecolor=colores_capa[capa],
                    linewidth=2.4, zorder=3)
    ejes[0].text(pos[u][0], pos[u][1] + 0.07, str(u), ha="center", va="center", fontsize=10.5,
                 color=TEXTO, zorder=4)
    ejes[0].text(pos[u][0], pos[u][1] - 0.17, f"d = {capa}", ha="center", va="center",
                 fontsize=7.5, color=colores_capa[capa], zorder=4)
anotar(ejes[0], f"orden de visita: {' → '.join(map(str, orden_bfs))}\nel 3 sale tercero: está a un salto",
       xy=pos[3], xytext=(0.02, 0.93), color=AZUL, flecha=False)
anotar(ejes[0], "la arista 4–5 sobra: BFS ya había\nllegado a los dos desde el 2",
       xy=(-1.6, -2.15), xytext=(0.03, 0.10), color=TEXTO)

# --- Derecha: DFS. Mismo grafo, mismo orden de vecinos, y sin embargo otro orden de visita:
# se hunde en 2-4-5 antes de mirar el 3.
dibujar(ejes[1], arbol_dfs, "DFS se hunde: la rama manda sobre la capa",
        "el número con º es el orden en que DFS entra en cada vértice")
for u in grafo:
    ejes[1].scatter(*pos[u], s=900, facecolor="none", edgecolor=MORADO, linewidth=2.4, zorder=3)
    ejes[1].text(pos[u][0], pos[u][1] + 0.07, str(u), ha="center", va="center", fontsize=10.5,
                 color=TEXTO, zorder=4)
    ejes[1].text(pos[u][0], pos[u][1] - 0.17, f"{orden_dfs.index(u) + 1}º", ha="center",
                 va="center", fontsize=7.5, color=MORADO, zorder=4)
anotar(ejes[1], f"orden de visita: {' → '.join(map(str, orden_dfs))}\nel 3 es el quinto: antes gastó la rama 2-4-5",
       xy=pos[3], xytext=(0.02, 0.93), color=MORADO, flecha=False)
anotar(ejes[1], "aquí la que sobra es la 2–5:\nel 5 entró por el 4, no por el 2",
       xy=(-1.25, -1.6), xytext=(0.30, 0.06), color=TEXTO)

guardar(fig, "bfs-y-dfs-capas-y-ramas")
