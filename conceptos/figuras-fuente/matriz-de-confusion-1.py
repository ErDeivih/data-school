"""matriz-de-confusion-1.py — la tabla de las cuatro casillas y el mismo test aplicado a
dos poblaciones con prevalencias muy distintas. Figura de la página de la matriz de
confusión (fase 6)."""

import numpy as np
from matplotlib.patches import Rectangle

from comun import *

estilo()


def matriz(ax, y0, vp, fn, fp, vn, nota, fuente=9.5, ancho=1.0):
    """Pinta una matriz 2x2 con los cuatro recuentos.

    `y0` es la coordenada de la fila de abajo, así que la matriz ocupa de `y0` a `y0 + 2`.
    El relleno de cada celda va de menos a más opaco según el recuento: así se ve de un
    vistazo qué casilla domina la tabla (con clases desbalanceadas, siempre el VN).
    """
    mayor = max(vp, fn, fp, vn)
    for col, fila, sigla, n, color in (
        (0, 1, "VP", vp, AZUL),        # predijo positivo y era positivo
        (1, 1, "FN", fn, NARANJA),     # predijo negativo y era positivo: se le escapó
        (0, 0, "FP", fp, ROJO),        # predijo positivo y era negativo: falsa alarma
        (1, 0, "VN", vn, VERDE),       # predijo negativo y era negativo
    ):
        ax.add_patch(Rectangle((col * ancho, y0 + fila), ancho, 1, edgecolor=TEXTO,
                               linewidth=0.9, facecolor=color,
                               alpha=0.06 + 0.30 * n / mayor))
        # La sigla va encima del recuento: en una celda estrecha, las dos cosas en la
        # misma línea se salen y se pisan con la celda de al lado.
        ax.text(col * ancho + ancho / 2, y0 + fila + 0.62, sigla, ha="center", va="center",
                fontsize=fuente - 1.0, color=TEXTO)
        ax.text(col * ancho + ancho / 2, y0 + fila + 0.30, f"{n:,}".replace(",", "."),
                ha="center", va="center", fontsize=fuente, color=TEXTO)
    ax.text(0, y0 + 2.08, nota, ha="left", va="bottom", fontsize=9, color=TEXTO)


fig, ejes = plt.subplots(1, 2, figsize=(11.2, 4.6))

# --- Izquierda: la tabla del ejemplo (200 pacientes, 40 enfermos, 12 falsas alarmas).
# Los totales de cada fila y cada columna van en los rótulos: son los márgenes de la
# tabla, y las métricas derivadas se leen en esos mismos márgenes.
matriz(ejes[0], 0, 34, 6, 12, 148, "200 pacientes · 40 enfermos (prevalencia 20 %)", 13)
ejes[0].set_xlim(0, 2)
ejes[0].set_ylim(0, 2.4)
ejes[0].set_xticks([0.5, 1.5])
ejes[0].set_xticklabels(["dijo positivo\n46 alertas\nprecisión 0,74",
                         "dijo negativo\n154 casos"])
ejes[0].set_yticks([1.5, 0.5])
ejes[0].set_yticklabels(["era positivo\n40 casos\nsensibilidad 0,85",
                         "era negativo\n160 casos\nespecificidad 0,93"])
for lado in ("top", "right", "left", "bottom"):
    ejes[0].spines[lado].set_visible(False)
ejes[0].tick_params(length=0)
titulo(ejes[0], "Cuatro casillas: dos aciertos y dos errores",
       "filas: lo que era · columnas: lo que dijo el modelo · la diagonal son los aciertos")

# --- Derecha: el mismo test (sensibilidad 0,85 y especificidad 0,93) en dos poblaciones
# de 20.000 casos. El test no cambia; lo que cambia es cuántos negativos hay por cada
# positivo, y eso es lo que hunde la precisión.
matriz(ejes[1], 3.0, 3400, 600, 1200, 14800, "la misma prueba en un hospital: 20 % de enfermos",
       9.5, 1.25)
matriz(ejes[1], 0.0, 85, 15, 1492, 18408, "la misma prueba en un cribado: 0,5 % de enfermos",
       9.5, 1.25)
ejes[1].set_xlim(0, 7.4)
ejes[1].set_ylim(0, 6.1)
ejes[1].axis("off")
anotar(ejes[1], "precisión 0,74:\ntres de cada cuatro\nalertas son reales",
       xy=(0.5, 3.5), xytext=(0.40, 0.68), color=VERDE, flecha=False)
anotar(ejes[1], "precisión 0,054:\nsolo una de cada 19\nalertas es un enfermo",
       xy=(0.5, 0.5), xytext=(0.40, 0.14), color=ROJO, flecha=False)
titulo(ejes[1], "El test no empeora: cambia el terreno",
       "mismo test, misma sensibilidad y misma especificidad, otra proporción de enfermos")

guardar(fig, "confusion-matriz-y-prevalencia")
