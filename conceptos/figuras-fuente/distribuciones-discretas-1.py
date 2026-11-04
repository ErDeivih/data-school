"""distribuciones-discretas-1.py - el mismo mecanismo cuenta dos cosas distintas: la
binomial con n enorme y p diminuta se pega a la Poisson, y su cola no. Figura de la
pagina de distribuciones discretas."""

import numpy as np
from scipy import stats

from comun import *

estilo()

k = np.arange(0, 14)
n, p = 10000, 0.00025          # n * p = 2,5: el limite que define la Poisson
lam = n * p
binomial = stats.binom.pmf(k, n, p)
poisson = stats.poisson.pmf(k, lam)
sobredis = stats.nbinom.pmf(k, 1.0, 1 / 3.5)   # misma media 2,5, varianza 8,75

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.2))

# --- Izquierda: el centro. Dos modelos distintos que dan casi el mismo numero.
marcas, tallos, linea = ejes[0].stem(k, binomial, basefmt=" ", label="binomial n = 10.000, p = 0,00025")
plt.setp(marcas, color=AZUL, markersize=5)
plt.setp(tallos, color=AZUL, linewidth=1.3)
marcas2, tallos2, _ = ejes[0].stem(k + 0.16, poisson, basefmt=" ", label="Poisson con lambda = n · p = 2,5")
plt.setp(marcas2, color=ROJO, markersize=3.4)
plt.setp(tallos2, color=ROJO, linewidth=0.9, linestyle="--")
# La nota va a la derecha de las barras altas (a partir de k = 5 ya no hay nada) en vez
# de encima de los tallos, que era donde se pisaba con las barras y con su propia flecha.
anotar(ejes[0], "las dos barras son casi la misma altura:\nla binomial con n enorme es una Poisson",
       xy=(2.16, 0.24), xytext=(0.42, 0.46))
titulo(ejes[0], "El centro: la binomial se pega a la Poisson")
ejes[0].set_xlabel("número de sucesos en el intervalo")
ejes[0].set_ylabel("probabilidad")
ejes[0].set_ylim(0, 0.37)
ejes[0].legend(loc="upper right")
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="x")

# --- Derecha: la cola. Ahi es donde la media y la varianza deciden quien manda.
ejes[1].plot(k, poisson, color=ROJO, linewidth=1.6, marker="o", markersize=3.4,
             label="Poisson: media = varianza = 2,5")
ejes[1].plot(k, sobredis, color=MORADO, linewidth=1.6, marker="s", markersize=3.4,
             label="binomial negativa: media 2,5 y varianza 8,75")
ejes[1].set_yscale("log")
ejes[1].set_ylim(1e-6, 2)
anotar(ejes[1], "misma media, cola 16 veces mayor:\nla varianza (8,75 frente a 2,5)\nes la que elige el modelo",
       xy=(9, 1.4e-4), xytext=(0.36, 0.17), color=MORADO)
titulo(ejes[1], "La cola: la Poisson se queda corta",
       "con sobredispersión (varianza 8,75 frente a 2,5) la cola se alarga")
ejes[1].set_xlabel("número de sucesos en el intervalo")
ejes[1].set_ylabel("probabilidad (escala logaritmica)")
ejes[1].legend(loc="upper right")
rejilla(ejes[1], eje="both")
numeros(ejes[1], ejes="x")

guardar(fig, "discretas-binomial-pn-limite-y-cola")
