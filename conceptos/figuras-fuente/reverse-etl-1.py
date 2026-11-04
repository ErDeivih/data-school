"""reverse-etl-1.py — que manda más: el tamaño del lote o filtrar lo que cambio (fase 4).

Izquierda: duración de la sincronización segun los registros que hay que escribir, con dos
tamaños de lote. Derecha: las llamadas que necesita cada estrategia.
"""

import numpy as np

from comun import *

estilo()

ritmo = 5.0   # llamadas por segundo que permite la API

filas = np.logspace(2, 6, 400)

fig, ejes = plt.subplots(1, 2, figsize=(7.6, 3.7))

eje = ejes[0]
for lote, color in ((200, AZUL), (1000, NARANJA)):
    eje.plot(filas, np.ceil(filas / lote) / ritmo, color=color, linewidth=1.8)
eje.set_xscale("log")
eje.set_yscale("log")
eje.set_xlabel("registros que cambian")
eje.set_ylabel("duración (s)")
eje.set_xticks([100, 1000, 10000, 100000])
titulo(eje, "Filtrar lo cambiado manda más que el lote")
eje.axvline(3200, color=VERDE, linewidth=1.1, linestyle=":")
eje.axvline(480000, color=ROJO, linewidth=1.1, linestyle=":")
eje.text(0.06, 0.90, "lote de 200", transform=eje.transAxes, color=AZUL, fontsize=9)
eje.text(0.06, 0.76, "lote de 1.000", transform=eje.transAxes, color=NARANJA, fontsize=9)
anotar(eje, "3.200 cambios: 3 segundos", xy=(3200, 3.2), xytext=(0.30, 0.16), color=VERDE)
rejilla(eje, eje="both")
numeros(eje)

eje = ejes[1]
llamadas = [2400, 16]
eje.bar(["carga\ncompleta", "solo lo\ncambiado"], llamadas, color=[ROJO, VERDE], width=0.5)
for posicion, valor in enumerate(llamadas):
    eje.text(posicion, valor + 80, f"{valor}", ha="center", color=TEXTO, fontsize=9)
eje.set_ylabel("llamadas a la API")
titulo(eje, "Contar solo lo cambiado: 16 llamadas")
anotar(eje, "150 veces menos", xy=(1, 200), xytext=(0.40, 0.55), color=VERDE)
rejilla(eje)
numeros(eje, ejes="y")

guardar(fig, "reverse-etl-lote-y-cambio")
