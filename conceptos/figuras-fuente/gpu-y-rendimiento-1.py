"""gpu-y-rendimiento-1.py — cuándo manda el cálculo y cuándo manda la memoria.

Izquierda: el modelo roofline. El rendimiento alcanzable es min(P, I·B): por debajo de la cresta
los núcleos se pasan el rato esperando datos y por encima manda el pico del chip. Los dos puntos
son la misma capa con lote de 1 y con lote de 64: la intensidad aritmética los separa por dos
órdenes de magnitud.
Derecha: de qué se llena la VRAM. Los pesos, sus gradientes y el estado de Adam son un coste fijo
por parámetro; las activaciones crecen con el lote y son lo que decide dónde se acaba la memoria.
La figura de la página de GPU y rendimiento (fase 7).
"""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.4))

# --- Izquierda: el techo de cálculo y el techo de memoria ------------------------------
ax = ejes[0]
P = 30_000.0            # GFLOP/s: 30 TFLOPS de pico de cálculo
B = 1000.0              # GB/s: cada FLOP/byte alimenta 1000 GFLOP/s
intensidad = np.logspace(-1, 3.5, 400)
techo_memoria = intensidad * B
techo_calculo = np.full_like(intensidad, P)
alcanzable = np.minimum(techo_memoria, techo_calculo)

# La zona por debajo de la cresta es lo que de verdad se puede conseguir.
ax.fill_between(intensidad, 1e2, alcanzable, color=REJILLA, alpha=0.16, zorder=1)
ax.loglog(intensidad, techo_memoria, color=AZUL, linewidth=1.5, linestyle="--", zorder=2)
ax.loglog(intensidad, techo_calculo, color=VERDE, linewidth=1.5, linestyle="--", zorder=2)
ax.loglog(intensidad, alcanzable, color=MORADO, linewidth=2.2, zorder=3)
ax.plot([0.5], [500.0], marker="o", markersize=7, color=ROJO, zorder=5)
ax.plot([32.0], [30_000.0], marker="o", markersize=7, color=CIAN, zorder=5)

anotar(ax, "lote de 1: el 1,7 % del pico", xy=(0.5, 500.0), xytext=(0.03, 0.90), color=ROJO)
anotar(ax, "lote de 64: en la cresta", xy=(32.0, 30_000.0), xytext=(0.53, 0.90), color=CIAN)
anotar(ax, "techo por memoria: I · B", xy=(7.0, 7000.0), xytext=(0.30, 0.36), color=AZUL)
anotar(ax, "pico de cálculo: P", xy=(400.0, P), xytext=(0.56, 0.70), color=VERDE)
titulo(ax, "El lote decide si el chip calcula o espera",
       "rendimiento alcanzable frente a la intensidad")
ax.set_xlabel("intensidad aritmética (FLOP por byte)")
ax.set_ylabel("rendimiento (GFLOP/s)")
ax.set_ylim(1e2, 1e5)
rejilla(ax)
numeros(ax)

# --- Derecha: de qué se llena la memoria ---------------------------------------------
ax = ejes[1]
lote = np.arange(0, 257)
parametros = 100e6
fijo = parametros * 16 / 1e9              # GB: pesos + gradientes + los dos momentos de Adam
activaciones = 0.09 * lote                # GB: crecen de forma lineal con el lote
total = fijo + activaciones

# Area apilada: el coste fijo abajo y las activaciones encima.
ax.fill_between(lote, 0, fijo, color=AZUL, alpha=0.75, zorder=2)
ax.fill_between(lote, fijo, total, color=NARANJA, alpha=0.6, zorder=2)
ax.axhline(12.0, color=ROJO, linewidth=1.4, linestyle="--", zorder=3)

anotar(ax, "16 bytes por parámetro: pesos,\ngradientes y dos momentos de Adam",
       xy=(30.0, 0.8), xytext=(0.03, 0.92), color=AZUL)
anotar(ax, "las activaciones\ncrecen con el lote", xy=(140.0, fijo + 0.09 * 140 / 2),
       xytext=(0.64, 0.78), color=NARANJA)
anotar(ax, "12 GB de VRAM", xy=(20.0, 12.0), xytext=(0.02, 0.44), color=ROJO)
titulo(ax, "El coste fijo no cambia; el lote sí",
       "100 millones de parámetros con Adam en float32")
ax.set_xlabel("tamaño del lote")
ax.set_ylabel("memoria (GB)")
ax.set_xlim(0, 260)
ax.set_ylim(0, 30)
rejilla(ax)
numeros(ax)

guardar(fig, "gpu-y-rendimiento-roofline-y-memoria")
