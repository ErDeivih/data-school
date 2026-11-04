"""capa-semantica-y-metricas-1.py — media de ratios frente a ratio del total (fase 4).

Izquierda: la conversión de cada dia, la media de esos ratios y el ratio correcto del total.
Derecha: el trafico de cada dia, que es lo que la media ignora.
"""

import numpy as np

from comun import *

estilo()

visitas = np.array([50, 400, 250])
pedidos = np.array([12, 20, 25])
dias = ["lunes", "martes", "miércoles"]

ratio = pedidos / visitas * 100
correcto = pedidos.sum() / visitas.sum() * 100
media = ratio.mean()

fig, ejes = plt.subplots(1, 2, figsize=(7.6, 3.7))

eje = ejes[0]
eje.bar(dias, ratio, color=AZUL, width=0.55)
eje.axhline(media, color=NARANJA, linewidth=1.6, linestyle="--")
eje.axhline(correcto, color=ROJO, linewidth=1.6)
eje.set_ylabel("conversión (%)")
titulo(eje, "La media de los ratios no es el ratio del total")
anotar(eje, "media de ratios: 13,0 %", xy=(1.5, media), xytext=(0.34, 0.90), color=NARANJA)
anotar(eje, "ratio del total: 8,14 %", xy=(0.5, correcto), xytext=(0.40, 0.66), color=ROJO)
rejilla(eje)
numeros(eje, ejes="y")

eje = ejes[1]
eje.bar(dias, visitas, color=CIAN, width=0.55)
eje.set_ylabel("visitas")
titulo(eje, "El día del 5 % es el que más tráfico tuvo")
anotar(eje, "solo 50 visitas", xy=(0, 50), xytext=(0.03, 0.60), color=CIAN)
rejilla(eje)
numeros(eje, ejes="y")

guardar(fig, "capa-semantica-y-metricas-media-de-ratios")
