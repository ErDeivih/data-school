"""teorema-central-del-limite-1.py - la media de muchos datos se vuelve normal aunque los
datos no lo sean, y la aproximación falla primero en las colas."""

import numpy as np
from scipy import stats

from comun import *

estilo()

azar = np.random.default_rng(0)
replicas = 4000
tamanos = [1, 5, 30, 200]
medias = {m: azar.exponential(scale=1.0, size=(replicas, m)).mean(axis=1) for m in tamanos}
errores = {m: medias[m].std(ddof=1) for m in tamanos}      # error tipico real de cada tamano

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.0))

# --- Izquierda: la forma de la distribucion de la media segun el tamano de muestra.
colores = {1: ROSA, 5: MORADO, 30: VERDE, 200: AZUL}
for m in tamanos:
    z = (medias[m] - 1.0) / errores[m]                    # estandarizada: media 0, varianza 1
    ejes[0].hist(z, bins=70, range=(-4, 4), density=True, histtype="step",
                 color=colores[m], linewidth=1.4)
grigia = np.linspace(-4, 4, 400)
ejes[0].plot(grigia, stats.norm.pdf(grigia), color=TEXTO, linewidth=1.4, linestyle=":")
ejes[0].annotate("normal estandar", xy=(0.35, 0.375), xytext=(1.85, 0.70),
                 color=TEXTO, fontsize=8.5,
                 arrowprops=dict(arrowstyle="->", color=TEXTO, linewidth=0.9))
ejes[0].annotate("media de 1 dato: la cola\nde la exponencial sigue ahi",
                 xy=(2.42, 0.062), xytext=(1.55, 0.30), color=ROSA, fontsize=8.5,
                 arrowprops=dict(arrowstyle="->", color=ROSA, linewidth=0.9,
                                 connectionstyle="arc3,rad=-0.25"))
ejes[0].annotate("media de 200 datos", xy=(1.30, 0.285), xytext=(0.60, 0.535),
                 color=AZUL, fontsize=8.5,
                 arrowprops=dict(arrowstyle="->", color=AZUL, linewidth=0.9))
ejes[0].annotate("con 30 ya es una campana:\naqui el teorema funciona",
                 xy=(1.05, 0.32), xytext=(-4.0, 0.56), color=VERDE, fontsize=8.5,
                 arrowprops=dict(arrowstyle="->", color=VERDE, linewidth=0.9,
                                 connectionstyle="arc3,rad=0.15"))
ejes[0].set_title("La media se vuelve normal; los datos no")
ejes[0].set_xlabel("media de la muestra, estandarizada")
ejes[0].set_ylabel("densidad")
ejes[0].set_ylim(0, 0.79)
rejilla(ejes[0])
numeros(ejes[0], ejes="x")

# --- Derecha: cuantiles. Si la aproximacion fuera perfecta, todo caeria en la diagonal.
z200 = np.sort((medias[200] - 1.0) / errores[200])
prob = (np.arange(1, replicas + 1) - 0.5) / replicas
normal_q = stats.norm.ppf(prob)
t5_q = stats.t.ppf(prob, 5) / np.sqrt(5 / 3)              # t con varianza 1, para comparar
ejes[1].plot([-4.2, 4.2], [-4.2, 4.2], color=TEXTO, linewidth=1.0, linestyle=":")
ejes[1].plot(normal_q, t5_q, color=NARANJA, linewidth=1.3, linestyle="--",
             label="una t de Student con 5 grados de libertad (varianza 1)")
ejes[1].plot(normal_q, z200, color=AZUL, linewidth=1.6,
             label="la media de 200 datos exponenciales")
ejes[1].annotate("en el centro las tres lineas coinciden:\naqui el teorema ya funciona",
                 xy=(-0.4, -0.4), xytext=(-4.1, 0.9), color=TEXTO, fontsize=8.5,
                 arrowprops=dict(arrowstyle="->", color=TEXTO, linewidth=0.9))
ejes[1].annotate("en la cola la t se separa\ny la media también,\npero mucho menos",
                 xy=(3.4, 2.9), xytext=(0.4, 3.35), color=NARANJA, fontsize=8.5,
                 arrowprops=dict(arrowstyle="->", color=NARANJA, linewidth=0.9))
ejes[1].set_title("Cuantiles: quien se separa de la normal y donde")
ejes[1].set_xlabel("cuantil de la normal estandar")
ejes[1].set_ylabel("cuantil observado")
ejes[1].set_xlim(-4.2, 4.2)
ejes[1].set_ylim(-4.2, 5.4)
ejes[1].legend(loc="lower right")
rejilla(ejes[1])
numeros(ejes[1], ejes="both")

guardar(fig, "tcl-media-normal-y-cola")
