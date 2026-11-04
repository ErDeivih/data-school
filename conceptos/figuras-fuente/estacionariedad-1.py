"""estacionariedad-1.py — por qué una serie con tendencia no es estacionaria y que arregla"
diferenciar. La figura de la pagina de estacionariedad (fase 5)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)
n = 250
pasos = azar.normal(0.08, 1.0, n)          # deriva + ruido
nivel = np.cumsum(pasos)                    # paseo aleatorio con tendencia
cambio = np.diff(nivel)                     # lo que se modela al diferenciar

fig, ejes = plt.subplots(2, 1, figsize=(7.0, 5.2), sharex=True)

ejes[0].plot(nivel, color=AZUL, linewidth=1.6)
ejes[0].axhline(nivel.mean(), color=ROJO, linewidth=1.2, linestyle="--")
ejes[0].set_title("El nivel: la media depende del momento en que mires")
ejes[0].set_ylabel("precio")
ejes[0].annotate("media de toda la serie", xy=(20, nivel.mean()), xytext=(30, nivel.mean() - 14),
                 color=ROJO, fontsize=9,
                 arrowprops=dict(arrowstyle="-", color=ROJO, linewidth=0.9))
rejilla(ejes[0])
numeros(ejes[0])

ejes[1].plot(cambio, color=MORADO, linewidth=1.3)
ejes[1].axhline(cambio.mean(), color=ROJO, linewidth=1.2, linestyle="--")
ejes[1].axhline(0, color=TEXTO, linewidth=0.8, alpha=0.4)
ejes[1].set_title("El cambio (una diferencia): la media ya no se mueve")
ejes[1].set_xlabel("instante")
ejes[1].set_ylabel("variación")
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "estacionariedad-nivel-y-cambio")
