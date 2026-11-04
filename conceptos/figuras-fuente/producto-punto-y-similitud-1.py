"""producto-punto-y-similitud-1.py — el producto punto crece con la escala, el coseno no:
proyección, ángulo y por qué se normaliza. Figura de la pagina producto-punto-y-similitud."""

import numpy as np

from comun import *
from matplotlib.patches import Arc

estilo()

# Vectores redondos a proposito: x en el eje horizontal para que la proyeccion se vea.
x = np.array([3.0, 0.0])
y = np.array([2.0, 2.0])
y2 = 2.0 * y

producto = float(x @ y)
coseno = producto / (np.linalg.norm(x) * np.linalg.norm(y))
proyeccion = (producto / float(x @ x)) * x

# Dos columnas y dos filas, con el dibujo geometrico ocupando la columna izquierda entera:
# necesita las dos proporciones iguales para que el angulo se vea, y las dos barras de la
# derecha, una encima de otra, ganan el ancho que les faltaba en una fila de tres.
fig = plt.figure(figsize=(10.4, 7.2))
rejilla_paneles = fig.add_gridspec(2, 2, width_ratios=[1.3, 1.0])
geo = fig.add_subplot(rejilla_paneles[:, 0])
barras = fig.add_subplot(rejilla_paneles[0, 1])
cosenos = fig.add_subplot(rejilla_paneles[1, 1])

# ------------------------------------------------------- izquierda: el dibujo
geo.set_aspect("equal")
geo.set_xlim(-0.6, 4.9)
geo.set_ylim(-0.7, 4.8)

geo.annotate("", xy=x, xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color=AZUL, linewidth=2.0))
geo.annotate("", xy=y2, xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color=CIAN, linewidth=1.6, linestyle="--"))
geo.annotate("", xy=y, xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color=VERDE, linewidth=2.0))

# La proyeccion de y sobre x cae encima de x: esa es justo la idea.
geo.plot([0, proyeccion[0]], [0, proyeccion[1]], color=MORADO, linewidth=3.0,
         linestyle=":", zorder=3)
geo.plot([proyeccion[0]], [proyeccion[1]], marker="o", markersize=7, color=MORADO,
         zorder=4)
geo.plot([y[0], proyeccion[0]], [y[1], proyeccion[1]], color=REJILLA, linewidth=1.0,
         linestyle="--")

geo.add_patch(Arc((0, 0), 1.7, 1.7, angle=0, theta1=0, theta2=45,
                  color=TEXTO, linewidth=1.0))
geo.text(1.28, 0.36, "45°", fontsize=9, color=TEXTO)

# Las etiquetas van en coordenadas del eje (0-1): "y = (2, 2)" estaba escrita justo encima de
# las dos flechas que salen de ese punto, y ahora se aparta a la derecha con una flecha.
anotar(geo, "y = (2, 2)", xy=(2, 2), xytext=(0.72, 0.62), color=VERDE)
anotar(geo, "x = (3, 0)", xy=(3, 0), xytext=(0.57, 0.05), color=AZUL, flecha=False)
anotar(geo, "2y = (4, 4)", xy=(4, 4), xytext=(0.68, 0.92), color=CIAN, flecha=False)
anotar(geo, "2y: el doble de largo\ny el mismo ángulo", xy=(4, 4), xytext=(0.12, 0.64),
       color=CIAN, flecha=False)
anotar(geo, "la sombra de y sobre x\ncae en (2; 0)", xy=(2, 0), xytext=(0.51, 0.30),
       color=MORADO, flecha=False)
anotar(geo, "x · y = 6\n‖x‖ = 3   ‖y‖ = 2,83\ncos θ = 0,7071", xy=(0, 0), xytext=(0.11, 0.90),
       color=TEXTO, flecha=False)

titulo(geo, "El producto punto es una proyección")
numeros(geo)
rejilla(geo, "both")

# ------------------------------------------- arriba a la derecha: el producto se dispara
barras.bar([0, 1], [producto, float(x @ y2)], width=0.55, color=[VERDE, CIAN])
barras.set_xticks([0, 1])
barras.set_xticklabels(["y", "2y"], fontsize=10)
barras.set_ylim(0, 15)
barras.text(0, producto + 0.5, "6", ha="center", fontsize=10, color=TEXTO)
barras.text(1, float(x @ y2) + 0.5, "12", ha="center", fontsize=10, color=TEXTO)
titulo(barras, "El producto punto se dobla con la escala")
barras.set_ylabel("x · y")
# La franja de arriba, entre los dos números, esta vacia: la nota cabe allí sin tapar barras.
anotar(barras, "el número se duplica\nsin que la opinión cambie", xy=(1, 12),
       xytext=(0.05, 0.88), color=NARANJA)
# Solo el eje y: con los dos, el formateador se comeria las etiquetas "y" y "2y" del eje x.
numeros(barras, ejes="y")
rejilla(barras)

# ------------------------------------------- abajo a la derecha: el coseno se queda quieto
cos2 = float(x @ y2) / (np.linalg.norm(x) * np.linalg.norm(y2))
cosenos.bar([0, 1], [coseno, cos2], width=0.55, color=[VERDE, CIAN])
cosenos.set_xticks([0, 1])
cosenos.set_xticklabels(["y", "2y"], fontsize=10)
cosenos.set_ylim(0, 1.5)
cosenos.axhline(coseno, color=ROJO, linewidth=1.2, linestyle="--")
cosenos.text(0, coseno + 0.04, "0,7071", ha="center", fontsize=10, color=TEXTO)
cosenos.text(1, cos2 + 0.04, "0,7071", ha="center", fontsize=10, color=TEXTO)
titulo(cosenos, "El coseno no se mueve: mide dirección")
cosenos.set_ylabel("cos θ")
# Por encima de las dos barras (que acaban en 0,7071) queda libre toda la franja de arriba.
anotar(cosenos, "la misma altura: por eso se normaliza\npara comparar documentos de distinto tamaño",
       xy=(0.5, coseno), xytext=(0.98, 0.90), color=ROJO, align="right")
# Igual que en el panel de arriba: el formateador solo toca el eje y.
numeros(cosenos, ejes="y")
rejilla(cosenos)

# El nombre del fichero que espera la pagina: sin tilde, como todos los demas.
guardar(fig, "producto-punto-coseno-y-proyección")
