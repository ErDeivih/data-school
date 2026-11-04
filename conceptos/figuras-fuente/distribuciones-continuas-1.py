"""distribuciones-continuas-1.py - la lognormal: log(X) es simétrica, X no. La cola
derecha separa la media de la mediana. Figura de la pagina de distribuciones continuas."""

import numpy as np
from scipy import stats

from comun import *

estilo()

x = np.linspace(0.01, 3.5, 1500)
sigma = 0.5
y = np.log(x)                       # log(X) es normal: simetrica en la escala del logaritmo
dens = stats.lognorm.pdf(x, s=sigma)
mediana = np.exp(0.0)
media = np.exp(sigma ** 2 / 2)
p95 = stats.lognorm.ppf(0.95, s=sigma)

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.2))

# --- Izquierda: la densidad de X frente a la densidad de log(X).
ejes[0].plot(x, dens, color=AZUL, linewidth=1.8)
ejes[0].fill_between(x, dens, color=AZUL, alpha=0.10)
ejes[0].axvline(mediana, color=VERDE, linewidth=1.4)
ejes[0].axvline(media, color=ROJO, linewidth=1.4, linestyle="--")
# Las tres notas van a la derecha del pico, escalonadas en vertical: la curva ya está
# baja por ahí y así ninguna cae encima de la densidad ni de otra nota.
anotar(ejes[0], "mediana 1,00", xy=(mediana, 0.90), xytext=(0.40, 0.95), color=VERDE)
anotar(ejes[0], "media 1,13: la cola\nla empuja a la derecha", xy=(media, 0.80),
       xytext=(0.42, 0.72), color=ROJO)
anotar(ejes[0], "el 5 % de arriba empieza aquí\n(2,28: más del doble de la mediana)",
       xy=(p95, 0.03), xytext=(0.50, 0.34), color=MORADO)
titulo(ejes[0], "La variable X: asimétrica",
       "la cola de la derecha tira de la media y separa las dos medidas")
ejes[0].set_xlabel("valor de la variable (ingresos, precios, tamaños)")
ejes[0].set_ylabel("densidad")
ejes[0].set_ylim(0, 1.05)
rejilla(ejes[0])
numeros(ejes[0], ejes="x")

# --- Derecha: la misma variable mirada en escala logaritmica: ahi si es simetrica.
ejes[1].plot(y, dens * x, color=CIAN, linewidth=1.8)   # densidad de log(X): regla del cambio
ejes[1].fill_between(y, dens * x, color=CIAN, alpha=0.10)
ejes[1].axvline(0.0, color=VERDE, linewidth=1.4)
anotar(ejes[1], "aquí la mediana es el centro", xy=(0.0, 0.93), xytext=(0.05, 0.62),
       color=VERDE)
titulo(ejes[1], "Su logaritmo: simétrico y centrado",
       "en la escala del logaritmo la cola se reparte a los dos lados")
ejes[1].set_xlabel("logaritmo del valor")
ejes[1].set_ylabel("densidad de log(X)")
ejes[1].set_ylim(0, 1.05)
rejilla(ejes[1])
numeros(ejes[1], ejes="x")

guardar(fig, "continuas-lognormal-media-y-mediana")
