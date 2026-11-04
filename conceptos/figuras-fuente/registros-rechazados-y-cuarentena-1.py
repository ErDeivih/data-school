"""registros-rechazados-y-cuarentena-1.py — el bifurcador del pipeline y la tasa de rechazo
que decide si se para. La figura de la pagina de registros rechazados y cuarentena (fase 4)."""

import numpy as np

from comun import *

estilo()

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 4.4))

# --- Izquierda: el bifurcador ---------------------------------------------------------
izq.set_xlim(0, 10)
izq.set_ylim(0, 10)
izq.axis("off")


def caja(ax, x, y, texto, color=AZUL, ancho=2.6):
    """Caja redondeada con texto, en las coordenadas del eje."""
    ax.text(x, y, texto, ha="center", va="center", fontsize=8.5, color=color,
            bbox=dict(boxstyle="round,pad=0.45", facecolor="none", edgecolor=color,
                      linewidth=1.4))


caja(izq, 1.4, 5.2, "lote\ncrudo", REJILLA)
caja(izq, 4.3, 5.2, "validación\nregistro a registro")
caja(izq, 8.4, 8.2, "tabla\nbuena", VERDE)
caja(izq, 8.4, 2.0, "cuarentena\ncon el motivo", NARANJA)
caja(izq, 4.3, 9.1, "parada y aviso", ROJO)

izq.annotate("", xy=(3.1, 5.2), xytext=(2.5, 5.2),
             arrowprops=dict(arrowstyle="->", color=TEXTO, linewidth=1.1))
izq.annotate("", xy=(7.3, 7.9), xytext=(5.6, 5.9),
             arrowprops=dict(arrowstyle="->", color=VERDE, linewidth=1.1))
izq.annotate("", xy=(7.3, 2.3), xytext=(5.6, 4.5),
             arrowprops=dict(arrowstyle="->", color=NARANJA, linewidth=1.1))
izq.annotate("", xy=(4.3, 8.5), xytext=(4.3, 6.0),
             arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=1.1, linestyle="--"))

izq.text(9.9, 6.9, "cumple las reglas", ha="right", fontsize=8.5, color=VERDE)
izq.text(9.9, 3.6, "no cumple: se guarda entero", ha="right", fontsize=8.5, color=NARANJA)
izq.text(0.2, 7.3, "si la tasa supera el umbral,\nse para el lote entero", fontsize=8.5,
         color=ROJO)
titulo(izq, "Un lote, dos salidas y una parada",
       "el mismo registro nunca acaba en las dos tablas")

# --- Derecha: la tasa de rechazo de cada lote del dia ---------------------------------
lotes = ["lote 1", "lote 2", "lote 3", "lote 4", "lote 5"]
totales = np.array([500, 480, 510, 470, 490])
rechazados = np.array([1, 3, 2, 140, 1])
tasas = 100.0 * rechazados / totales

UMBRAL = 5.0
colores = [ROJO if t > UMBRAL else AZUL for t in tasas]
der.bar(range(5), tasas, color=colores, width=0.62)
der.axhline(UMBRAL, color=ROJO, linewidth=1.2, linestyle="--")
der.text(4.42, UMBRAL + 1.1, "umbral 5 %", ha="right", fontsize=8.5, color=ROJO)

for i, t in enumerate(tasas):
    der.text(i, t + 0.9, ("%.1f" % t).replace(".", ",") + " %", ha="center", fontsize=8.5,
             color=ROJO if t > UMBRAL else TEXTO)

anotar(der, "29,8 % no es ruido: el origen\nha cambiado de unidad o de esquema",
       xy=(3.0, 28.0), xytext=(0.06, 0.76), color=ROJO)
anotar(der, "el lote 4 no se escribe:\nni sus 330 filas buenas",
       xy=(3.55, 18.0), xytext=(0.02, 0.34), color=TEXTO)

der.set_xticks(range(5))
der.set_xticklabels(lotes, fontsize=8.5)
der.set_ylabel("registros rechazados (%)")
der.set_ylim(0, 36)
titulo(der, "La tasa de rechazo decide si se para",
       "mismo umbral para lotes de tamaño parecido")
rejilla(der)
numeros(der, ejes="y")

guardar(fig, "rechazos-cuarentena-y-umbral")
