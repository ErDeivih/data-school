"""pipelines-de-ml-1.py — la fuga de datos según qué transformación se ajuste fuera del
pipeline: con el escalado apenas se nota, con una selección supervisada el resultado se
dispara. Figura de la página de pipelines de machine learning (fase 6)."""

import numpy as np
from sklearn.datasets import make_classification
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import make_pipeline

from comun import *

estilo()

# --- Panel izquierdo: los dos pares de números del ejemplo de la página.
etiquetas = ["escalado\n(2 columnas)", "selección supervisada\n(500 columnas)"]
fuera = [0.967, 0.867]        # transformación ajustada con TODAS las filas, antes de validar
dentro = [0.975, 0.417]       # la misma transformación, dentro del pipeline y de cada pliegue

# --- Panel derecho: el mismo experimento llevado a varios tamaños de selección. Se promedian
# cinco conjuntos con la receta del ejemplo (60 filas, 500 columnas de las que 3 informan,
# etiqueta con ruido) para que la curva no dependa de una sola semilla.
ks = np.array([2, 5, 10, 20, 40, 80])
fuga, limpio = [], []
for k in ks:
    notas_fuga, notas_limpias = [], []
    for semilla in range(5):
        X, y = make_classification(n_samples=60, n_features=500, n_informative=3,
                                   n_redundant=0, flip_y=0.15, random_state=semilla)
        pliegues = StratifiedKFold(3, shuffle=True, random_state=0)
        # MAL: el selector mira la etiqueta de TODAS las filas, prueba incluida.
        elegidas = SelectKBest(f_classif, k=int(k)).fit(X, y).get_support()
        notas_fuga.append(cross_val_score(LogisticRegression(max_iter=1000), X[:, elegidas],
                                          y, cv=pliegues).mean())
        # BIEN: el mismo selector, pero reajustado dentro de cada pliegue.
        notas_limpias.append(cross_val_score(
            make_pipeline(SelectKBest(f_classif, k=int(k)), LogisticRegression(max_iter=1000)),
            X, y, cv=pliegues).mean())
    fuga.append(float(np.mean(notas_fuga)))
    limpio.append(float(np.mean(notas_limpias)))

fig, ejes = plt.subplots(1, 2, figsize=(11.2, 4.4))

# --- Izquierda: dos grupos de barras, uno por cada transformación del ejemplo.
x = np.arange(2)
ejes[0].bar(x - 0.19, fuera, width=0.36, color=ROJO, zorder=3,
            label="ajustada fuera, con todo el conjunto")
ejes[0].bar(x + 0.19, dentro, width=0.36, color=AZUL, zorder=3,
            label="dentro del pipeline, por pliegue")
for xi, v in zip(x - 0.19, fuera):
    ejes[0].text(xi, v + 0.03, ("%.3f" % v).replace(".", ","), ha="center", fontsize=9,
                 color=ROJO)
for xi, v in zip(x + 0.19, dentro):
    ejes[0].text(xi, v + 0.03, ("%.3f" % v).replace(".", ","), ha="center", fontsize=9,
                 color=AZUL)
anotar(ejes[0], "mismos datos y mismo modelo:\nla diferencia es dónde vive la selección",
       xy=(1.19, 0.552), xytext=(0.40, 0.93), color=ROJO, flecha=False)
ejes[0].set_xticks(x, etiquetas)
ejes[0].set_ylim(0, 1.25)
ejes[0].set_xlim(-0.6, 1.6)
titulo(ejes[0], "No toda transformación fuga igual",
       "en rojo, ajustada con todas las filas; en azul, dentro del pipeline, pliegue a pliegue")
ejes[0].set_ylabel("exactitud en validación")
ejes[0].set_xlabel("transformación que aprende algo de los datos")
rejilla(ejes[0])
numeros(ejes[0], ejes="y")

# --- Derecha: cómo crece el engaño con el número de columnas que conserva el selector.
ejes[1].plot(ks, fuga, color=ROJO, linewidth=1.9, marker="o", markersize=5,
             label="selección fuera del pipeline")
ejes[1].plot(ks, limpio, color=AZUL, linewidth=1.9, marker="o", markersize=5,
             label="selección dentro del pipeline")
anotar(ejes[1], "selección fuera: el selector mira la prueba\ny el resultado se infla solo",
       xy=(20, fuga[3]), xytext=(0.30, 0.94), color=ROJO, flecha=False)
anotar(ejes[1], "selección dentro: solo ve\nel pliegue de entrenamiento", xy=(40, limpio[4]),
       xytext=(0.30, 0.12), color=AZUL, flecha=False)
titulo(ejes[1], "Cuanto más dejas elegir, más engaña",
       "media de cinco conjuntos con la receta del ejemplo y 3 pliegues")
ejes[1].set_xscale("log")
ejes[1].set_xticks(ks)
ejes[1].set_xticklabels([str(int(k)) for k in ks])
ejes[1].minorticks_off()          # sin esto la escala log añade etiquetas de 3x10^0 que se pisan
ejes[1].set_ylim(0.4, 1.0)
ejes[1].set_xlabel("columnas que conserva el selector, k")
ejes[1].set_ylabel("exactitud en validación")
rejilla(ejes[1])
numeros(ejes[1], ejes="y")

guardar(fig, "pipelines-de-ml-fuga-segun-transformación")
