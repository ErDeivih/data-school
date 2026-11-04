"""modelos-de-difusion-1.py — la senal que queda y el error que se amplifica a lo largo de
la cadena de ruido. La figura de la pagina de modelos de difusión (fase 7)."""

import numpy as np

from comun import *

estilo()
T = 1000                                        # numero de pasos del proceso directo
betas = np.linspace(1e-4, 0.02, T)              # calendario lineal: fijo, no se aprende
abar = np.cumprod(1.0 - betas)                  # alpha_bar_t: cuanto queda de la senal original
t = np.arange(T)

fig, ejes = plt.subplots(1, 2, figsize=(9.4, 3.9))

# --- Panel 1: los dos pesos de la forma cerrada ---
ejes[0].plot(t, np.sqrt(abar), color=AZUL, linewidth=2.0)
ejes[0].plot(t, np.sqrt(1 - abar), color=ROJO, linewidth=2.0)
titulo(ejes[0], "La senal se apaga y el ruido crece",
       "los dos pesos al cuadrado suman 1 en todo momento")
ejes[0].set_xlabel("paso t del proceso directo")
ejes[0].set_ylabel("peso de cada termino")
anotar(ejes[0], "peso de la senal", xy=(150, np.sqrt(abar[150])), xytext=(0.05, 0.82), color=AZUL)
anotar(ejes[0], "peso del ruido", xy=(150, np.sqrt(1 - abar[150])), xytext=(0.05, 0.30), color=ROJO)
rejilla(ejes[0])
numeros(ejes[0])

# --- Panel 2: relacion senal-ruido y amplificacion de un error en eps ---
snr = abar / (1 - abar)
ampl = np.sqrt((1 - abar) / abar)               # cuanto se amplifica un fallo al estimar x0
ejes[1].semilogy(t, snr, color=VERDE, linewidth=2.0)
ejes[1].semilogy(t, ampl, color=MORADO, linewidth=2.0, linestyle="--")
ejes[1].axhline(1.0, color=REJILLA, linewidth=1.0, linestyle=":")
titulo(ejes[1], "De aqui sale la escala de cada paso",
       "la red tiene que saber en que paso esta")
ejes[1].set_xlabel("paso t del proceso directo")
ejes[1].set_ylabel("factor (escala logaritmica)")
anotar(ejes[1], "SNR: senal partido por ruido", xy=(300, snr[300]), xytext=(0.10, 0.74), color=VERDE)
anotar(ejes[1], "amplifica un error en eps", xy=(800, ampl[800]), xytext=(0.05, 0.26), color=MORADO)
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "modelos-de-difusion-senal-y-error")
