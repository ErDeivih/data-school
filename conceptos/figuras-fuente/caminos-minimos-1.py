"""caminos-minimos-1.py — Dijkstra cuando los pesos no son negativos y el mismo algoritmo
cuando aparece una arista negativa. Página de caminos mínimos (fase 10)."""

import heapq

import numpy as np

from comun import *

estilo()

# --- Grafo 1, no dirigido y con todos los pesos positivos: el ejemplo de la página.
aristas1 = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 5), (2, 3, 8), (3, 4, 3), (2, 4, 10)]
pos1 = {0: (0.12, 0.50), 2: (0.42, 0.62), 1: (0.36, 0.26), 3: (0.68, 0.28), 4: (0.90, 0.58)}
# Dónde se escribe la distancia de cada vértice, elegido para no pisar ninguna arista ni
# ninguna etiqueta de peso. El 2 lo lleva a la izquierda porque arriba está la nota del empate.
donde1 = {0: (0.12, 0.375), 1: (0.36, 0.135), 2: (0.27, 0.665), 3: (0.68, 0.155), 4: (0.90, 0.695)}

# --- Grafo 2, dirigido y con una arista negativa: 3 -> 1 cuesta -4.
aristas2 = [(0, 1, 3), (0, 2, 1), (2, 3, 2), (3, 1, -4), (1, 4, 5), (3, 4, 7)]
pos2 = {0: (0.10, 0.46), 2: (0.30, 0.66), 3: (0.46, 0.30), 1: (0.74, 0.52), 4: (0.92, 0.26)}


def dijkstra_cierra(n, aristas, origen, dirigido):
    """La versión de libro: cuando un vértice sale de la cola queda CERRADO y no se vuelve a
    mirar. Ese cierre es lo que se apoya en que los pesos no son negativos."""
    adyacencia = {i: [] for i in range(n)}
    for u, v, w in aristas:
        adyacencia[u].append((v, w))
        if not dirigido:
            adyacencia[v].append((u, w))
    dist = [float("inf")] * n
    cerrado = [False] * n
    dist[origen] = 0.0
    cola = [(0.0, origen)]
    while cola:
        d, u = heapq.heappop(cola)
        if cerrado[u]:
            continue                     # entrada vieja de un vértice ya cerrado
        cerrado[u] = True
        for v, w in adyacencia[u]:
            if not cerrado[v] and d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(cola, (dist[v], v))
    return dist


def bellman_ford(n, aristas, origen):
    """Admite pesos negativos: relaja n-1 veces TODAS las aristas y no cierra nada."""
    dist = [float("inf")] * n
    dist[origen] = 0.0
    for _ in range(n - 1):
        for u, v, w in aristas:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    return dist


dist1 = dijkstra_cierra(5, aristas1, 0, dirigido=False)
dist2_dij = dijkstra_cierra(5, aristas2, 0, dirigido=True)
dist2_real = bellman_ford(5, aristas2, 0)

# Aristas del árbol de caminos mínimos del grafo 1: las que cumplen la igualdad de la
# relajación. Salen cinco, no cuatro, porque el vértice 4 empata por dos rutas distintas.
arbol1 = {frozenset((u, v)) for u, v, w in aristas1
          if abs(dist1[u] + w - dist1[v]) < 1e-9 or abs(dist1[v] + w - dist1[u]) < 1e-9}

ALTO = 0.8          # el eje y mide 0,8 para que un paso en x mida lo mismo en pantalla que en y


def frac(x, y):
    """Pasa coordenadas del dibujo (cuadradas) a fracción de eje, que es lo que usa anotar()."""
    return (x, y / ALTO)


def nodo(eje, p, texto, color=TEXTO):
    eje.scatter(*p, s=760, facecolor="none", edgecolor=color, linewidth=2.4, zorder=4)
    eje.text(p[0], p[1], texto, ha="center", va="center", fontsize=10.5, color=TEXTO, zorder=5)


def peso(eje, a, b, texto, color=NARANJA, desvio=0.035):
    """Etiqueta del peso, apartada de la arista por la perpendicular y siempre hacia arriba."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    largo = float(np.hypot(dx, dy))
    px, py = -dy / largo, dx / largo
    if py < 0:
        px, py = -px, -py
    eje.text((a[0] + b[0]) / 2 + px * desvio, (a[1] + b[1]) / 2 + py * desvio, texto,
             fontsize=8.5, color=color, ha="center", va="center", zorder=6)


def lienzo(eje, corto, sub):
    eje.set_xlim(0, 1)
    eje.set_ylim(0, ALTO)
    eje.axis("off")                               # es un diagrama: ni ejes ni rejilla
    titulo(eje, corto, sub)


fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.6))


# --- Izquierda: el grafo 1 y las distancias mínimas desde el 0. Las aristas azules son las
# del árbol de caminos mínimos; la 0-1 y la 2-3 no lo son.
lienzo(ejes[0], "Con pesos positivos, Dijkstra acierta",
       "aristas azules, el árbol de caminos mínimos desde el vértice 0")
for u, v, w in aristas1:
    en_arbol = frozenset((u, v)) in arbol1
    ejes[0].annotate("", xy=pos1[v], xytext=pos1[u], zorder=1,
                     arrowprops=dict(arrowstyle="-", shrinkA=16, shrinkB=16,
                                     color=AZUL if en_arbol else REJILLA,
                                     linewidth=2.4 if en_arbol else 1.3))
    peso(ejes[0], pos1[u], pos1[v], f"{w}")
for u in pos1:
    nodo(ejes[0], pos1[u], str(u))
    eje_x, eje_y = donde1[u]
    ejes[0].text(eje_x, eje_y, f"d = {dist1[u]:g}", ha="center", va="center",
                 fontsize=8.5, color=ROJO if u == 0 else AZUL, zorder=5)
anotar(ejes[0], "el 1 se cierra en 3, no en 4:\nla ruta 0 → 2 → 1 mejora la arista directa",
       xy=(0.33, 0.23), xytext=frac(0.02, 0.07), color=AZUL)
anotar(ejes[0], "el 4 empata: 0 → 2 → 4 y 0 → 2 → 1 → 3 → 4 cuestan 11",
       xy=pos1[4], xytext=frac(0.99, 0.75), color=TEXTO, flecha=False, align="right")

# --- Derecha: el grafo 2. La arista 3 -> 1 vale -4 y el cierre prematuro de Dijkstra deja el
# resultado por encima del real en dos vértices.
lienzo(ejes[1], "Con una arista negativa, da números falsos",
       "en rojo, el Dijkstra clásico; en verde, el coste real que da Bellman-Ford")
for u, v, w in aristas2:
    negativa = w < 0
    ejes[1].annotate("", xy=pos2[v], xytext=pos2[u], zorder=1,
                     arrowprops=dict(arrowstyle="-|>", shrinkA=16, shrinkB=18,
                                     color=ROJO if negativa else REJILLA,
                                     linewidth=2.6 if negativa else 1.3))
    peso(ejes[1], pos2[u], pos2[v], f"{w:+d}".replace("-", "−") if negativa else f"{w}",
         color=ROJO if negativa else NARANJA,
         desvio={frozenset((0, 1)): 0.075, frozenset((2, 3)): 0.030}.get(frozenset((u, v)), 0.045))
for u in pos2:
    mal = abs(dist2_dij[u] - dist2_real[u]) > 1e-9
    nodo(ejes[1], pos2[u], str(u), color=ROJO if mal else TEXTO)
    if mal:
        # Los dos valores van a la izquierda del vértice: a la derecha está la flecha roja de
        # la arista negativa y la etiqueta del peso.
        dx, dy = (-0.02, -0.08) if u == 1 else (-0.06, -0.08)
        ejes[1].text(pos2[u][0] + dx, pos2[u][1] + dy, f"Dijkstra {dist2_dij[u]:g}",
                     ha="center", va="center", fontsize=8.5, color=ROJO, zorder=5)
        ejes[1].text(pos2[u][0] + dx, pos2[u][1] + dy - 0.065,
                     f"real {dist2_real[u]:g}".replace("-", "−"),
                     ha="center", va="center", fontsize=8.5, color=VERDE, zorder=5)
    else:
        ejes[1].text(pos2[u][0], pos2[u][1] - 0.125, f"{dist2_real[u]:g}", ha="center",
                     va="center", fontsize=8.5, color=TEXTO, zorder=5)
anotar(ejes[1], "el Dijkstra clásico cierra el 1 con la arista directa (3)\ny ya no vuelve: el atajo 0 → 2 → 3 → 1 cuesta 1 + 2 − 4 = −1",
       xy=(0.60, 0.41), xytext=frac(0.02, 0.76), color=ROJO, flecha=False)

guardar(fig, "caminos-minimos-dijkstra-y-negativos")
