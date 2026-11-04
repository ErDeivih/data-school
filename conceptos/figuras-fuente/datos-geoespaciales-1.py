"""datos-geoespaciales-1.py — por qué un grado de longitud no vale lo mismo en todas partes y
cuánto trabajo ahorra la caja envolvente antes de calcular distancias. Figura de la página de
datos geoespaciales (fase 6)."""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.2))

# --- Panel izquierdo: la trampa de tratar los grados como kilómetros constantes.
lat = np.linspace(0.0, 75.0, 400)
km_grado = 111.32 * np.cos(np.radians(lat))
ejes[0].plot(lat, km_grado, color=AZUL, linewidth=1.9, label="lo que mide de verdad")
ejes[0].axhline(111.32, color=ROJO, linewidth=1.4, linestyle="--",
                label="lo que mide si usas 111,32 fijo")
en_60 = 111.32 * np.cos(np.radians(60.0))
anotar(ejes[0], f"a 60° de latitud son {en_60:.1f} km:\nmultiplicas la distancia por dos",
       xy=(60.0, en_60), xytext=(0.34, 0.74), color=ROJO)
ejes[0].set_xlabel("latitud (grados)")
ejes[0].set_ylabel("kilómetros que hay\nen un grado de longitud")
ejes[0].set_ylim(0.0, 125.0)
ejes[0].legend(loc="lower left")
rejilla(ejes[0])
numeros(ejes[0])
titulo(ejes[0], "Un grado de longitud encoge al subir",
       "el error de usar 111,32 fijo crece como 1/cos(latitud) − 1")

# --- Panel derecho: el índice espacial vive de descartar sin medir distancias.
rng = np.random.default_rng(7)
puntos = rng.uniform(0.0, 100.0, (400, 2))       # 400 puntos en una región de 100 x 100 km
qx, qy, radio = 50.0, 50.0, 8.0
distancia = np.hypot(puntos[:, 0] - qx, puntos[:, 1] - qy)
en_circulo = distancia <= radio
en_caja = (np.abs(puntos[:, 0] - qx) <= radio) & (np.abs(puntos[:, 1] - qy) <= radio)

ejes[1].scatter(puntos[~en_caja, 0], puntos[~en_caja, 1], s=8, color=REJILLA, zorder=2)
ejes[1].scatter(puntos[en_caja, 0], puntos[en_caja, 1], s=16, color=AZUL, zorder=3,
                label=f"candidatos dentro de la caja: {int(en_caja.sum())}")
ejes[1].scatter(puntos[en_circulo, 0], puntos[en_circulo, 1], s=26, color=NARANJA, zorder=4,
                label=f"a menos de {radio:.0f} km: {int(en_circulo.sum())}")
caja = plt.Rectangle((qx - radio, qy - radio), 2 * radio, 2 * radio, fill=False,
                     edgecolor=AZUL, linewidth=1.4, zorder=5)
ejes[1].add_patch(caja)
ejes[1].add_patch(plt.Circle((qx, qy), radio, fill=False, edgecolor=NARANJA, linewidth=1.4,
                             zorder=5))
ejes[1].scatter([qx], [qy], marker="x", s=60, color=ROJO, zorder=6)
ahorro = 100.0 * (1.0 - en_caja.sum() / puntos.shape[0])
anotar(ejes[1], f"la caja deja fuera el {ahorro:.0f} % de los puntos\nsin calcular una distancia",
       xy=(qx - radio, qy + radio), xytext=(0.02, 0.72), color=AZUL)
ejes[1].set_xlabel("kilómetros al este")
ejes[1].set_ylabel("kilómetros al norte")
ejes[1].set_aspect("equal")
ejes[1].set_xlim(-2.0, 102.0)
ejes[1].set_ylim(-2.0, 102.0)
ejes[1].legend(loc="lower right")
rejilla(ejes[1], "both")
numeros(ejes[1])
titulo(ejes[1], "La caja descarta antes de medir",
       "el índice espacial filtra por rectángulos y solo mide los candidatos")

guardar(fig, "datos-geoespaciales-grados-y-caja")
