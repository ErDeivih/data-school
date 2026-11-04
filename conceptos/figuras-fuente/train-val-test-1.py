"""train-val-test-1.py - el ganador de la validación parece mejor de lo que es: es el máximo
de 20 notas ruidosas. Figura de la pagina de train / validación / prueba (fase 6)."""

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

from comun import *

estilo()

# 500 filas de 20 columnas de ruido puro: no hay senal que aprender, la exactitud real del
# problema es 0,5. Si el elegido saca mas en validacion, esa ventaja es casualidad del reparto.
def ronda(semilla, candidatos=20):
    azar = np.random.default_rng(semilla)
    X = azar.normal(size=(500, 20))
    y = azar.integers(0, 2, 500)
    X_tr, X_resto, y_tr, y_resto = train_test_split(X, y, test_size=0.5, random_state=semilla)
    X_va, X_te, y_va, y_te = train_test_split(X_resto, y_resto, test_size=0.5, random_state=semilla)
    # 20 candidatos distintos: cada arbol mira 3 variables al azar en cada division
    modelos = [DecisionTreeClassifier(max_depth=5, max_features=3, random_state=s).fit(X_tr, y_tr)
               for s in range(candidatos)]
    notas = np.array([m.score(X_va, y_va) for m in modelos])
    elegido = int(np.argmax(notas))          # el "mejor" segun validacion
    return notas, notas[elegido], modelos[elegido].score(X_te, y_te)

notas, en_validacion, en_prueba = [], [], []
for semilla in range(20):
    n, v, t = ronda(semilla)
    notas.append(n)
    en_validacion.append(v)
    en_prueba.append(t)
notas = np.array(notas)                       # 20 rondas x 20 candidatos

media_validacion = float(np.mean(en_validacion))
media_prueba = float(np.mean(en_prueba))
# Error tipico de una exactitud medida sobre 125 ejemplos (la mitad de las 500 filas
# partida otra vez por la mitad): raiz de p(1-p)/n. Es el margen con el que hay que
# comparar la brecha.
error_tipico = float(np.sqrt(0.5 * 0.5 / 125))

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.2))

# --- Izquierda: cada ronda es una tirada; el maximo de 20 es el que se elige.
for j in range(notas.shape[0]):
    ejes[0].scatter(np.full(notas.shape[1], j), notas[j], color=AZUL, s=13, alpha=0.55,
                    linewidths=0, zorder=3)
elegidos = notas.max(axis=1)
ejes[0].scatter(np.arange(notas.shape[0]), elegidos, color=ROJO, s=30, zorder=4)
ejes[0].axhline(0.5, color=TEXTO, linewidth=1.4, linestyle="--")
anotar(ejes[0], "en rojo, el máximo de los 20:\nes el que se lleva a producción",
       xy=(17, elegidos[17]), xytext=(0.03, 0.80), color=ROJO)
titulo(ejes[0], "Veinte notas ruidosas por ronda",
       "la linea de puntos es la verdad, 0,5: no hay senal que aprender")
ejes[0].set_xlabel("ronda de selección")
ejes[0].set_ylabel("exactitud en validación")
ejes[0].set_ylim(0.28, 0.78)
rejilla(ejes[0])
numeros(ejes[0], ejes="y")

# --- Derecha: el mismo modelo, medido en los dos conjuntos.
barras = ejes[1].bar(["en validación\n(el que se elige)", "en prueba\n(datos nuevos)"],
                     [media_validacion, media_prueba], color=[ROJO, AZUL], width=0.52)
ejes[1].axhline(0.5, color=TEXTO, linewidth=1.4, linestyle="--")
# Barra de error: el error tipico de una exactitud medida sobre los 125 ejemplos de prueba.
# Se desplaza a la derecha para que su trazo no cruce la etiqueta del valor.
ejes[1].errorbar([1.14], [media_prueba], yerr=[error_tipico], color=TEXTO, capsize=6,
                 linewidth=1.2, zorder=4)
for barra, valor in zip(barras, [media_validacion, media_prueba]):
    ejes[1].text(barra.get_x() + barra.get_width() / 2 - 0.06, valor + 0.026, "%.3f" % valor,
                 ha="center", fontsize=9.5, color=TEXTO)
anotar(ejes[1], "media de 20 rondas; la barra\nde error es el margen de +-%.3f\ncon 125 ejemplos de prueba"
       % error_tipico, xy=(1.14, media_prueba + error_tipico), xytext=(0.34, 0.13))
titulo(ejes[1], "La ventaja del elegido no se repite",
       "el mismo modelo, medido en el conjunto que lo eligio y en datos nuevos")
ejes[1].set_ylabel("exactitud media en 20 rondas")
ejes[1].set_ylim(0.3, 0.68)
ejes[1].set_yticks([0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65])
rejilla(ejes[1])
numeros(ejes[1], ejes="y")

guardar(fig, "train-val-test-ganador-optimista")
