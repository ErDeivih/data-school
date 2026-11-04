"""data-snooping-y-multiple-testing-1.py — probar muchas ideas: la probabilidad de que
alguna salga significativa por azar y donde cae el máximo de puro ruido. Figura de la
pagina de data snooping (fase 9)."""

import numpy as np
from statistics import NormalDist

from comun import *

estilo()
Z = NormalDist()
azar = np.random.default_rng(0)

fig, ejes = plt.subplots(2, 1, figsize=(7.2, 6.6))

# --- Arriba: la tasa de error por familia crece con el numero de intentos -------------
m = np.unique(np.round(np.logspace(0, 3.3, 200)).astype(int))
fwer = 1 - (1 - 0.05) ** m
ejes[0].plot(m, fwer, color=AZUL, linewidth=1.9)
ejes[0].axhline(0.05, color=ROJO, linewidth=1.3, linestyle="--")
ejes[0].set_xscale("log")
ejes[0].set_ylim(0, 1.12)
ejes[0].set_xlabel("m: número de variantes probadas (escala logarítmica)")
ejes[0].set_ylabel("P(algún falso positivo)")
titulo(ejes[0], "Probar 20 variantes sin ninguna habilidad: 64 % de «descubrir» algo",
       "la probabilidad de que aparezca al menos un falso positivo se acumula con cada intento")
anotar(ejes[0], "el 5 % que crees que tienes\nen un solo contraste", xy=(1.4, 0.05),
       xytext=(0.02, 0.30), color=ROJO)
anotar(ejes[0], f"con m = 20: {1 - 0.95 ** 20:.2f}".replace(".", ","), xy=(20, 1 - 0.95 ** 20),
       xytext=(0.28, 0.72), color=AZUL)
anotar(ejes[0], "con m = 1 000: 0,994", xy=(1000, 1 - 0.95 ** 1000),
       xytext=(0.98, 0.48), color=AZUL, align="right")
rejilla(ejes[0], "both")
numeros(ejes[0], "y")

# --- Abajo: el mejor de mil intentos nulos no es un hallazgo --------------------------
n_est, dias = 1000, 250
r = azar.normal(0.0, 0.01, size=(n_est, dias))
t = r.mean(axis=1) / (r.std(axis=1, ddof=1) / np.sqrt(dias))
mejor = float(t.max())
umbr_bonf = float(Z.inv_cdf(1 - 0.025 / n_est))
esperado = float(np.sqrt(2 * np.log(n_est)))

ejes[1].hist(t, bins=60, color=AZUL, alpha=0.7, edgecolor="none")
# Las rayas se cortan antes del techo para dejar libre la banda donde van las etiquetas.
for x, color in ((2.0, ROJO), (mejor, VERDE), (esperado, MORADO), (umbr_bonf, NARANJA)):
    ejes[1].plot([x, x], [0, 56], color=color, linewidth=1.5,
                 linestyle="--" if color == ROJO else ":", solid_capstyle="butt")
ejes[1].set_ylim(0, 88)
ejes[1].set_xlabel("estadístico t de cada variante")
ejes[1].set_ylabel("nº de variantes")
titulo(ejes[1], f"1 000 variantes sin ninguna habilidad: la mejor da t = {mejor:.2f}".replace(".", ","),
       "el máximo de puro ruido crece con el número de intentos, y aquí no llega ni a eso")
anotar(ejes[1], "t = 2: el umbral del 5 % si fuera un solo contraste",
       xy=(2.0, 56), xytext=(0.99, 0.94), color=ROJO, align="right", flecha=False)
anotar(ejes[1], f"t = {mejor:.2f}: lo que dio la mejor de las 1 000".replace(".", ","),
       xy=(mejor, 56), xytext=(0.99, 0.86), color=VERDE, align="right", flecha=False)
anotar(ejes[1], f"t = {esperado:.2f}: lo que da el azar con 1 000 intentos".replace(".", ","),
       xy=(esperado, 56), xytext=(0.99, 0.78), color=MORADO, align="right", flecha=False)
anotar(ejes[1], f"t = {umbr_bonf:.2f}: lo que exigiría Bonferroni".replace(".", ","),
       xy=(umbr_bonf, 56), xytext=(0.99, 0.70), color=NARANJA, align="right", flecha=False)
rejilla(ejes[1])
numeros(ejes[1], "x")

guardar(fig, "snooping-maximo-por-azar")
