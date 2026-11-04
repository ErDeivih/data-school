"""normalizacion-por-lotes-1.py — qué le hace la normalización a un valor y de dónde salen
las estadísticas que se usan en inferencia.

Izquierda: el mismo dato (un 1) dentro de lotes de distinto tamaño. Su valor normalizado
depende mucho de quién le acompañe: −1 en un lote de dos y −0,03 en uno de mil.
Derecha: la media acumulada arranca en cero y tarda decenas de lotes en acercarse al valor
real; ese sesgo inicial es el que estropea las métricas de los primeros pasos.
La figura de la página de normalización por lotes (fase 7).
"""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.4))

# --- Izquierda: el mismo dato, normalizado dentro de lotes de distinto tamaño ---------
ax = ejes[0]
# Lote de m elementos: m-1 unos y un tres. Seguimos el valor normalizado de uno de los unos.
m = np.arange(2, 2001)
media = (m + 2.0) / m                        # ((m-1)·1 + 3) / m
varianza = 4.0 / m - 4.0 / m ** 2            # E[x²] − media², con E[x²] = ((m-1)·1 + 9)/m
x_sombrero = (1.0 - media) / np.sqrt(varianza)
ax.semilogx(m, x_sombrero, color=AZUL, linewidth=1.9)
ax.axhline(0.0, color=TEXTO, linewidth=0.8, alpha=0.35)
anotar(ax, "en un lote de 2 el uno vale −1:\nla normalización lo manda al extremo",
       xy=(2.0, -1.0), xytext=(0.08, 0.15), color=AZUL)
anotar(ax, "en un lote de 1000, −0,03:\nel mismo dato, otra salida",
       xy=(1000.0, -0.0316), xytext=(0.52, 0.86), color=AZUL)
titulo(ax, "El valor normalizado depende del lote que le toque",
       "lote de m elementos con m−1 unos y un tres; se sigue el valor normalizado de un uno")
ax.set_xlabel("tamaño del lote m (escala logarítmica)")
ax.set_ylabel("valor normalizado del uno")
ax.set_ylim(-1.2, 0.3)
rejilla(ax)
numeros(ax)

# --- Derecha: la media acumulada arranca sesgada -------------------------------------
ax = ejes[1]
lotes = np.arange(0, 81)
medias_del_lote = np.array([3.0, 5.0, 7.0])   # tres lotes seguidos, media real 5
for alfa, color in ((0.1, VERDE), (0.01, MORADO)):
    acumulada = np.zeros(lotes.size)
    for t in range(1, lotes.size):
        acumulada[t] = (1 - alfa) * acumulada[t - 1] + alfa * medias_del_lote[(t - 1) % 3]
    ax.plot(lotes, acumulada, color=color, linewidth=1.9,
            label=f"α = {alfa:.2f}".replace(".", ","))
ax.axhline(5.0, color=ROJO, linewidth=1.2, linestyle="--")
anotar(ax, "el valor real de la media es 5", xy=(0.2, 5.0), xytext=(0.12, 0.93), color=ROJO)
anotar(ax, "con α = 0,1 hacen falta unas diez\nactualizaciones para acercarse",
       xy=(3.0, 1.393), xytext=(0.24, 0.40), color=VERDE)
anotar(ax, "con α = 0,01 el sesgo inicial\ndura cientos de lotes",
       xy=(80.0, 3.55), xytext=(0.62, 0.72), color=MORADO)
titulo(ax, "Las estadísticas de inferencia empiezan en cero",
       "media acumulada tras cada lote, con los lotes de media 3, 5 y 7 repetidos")
ax.set_xlabel("lote")
ax.set_ylabel("media acumulada")
ax.set_ylim(-0.25, 5.6)
ax.legend(loc="lower right")
rejilla(ax)
numeros(ax)

guardar(fig, "normalizacion-por-lotes-tamano-y-estadisticas")
