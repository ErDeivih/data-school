"""arboles-binarios-1.py — el orden de inserción decide la forma, y la forma decide el coste.

Izquierda: lo que cuesta encontrar una clave. En un árbol equilibrado el coste crece como
log2(n); si las claves entran ya ordenadas, el árbol degenera en una lista y el coste pasa a
ser la mitad de n. Con un millón de claves, veinte comparaciones contra quinientas mil.
Derecha: los dos árboles dibujados con las mismas siete claves. Uno mide 3 niveles; el otro,
6, y buscar la última cuesta siete comparaciones. El recorrido in-order devuelve las claves
ordenadas en los dos casos: la forma cambia, el orden no.
La figura de la página de árboles binarios (fase 10).
"""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(11.2, 4.8))


class Nodo:
    """Nodo mínimo de un árbol de búsqueda binario: clave y los dos subárboles."""

    def __init__(self, clave):
        self.clave = clave
        self.izq = None
        self.der = None


def insertar(raiz, clave):
    if raiz is None:
        return Nodo(clave)
    if clave < raiz.clave:
        raiz.izq = insertar(raiz.izq, clave)
    else:
        raiz.der = insertar(raiz.der, clave)
    return raiz


def in_order(nodo, salida):
    """Recorrido en orden: izquierda, raíz, derecha. Devuelve las claves ordenadas."""
    if nodo is None:
        return
    in_order(nodo.izq, salida)
    salida.append(nodo.clave)
    in_order(nodo.der, salida)


# --- Izquierda: lo que cuesta una búsqueda según la forma del árbol --------------
ax = ejes[0]
n = np.logspace(0.9, 6, 200)
ax.loglog(n, np.log2(n) + 1, color=AZUL, linewidth=2.0)
ax.loglog(n, n / 2, color=ROJO, linewidth=2.0)
anotar(ax, "equilibrado: unos log2(n) pasos\ncon un millón de claves, veinte",
       xy=(1e3, 11.0), xytext=(0.05, 0.13), color=AZUL)
anotar(ax, "degenerado: hay que recorrer media lista\ncon un millón de claves, quinientas mil",
       xy=(3e4, 1.5e4), xytext=(0.10, 0.80), color=ROJO)
anotar(ax, "entre las dos curvas hay 25.000 veces\nde diferencia con un millón de claves",
       xy=(1e6, 6e4), xytext=(0.30, 0.60), color=MORADO, flecha=False)
titulo(ax, "La forma del árbol es el coste de buscar",
       "comparaciones hasta encontrar la clave, en escala doble logarítmica")
ax.set_xlabel("claves guardadas")
ax.set_ylabel("comparaciones")
rejilla(ax, eje="both")
numeros(ax)

# --- Derecha: los dos árboles, con las mismas siete claves -----------------------
ax = ejes[1]
claves = [50, 30, 70, 20, 40, 60, 80]
equilibrado = None
for c in claves:                        # entran desordenadas: 50 primero, la raíz parte el resto
    equilibrado = insertar(equilibrado, c)
degenerado = None
for c in sorted(claves):                # entran ya ordenadas: cada una cuelga de la anterior
    degenerado = insertar(degenerado, c)


def dibujar_arbol(arbol, color, x0, y0, dx):
    """Árbol vertical: la x es el número de orden (in-order) y la y, el nivel."""
    posiciones, contador, niveles = {}, [0], {}

    def recorrer(nodo, nivel):
        if nodo is None:
            return
        recorrer(nodo.izq, nivel + 1)
        posiciones[nodo] = (x0 + contador[0] * dx, y0 - nivel)
        contador[0] += 1
        niveles[nodo] = nivel
        recorrer(nodo.der, nivel + 1)

    recorrer(arbol, 0)
    # La altura es un nivel más que el nivel más bajo: la raíz sola ya mide 1.
    return posiciones, max(niveles.values()) + 1


def dibujar_cadena(arbol, color, x0, y0, dy):
    """Cadena vertical: solo hay hijo derecho, así que baja un escalón por clave."""
    posiciones, nodo, i = {}, arbol, 0
    while nodo is not None:
        posiciones[nodo] = (x0, y0 - i * dy)
        nodo = nodo.der
        i += 1
    # Con i nodos en fila hay i − 1 aristas, y esa es la altura de la cadena.
    return posiciones, i - 1


def pintar(posiciones, color):
    for nodo, (x, y) in posiciones.items():
        for hijo in (nodo.izq, nodo.der):
            if hijo is not None and hijo in posiciones:
                xh, yh = posiciones[hijo]
                ax.plot([x, xh], [y, yh], color=REJILLA, linewidth=1.1, zorder=1)
    for nodo, (x, y) in posiciones.items():
        ax.scatter([x], [y], s=250, color=color, zorder=3)
        ax.text(x, y, str(nodo.clave), ha="center", va="center", color="white", fontsize=7.5,
                zorder=4)


pos_equilibrado, alto_equilibrado = dibujar_arbol(equilibrado, AZUL, 1.6, 0.0, 1.55)
pos_degenerado, alto_degenerado = dibujar_cadena(degenerado, ROJO, 12.0, -1.2, 0.72)
pintar(pos_equilibrado, AZUL)
pintar(pos_degenerado, ROJO)
orden_equilibrado = []
in_order(equilibrado, orden_equilibrado)
orden_degenerado = []
in_order(degenerado, orden_degenerado)
ax.text(5.9, -2.55, f"entran desordenadas: altura {alto_equilibrado}", ha="right",
        fontsize=8.5, color=AZUL)
ax.text(5.9, -3.35, "in-order: " + " ".join(str(c) for c in orden_equilibrado), ha="right",
        fontsize=8.5, color=TEXTO)
ax.text(10.9, -2.55, f"entran ordenadas: altura {alto_degenerado}", ha="right",
        fontsize=8.5, color=ROJO)
ax.text(11.5, -3.35, "in-order: " + " ".join(str(c) for c in orden_degenerado), ha="right",
        fontsize=8.5, color=TEXTO)
anotar(ax, "cada clave cuelga de la anterior:\nes una lista con forma de árbol",
       xy=(12.0, -1.8), xytext=(0.20, 0.06), color=ROJO)
titulo(ax, "El mismo conjunto, dos árboles distintos",
       "siete claves; la forma cambia y el recorrido in-order sale ordenado en los dos casos")
ax.set_axis_off()
ax.set_xlim(-0.4, 13.4)
ax.set_ylim(-7.0, 1.4)

guardar(fig, "arboles-binarios-forma-y-coste")
