"""motores-de-inferencia-para-llms-1.py — las dos caras de servir un modelo abierto: la
memoria que hay que llenar y el tiempo que cuesta generar. Arriba, cuantos GiB ocupan los pesos
segun los bits por peso y cuantos tokens por segundo salen de esa misma tarjeta. Abajo, el
efecto del lote (el tiempo sube despacio, la producción sube rapido) y el reparto de la
memoria entre pesos, cache y margen. Figura de la pagina de motores de inferencia (fase 8)."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from comun import *

estilo()

# Esta figura se guarda con el encuadre de la FIGURA, no con bbox_inches="tight".
# Medido con matplotlib 3.11.2: en cuanto hay dos ejes y el segundo lleva una etiqueta de eje
# girada, get_tightbbox devuelve un alto de 205.602 puntos y el SVG sale con un viewBox de
# 134.860 puntos: el ajuste del encuadre se realimenta. La causa esta en ese calculo, no en los
# datos, asi que aqui se evita: los margenes se fijan con el gridspec y se escriben los SVG a
# mano, aplicando los mismos centinelas de color que comun.guardar().
plt.rcParams["figure.constrained_layout.use"] = False

M_GPU = 24.0                 # GB de la tarjeta del ejemplo, memoria nominal
N_PARAMETROS = 7.0e9
BYTES_POR_GB = 1024 ** 3
B_GB_S = 900.0               # ancho de banda de memoria de la tarjeta

BITS = [32, 16, 8, 4]
PESOS = [N_PARAMETROS * b / 8 / BYTES_POR_GB for b in BITS]
# El techo de velocidad de la decodificacion: hay que releer los pesos enteros por cada token.
VELOCIDAD = [1000 * B_GB_S / p for p in PESOS]

fig = plt.figure(figsize=(8.8, 7.4))
rejilla_ = fig.add_gridspec(2, 2, hspace=0.62, wspace=0.34,
                            left=0.09, right=0.97, top=0.90, bottom=0.09)

# --- A: cuantos GB ocupan los pesos -------------------------------------------
ax = fig.add_subplot(rejilla_[0, 0])
colores = [ROJO if p >= M_GPU else (NARANJA if p >= 0.5 * M_GPU else VERDE) for p in PESOS]
barras = ax.barh(np.arange(len(BITS)), PESOS, color=colores, height=0.6)
for barra, valor in zip(barras, PESOS):
    ax.text(valor + 0.6, barra.get_y() + barra.get_height() / 2,
            f"{valor:.2f} GiB".replace(".", ","), va="center", ha="left", fontsize=8.5,
            color=TEXTO)
ax.axvline(M_GPU, color=TEXTO, linewidth=1.4, linestyle="--")
# El rotulo va pegado a la linea y por debajo de la barra larga: dentro del eje, para que se
# vea a que linea senala, pero fuera del hueco por el que pasa la barra de 32 bits.
ax.text(M_GPU + 0.7, 2.55, "24 GiB", ha="left", va="center", fontsize=8, color=TEXTO)
ax.set_yticks(np.arange(len(BITS)))
ax.set_yticklabels([f"{b} bits" for b in BITS], fontsize=8.5)
ax.set_ylim(3.7, -0.7)
ax.set_xlim(0, 32)
ax.set_xlabel("gibibytes que ocupan los pesos")
titulo(ax, "Comprimir los pesos los hace caber",
       "16 bits: 13,04 GiB; 8: 6,52; 4: 3,26; en 32 bits no caben")
rejilla(ax, "x")
numeros(ax, "x")

# --- B: tokens por segundo de esa misma tarjeta --------------------------------
ax = fig.add_subplot(rejilla_[0, 1])
barras = ax.bar(np.arange(len(BITS)), VELOCIDAD, color=[VERDE, VERDE, NARANJA, ROJO],
                width=0.62)
for barra, valor in zip(barras, VELOCIDAD):
    ax.text(barra.get_x() + barra.get_width() / 2, valor * 1.02,
            f"{valor:,.0f}".replace(",", "."), ha="center", va="bottom", fontsize=8.5,
            color=TEXTO)
ax.set_xticks(np.arange(len(BITS)))
ax.set_xticklabels([f"{b} bits" for b in BITS], fontsize=8.5)
ax.set_ylim(0, 330000)
# El eje no se recorta: la columna de 32 bits mide mil veces mas que la de 16, y ese contraste
# es el mensaje. Recortarlo para "que se vean todas" las volveria indistinguibles.
ax.set_ylabel("tokens/s por secuencia")
titulo(ax, "El tiempo por token va con los GiB leidos",
       "es el techo que impone el ancho de banda de memoria")
rejilla(ax)

# --- C: el efecto del lote -----------------------------------------------------
ax = fig.add_subplot(rejilla_[1, 0])
lotes = np.array([1, 2, 4, 8, 16, 32])
ms = (PESOS[1] + 1.95 * lotes) / B_GB_S * 1000
ax.plot(lotes, lotes * 1000 / ms, color=AZUL, linewidth=1.8, marker="o", markersize=4,
        label="tokens por segundo del conjunto")
ax.plot(lotes, 1000 / ms, color=ROJO, linewidth=1.6, marker="o", markersize=4,
        label="tokens por segundo por secuencia")
ax.set_xscale("log", base=2)
ax.set_xticks(lotes)
ax.set_xticklabels([str(l) for l in lotes])
ax.set_ylim(0, 560)
ax.set_xlabel("secuencias en el lote")
ax.set_ylabel("tokens por segundo")
ax.legend(loc="center right", framealpha=0.0, fontsize=8)
anotar(ax, "el conjunto sube, la espera también", xy=(8, 8 * 1000 / ms[3]),
       xytext=(0.04, 0.14), color=ROJO)
titulo(ax, "Agrupar sube la producción",
       "los pesos se leen una vez por paso y sirven para todo el lote")
rejilla(ax)
numeros(ax, "x")

# --- D: el reparto de la memoria de la tarjeta --------------------------------
# Una barra apilada por fila, con la cifra de la cache al final y sin leyenda: las etiquetas de
# color en una esquina se pisaban entre ellas y el rotulo del extremo se salia del eje.
ax = fig.add_subplot(rejilla_[1, 1])
filas = [("4 bits", PESOS[3], 2.0, 1.95 * 9), ("16 bits", PESOS[1], 2.0, 1.95 * 4)]
alto = 0.34
for y, (etiqueta, pesos, activaciones, cache_max) in enumerate(filas):
    ax.barh(y, pesos, color=AZUL, height=alto)
    ax.barh(y, activaciones, left=pesos, color=NARANJA, height=alto)
    ax.barh(y, cache_max, left=pesos + activaciones, color=VERDE, height=alto)
    ax.text(pesos + activaciones + cache_max + 0.5, y,
            f"{cache_max:.1f} GiB de cache".replace(".", ","), va="center", ha="left",
            fontsize=8, color=VERDE)
ax.axvline(M_GPU, color=TEXTO, linewidth=1.4, linestyle="--")
ax.text(M_GPU + 0.6, 1.75, "24 GiB", ha="left", va="center", fontsize=8, color=TEXTO)
ax.set_yticks([0, 1])
ax.set_yticklabels([f"{f[0]}: pesos {f[1]:.2f}".replace(".", ",") for f in filas],
                   fontsize=8.5)
ax.set_ylim(-0.62, 2.05)
ax.set_xlim(0, 44)
ax.set_xticks([0, 5, 10, 15, 20])
ax.set_xlabel("gibibytes de la tarjeta: pesos, activaciones y cache")
titulo(ax, "Los pesos son fijos, la cache crece",
       "los pesos son azul, las activaciones naranja y la cache verde")
rejilla(ax, "x")
numeros(ax, "x")

# Los mismos centinelas de color que usa comun.guardar(), para que la figura siga el tema
# claro/oscuro del portal. Sin reescribirlos aqui, el SVG se quedaria con los colores fijos.
CENTINELAS = [
    ["#101418", "var(--fig-texto, #101418)"],
    ["#9aa4b2", "var(--fig-rejilla, #9aa4b2)"],
    ["#2563eb", "var(--fig-azul, #2563eb)"],
    ["#dc2626", "var(--fig-rojo, #dc2626)"],
    ["#059669", "var(--fig-verde, #059669)"],
    ["#d97706", "var(--fig-naranja, #d97706)"],
    ["#7c3aed", "var(--fig-morado, #7c3aed)"],
    ["#0891b2", "var(--fig-cian, #0891b2)"],
    ["#db2777", "var(--fig-rosa, #db2777)"],
]

import os

SALIDA = Path(__file__).resolve().parent.parent / "web" / "figuras"
SALIDA.mkdir(parents=True, exist_ok=True)
NOMBRE = "motores-memoria-y-lote"

fig.savefig(SALIDA / (NOMBRE + ".svg"), format="svg", transparent=True)
svg = (SALIDA / (NOMBRE + ".svg")).read_text(encoding="utf-8")
for fijo, variable in CENTINELAS:
    svg = svg.replace(fijo, variable).replace(fijo.upper(), variable)
svg = svg.replace('<rect width="100%" height="100%"', '<rect style="display:none" width="100%" height="100%"')
(SALIDA / (NOMBRE + ".svg")).write_text(svg, encoding="utf-8")

if os.environ.get("FIGURAS_PNG"):
    carpeta = Path(os.environ["FIGURAS_PNG"])
    carpeta.mkdir(parents=True, exist_ok=True)
    fig.savefig(carpeta / (NOMBRE + ".png"), format="png", dpi=150, facecolor="white")

plt.close(fig)
print(NOMBRE + ".svg")

