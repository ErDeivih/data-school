"""quantconnect-y-lean-1.py — el filtro de universo de la plataforma se hace sobre dinero
negociado al dia, no sobre el precio de la accion. Figura de la pagina de QuantConnect y LEAN
(fase 9)."""

import numpy as np

from comun import *

estilo()

simbolos = ["AAA", "BBB", "CCC", "DDD", "EEE"]
precio = np.array([12.5, 340.0, 8.2, 95.0, 45.0])
volumen = np.array([4_000_000, 120_000, 25_000_000, 900_000, 3_100_000], dtype=float)
dolares = precio * volumen / 1e6            # millones de dolares negociados al dia
umbral = 60.0
pasa = dolares > umbral
x = np.arange(len(simbolos))

fig, ejes = plt.subplots(2, 1, figsize=(7.0, 5.8), sharex=True)

# --- arriba: el filtro grueso que aplica el motor
colores = [VERDE if ok else ROJO for ok in pasa]
ejes[0].bar(x, dolares, width=0.62, color=colores, alpha=0.75, zorder=2)
ejes[0].axhline(umbral, color=ROJO, linewidth=1.2, linestyle="--", zorder=3)
for xi, d in zip(x, dolares):
    ejes[0].text(xi, d + 5, f"{d:.1f}".replace(".", ","), ha="center", fontsize=8.5, color=TEXTO)
ejes[0].set_xlim(-0.75, 4.75)
ejes[0].set_ylim(0, 245)
ejes[0].text(-0.6, 67, "umbral: 60 millones", color=ROJO, fontsize=8.5)
titulo(ejes[0], "El filtro de universo: dinero negociado",
       "cada barra es precio x volumen; en verde los que pasan el umbral")
ejes[0].set_ylabel("millones de USD al dia")
anotar(ejes[0], "AAA y BBB no llegan al umbral:\nse quedan fuera del universo",
       xy=(1, dolares[1] + 8), xytext=(0.03, 0.62), color=ROJO)
anotar(ejes[0], "pasan CCC, DDD y EEE", xy=(2, dolares[2]),
       xytext=(0.97, 0.88), color=VERDE, align="right")
rejilla(ejes[0])
numeros(ejes[0], "y")

# --- abajo: el precio, que es lo que NO se usa para filtrar
ejes[1].bar(x, precio, width=0.62, color=AZUL, alpha=0.75, zorder=2)
for xi, p in zip(x, precio):
    ejes[1].text(xi, p + 9, f"{p:.1f}".replace(".", ","), ha="center", fontsize=8.5, color=TEXTO)
ejes[1].set_ylim(0, 405)
titulo(ejes[1], "El precio solo: ordena al reves",
       "la accion con el precio más alto es la segunda menos negociada")
ejes[1].set_ylabel("USD por accion")
ejes[1].set_xticks(x)
ejes[1].set_xticklabels(simbolos)
anotar(ejes[1], "eligiendo por precio ganarian BBB y DDD;\npor liquidez ganan CCC y EEE",
       xy=(1, precio[1]), xytext=(0.42, 0.60), color=TEXTO)
rejilla(ejes[1])
numeros(ejes[1], "y")

guardar(fig, "quantconnect-universo-por-liquidez")
