"""arima-sarima-1.py — la diferencia entre la memoria del AR y la del MA.

Un AR(1) arrastra el nivel durante muchos pasos y vuelve a su media; un MA(1) arrastra el shock
un solo paso y después lo olvida. La figura de la pagina de ARIMA y SARIMA (fase 5)."""

import numpy as np

from comun import *

estilo()

c, phi = 5.0, 0.5                           # los parametros del AR(1)
media = c / (1 - phi)                       # media de largo plazo: 10
h = np.arange(0, 9)
camino = [13.0]                             # ultima observacion de la serie: 13
for _ in range(8):
    camino.append(c + phi * camino[-1])
camino = np.array(camino)

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.1))

# --- Panel 1: pronosticos de un AR(1): vuelven a la media ---------------------
ejes[0].plot(h, camino, color=AZUL, linewidth=1.9, marker="o", markersize=4)
ejes[0].axhline(media, color=ROJO, linewidth=1.4, linestyle="--")
ejes[0].axhline(camino[0], color=REJILLA, linewidth=1.2, linestyle=":")
ejes[0].set_ylim(9.3, 13.5)
ejes[0].set_title("El AR vuelve a su media, y no la olvida")
ejes[0].set_xlabel("pasos hacia delante")
ejes[0].set_ylabel("pronostico")
rejilla(ejes[0])
numeros(ejes[0])
anotar(ejes[0], "hoy: el último dato, 13",
      xy=(0, 13), xytext=(0.30, 0.93), color=TEXTO)
anotar(ejes[0], "la media de largo plazo es c/(1-phi) = 10",
      xy=(6.5, media), xytext=(0.22, 0.67), color=ROJO)
anotar(ejes[0], "cada paso recorta la distancia a la media en un factor phi:\nquedan 3, 1,5, 0,75... y el pronostico se aplana en 10",
      xy=(2, camino[2]), xytext=(0.05, 0.05), color=AZUL, flecha=False)

# --- Panel 2: pronosticos de un MA(1): olvidan el shock -----------------------
mu, theta, shock = 10.0, 0.6, -2.0
h2 = np.arange(0, 4)
camino_ma = np.array([mu + theta * shock, mu, mu, mu])

ejes[1].plot(h2, camino_ma, color=MORADO, linewidth=1.9, marker="o", markersize=5)
ejes[1].axhline(mu, color=ROJO, linewidth=1.4, linestyle="--")
ejes[1].axhline(mu + theta * shock, color=CIAN, linewidth=1.2, linestyle=":")
ejes[1].set_ylim(8.4, 11.1)
ejes[1].set_title("El MA olvida el shock tras un paso")
ejes[1].set_xlabel("pasos hacia delante")
ejes[1].set_ylabel("pronostico")
rejilla(ejes[1])
numeros(ejes[1])
anotar(ejes[1], "el shock de ayer valia -2:\nhoy arrastra 0,6 veces eso",
      xy=(0, mu + theta * shock), xytext=(0.10, 0.30), color=CIAN)
anotar(ejes[1], "del segundo paso en adelante\nel pronostico ya es la media",
      xy=(2, mu), xytext=(0.26, 0.84), color=MORADO)
ejes[1].text(1.5, 8.58, "la media del proceso, mu = 10", color=ROJO, fontsize=9, ha="center")

guardar(fig, "arima-memoria-ar-frente-a-ma")
