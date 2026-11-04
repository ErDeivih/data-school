"""programacion-dinamica-1.py — de dónde sale el ahorro: subproblemas repetidos y una tabla.
La figura de la página de programación dinámica (fase 10).

Izquierda: el árbol de llamadas de fib(5), tal como lo genera la recursión ingenua. Son 15
llamadas para 6 valores distintos: en rojo, los subproblemas que se vuelven a calcular.
Derecha: la tabla de la mochila 0/1 del ejemplo (4 objetos, capacidad 5). Cada celda se
rellena una sola vez desde la de arriba, y el camino rojo reconstruye la solución óptima.
"""

import numpy as np
from matplotlib.patches import Rectangle

from comun import *

estilo()
azar = np.random.default_rng(7)

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.6))

# --- Izquierda: el árbol de llamadas de fib(5) ----------------------------------------
def arbol_fib(n):
    """Árbol de llamadas de la recursión ingenua: (valor, [hijos])."""
    if n < 2:
        return (n, [])
    return (n, [arbol_fib(n - 1), arbol_fib(n - 2)])


arbol = arbol_fib(5)
valores_llamados = []
posiciones = {}
contador_x = [0.0]


def colocar(nodo, profundidad):
    """Coloca cada nodo: las hojas en orden y los padres en el centro de sus hijos."""
    valor, hijos = nodo
    valores_llamados.append(valor)
    if not hijos:
        x = contador_x[0]
        contador_x[0] += 1.0
    else:
        xs = [colocar(h, profundidad + 1) for h in hijos]
        x = sum(xs) / len(xs)
    posiciones[id(nodo)] = (x, -profundidad)
    return x


colocar(arbol, 0)
repeticiones = {v: valores_llamados.count(v) for v in set(valores_llamados)}

ax = ejes[0]
ax.axis("off")


def pintar(nodo):
    valor, hijos = nodo
    x, y = posiciones[id(nodo)]
    for hijo in hijos:
        xh, yh = posiciones[id(hijo)]
        ax.plot([x, xh], [y, yh], color=REJILLA, linewidth=1.1, zorder=1)
    for hijo in hijos:
        pintar(hijo)
    repetido = repeticiones[valor] > 1
    ax.scatter([x], [y], s=430, color=ROJO if repetido else AZUL, alpha=0.14, zorder=2)
    ax.scatter([x], [y], s=430, facecolor="none",
               edgecolor=ROJO if repetido else AZUL, linewidth=1.3, zorder=3)
    ax.text(x, y, f"fib({valor})" if valor > 1 else f"fib({valor})", ha="center", va="center",
            fontsize=7.5, color=ROJO if repetido else AZUL, zorder=4)


pintar(arbol)
ax.plot([], [], marker="o", markersize=9, markerfacecolor="none", markeredgecolor=AZUL,
        linestyle="none", label="valor que se calcula una sola vez")
ax.plot([], [], marker="o", markersize=9, markerfacecolor="none", markeredgecolor=ROJO,
        linestyle="none", label="subproblema repetido")
ax.set_xlim(-0.8, contador_x[0] - 0.2)
ax.set_ylim(-5.6, 1.5)
anotar(ax, f"{len(valores_llamados)} llamadas para {len(repeticiones)} valores distintos:\n"
           f"el resto es trabajo repetido", xy=(0.5, 0.0), xytext=(0.02, 0.94), color=TEXTO,
       flecha=False)
anotar(ax, "fib(2) se recalcula tres veces\nen un problema de cinco", xy=(0.5, 0.0),
       xytext=(0.62, 0.06), color=ROJO, flecha=False)
titulo(ax, "La recursión ingenua repite el mismo cálculo",
       "árbol de llamadas de fib(5): 15 llamadas, 6 subproblemas distintos")
ax.legend(loc="lower left", fontsize=8.5)

# --- Derecha: la tabla de la mochila 0/1 del ejemplo -----------------------------------
pesos, valores, capacidad = [2, 3, 4, 5], [3, 4, 5, 6], 5
n = len(pesos)
F = [[0] * (capacidad + 1) for _ in range(n + 1)]
for i in range(1, n + 1):
    for c in range(capacidad + 1):
        F[i][c] = F[i - 1][c]
        if pesos[i - 1] <= c:
            F[i][c] = max(F[i][c], valores[i - 1] + F[i - 1][c - pesos[i - 1]])

# Reconstrucción hacia atrás: las celdas que decide el camino óptimo.
camino, i, c = [(n, capacidad)], n, capacidad
while i > 0:
    if F[i][c] != F[i - 1][c]:
        c -= pesos[i - 1]
    i -= 1
    camino.append((i, c))

ax = ejes[1]
ax.axis("off")
maximo = max(max(fila) for fila in F)
rotulos = ["ninguno", "A (2, 3)", "B (3, 4)", "C (4, 5)", "D (5, 6)"]
for fila in range(n + 1):
    y = n - fila
    ax.text(-1.35, y + 0.5, rotulos[fila], ha="left", va="center", fontsize=8.5, color=TEXTO)
    for col in range(capacidad + 1):
        valor = F[fila][col]
        ax.add_patch(Rectangle((col, y), 1, 1, edgecolor=REJILLA, linewidth=0.8,
                               facecolor=AZUL, alpha=0.04 + 0.36 * valor / maximo))
        ax.text(col + 0.5, y + 0.5, str(valor), ha="center", va="center", fontsize=9,
                color=TEXTO)
for col in range(capacidad + 1):
    ax.text(col + 0.5, -0.45, f"c = {col}", ha="center", va="center", fontsize=8, color=TEXTO)
# El camino de la reconstrucción: de la esquina óptima hacia arriba, saltando cuando el
# objeto entra en la mochila.
for (f1, c1), (f2, c2) in zip(camino, camino[1:]):
    x1, y1 = c1 + 0.5, n - f1 + 0.5
    x2, y2 = c2 + 0.5, n - f2 + 0.5
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=1.4,
                                shrinkA=13, shrinkB=13), zorder=5)
for f1, c1 in camino:
    ax.add_patch(Rectangle((c1 + 0.06, n - f1 + 0.06), 0.88, 0.88, facecolor="none",
                           edgecolor=ROJO, linewidth=1.8, zorder=6))
anotar(ax, "la esquina de abajo vale 7, y el camino rojo\nhacia arriba dice qué objetos entran: A y B",
       xy=(5.5, 0.5), xytext=(0.02, 0.15), color=ROJO, flecha=False)
anotar(ax, "cada celda se rellena una sola vez mirando la de arriba:\n"
           "24 estados frente a 2⁴ = 16 combinaciones",
       xy=(2.5, 2.5), xytext=(0.02, 0.03), color=AZUL, flecha=False)
titulo(ax, "La tabla rellena cada estado una sola vez",
       "mochila 0/1 del ejemplo: filas, objetos considerados; columnas, capacidad")
ax.set_xlim(-1.6, 6.4)
ax.set_ylim(-2.6, 5.6)

guardar(fig, "programacion-dinamica-arbol-y-tabla")
