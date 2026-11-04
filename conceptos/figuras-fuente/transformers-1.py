"""transformers-1.py — el precio del transformer: cuándo manda la atención y qué memoria pide.

Izquierda: el coste por capa de las dos subcapas. La red hacia delante crece con n y la
atención con n², así que se cruzan en n = d_ff = 2.048: por debajo manda la FFN y por encima
la atención, y por goleada.
Derecha: la memoria de las matrices de atención, que también crece con n². Con 2.048 tokens
son 128 MiB por capa, y 3 GB en un modelo de 24 capas: es el motivo real de que el contexto
largo sea caro.
La figura de la página de transformers (fase 7).
"""

import numpy as np

from comun import *

estilo()

D_MODEL, D_FF, CABEZAS = 512, 2048, 8

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.4))

# --- Izquierda: cuándo manda cada subcapa ---------------------------------------------
ax = ejes[0]
n = np.logspace(np.log10(32), np.log10(16384), 300)
# Las dos cuentas de la página: 2n²d para la atención y 2n·d·d_ff para la red hacia delante.
atencion = 2 * n ** 2 * D_MODEL / 1e9
ffn = 2 * n * D_MODEL * D_FF / 1e9
ax.loglog(n, ffn, color=AZUL, linewidth=1.8)
ax.loglog(n, atencion, color=ROJO, linewidth=1.8)
# El cruce: 2n²d = 2n·d·d_ff se simplifica a n = d_ff.
cruce = 2 * D_FF ** 2 * D_MODEL / 1e9
ax.plot([D_FF], [cruce], marker="o", markersize=7, color=TEXTO, zorder=3)
anotar(ax, "la red hacia delante manda\npor debajo de n = 2.048",
       xy=(128, 2 * 128 * D_MODEL * D_FF / 1e9), xytext=(0.04, 0.88), color=AZUL)
anotar(ax, "la atención manda por encima\ny crece con n²",
       xy=(8192, 2 * 8192 ** 2 * D_MODEL / 1e9), xytext=(0.50, 0.13), color=ROJO)
titulo(ax, "Atención y FFN se cruzan en n = 2.048",
       "coste por capa con d_model 512 y d_ff 2.048, en escala doble logarítmica")
ax.set_xlabel("tokens de la secuencia (n)")
ax.set_ylabel("miles de millones de operaciones (GFLOP)")
ax.set_xticks([64, 256, 1024, 4096, 16384])
ax.set_ylim(1e-3, 5e3)                  # deja aire arriba para las notas
rejilla(ax, eje="both")
numeros(ax)

# --- Derecha: la memoria de la matriz de atención -------------------------------------
ax = ejes[1]
n = np.logspace(np.log10(128), np.log10(8192), 300)
por_capa = CABEZAS * n ** 2 * 4 / 2 ** 20          # cabezas x n² x 4 bytes (float32), en MiB
ax.loglog(n, por_capa, color=AZUL, linewidth=1.8)
ax.loglog(n, 24 * por_capa, color=ROJO, linewidth=1.8)
# Los tres tamaños que cita la página, marcados sobre la curva de una sola capa.
ax.plot([512, 1024, 2048], [CABEZAS * d ** 2 * 4 / 2 ** 20 for d in (512, 1024, 2048)],
        linestyle="none", marker="o", markersize=5, color=AZUL)
anotar(ax, "24 capas con 2.048 tokens:\n3 GB solo en atención",
       xy=(2048, 24 * CABEZAS * 2048 ** 2 * 4 / 2 ** 20), xytext=(0.04, 0.86), color=ROJO)
anotar(ax, "una capa: 8, 32 y 128 MiB\ncon 512, 1.024 y 2.048 tokens",
       xy=(1024, CABEZAS * 1024 ** 2 * 4 / 2 ** 20), xytext=(0.46, 0.16), color=AZUL)
titulo(ax, "La memoria de atención crece con n²",
       "matrices de 8 cabezas en float32, por capa, en mebibytes")
ax.set_xlabel("tokens de la secuencia (n)")
ax.set_ylabel("memoria de las matrices (MiB)")
ax.set_xticks([128, 256, 512, 1024, 2048, 4096, 8192])
ax.set_ylim(0.2, 2e5)                   # deja aire arriba para la nota
rejilla(ax, eje="both")
numeros(ax)

guardar(fig, "transformers-coste-y-memoria")
