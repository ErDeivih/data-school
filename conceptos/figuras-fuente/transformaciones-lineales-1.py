"""transformaciones-lineales-1.py — una matriz es una acción sobre el espacio: las columnas
son las imágenes de la base. Figura de la pagina transformaciones-lineales."""

import numpy as np

from comun import *

estilo()

# Las matrices del ejemplo de la pagina.
R = np.array([[0.0, -1.0], [1.0, 0.0]])     # rotar 90 grados
S = np.array([[2.0, 0.0], [0.0, 3.0]])      # estirar cada eje de otra manera
H = np.array([[1.0, 1.0], [0.0, 1.0]])      # cizallar
P = np.array([[1.0, 0.0], [0.0, 0.0]])      # proyectar sobre el eje x

cuadrado = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])

fig, ejes = plt.subplots(2, 2, figsize=(8.4, 7.4))


def pintar(ax, M, titulo):
    """Dibuja el cuadrado de partida, su imagen por M y las imagenes de la base."""
    ax.set_aspect("equal")
    ax.set_xlim(-1.8, 2.8)
    ax.set_ylim(-1.8, 3.6)
    ax.fill(cuadrado[:, 0], cuadrado[:, 1], facecolor=REJILLA, alpha=0.35,
            edgecolor=REJILLA, linewidth=1.1)
    im = (M @ cuadrado.T).T
    ax.fill(im[:, 0], im[:, 1], facecolor=CIAN, alpha=0.20, edgecolor=CIAN,
            linewidth=1.7)
    ax.annotate("", xy=M[:, 0], xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color=AZUL, linewidth=1.9))
    ax.annotate("", xy=M[:, 1], xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=1.9))
    ax.set_title(titulo, fontsize=9.5)
    numeros(ax)
    rejilla(ax, "both")


pintar(ejes[0, 0], R, "Rotar: gira sin estirar y sin cambiar el área\n"
                      "det = 1. La columna 1 (azul) es T(e₁); la roja, T(e₂)")
ejes[0, 0].text(0.12, 1.15, "T(e₁)", fontsize=8.5, color=AZUL)
ejes[0, 0].text(-1.65, 0.12, "T(e₂)", fontsize=8.5, color=ROJO)
ejes[0, 0].text(-1.7, -1.5, "el cuadrado gris de partida (0, 0) a (1, 1)",
                fontsize=8.5, color=TEXTO)

pintar(ejes[0, 1], S, "Escalar: cada eje por su cuenta, y el orden importa\n"
                      "det = 2 · 3 = 6: las áreas se multiplican por 6")
ejes[0, 1].text(2.05, -0.75, "S(R p) = (-2, 9)\nR(S p) = (-3, 6)", fontsize=8.5,
                color=NARANJA)
ejes[0, 1].text(0.35, 3.55, "estirar no es lo mismo\nque rotar: no conmutan",
                fontsize=8.5, color=NARANJA, va="top")

pintar(ejes[1, 0], H, "Cizallar: inclina la figura sin cambiar el área\n"
                      "det = 1, pero las distancias sí cambian")
ejes[1, 0].text(1.0, 2.3, "la base se queda\nen su sitio y las\nalturas se desplazan",
                fontsize=8.5, color=MORADO, va="top")

pintar(ejes[1, 1], P, "Proyectar: la columna 2 es el vector cero\ndet = 0, y lo aplastado no vuelve")
ejes[1, 1].text(0.1, -0.45, "el eje y entero\nacaba en (0, 0):\nP² = P", fontsize=8.5,
                color=ROJO, va="top")

guardar(fig, "matriz-como-accion")
