"""svm-1.py — la geometria del margen máximo: quien decide la frontera son unos pocos
puntos, y el parámetro C decide cuanto se ensancha el pasillo. Pagina de SVM (fase 6)."""

import numpy as np
from sklearn.datasets import make_classification
from sklearn.svm import SVC

from comun import *

estilo()
azar = np.random.default_rng(7)

# Dos nubes de puntos linealmente separables: se ve el pasillo entero.
X, y = make_classification(n_samples=44, n_features=2, n_informative=2, n_redundant=0,
                           n_clusters_per_class=1, class_sep=1.4, flip_y=0.0,
                           random_state=7)

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.5))

# --- Izquierda: el margen y los vectores de soporte.
svm = SVC(kernel="linear", C=1.0).fit(X, y)
w = svm.coef_[0]
b = svm.intercept_[0]
margen = 2 / np.linalg.norm(w)              # distancia entre las dos lineas de apoyo
x0, x1 = X[:, 0].min() - 0.6, X[:, 0].max() + 0.6
xs = np.array([x0, x1])
frontera = -(w[0] * xs + b) / w[1]
arriba = -(w[0] * xs + b - 1) / w[1]
abajo = -(w[0] * xs + b + 1) / w[1]

ejes[0].fill_between(xs, abajo, arriba, color=AZUL, alpha=0.12, zorder=1)
ejes[0].plot(xs, arriba, color=AZUL, linewidth=1.1, linestyle="--")
ejes[0].plot(xs, abajo, color=AZUL, linewidth=1.1, linestyle="--")
ejes[0].plot(xs, frontera, color=TEXTO, linewidth=1.6)
for clase, color, marca in ((0, MORADO, "o"), (1, NARANJA, "s")):
    ejes[0].scatter(X[y == clase, 0], X[y == clase, 1], s=26, color=color,
                    marker=marca, zorder=3, label=("clase 0" if clase == 0 else "clase 1"))
# Los vectores de soporte son los unicos puntos que tocan el pasillo: se marcan con un anillo.
ejes[0].scatter(X[svm.support_, 0], X[svm.support_, 1], s=115, facecolor="none",
                edgecolor=ROJO, linewidth=1.3, zorder=4, label="vectores de soporte")
anotar(ejes[0], f"margen {coma(round(margen, 2))}:\nla frontera se pone en medio",
       xy=(xs.mean(), -(w[0] * xs.mean() + b) / w[1]), xytext=(0.03, 0.93), color=TEXTO)
anotar(ejes[0], "solo estos 3 puntos mandan",
       xy=(X[svm.support_][2, 0], X[svm.support_][2, 1]), xytext=(0.58, 0.50),
       color=ROJO, flecha=False)
anotar(ejes[0], "quita los demás y la frontera no cambia",
       xy=(X[svm.support_][2, 0], X[svm.support_][2, 1]), xytext=(0.31, 0.02), color=ROJO)
titulo(ejes[0], "El margen es el pasillo más ancho posible",
       "la frontera se coloca donde deja más aire a los dos lados")
ejes[0].set_xlabel("variable 1")
ejes[0].set_ylabel("variable 2")
ejes[0].legend(loc="upper right", fontsize=8)
ejes[0].set_xlim(x0, x1)
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="both")

# --- Derecha: qué hace C con ese pasillo (y con cuántos puntos lo sujetan).
ces = np.logspace(-2, 2.3, 24)
anchos = []
for c in ces:
    modelo = SVC(kernel="linear", C=float(c)).fit(X, y)
    anchos.append(2 / np.linalg.norm(modelo.coef_[0]))
anchos = np.array(anchos)

ejes[1].plot(ces, anchos, color=AZUL, linewidth=1.9, marker="o", markersize=3.5,
             label="ancho del margen")
ejes[1].axvline(1.0, color=REJILLA, linewidth=1.0, linestyle=":")
anotar(ejes[1], "C grande: pasillo estrecho,\nel modelo se pega a los datos",
       xy=(60, float(np.interp(60, ces, anchos))), xytext=(0.50, 0.62), color=AZUL)
anotar(ejes[1], "C pequeño: pasillo ancho\ny muchos puntos sujetándolo",
       xy=(0.05, float(np.interp(0.05, ces, anchos))), xytext=(0.03, 0.06), color=VERDE)
titulo(ejes[1], "C decide cuánto se ensancha el pasillo",
       "en escala logarítmica; C = 1 es el valor por defecto de scikit-learn")
ejes[1].set_xlabel("C: castigo por cada punto mal clasificado")
ejes[1].set_ylabel("ancho del margen")
ejes[1].set_xscale("log")
ejes[1].set_ylim(0, max(anchos) * 1.18)
ejes[1].legend(loc="upper right", fontsize=8)
rejilla(ejes[1], eje="both")
numeros(ejes[1], ejes="y")

guardar(fig, "svm-margen-y-parametro-c")
