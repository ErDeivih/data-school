"""perceptron-y-mlp-1.py — por qué una recta no separa dos círculos y una capa oculta sí.

Dos círculos concéntricos: el disco central es una clase y el anillo la otra. Ninguna recta
los separa, por bien que se coloque. Izquierda: la mejor frontera lineal posible, que se
queda en la mitad. Derecha: la misma frontera cuando entre la entrada y la salida hay ocho
neuronas ocultas. La figura de la página de perceptrón y perceptrón multicapa (fase 7).
"""

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier

from comun import *

estilo()
azar = np.random.default_rng(7)

# Los dos círculos: el disco (radio 0,4) es la clase 0 y el anillo (radio 1) la clase 1.
# El ruido es de 0,07 en cada coordenada, así que las dos clases se rozan en el borde.
n = 200
angulo = azar.uniform(0.0, 2.0 * np.pi, 2 * n)
# sqrt(uniforme) reparte los puntos por igual en el área del disco, no amontonados en el centro
radio = np.concatenate([0.40 * np.sqrt(azar.uniform(0.0, 1.0, n)), np.full(n, 1.0)])
X = np.c_[radio * np.cos(angulo), radio * np.sin(angulo)] + azar.normal(0.0, 0.07, (2 * n, 2))
y = np.r_[np.zeros(n, dtype=int), np.ones(n, dtype=int)]

# Malla sobre la que se pregunta al modelo qué clase asigna a cada punto. Paso de 0,02:
# suficiente para que la frontera salga suave y el SVG no se llene de micro-polígonos.
xx, yy = np.meshgrid(np.arange(-1.6, 1.6, 0.02), np.arange(-1.6, 1.6, 0.02))
malla = np.c_[xx.ravel(), yy.ravel()]

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.6))

# --- Izquierda: la frontera de una regresión logística es una recta ------------------
ax = ejes[0]
lineal = LogisticRegression(max_iter=1000).fit(X, y)
acierto_lineal = float(lineal.score(X, y))
ax.contourf(xx, yy, lineal.predict(malla).reshape(xx.shape),
            levels=[-0.5, 0.5, 1.5], colors=[AZUL, ROJO], alpha=0.10, zorder=1)
ax.contour(xx, yy, lineal.predict(malla).reshape(xx.shape),
           levels=[0.5], colors=[TEXTO], linewidths=1.2, zorder=2)
ax.scatter(X[y == 0, 0], X[y == 0, 1], s=13, color=AZUL, zorder=3, label="clase 0: el disco")
ax.scatter(X[y == 1, 0], X[y == 1, 1], s=13, color=ROJO, zorder=3, label="clase 1: el anillo")
# La esquina de arriba a la derecha queda fuera del anillo: ahí cabe la nota sin tapar nada.
anotar(ax, f"acierta el {acierto_lineal * 100:.0f} %: la recta deja\nmedia clase 1 del lado del disco",
       xy=(0.75, 0.75), xytext=(0.97, 0.95), color=ROJO, align="right")
titulo(ax, "Una recta: media clase mal clasificada",
       "la mejor frontera lineal posible sobre dos círculos")
ax.set_xlabel("variable 1")
ax.set_ylabel("variable 2")
ax.set_aspect("equal")          # sin esto el círculo se dibuja como una elipse
ax.legend(loc="lower left")
rejilla(ax)
numeros(ax)

# --- Derecha: ocho neuronas ocultas bastan para curvar la frontera -------------------
ax = ejes[1]
red = MLPClassifier(hidden_layer_sizes=(8,), max_iter=3000, random_state=0).fit(X, y)
acierto_red = float(red.score(X, y))
ax.contourf(xx, yy, red.predict(malla).reshape(xx.shape),
            levels=[-0.5, 0.5, 1.5], colors=[AZUL, ROJO], alpha=0.10, zorder=1)
ax.contour(xx, yy, red.predict(malla).reshape(xx.shape),
           levels=[0.5], colors=[TEXTO], linewidths=1.2, zorder=2)
ax.scatter(X[y == 0, 0], X[y == 0, 1], s=13, color=AZUL, zorder=3)
ax.scatter(X[y == 1, 0], X[y == 1, 1], s=13, color=ROJO, zorder=3)
anotar(ax, f"acierta el {acierto_red * 100:.0f} %: la frontera se\ncierra alrededor del disco",
       xy=(0.75, 0.75), xytext=(0.97, 0.95), color=VERDE, align="right")
titulo(ax, "Una capa oculta curva la frontera",
       "8 neuronas ocultas: la red rodea el disco en vez de partirlo")
ax.set_xlabel("variable 1")
ax.set_aspect("equal")
rejilla(ax)
numeros(ax)

guardar(fig, "perceptron-mlp-recta-frente-a-capa-oculta")
