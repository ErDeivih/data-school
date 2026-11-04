"""ordenacion-externa-1.py — cuántas pasadas por el disco cuesta ordenar 10 GB según las vías de
la fusión, y cuánto se alarga cada vuelta con la selección por reemplazo. Página de ordenación
externa (fase 10)."""

import numpy as np

from comun import *
import heapq

estilo()
azar = np.random.default_rng(7)

# --- Izquierda: el tráfico de disco depende de las rondas, no de las comparaciones.
n, M, bytes_registro = 100_000_000, 1_000_000, 100     # 10 GB de datos, 100 MB de memoria


def trafico_gb(vias):
    """GB leídos y escritos: una pasada para crear las vueltas y una por ronda de fusión."""
    vueltas, rondas = -(-n // M), 0
    while vueltas > 1:
        vueltas = -(-vueltas // vias)
        rondas += 1
    return 2 * n * (1 + rondas) * bytes_registro / 1e9


vias = np.array([2, 4, 8, 16, 32, 64, 128, 256])
gb = np.array([trafico_gb(int(k)) for k in vias])

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.5))

ejes[0].semilogx(vias, gb, color=AZUL, linewidth=2.0, marker="o", markersize=5)
ejes[0].axhline(gb[-1], color=REJILLA, linewidth=1.2, linestyle=":")
anotar(ejes[0], "40 GB es el suelo: una sola ronda\nno se puede bajar de ahí",
       xy=(256, gb[-1]), xytext=(0.03, 0.20), color=REJILLA, flecha=False)
anotar(ejes[0], f"de 4 a 128 vías el tráfico\ncae de {gb[1]:.0f} a {gb[-2]:.0f} GB",
       xy=(128, gb[-2]), xytext=(0.36, 0.86), color=AZUL, flecha=False)
titulo(ejes[0], "Más vías, menos pasadas por el disco",
       "10 GB de datos con 100 MB de memoria: cada ronda lee y escribe todo otra vez")
ejes[0].set_xlabel("vías de la fusión k")
ejes[0].set_ylabel("tráfico de disco (GB)")
ejes[0].set_xticks(vias)
ejes[0].set_xticklabels([str(int(k)) for k in vias])
ejes[0].set_ylim(30, 150)
ejes[0].minorticks_off()
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="both")

# --- Derecha: la selección por reemplazo alarga la vuelta hasta casi 2M.
M_vuelta = 500
datos = list(azar.integers(0, 10 ** 9, size=20000).tolist())

i, largos, monton = 0, [], []
while i < len(datos) or monton:
    while len(monton) < M_vuelta and i < len(datos):
        heapq.heappush(monton, datos[i])
        i += 1
    congelados, larga = [], 0
    while monton:
        x = heapq.heappop(monton)
        larga += 1
        if i < len(datos):
            nuevo = datos[i]
            i += 1
            if nuevo >= x:
                heapq.heappush(monton, nuevo)
            else:
                congelados.append(nuevo)
    largos.append(larga)
    monton = congelados
    heapq.heapify(monton)

media = sum(largos) / len(largos)
sin_reemplazo = -(-len(datos) // M_vuelta)

barras = ejes[1].bar(["vuelta de M", "selección\npor reemplazo"], [M_vuelta, media],
                     color=[REJILLA, VERDE], width=0.55)
ejes[1].axhline(2 * M_vuelta, color=MORADO, linewidth=1.4, linestyle="--")
anotar(ejes[1], "el techo teórico: 2M = 1.000", xy=(1.2, 2 * M_vuelta),
       xytext=(0.03, 0.94), color=MORADO, flecha=False)
anotar(ejes[1], f"con vueltas de M salen {sin_reemplazo} vueltas", xy=(0, M_vuelta),
       xytext=(0.03, 0.60), color=TEXTO, flecha=False)
anotar(ejes[1], f"con selección por reemplazo, {len(largos)} vueltas\nde {media:.0f} registros de media",
       xy=(1, media), xytext=(0.03, 0.44), color=VERDE, flecha=False)
titulo(ejes[1], "La vuelta se alarga hasta casi 2M",
       "longitud media de cada vuelta con 20.000 registros y M = 500")
ejes[1].set_ylabel("registros por vuelta")
ejes[1].set_ylim(0, 1250)
rejilla(ejes[1], eje="y")
numeros(ejes[1], ejes="y")

guardar(fig, "ordenacion-externa-rondas-y-vuelta")
