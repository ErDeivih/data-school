"""ley-de-los-grandes-numeros-1.py - la media se pega al valor esperado como 1/raiz de n,
que es lento. Con el dado del ejemplo (mu = 3,5, sigma^2 = 35/12)."""

import numpy as np

from comun import *

estilo()

azar = np.random.default_rng(1)
tamanos = np.array([10, 30, 100, 300, 1000, 3000, 10000, 100000])
replicas = 400
mu, sigma = 3.5, np.sqrt(35 / 12)

# --- Izquierda: cinco caminos de la media acumulada de un dado.
n = 100000
tiradas = azar.integers(1, 7, size=(5, n))
acumulada = tiradas.cumsum(axis=1) / np.arange(1, n + 1)

fig, ejes = plt.subplots(1, 2, figsize=(10.2, 4.0))

colores = [AZUL, VERDE, NARANJA, MORADO, CIAN]
for i in range(5):
    ejes[0].plot(acumulada[i], color=colores[i], linewidth=1.1)
ejes[0].axhline(mu, color=ROJO, linewidth=1.6, linestyle="--")
ejes[0].set_xscale("log")
ejes[0].annotate("la esperanza, 3,5", xy=(30, mu), xytext=(1.6, 3.72), color=ROJO, fontsize=9,
                 arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9))
ejes[0].annotate("al principio cada tirada mueve la media: 5 tiradas no dicen nada",
                 xy=(3, 2.6), xytext=(1.2, 1.45), color=TEXTO, fontsize=8.5,
                 arrowprops=dict(arrowstyle="->", color=TEXTO, linewidth=0.9))
ejes[0].annotate("hacia 10.000 ya nadie se separa de la linea",
                 xy=(30000, 3.46), xytext=(60, 2.6), color=TEXTO, fontsize=8.5,
                 arrowprops=dict(arrowstyle="->", color=TEXTO, linewidth=0.9))
ejes[0].set_title("La media acumulada de un dado se pega a 3,5")
ejes[0].set_xlabel("número de tiradas (escala logaritmica)")
ejes[0].set_ylabel("media acumulada")
ejes[0].set_ylim(1.0, 4.4)
rejilla(ejes[0])
numeros(ejes[0], ejes="x")

# --- Derecha: cuanto se desvian 400 replicas de la media, tamano a tamano.
desviaciones = np.empty((replicas, len(tamanos)))
for j, m in enumerate(tamanos):
    desviaciones[:, j] = azar.integers(1, 7, size=(replicas, m)).mean(axis=1)
medida = desviaciones.std(axis=0, ddof=1)
teorica = sigma / np.sqrt(tamanos)

ejes[1].plot(tamanos, teorica, color=TEXTO, linewidth=1.3, linestyle=":",
             label="teórica: sigma / raiz de n")
ejes[1].plot(tamanos, medida, color=AZUL, linewidth=1.8, marker="o", markersize=4.5,
             label="medida en 400 replicas")
ejes[1].set_xscale("log")
ejes[1].set_yscale("log")
ejes[1].annotate("cuatro veces más tiradas\npara la mitad de error:\n10 veces menos, 100 veces más datos",
                 xy=(1000, teorica[4]), xytext=(11, 0.016), color=NARANJA, fontsize=8.5,
                 arrowprops=dict(arrowstyle="->", color=NARANJA, linewidth=0.9))
ejes[1].set_title("El error baja con la raiz de n")
ejes[1].set_xlabel("tamaño de la muestra (escala logaritmica)")
ejes[1].set_ylabel("desviación típica de las medias")
ejes[1].legend(loc="upper right")
rejilla(ejes[1])
numeros(ejes[1], ejes="x")

guardar(fig, "lgd-media-y-ritmo-de-convergencia")
