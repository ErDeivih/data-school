"""optimizacion-con-restricciones-1.py — el multiplicador de Lagrange es la tangencia entre
el objetivo y la restricción, y mide el precio sombra. Figura de la pagina de optimización
con restricciones."""

import numpy as np

from comun import *

estilo()
fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.2))

# --- Panel 1: por que el optimo no es donde el gradiente se anula.
eje = np.linspace(0.2, 13, 400)
X1, X2 = np.meshgrid(eje, eje)
producto = X1 * X2

niveles = [2, 8, 18, 36]
cs = ejes[0].contour(X1, X2, producto, levels=niveles, colors=AZUL, linewidths=1.2)
ejes[0].clabel(cs, fmt=coma, fontsize=8, inline=True)
ejes[0].plot([0, 12], [12, 0], color=ROJO, linewidth=1.8)
# La recta se rotula en la esquina de arriba a la izquierda, por encima de las curvas de
# nivel y a la derecha de la etiqueta "18" del contorno: pegada a la recta el texto se
# cruzaba con ella.
anotar(ejes[0], "x1 + x2 = 12", xy=(2.6, 9.4), xytext=(0.20, 0.93), color=ROJO, flecha=False)
ejes[0].plot([6], [6], "o", color=VERDE, markersize=8, zorder=5)
# Este rotulo va arriba a la derecha y baja casi en vertical hasta el punto: asi no se
# cruza con las dos etiquetas de los gradientes, que quedan a su izquierda.
anotar(ejes[0], "el óptimo: tangencia entre\nla curva de nivel y la recta",
       xy=(5.75, 6.25), xytext=(0.50, 0.90), color=VERDE)
ejes[0].annotate("", xy=(7.4, 7.4), xytext=(6.2, 6.2),
                 arrowprops=dict(arrowstyle="-|>", color=VERDE, linewidth=1.7))
ejes[0].annotate("", xy=(7.8, 5.4), xytext=(6.5, 6.3),
                 arrowprops=dict(arrowstyle="-|>", color=ROJO, linewidth=1.7))
ejes[0].annotate("gradiente del objetivo", xy=(7.6, 8.1), color=VERDE, fontsize=8)
ejes[0].annotate("gradiente de la restricción", xy=(8.0, 4.7), color=ROJO, fontsize=8)
titulo(ejes[0], "El óptimo: los gradientes se alinean",
       "no donde el gradiente del objetivo se anula")
ejes[0].set_xlabel("x1")
ejes[0].set_ylabel("x2")
ejes[0].set_xlim(0, 13)
ejes[0].set_ylim(0, 13)
numeros(ejes[0])

# --- Panel 2: que significa el valor del multiplicador.
c = np.linspace(8, 14.5, 200)
maximo = (c / 2) ** 2
ejes[1].plot(c, maximo, color=AZUL, linewidth=1.8)
ejes[1].plot([12], [36], "o", color=VERDE, markersize=8, zorder=5)
ejes[1].plot(c, 6 * (c - 12) + 36, color=NARANJA, linewidth=1.5, linestyle="--")
# Las tres notas van en coordenadas del eje (0-1): la de arriba se comia el titulo y las
# dos naranjas se pisaban entre si. Cada una cae ahora en una franja vacia distinta.
ejes[1].set_ylim(10, 55)
anotar(ejes[1], "relajar la restricción de 12 a 13\nsube el máximo de 36 a 42,25",
       xy=(13.05, 42.25), xytext=(0.03, 0.90), color=TEXTO)
anotar(ejes[1], "esa recta es la tangente:\npendiente 6", xy=(11.5, 33.0),
       xytext=(0.28, 0.18), color=NARANJA)
anotar(ejes[1], "el 6 es el multiplicador", xy=(12.0, 36.0),
       xytext=(0.62, 0.42), color=NARANJA)
titulo(ejes[1], "El multiplicador es el precio sombra",
       "cuánto mejora el objetivo al relajar una unidad")
ejes[1].set_xlabel("lado derecho de la restricción")
ejes[1].set_ylabel("máximo de x1 * x2")
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "restricciones-tangencia-y-precio-sombra")
