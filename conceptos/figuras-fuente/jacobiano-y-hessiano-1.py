"""jacobiano-y-hessiano-1.py — la curvatura decide lo que el gradiente no puede:
mínimo, máximo o silla. Figura de la pagina de jacobiano y hessiano."""

import numpy as np

from comun import *

estilo()

# --- Panel 1: dos funciones con gradiente nulo en el origen. Solo la curvatura las separa.
u = np.linspace(-1.5, 1.5, 120)
X, Y = np.meshgrid(u, u)

# Dos filas de dos paneles: con tres en una fila cada panel queda estrecho y el texto no cabe.
# La columna izquierda lleva los dos dibujos y la derecha la matriz con su criterio, que es como
# los nombra el pie de la pagina («los dos dibujos de la izquierda», «la matriz de la derecha»).
fig, ejes = plt.subplots(2, 2, figsize=(11.0, 7.2))
e0, e2 = ejes[0]        # arriba: la curvatura (izquierda) y la matriz (derecha)
e1, e3 = ejes[1]        # abajo: los autovalores (izquierda) y el criterio (derecha)

e0.contourf(X, Y, X**2 + Y**2, levels=12, cmap="Blues")
cs = e0.contour(X, Y, X**2 - Y**2, levels=[-1.5, -0.75, 0.75, 1.5], colors=ROJO, linewidths=1.0)
e0.clabel(cs, fmt=coma, fontsize=7, inline=True)
e0.plot(0, 0, marker="o", color=TEXTO, markersize=5)
# La nota cae en el claro del centro, que es lo unico sin lineas rojas ni etiquetas. Va en
# morado a proposito: el fondo de colores no cambia con el tema del portal, asi que el texto
# no puede usar TEXTO (que en tema oscuro es casi blanco y no se leeria encima del azul claro).
anotar(e0, "aquí el gradiente vale 0 en los dos", xy=(0.0, 0.0), xytext=(0.30, 0.62),
       color=MORADO)
e0.set_xlabel("x")
e0.set_ylabel("y")
titulo(e0, "Mismo gradiente nulo, distinta curvatura",
       "fondo azul: valle · líneas rojas: silla")
numeros(e0)

# --- Panel 2: la curvatura se mide a lo largo de las direcciones propias del Hessiano.
t = np.linspace(-1.6, 1.6, 200)
e1.plot(t, t**2, color=AZUL, linewidth=1.7)
e1.plot(t, -t**2, color=ROJO, linewidth=1.7)
e1.axhline(0, color=TEXTO, linewidth=0.8, alpha=0.4)
e1.plot([0], [0], marker="o", color=TEXTO, markersize=5)
# Las dos parabolas dejan libre la banda de arriba y la de abajo, una para cada nota.
anotar(e1, "autovalor positivo: la curva sube", xy=(1.05, 1.1), xytext=(0.22, 0.94), color=AZUL)
anotar(e1, "autovalor negativo: la curva baja", xy=(1.05, -1.1), xytext=(0.22, 0.06), color=ROJO)
e1.set_xlabel("desplazamiento desde el punto critico")
e1.set_ylabel("variación de f")
e1.set_ylim(-3.5, 3.1)
titulo(e1, "Los autovalores son las dos curvaturas")
rejilla(e1)

# --- Panel 3: el mismo criterio leido en la matriz. f(x, y) = 3x^2 y + y^3 en el punto (1, 2).
H = np.array([[12.0, 6.0], [6.0, 12.0]])
e2.imshow(H, cmap="Blues", vmin=0, vmax=14)
etiquetas = ["f_xx", "f_xy", "f_yx", "f_yy"]
for i in range(2):
    for j in range(2):
        e2.text(j, i - 0.20, etiquetas[2 * i + j], ha="center", va="center", fontsize=9)
        e2.text(j, i + 0.22, coma(H[i, j]), ha="center", va="center", fontsize=12)
e2.set_xticks([0, 1]); e2.set_xticklabels(["deriva de x", "deriva de y"], fontsize=8)
e2.set_yticks([0, 1]); e2.set_yticklabels(["deriva de x", "deriva de y"], fontsize=8)
titulo(e2, "H en el punto (1, 2)", "simétrica y definida positiva")

# --- Panel 4: las dos comprobaciones que se leen en la matriz, con espacio para leerlas.
e3.axis("off")
titulo(e3, "El criterio aplicado a esta matriz", "lo que hay que mirar y lo que sale")
e3.text(0.04, 0.72, "un autovalor de cada signo = silla", transform=e3.transAxes,
        fontsize=10, va="center", color=ROJO)
e3.text(0.04, 0.50, "f_xy = f_yx: si no cuadra, la derivada está mal", transform=e3.transAxes,
        fontsize=10, va="center", color=TEXTO)
e3.text(0.04, 0.26, "menores 12 y 12*12 - 6*6 = 108,\nlos dos > 0: la curva sube en toda dirección\n(y en un punto crítico eso es un mínimo)",
        transform=e3.transAxes, fontsize=10, va="center", color=VERDE)

guardar(fig, "jacobiano-hessiano-curvatura")
