"""arboles-de-decision-1.py — dos ideas de la pagina de árboles de decisión: que mide la
impureza (y por qué Gini y entropia casi siempre eligen el mismo corte) y por qué un árbol
sin limite de profundidad memoriza. Fase 6."""

import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from comun import *

estilo()
azar = np.random.default_rng(7)

# --- Panel izquierdo: impureza de un nodo segun su mezcla de clases.
# p es la proporcion de la clase 1; el nodo es 50/50 cuando p = 0,5.
p = np.linspace(1e-9, 1 - 1e-9, 400)
gini = 2 * p * (1 - p)                                     # 1 - (p^2 + (1-p)^2)
entropia = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))    # bits, maximo 1
error = 1 - np.maximum(p, 1 - p)                           # 1 - acierto de la clase mayoritaria

# --- Panel derecho: acierto en entrenamiento y en validacion segun la profundidad.
X, y = make_classification(n_samples=260, n_features=4, n_informative=3, n_redundant=0,
                           class_sep=0.55, flip_y=0.15, random_state=7)
X_tr, X_va, y_tr, y_va = train_test_split(X, y, test_size=0.35, random_state=7)
profundidades = [1, 2, 3, 4, 5, 6, 8, 12, 16]
eje_x = np.array(profundidades, dtype=float)               # 17 = "sin limite de profundidad"
eje_x[-1] = 17
train, val = [], []
for d in profundidades:
    arbol = DecisionTreeClassifier(max_depth=d, random_state=0).fit(X_tr, y_tr)
    train.append(arbol.score(X_tr, y_tr))
    val.append(arbol.score(X_va, y_va))

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.2))

# --- Izquierda: las tres medidas de impureza caen a cero en los nodos puros.
ejes[0].plot(p, gini, color=AZUL, linewidth=1.8, label="Gini  = 1 − Σ p²")
ejes[0].plot(p, entropia, color=MORADO, linewidth=1.8, label="entropía  = −Σ p·log₂ p")
ejes[0].plot(p, error, color=NARANJA, linewidth=1.6, linestyle="--",
             label="error de la clase mayoritaria")
ejes[0].axvline(0.5, color=TEXTO, linewidth=0.9, alpha=0.35)
anotar(ejes[0], "con 50 % de cada clase\nlas tres valen lo máximo",
       xy=(0.5, 1.0), xytext=(0.55, 0.80), color=TEXTO)
anotar(ejes[0], "nodo puro: impureza cero,\nno hay nada que dividir",
       xy=(0.03, 0.0), xytext=(0.02, 0.42), color=VERDE)
titulo(ejes[0], "La impureza mide la mezcla del nodo",
       "Gini y entropía suben y bajan juntas; el error de clasificación no")
ejes[0].set_xlabel("proporción de la clase 1 en el nodo")
ejes[0].set_ylabel("impureza")
ejes[0].set_xlim(0, 1)
ejes[0].set_ylim(-0.03, 1.12)
ejes[0].legend(loc="lower center")
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="both")

# --- Derecha: el acierto de entrenamiento llega a 1 mientras el de validacion no sube.
ejes[1].plot(eje_x, train, color=ROJO, linewidth=1.8, marker="o", markersize=4,
             label="acierto en entrenamiento")
ejes[1].plot(eje_x, val, color=AZUL, linewidth=1.8, marker="s", markersize=4,
             label="acierto en datos no vistos")
anotar(ejes[1], "memoriza: 100 % en entrenamiento\ny ni un punto más fuera",
       xy=(16, 1.0), xytext=(0.34, 0.88), color=ROJO)
anotar(ejes[1], "podar aquí es lo que se gana:\nel árbol profundo no aporta nada",
       xy=(5, 0.626), xytext=(0.10, 0.12), color=AZUL)
titulo(ejes[1], "Sin poda memoriza; el acierto real no sube",
       "la distancia entre las dos curvas es el sobreajuste, medido en puntos de acierto")
ejes[1].set_xlabel("profundidad máxima del árbol (17 = sin límite)")
ejes[1].set_ylabel("acierto")
ejes[1].set_xticks([1, 4, 8, 12, 17])
ejes[1].set_xticklabels(["1", "4", "8", "12", "sin\nlímite"])
ejes[1].set_ylim(0.55, 1.06)
ejes[1].legend(loc="center right")
rejilla(ejes[1])
numeros(ejes[1], ejes="y")

guardar(fig, "arboles-impureza-y-sobreajuste")
