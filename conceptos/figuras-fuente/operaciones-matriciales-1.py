"""operaciones-matriciales-1.py — el producto de matrices no es conmutativo y exige que la
dimensión interior coincida. Figura de la pagina operaciones-matriciales."""

import numpy as np

from comun import *

estilo()

# Las matrices del ejemplo de la pagina: no se sortea nada, salen siempre igual.
A = np.array([[1.0, 2.0], [3.0, 4.0]])
B = np.array([[0.0, 1.0], [1.0, 0.0]])       # intercambia las coordenadas
AB = A @ B
BA = B @ A

cuadrado = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])


def imagen(M, figuras):
    """Aplica la matriz M a una lista de puntos (cada fila, un punto)."""
    return (M @ figuras.T).T


fig, (izq, der) = plt.subplots(1, 2, figsize=(10.8, 4.4))

# ---------------------------------------- izquierda: el mismo cuadrado, dos destinos
izq.set_aspect("equal")
izq.set_xlim(-1.0, 9.2)
izq.set_ylim(-1.6, 8.4)

izq.fill(cuadrado[:, 0], cuadrado[:, 1], facecolor=REJILLA, alpha=0.35,
         edgecolor=REJILLA, linewidth=1.2, label="cuadrado de partida")
izq.fill(imagen(AB, cuadrado)[:, 0], imagen(AB, cuadrado)[:, 1], facecolor=AZUL,
         alpha=0.18, edgecolor=AZUL, linewidth=1.6, label="A @ B")
izq.fill(imagen(BA, cuadrado)[:, 0], imagen(BA, cuadrado)[:, 1], facecolor=MORADO,
         alpha=0.18, edgecolor=MORADO, linewidth=1.6, label="B @ A")

# Las columnas de cada producto son las imagenes de los dos vectores de la base.
izq.annotate("", xy=AB[:, 0], xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color=AZUL, linewidth=1.6))
izq.annotate("", xy=BA[:, 0], xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color=MORADO, linewidth=1.6))

p = imagen(AB, np.array([[1.0, 1.0]]))[0]
q = imagen(BA, np.array([[1.0, 1.0]]))[0]
izq.plot([1.0], [1.0], marker="o", markersize=6, color=NARANJA)
izq.plot([p[0]], [p[1]], marker="o", markersize=6, color=AZUL)
izq.plot([q[0]], [q[1]], marker="o", markersize=6, color=MORADO)
izq.annotate("el cuadrado de partida", xy=(0.7, 0.7), xytext=(0.3, -1.35),
             fontsize=8.5, color=TEXTO, ha="left",
             arrowprops=dict(arrowstyle="->", color=TEXTO, linewidth=0.9))
izq.annotate("(3, 7)", xy=(p[0], p[1]), xytext=(3.3, 8.0), fontsize=9.5, color=AZUL)
izq.annotate("(7, 3)", xy=(q[0], q[1]), xytext=(7.3, 3.7), fontsize=9.5, color=MORADO)

izq.set_title("En A @ B se aplica primero B; en B @ A, primero A:\n"
              "la esquina (1, 1) viaja a (3, 7) o a (7, 3)", fontsize=10.5)
izq.set_xlabel("Las flechas son las primeras columnas; las dos figuras tienen área 2",
               fontsize=9)
izq.legend(loc="lower right", fontsize=8.5)
numeros(izq)
rejilla(izq, "both")

# ------------------------------------- derecha: la dimension interior tiene que encajar
der.set_xlim(0, 10)
der.set_ylim(-0.1, 7.5)
der.axis("off")
der.set_title("La dimensión interior k se recorre y desaparece", fontsize=10.5)

# A es (m, k): alto m, ancho k.  B es (k, n): alto k, ancho n.
der.fill([0.6, 2.8, 2.8, 0.6], [4.0, 4.0, 5.6, 5.6], facecolor=AZUL, alpha=0.15,
         edgecolor=AZUL, linewidth=1.4)
der.fill([3.4, 4.8, 4.8, 3.4], [3.4, 3.4, 5.6, 5.6], facecolor=MORADO, alpha=0.15,
         edgecolor=MORADO, linewidth=1.4)
der.fill([5.6, 7.0, 7.0, 5.6], [4.0, 4.0, 5.6, 5.6], facecolor=VERDE, alpha=0.15,
         edgecolor=VERDE, linewidth=1.4)

der.text(1.7, 4.8, "A", ha="center", va="center", fontsize=11, color=AZUL)
der.text(4.1, 4.5, "B", ha="center", va="center", fontsize=11, color=MORADO)
der.text(6.3, 4.8, "AB", ha="center", va="center", fontsize=11, color=VERDE)
der.text(3.1, 4.8, "@", ha="center", va="center", fontsize=13, color=TEXTO)
der.text(5.2, 4.8, "=", ha="center", va="center", fontsize=13, color=TEXTO)

# Las dos dimensiones interiores: el ancho de A y el alto de B.
der.plot([0.6, 2.8], [3.85, 3.85], color=NARANJA, linewidth=2.6)
der.plot([3.28, 3.28], [3.4, 5.6], color=NARANJA, linewidth=2.6)
der.text(1.7, 3.5, "k columnas", ha="center", va="center", fontsize=9, color=NARANJA)
der.text(3.05, 2.85, "k filas", ha="center", va="center", fontsize=9, color=NARANJA,
         rotation=90)
der.text(3.2, 6.3, "la k tiene que ser la misma en las dos", ha="center", va="center",
         fontsize=9, color=NARANJA)
der.text(0.45, 4.8, "m", ha="center", va="center", fontsize=9, color=AZUL)
der.text(4.1, 3.05, "n", ha="center", va="center", fontsize=9, color=MORADO)
der.text(6.3, 5.85, "m", ha="center", va="center", fontsize=9, color=VERDE)
der.text(6.3, 3.65, "n", ha="center", va="center", fontsize=9, color=VERDE)

der.text(3.6, 1.75, "Solo quedan las dimensiones exteriores: (m, k) @ (k, n) → (m, n)",
         ha="center", va="center", fontsize=9.5, color=TEXTO)
der.text(3.6, 1.05, "A (2, 3) @ B (3, 2) → (2, 2): encaja", ha="center", va="center",
         fontsize=9.5, color=VERDE)
der.text(3.6, 0.4, "A (2, 3) @ A (2, 3): la interior sería 3 y 2 → el producto no existe",
         ha="center", va="center", fontsize=9.5, color=ROJO)

guardar(fig, "producto-no-conmutativo")
