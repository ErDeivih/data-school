"""bagging-y-random-forest-1.py — por qué promediar modelos correlacionados tiene un suelo
y por qué el error out-of-bag es una validación gratis. Pagina de bagging y Random Forest."""

import warnings

import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from comun import *

# Un bosque de 1 o 2 arboles no puede estimar el OOB: sklearn avisa y no es un fallo.
warnings.filterwarnings("ignore", message="Some inputs do not have OOB scores")

estilo()
# --- Panel izquierdo: varianza del promedio, Var = rho + (1 - rho) / n, con sigma^2 = 1.
promedios = np.arange(1, 101)
series = []
for rho, color in ((0.0, VERDE), (0.3, AZUL), (0.8, ROJO)):
    var = rho + (1 - rho) / promedios          # el primer termino no depende de n
    series.append((rho, color, var))
# --- Panel derecho: error out-of-bag y error en datos no vistos, al crecer el bosque.
X, y = make_classification(n_samples=400, n_features=6, n_informative=3, n_redundant=0,
                           class_sep=0.55, flip_y=0.15, random_state=7)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.35, random_state=7)
cuantos = [1, 2, 3, 4, 5, 6, 8, 10, 13, 16, 20, 25, 30, 40, 50, 60]
oob, prueba = [], []
for n in cuantos:
    bosque = RandomForestClassifier(n_estimators=n, oob_score=True, random_state=0,
                                    n_jobs=1).fit(X_tr, y_tr)
    oob.append(1 - bosque.oob_score_)
    prueba.append(1 - bosque.score(X_te, y_te))

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.2))

# --- Izquierda: cada rho deja un suelo distinto por debajo del cual no se baja.
for rho, color, var in series:
    ejes[0].plot(promedios, var, color=color, linewidth=1.8, label=f"ρ = {coma(rho)}")
    ejes[0].axhline(rho, color=color, linewidth=1.0, linestyle=":", alpha=0.8)
anotar(ejes[0], "suelo ρ: 100 modelos no bajan de ahí",
       xy=(60, 0.8), xytext=(0.24, 0.71), color=ROJO)
anotar(ejes[0], "sin correlación, promediar\nsí reparte la varianza",
       xy=(40, 0.025), xytext=(0.42, 0.29), color=VERDE)
titulo(ejes[0], "Promediar no borra la correlación",
       "varianza del promedio de n modelos, con varianza individual 1")
ejes[0].set_xlabel("número de modelos promediados")
ejes[0].set_ylabel("varianza del promedio")
ejes[0].set_yscale("log")
ejes[0].set_xlim(0, 100)
ejes[0].set_ylim(3e-3, 4)
ejes[0].legend(loc="center right", title="correlación entre modelos", title_fontsize=8.5)
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="x")

# --- Derecha: el error OOB y el de prueba convergen; más árboles ya casi no mejoran.
ejes[1].plot(cuantos, oob, color=NARANJA, linewidth=1.8, marker="o", markersize=4,
             label="error out-of-bag (validación gratis)")
ejes[1].plot(cuantos, prueba, color=AZUL, linewidth=1.8, marker="s", markersize=4,
             label="error en datos que el bosque no vio")
anotar(ejes[1], "al principio el OOB es pesimista",
       xy=(3, 0.40), xytext=(0.06, 0.92), color=NARANJA)
anotar(ejes[1], "a partir de aquí añadir\nárboles ya no cambia nada",
       xy=(45, 0.235), xytext=(0.42, 0.28), color=AZUL)
titulo(ejes[1], "El OOB estima el error sin reservar datos",
       "en este bosque se queda algo por debajo del error real")
ejes[1].set_xlabel("número de árboles del bosque")
ejes[1].set_ylabel("tasa de error")
ejes[1].set_ylim(0.15, 0.60)
ejes[1].legend(loc="upper right")
rejilla(ejes[1])
numeros(ejes[1], ejes="both")

guardar(fig, "bagging-suelo-de-varianza-y-oob")
