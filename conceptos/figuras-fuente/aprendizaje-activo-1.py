"""aprendizaje-activo-1.py — elegir por incertidumbre manda al anotador a la frontera, y con
el mismo presupuesto de etiquetas se aprende más que eligiendo al azar. Figura de la página
de aprendizaje activo (fase 6)."""

import numpy as np
from sklearn.datasets import make_moons
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from comun import *

estilo()

# Dos lunas entrelazadas con ruido, como en el ejemplo de la página: 100 puntos y un
# presupuesto de 24 etiquetas, empezando por 4 elegidas al azar.
X, y = make_moons(n_samples=100, noise=0.25, random_state=0)


def curva(estrategia, semilla, tope=24):
    """Devuelve la exactitud tras cada etiqueta nueva y el orden en que se pidieron."""
    azar = np.random.default_rng(semilla)
    idx = np.arange(len(y))
    azar.shuffle(idx)                       # el orden de llegada de los datos es aleatorio
    etiquetados = [int(i) for i in idx[:4]]
    sin_etiquetar = [int(i) for i in idx[4:]]
    modelo = LogisticRegression(max_iter=1000)
    historia, pedidos = [], []
    while len(etiquetados) < tope:
        modelo.fit(X[etiquetados], y[etiquetados])
        historia.append(accuracy_score(y, modelo.predict(X)))
        if estrategia == "aleatorio":
            elegido = int(azar.choice(sin_etiquetar, size=1, replace=False)[0])
        else:
            # Incertidumbre: la probabilidad más cercana a 0,5 es el punto de la frontera.
            p = modelo.predict_proba(X[sin_etiquetar])[:, 1]
            elegido = sin_etiquetar[int(np.argmin(np.abs(p - 0.5)))]
        pedidos.append(elegido)
        etiquetados.append(elegido)
        sin_etiquetar.remove(elegido)
    modelo.fit(X[etiquetados], y[etiquetados])
    historia.append(accuracy_score(y, modelo.predict(X)))
    return np.array(historia), pedidos


# Cinco semillas por estrategia: una sola ejecución depende demasiado del reparto inicial.
medias, primeros = {}, {}
for estrategia in ("aleatorio", "incertidumbre"):
    notas, pedidos = zip(*[curva(estrategia, s) for s in range(5)])
    medias[estrategia] = np.mean(notas, axis=0)
    primeros[estrategia] = pedidos[0][:8]     # las 8 primeras consultas de la semilla 0

etiquetas = np.arange(4, 25)

fig, ejes = plt.subplots(1, 2, figsize=(11.2, 4.5))

# --- Izquierda: dónde caen las consultas de cada estrategia sobre los 100 puntos.
ejes[0].scatter(X[y == 0, 0], X[y == 0, 1], color=AZUL, s=26, alpha=0.40, linewidths=0,
                zorder=3)
ejes[0].scatter(X[y == 1, 0], X[y == 1, 1], color=ROJO, s=26, alpha=0.40, linewidths=0,
                zorder=3)
for estrategia, color, marca in (("aleatorio", NARANJA, "s"), ("incertidumbre", VERDE, "o")):
    puntos = X[primeros[estrategia]]
    ejes[0].scatter(puntos[:, 0], puntos[:, 1], color=color, marker=marca, s=54,
                    edgecolors=TEXTO, linewidths=0.8, zorder=5, label=estrategia)
ejes[0].legend(loc="lower right")
anotar(ejes[0], "la incertidumbre se pega\na la frontera entre las dos lunas",
       xy=(0.0, 0.0), xytext=(0.03, 0.92), color=VERDE, flecha=False)
titulo(ejes[0], "Las ocho primeras consultas de cada estrategia",
       "los puntos de color son los 100 del problema; el azar reparte por todas partes")
ejes[0].set_xlabel("primera variable")
ejes[0].set_ylabel("segunda variable")
rejilla(ejes[0], "both")
numeros(ejes[0])

# --- Derecha: la curva que decide si el aprendizaje activo sirve. Es el criterio de parada
# honesto de la página: cuando deja de subir, etiquetar más no aporta.
ejes[1].plot(etiquetas, medias["aleatorio"], color=NARANJA, linewidth=1.9, marker="s",
             markersize=4, label="elegir al azar")
ejes[1].plot(etiquetas, medias["incertidumbre"], color=VERDE, linewidth=1.9, marker="o",
             markersize=4, label="elegir por incertidumbre")
en_12 = float(medias["incertidumbre"][8] - medias["aleatorio"][8])
anotar(ejes[1], "con 12 etiquetas, %.3f de ventaja" % en_12, xy=(12, medias["aleatorio"][8]),
       xytext=(0.03, 0.94), color=VERDE, flecha=False)
ejes[1].legend(loc="lower right")
titulo(ejes[1], "Mismo presupuesto, mejor elección",
       "media de cinco semillas; la exactitud se mide sobre los mismos 100 puntos")
ejes[1].set_xlabel("etiquetas pedidas al anotador")
ejes[1].set_ylabel("exactitud sobre los 100 puntos")
ejes[1].set_ylim(0.60, 0.92)
rejilla(ejes[1])
numeros(ejes[1], ejes="y")

guardar(fig, "aprendizaje-activo-incertidumbre-vs-azar")
print("a 12 etiquetas: azar %.3f  incertidumbre %.3f" % (medias["aleatorio"][8],
                                                          medias["incertidumbre"][8]))
