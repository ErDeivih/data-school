"""venta-en-corto-mecanica-1.py — la ventaja de una posición corta se acumula con los días, pero
el alquiler de las acciones también. Cada tasa de alquiler tiene su día de ruptura, y ese día es
más corto cuanto peor es el préstamo. Página de Vender en corto (fase 9)."""

import matplotlib
import numpy as np

from comun import *

estilo()

PRECIO = 100.0          # precio de la acción, en EUR
VENTAJA_DIA = 0.04      # lo que esperas ganar por acción y día mientras la tesis aguanta
DIAS = 60

dias = np.arange(0, DIAS + 1)
bruto = VENTAJA_DIA * dias

casos = [(0.02, VERDE, "2 % anual"),
         (0.03, AZUL, "3 %"),
         (0.12, NARANJA, "12 %"),
         (0.40, ROJO, "40 %, difícil de prestar")]

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.5))

# --- Izquierda: el beneficio bruto es una recta; el coste del alquiler, otra con más pendiente.
ejes[0].plot(dias, bruto, color=TEXTO, linewidth=2.2, label="ventaja acumulada (bruta)")
# Los cuatro cortes caen entre el día 0,4 y el 7,3: en el eje se pisan, así que van en una lista
# aparte, en la esquina libre de abajo a la derecha.
lineas_corte = []
for tasa, color, etiqueta in casos:
    coste = tasa * PRECIO / 365 * dias
    neto = bruto - coste
    ejes[0].plot(dias, neto, color=color, linewidth=1.9, label=f"alquiler {etiqueta}")
    # El día en que la recta cruza el cero: a partir de ahí, mantener abierto cuesta dinero.
    corte = VENTAJA_DIA / (tasa * PRECIO / 365)
    lineas_corte.append(f"{etiqueta.split(',')[0]}: {corte:.1f} días de aguante")
    if corte <= DIAS:
        ejes[0].plot([corte], [0], marker="o", color=color, markersize=6, zorder=5)
ejes[0].text(0.985, 0.58, "\n".join(reversed(lineas_corte)), transform=ejes[0].transAxes,
             fontsize=7.5, color=TEXTO, ha="right", va="bottom", linespacing=1.45)
anotar(ejes[0], "con el préstamo caro, la tesis\nse agota mucho antes de que\nel precio se mueva",
       xy=(0.37, 0.0), xytext=(0.04, 0.50), color=ROJO)
titulo(ejes[0], "Cada día que aguantas cuesta alquiler",
       "ventaja bruta y resultado neto, por acción y en euros")
ejes[0].set_xlabel("días con la posición abierta")
ejes[0].set_ylabel("resultado por acción (EUR)")
ejes[0].set_xlim(-1.5, DIAS + 1)
ejes[0].legend(loc="upper left", fontsize=7.0)
rejilla(ejes[0], eje="y")
numeros(ejes[0], ejes="both")

# --- Derecha: el mismo cálculo, pero mirando cuántos días aguantas según la ventaja y la tasa.
tasas = np.array([0.02, 0.03, 0.06, 0.12, 0.40])
ventajas = np.array([0.02, 0.04, 0.10, 0.25])
matriz = ventajas[None, :] / (tasas[:, None] * PRECIO / 365)
imagen = ejes[1].imshow(matriz, cmap="YlOrRd_r", aspect="auto", origin="lower",
                        norm=matplotlib.colors.LogNorm(vmin=0.3, vmax=50))
ejes[1].set_xticks(range(len(ventajas)))
ejes[1].set_xticklabels([f"{v * 10000:.0f}" for v in ventajas], fontsize=8.5)
ejes[1].set_yticks(range(len(tasas)))
ejes[1].set_yticklabels([f"{t * 100:g}" for t in tasas], fontsize=8.5)
for fila in range(len(tasas)):
    for columna in range(len(ventajas)):
        ejes[1].text(columna, fila, f"{matriz[fila, columna]:.0f}", ha="center", va="center",
                     fontsize=9, color=TEXTO)
titulo(ejes[1], "Días de aguante hasta pagar el alquiler",
       "celdas: días que la posición sigue en positivo, según la ventaja y la tasa anual")
ejes[1].set_xlabel("ventaja esperada de la operación (puntos básicos)")
ejes[1].set_ylabel("tasa de alquiler anual (%)")
barra = fig.colorbar(imagen, ax=ejes[1], pad=0.02)
barra.set_label("días hasta el equilibrio", fontsize=8)
barra.ax.tick_params(labelsize=8)

guardar(fig, "venta-en-corto-coste-y-dias")
