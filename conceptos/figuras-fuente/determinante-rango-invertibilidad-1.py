"""determinante-rango-invertibilidad-1.py — el determinante como factor de áreas, la matriz
singular que aplasta y la casi singular que engaña. Figura de la pagina
determinante-rango-invertibilidad."""

import numpy as np

from comun import *

estilo()

# Las matrices del ejemplo de la pagina.
B = np.array([[2.0, 1.0], [1.0, 3.0]])          # invertible: det = 5
A = np.array([[1.0, 2.0], [2.0, 4.0]])          # singular: det = 0
C = np.array([[1.0, 2.0], [2.0, 4.0001]])       # casi singular: det = 0,0001

cuadrado = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]])


def imagen(M, puntos):
    return (M @ puntos.T).T


def n0(v):
    """Numero corto con coma decimal y sin el '-0' que deja el redondeo."""
    if abs(v) < 1e-9:
        v = 0.0
    return ("%g" % round(float(v), 6)).replace(".", ",")


# Cuatro paneles en dos filas. El ancho sube a 10,8 pulgadas porque los subtitulos de los
# paneles de la izquierda, escritos largos, se salian de su columna y se metian en los ticks
# del panel de al lado (medido: la caja del subtitulo de arriba llegaba a x=427 y el «5» del
# panel derecho empieza en x=682, pero el subtitulo del panel 4 se salia del lienzo).
fig, ejes = plt.subplots(2, 2, figsize=(10.8, 7.4))

# ------------------------------------------- arriba izquierda: el area se multiplica
ax = ejes[0, 0]
ax.set_aspect("equal")
ax.set_xlim(-0.6, 3.7)
ax.set_ylim(-0.7, 4.7)
ax.fill(cuadrado[:, 0], cuadrado[:, 1], facecolor=REJILLA, alpha=0.35,
        edgecolor=REJILLA, linewidth=1.1)
im = imagen(B, cuadrado)
ax.fill(im[:, 0], im[:, 1], facecolor=AZUL, alpha=0.20, edgecolor=AZUL, linewidth=1.6)
ax.annotate("", xy=B[:, 0], xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color=AZUL, linewidth=1.7))
ax.annotate("", xy=B[:, 1], xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color=MORADO, linewidth=1.7))
ax.text(2.05, 0.45, "columna 1", fontsize=8.5, color=AZUL)
ax.text(0.35, 3.05, "columna 2", fontsize=8.5, color=MORADO)
ax.text(1.55, 1.55, "det = 5", fontsize=11, color=AZUL, ha="center", va="center")
# Ticks escritos a mano: los automaticos sacaban un «-1» por debajo del eje que caia sobre el
# «-1» del panel de al lado (medido: y=378..392 contra y=380..394, mismo carril).
ax.set_xticks([0, 1, 2, 3])
ax.set_yticks([0, 1, 2, 3, 4])
titulo(ax, "El determinante mide el área",
       "el cuadrado gris se convierte en un paralelogramo")
numeros(ax)
rejilla(ax, "both")

# ------------------------------------------- arriba derecha: det = 0, todo aplastado
ax = ejes[0, 1]
ax.set_aspect("equal")
ax.set_xlim(-0.6, 3.7)
ax.set_ylim(-0.7, 6.7)
ax.fill(cuadrado[:, 0], cuadrado[:, 1], facecolor=REJILLA, alpha=0.35,
        edgecolor=REJILLA, linewidth=1.1)
ax.plot([0.0, 3.0], [0.0, 6.0], color=ROJO, linewidth=2.4)
ax.annotate("", xy=A[:, 0], xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=1.7))
ax.annotate("", xy=A[:, 1], xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color=NARANJA, linewidth=1.7))
# La nota se va al hueco de abajo a la derecha (por debajo de las dos flechas) en vez de
# quedarse sobre la recta, que la atravesaba de lado a lado.
anotar(ax, "la 2.ª columna es\nel doble de la 1.ª", xy=(2.0, 4.0), xytext=(0.56, 0.10),
       color=ROJO)
ax.set_xticks([0, 1, 2, 3])
ax.set_yticks([0, 1, 2, 3, 4, 5, 6])
titulo(ax, "Det = 0: el cuadrado se aplasta",
       "las columnas apuntan igual: ni área ni inversa")
numeros(ax)
rejilla(ax, "both")

# ------------------------------------------- abajo izquierda: la casi singular
ax = ejes[1, 0]
ax.set_aspect("equal")
ax.set_xlim(-0.6, 3.7)
ax.set_ylim(-0.7, 6.7)
ax.fill(cuadrado[:, 0], cuadrado[:, 1], facecolor=REJILLA, alpha=0.35,
        edgecolor=REJILLA, linewidth=1.1)
ax.plot([0.0, 3.0], [0.0, 6.00015], color=NARANJA, linewidth=2.4)
ax.annotate("", xy=C[:, 0], xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color=CIAN, linewidth=1.7))
ax.annotate("", xy=C[:, 1], xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color=NARANJA, linewidth=1.7))
anotar(ax, "a ojo, igual que la de arriba,\npero el área es 0,0001: κ(C) ≈ 2,5 · 10⁵",
       xy=(2.0, 4.0), xytext=(0.50, 0.10), color=NARANJA)
ax.set_xticks([0, 1, 2, 3])
ax.set_yticks([0, 1, 2, 3, 4, 5, 6])
titulo(ax, "Casi singular: engaña a la vista",
       "invertible, pero inservible en la práctica")
numeros(ax)
rejilla(ax, "both")

# ------------------------------------------- abajo derecha: la solucion que salta
ax = ejes[1, 1]
b1 = np.array([3.0, 6.0])
b2 = np.array([3.0, 6.0001])
x1 = np.linalg.solve(C, b1)
x2 = np.linalg.solve(C, b2)
ax.set_xlim(0.3, 4.3)
ax.set_ylim(-1.0, 2.2)
ax.plot([x1[0], x2[0]], [x1[1], x2[1]], color=REJILLA, linewidth=1.4, linestyle="--")
ax.plot([x1[0]], [x1[1]], marker="o", markersize=8, color=AZUL)
ax.plot([x2[0]], [x2[1]], marker="o", markersize=8, color=ROJO)
ax.annotate("b = (3; 6)  →  x = (%s; %s)" % (n0(x1[0]), n0(x1[1])),
            xy=(x1[0], x1[1]), xytext=(2.25, 1.05), fontsize=9, color=AZUL, ha="left",
            arrowprops=dict(arrowstyle="->", color=AZUL, linewidth=0.9))
ax.annotate("b = (3; 6,0001)  →  x = (%s; %s)" % (n0(x2[0]), n0(x2[1])),
            xy=(x2[0], x2[1]), xytext=(1.15, 1.9), fontsize=9, color=ROJO,
            arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9))
ax.set_xlabel("x₁")
ax.set_ylabel("x₂")
# El tick «4,5» se salia del lienzo (medido: x=1200..1222 con la figura de 1188 px de ancho).
ax.set_xticks([0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])
ax.set_yticks([-0.5, 0.0, 0.5, 1.0, 1.5, 2.0])
titulo(ax, "La solución salta con el último decimal",
       "0,0001 en b y la solución salta 2 unidades")
numeros(ax)
rejilla(ax, "both")

guardar(fig, "determinante-area-y-casi-singular")
