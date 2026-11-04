"""json-y-datos-anidados-1.py — un objeto JSON con una lista dentro se convierte en una tabla
con una fila por elemento de la lista. La figura de la pagina de JSON y datos anidados (fase 3)."""

import numpy as np

from comun import *

estilo()

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 4.4))


def caja(ax, x, y, ancho, texto, color, tam=8.5):
    """Un rectángulo con su texto centrado: cada caja es un nodo del JSON."""
    ax.add_patch(plt.Rectangle((x - ancho / 2, y - 0.62), ancho, 1.24, fill=False,
                               edgecolor=color, linewidth=1.3, zorder=2))
    ax.text(x, y, texto, ha="center", va="center", color=color, fontsize=tam, zorder=3)


def une(ax, x1, y1, x2, y2, color=REJILLA):
    ax.plot([x1, x2], [y1, y2], color=color, linewidth=1.0, zorder=1)


# --- Izquierda: la estructura tal como viene en el JSON ----------------------
izq.set_xlim(0, 10)
izq.set_ylim(0, 11)
izq.axis("off")
titulo(izq, "El JSON de entrada: un objeto con una lista",
       "cada elemento de la lista es un registro aparte")

caja(izq, 5.0, 10.0, 5.2, "registro (objeto)", AZUL)
caja(izq, 2.2, 7.8, 3.8, 'sensor: "S1"', VERDE)
caja(izq, 7.4, 7.8, 4.6, "lecturas (lista de 2)", NARANJA)
caja(izq, 6.9, 5.2, 3.6, "[0] hora 08:00 · temp 19,5", CIAN)
caja(izq, 6.9, 3.0, 3.6, "[1] hora 09:00 · temp 21,0", CIAN)

# Conectores en codo, para que se vea quien cuelga de quien
une(izq, 5.0, 9.38, 5.0, 8.9)
une(izq, 2.2, 8.9, 7.4, 8.9)
une(izq, 2.2, 8.9, 2.2, 8.42)
une(izq, 7.4, 8.9, 7.4, 8.42)
# Al primer elemento, recto; al segundo, rodeando por la derecha para no taparlo
une(izq, 7.4, 7.18, 7.4, 6.6)
une(izq, 6.9, 6.6, 6.9, 5.82)
une(izq, 7.4, 6.6, 9.6, 6.6)
une(izq, 9.6, 6.6, 9.6, 3.0)
une(izq, 9.6, 3.0, 8.7, 3.0)

# La nota va en la franja de abajo a la izquierda, que queda libre: las cajas empiezan en y = 3.
anotar(izq, "los dos elementos de la lista\nserán dos filas del mismo sensor",
       xy=(5.0, 4.0), xytext=(0.02, 0.08))

# --- Derecha: el resultado de aplanar ---------------------------------------
der.axis("off")
titulo(der, "Aplanado: una fila por lectura",
       "el sensor se repite en cada fila")

tabla = der.table(cellText=[["S1", "08:00", "19,5"],
                            ["S1", "09:00", "21,0"],
                            ["S2", "08:00", "22,4"]],
                  colLabels=["sensor", "hora", "temp"],
                  loc="center", cellLoc="center",
                  bbox=[0.04, 0.34, 0.92, 0.50])
tabla.auto_set_font_size(False)
tabla.set_fontsize(9.5)
for (fila, _col), celda in tabla.get_celld().items():
    celda.set_edgecolor(REJILLA)
    celda.set_facecolor("none")
    celda.set_linewidth(0.7)
    if fila == 0:
        celda.get_text().set_color(AZUL)
        celda.get_text().set_fontweight("bold")

der.text(0.5, 0.12, "3 filas: el registro 1 aporta 2 y el registro 2 aporta 1",
         transform=der.transAxes, ha="center", va="center", color=TEXTO, fontsize=8.5)

guardar(fig, "json-y-datos-anidados-arbol-y-tabla")
