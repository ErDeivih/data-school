"""contraste-de-hipotesis-1.py — dos caras del mismo contraste: la región crítica sobre la
distribución nula del estadístico y el intervalo de confianza de la media. Las ocho piezas
del ejemplo (media 5,450 mm frente a una tolerancia de 5,500). Figura de la página de
contraste de hipótesis."""

import numpy as np
from scipy import stats

from comun import *

estilo()

piezas = np.array([5.2, 4.8, 6.1, 5.5, 4.9, 5.8, 5.0, 6.3])
n = piezas.size
media = piezas.mean()                     # 5,450 mm
error = piezas.std(ddof=1) / np.sqrt(n)   # 0,2009 mm
t_obs = (media - 5.5) / error             # -0,249
t_crit = stats.t.ppf(0.975, df=n - 1)     # 2,365 con 7 grados de libertad
bajo, alto = media - t_crit * error, media + t_crit * error

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.1))

# --- Izquierda: la distribución de t bajo H0 y la zona en la que se rechaza.
eje = np.linspace(-4.6, 4.6, 1200)
dens = stats.t.pdf(eje, df=n - 1)
ejes[0].plot(eje, dens, color=AZUL, linewidth=1.8)
cola = np.abs(eje) >= t_crit
ejes[0].fill_between(eje, dens, where=cola, color=ROJO, alpha=0.22)
ejes[0].axvline(t_crit, color=ROJO, linewidth=1.1, linestyle="--")
ejes[0].axvline(-t_crit, color=ROJO, linewidth=1.1, linestyle="--")
ejes[0].axvline(t_obs, color=MORADO, linewidth=1.8)
anotar(ejes[0], "región crítica:\n|t| > 2,365", xy=(3.4, 0.05), xytext=(0.80, 0.55),
       color=ROJO)
anotar(ejes[0], "lo observado, t = −0,249:\nse queda muy lejos del umbral",
       xy=(t_obs, 0.30), xytext=(0.06, 0.92), color=MORADO)
ejes[0].set_xlabel("valor del estadístico t si H₀ fuera cierta")
ejes[0].set_ylabel("densidad")
ejes[0].set_ylim(0, 0.46)
titulo(ejes[0], "No cae en la región crítica: no se rechaza",
       "una t de −0,249 es un resultado corriente cuando la máquina está centrada")
rejilla(ejes[0])
numeros(ejes[0], ejes="x")

# --- Derecha: el intervalo del 95 % de la media. Es el mismo juicio, en milimetros.
ejes[1].plot([bajo, alto], [0, 0], color=AZUL, linewidth=7, solid_capstyle="butt")
ejes[1].axvline(media, color=MORADO, linewidth=1.6, linestyle="--")
ejes[1].axvline(5.5, color=VERDE, linewidth=1.6)
ejes[1].plot([6.0], [0], "o", color=ROJO, markersize=8, zorder=3)
anotar(ejes[1], "μ₀ = 5,500 está dentro:\np = 0,811, no se rechaza",
       xy=(5.5, 0.06), xytext=(0.06, 0.80), color=VERDE)
anotar(ejes[1], "μ₀ = 6,000 queda fuera:\np = 0,029, se rechaza",
       xy=(6.0, -0.06), xytext=(0.62, 0.26), color=ROJO)
anotar(ejes[1], "la media muestral, 5,450", xy=(media, -0.05), xytext=(0.06, 0.34),
       color=MORADO)
ejes[1].set_xlabel("media poblacional (milímetros)")
ejes[1].set_ylim(-0.45, 0.45)
ejes[1].set_yticks([])
ejes[1].set_xlim(4.5, 6.5)
titulo(ejes[1], "El intervalo del 95 % de la media",
       "todo valor nulo que caiga fuera se rechaza al mismo nivel")
rejilla(ejes[1], eje="x")
numeros(ejes[1], ejes="x")

guardar(fig, "contraste-region-critica-y-su-intervalo")
