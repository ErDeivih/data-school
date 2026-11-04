"""knn-1.py — las dos caras de KNN: la frontera que memoriza con k = 1 y el vecindario que
se vacía al crecer la dimensión. Página de K vecinos más cercanos (fase 6)."""

import numpy as np
from sklearn.datasets import make_classification
from sklearn.neighbors import KNeighborsClassifier

from comun import *

estilo()
azar = np.random.default_rng(7)

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.6))

# --- Izquierda: dos fronteras de decisión sobre los mismos 60 puntos.
# class_sep bajo y flip_y alto a propósito: con datos limpios las dos fronteras coinciden
# y no se vería nada. Con ruido, k = 1 dibuja islas y k = 15 pasa por encima del ruido.
X, y = make_classification(n_samples=60, n_features=2, n_informative=2, n_redundant=0,
                           n_clusters_per_class=1, class_sep=0.9, flip_y=0.12,
                           random_state=7)

# Malla de fondo: el plano entero se trocea en celdas y se predice la clase de cada una.
# Con k = 1 se rellena la zona que el modelo se queda: sale a islas alrededor de cada punto.
malla_x, malla_y = np.meshgrid(np.linspace(X[:, 0].min() - 0.7, X[:, 0].max() + 0.7, 260),
                               np.linspace(X[:, 1].min() - 0.7, X[:, 1].max() + 0.7, 260))
plano = np.column_stack([malla_x.ravel(), malla_y.ravel()])

modelo1 = KNeighborsClassifier(n_neighbors=1).fit(X, y)
zona1 = modelo1.predict(plano).reshape(malla_x.shape)
ejes[0].contourf(malla_x, malla_y, zona1, levels=[-0.5, 0.5, 1.5],
                 colors=[AZUL, AZUL], alpha=0.13, zorder=1)

# Con k = 15 la frontera es una sola línea: aquí sí importa dónde cae y no el relleno.
modelo15 = KNeighborsClassifier(n_neighbors=15).fit(X, y)
zona15 = modelo15.predict(plano).reshape(malla_x.shape)
ejes[0].contour(malla_x, malla_y, zona15, levels=[0.5], colors=[NARANJA],
                linewidths=2.0, linestyles="--", zorder=3)

for clase, color, marca in ((0, MORADO, "o"), (1, ROJO, "s")):
    ejes[0].scatter(X[y == clase, 0], X[y == clase, 1], s=26, color=color, marker=marca,
                    zorder=4, label=("clase 0" if clase == 0 else "clase 1"))

# Con k = 1 cada punto es su propio vecino a distancia 0, así que el acierto de
# entrenamiento es 100 % por construcción: no mide aprendizaje, mide memorización.
aciertoEntrenamiento = modelo1.score(X, y)

anotar(ejes[0], f"k = 1: acierto de entrenamiento {aciertoEntrenamiento:.0%}\ny zona a islas",
       xy=(float(X[3, 0]), float(X[3, 1])), xytext=(0.03, 0.90), color=AZUL)
anotar(ejes[0], "k = 15: la frontera no se\npega a los puntos raros",
       xy=(float(X[1, 0]), float(X[1, 1])), xytext=(0.40, 0.83), color=NARANJA)
anotar(ejes[0], "frontera de k = 15", flecha=False,
       xy=(float(X[1, 0]), float(X[1, 1])), xytext=(0.50, 0.72), color=NARANJA)
titulo(ejes[0], "k = 1 memoriza; k = 15 generaliza",
       "las dos curvas son el mismo modelo con otro número de vecinos")
ejes[0].set_xlabel("variable 1")
ejes[0].set_ylabel("variable 2")
ejes[0].legend(loc="upper right", fontsize=8)
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="both")

# --- Derecha: la maldición de la dimensionalidad, medida sobre puntos uniformes.
# En una caja de lado 1 la distancia máxima posible crece como la raíz de d; lo que
# importa es que el vecino más cercano no se acerca al ritmo del más lejano.
# Misma semilla y mismas dimensiones que el bloque de la página: así el cociente que
# cita el pie (unas 140 veces en d = 2, 0,84 en d = 500) es el que dibuja esta curva.
azar_dim = np.random.default_rng(0)
dimensiones = np.array([2, 5, 20, 100, 500])
cocientes = []
for d in dimensiones:
    nube = azar_dim.uniform(size=(1000, d))
    consulta = azar_dim.uniform(size=d)
    distancias = np.sqrt(((nube - consulta) ** 2).sum(axis=1))
    cocientes.append(distancias.min() / distancias.max())

ejes[1].plot(dimensiones, cocientes, color=ROJO, linewidth=1.9, marker="o", markersize=4.5)
ejes[1].axhline(1.0, color=REJILLA, linewidth=1.0, linestyle=":")
anotar(ejes[1], "con 2 dimensiones el vecino\nestá 140 veces más cerca", flecha=False,
       xy=(2, cocientes[0]), xytext=(0.40, 0.93), color=ROJO)
anotar(ejes[1], "a 500 dimensiones casi da igual\nel vecino más cercano que el más lejano",
       xy=(500, cocientes[-1]), xytext=(0.42, 0.50), color=TEXTO, flecha=False)
titulo(ejes[1], "El vecindario se vacía al crecer la dimensión",
       "cociente entre la distancia al vecino más cercano y al más lejano")
ejes[1].set_xlabel("número de dimensiones")
ejes[1].set_ylabel("cociente cercano / lejano")
ejes[1].set_xscale("log")
ejes[1].set_ylim(0, 1.05)
rejilla(ejes[1], eje="both")
numeros(ejes[1], ejes="both")

guardar(fig, "knn-frontera-y-dimensionalidad")
