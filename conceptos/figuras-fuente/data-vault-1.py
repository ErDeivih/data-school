"""data-vault-1.py — las tres piezas del modelo y por qué un cambio del origen solo anade filas.
Figura de la pagina 'data-vault' (fase 4)."""

import numpy as np

from comun import *

estilo()

fig, (arriba, abajo) = plt.subplots(2, 1, figsize=(7.6, 6.2),
                                    gridspec_kw={"height_ratios": [1.05, 0.85]})

# --- Arriba: hub, enlaces y satelites -------------------------------------
arriba.set_xlim(0, 10)
arriba.set_ylim(0, 6.4)
arriba.axis("off")

cajas = [
    ((0.15, 3.60, 3.00, 1.80), VERDE, "SAT_CLIENTE",
     ["ciudad, alta, segmento", "load_date + hashdiff", "una fila por cambio"]),
    ((3.50, 3.60, 3.00, 1.80), AZUL, "HUB_CLIENTE",
     ["hub_key = hash(id)", "id · load_date · origen", "una fila por cliente"]),
    ((6.85, 3.60, 3.00, 1.80), CIAN, "SAT_CLIENTE_CRM",
     ["los mismos atributos", "de la fuente CRM", "otro satélite, no un update"]),
    ((3.35, 0.95, 3.30, 1.55), MORADO, "ENLACE_CLIENTE_PEDIDO",
     ["hub_key_cliente + hub_key_pedido", "+ load_date", "una fila por relación"]),
]
for (x, y, ancho, alto), color, nombre, lineas in cajas:
    arriba.add_patch(plt.Rectangle((x, y), ancho, alto, fill=False, edgecolor=color, linewidth=1.7))
    arriba.text(x + ancho / 2, y + alto - 0.34, nombre, ha="center", va="center", fontsize=9.5,
                color=color)
    for k, linea in enumerate(lineas):
        color_linea = REJILLA if k == len(lineas) - 1 else TEXTO
        arriba.text(x + ancho / 2, y + alto - 0.70 - 0.33 * k, linea, ha="center", va="center",
                    fontsize=8, color=color_linea)

for xy, xytext in (((5.0, 3.60), (5.0, 2.50)), ((3.50, 4.50), (3.15, 4.50)),
                   ((6.50, 4.50), (6.85, 4.50))):
    arriba.annotate("", xy=xy, xytext=xytext,
                    arrowprops=dict(arrowstyle="<->", color=TEXTO, linewidth=1.0, shrinkA=0,
                                    shrinkB=0))
titulo(arriba, "Una fila por clave de negocio; el resto cuelga de ella",
       "el hub identifica, el enlace relaciona, el satélite describe y guarda la historia")

# --- Abajo: el satelite solo inserta --------------------------------------
# Dias desde el 1 de enero: las cuatro llegadas del origen y la vida de cada version
llegadas = np.array([9, 61, 166, 244])
barras = [(9, 52, 2, AZUL), (61, 183, 1, VERDE), (244, 122, 0, MORADO)]
for inicio, ancho, y, color in barras:
    abajo.barh(y, ancho, left=inicio, height=0.42, color=color, alpha=0.9)
abajo.axvline(166, color=ROJO, linewidth=1.1, linestyle="--")
abajo.scatter([166], [1.42], marker="X", s=55, color=ROJO, zorder=3)
abajo.set_ylim(-0.6, 2.95)
abajo.set_xlim(0, 380)
titulo(abajo, "Nada se actualiza: cada cambio añade una fila",
       "la versión vigente es la de load_date más alta")
abajo.set_xlabel("2024 (cada marca es una llegada del origen)")
numeros(abajo)
rejilla(abajo, eje="x")
abajo.set_yticks([0, 1, 2])
abajo.set_yticklabels(["v3 Valencia", "v2 Barcelona", "v1 Madrid"], fontsize=8.5)
abajo.set_xticks(llegadas)
abajo.set_xticklabels(["10 ene", "02 mar", "15 jun", "01 sep"], fontsize=8.5)
anotar(abajo, "Aquí vuelve a llegar Barcelona:\nmismo hashdiff, cero filas nuevas",
       xy=(166, 1.42), xytext=(0.50, 0.86), color=ROJO)

guardar(fig, "data-vault-satelite-append")
