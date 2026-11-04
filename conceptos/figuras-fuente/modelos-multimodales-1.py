"""modelos-multimodales-1.py — lo que cuesta una modalidad dentro del contexto. Arriba, los
tokens que ocupa cada cosa segun el parámetro que los mueve: caracteres de texto, lado de la
imagen y segundos de audio. Abajo a la izquierda, el crecimiento cuadrático del número de
parches con el lado. Abajo a la derecha, el coste de atención, que va con el cuadrado de toda
la secuencia. Figura de la pagina de modelos multimodales (fase 8)."""

import numpy as np
import matplotlib.pyplot as plt

from comun import *

estilo()

fig = plt.figure(figsize=(8.6, 7.2))
# El panel de arriba lleva seis etiquetas y pide algo mas de alto; el hueco entre filas es
# generoso porque el subtitulo de los paneles de abajo chocaba con la primera marca del eje.
rejilla_ = fig.add_gridspec(2, 2, height_ratios=[1.05, 1.0], hspace=0.58, wspace=0.30)

# --- Arriba: el presupuesto de contexto en tokens -----------------------------
ax = fig.add_subplot(rejilla_[0, :])
casos = [
    ("texto: 2.000 caracteres", 500, AZUL),
    ("imagen 224 px", 196, MORADO),
    ("imagen 448 px", 784, MORADO),
    ("imagen 1.008 px", 3969, MORADO),
    ("audio 30 s", 1500, CIAN),
    ("audio 10 min", 30000, CIAN),
]
ys = np.arange(len(casos))
for y, (etiqueta, valor, color) in zip(ys, casos):
    ax.barh(y, valor, color=color, height=0.62)
    ax.text(valor * 1.10, y, f"{valor:,}".replace(",", "."), va="center", ha="left",
            fontsize=8.5, color=TEXTO)
ax.set_yticks(ys)
ax.set_yticklabels([c[0] for c in casos], fontsize=8.5)
ax.invert_yaxis()
ax.set_xscale("log")
ax.set_xlim(100, 200000)
ax.set_xlabel("tokens que ocupan en el contexto")
titulo(ax, "Todo compite por la misma ventana",
       "una imagen de 1.008 px ocupa más contexto que 2.000 palabras de texto")
rejilla(ax, "x")
numeros(ax, "x")

# --- Abajo izquierda: el numero de parches crece con el cuadrado del lado ------
ax = fig.add_subplot(rejilla_[1, 0])
lados = np.linspace(96, 1120, 300)
troceado = 16
ax.plot(lados, (np.ceil(lados / troceado)) ** 2, color=AZUL, linewidth=1.8)
for lado in (224, 448, 1008):
    n = int(np.ceil(lado / troceado)) ** 2
    ax.plot([lado], [n], marker="o", markersize=5, color=ROJO, zorder=4)
# Las dos notas van en el hueco que deja la curva por debajo: contra el eje y se comian la
# etiqueta del eje.
anotar(ax, "de 224 a 448 px: 196 -> 784", xy=(448, 784), xytext=(0.26, 0.42), color=ROJO)
anotar(ax, "1.008 px: 3.969 parches", xy=(1008, 3969), xytext=(0.62, 0.74), color=ROJO,
       align="right")
ax.set_yscale("log")
ax.set_xlabel("lado de la imagen, en pixeles")
ax.set_ylabel("parches (escala logaritmica)")
titulo(ax, "El coste va con el cuadrado del lado",
       "parches de 16 x 16: doblar el lado multiplica por cuatro")
rejilla(ax)
numeros(ax)

# --- Abajo derecha: el coste de atencion va con el cuadrado de la secuencia ---
ax = fig.add_subplot(rejilla_[1, 1])
n_texto = 600
lados = np.array([224, 336, 448, 672, 1008])
parches = (np.ceil(lados / 16) ** 2).astype(int)
totales = n_texto + parches
relativo = totales ** 2 / n_texto ** 2
barras = ax.barh(np.arange(len(lados)), relativo, color=NARANJA, height=0.62)
for i, (barra, valor, total) in enumerate(zip(barras, relativo, totales)):
    ax.text(barra.get_width() * 1.08, i, f"{valor:.1f}x", va="center", ha="left",
            fontsize=8.5, color=TEXTO)
ax.set_yticks(np.arange(len(lados)))
ax.set_yticklabels([f"+ {t} vec." for t in parches], fontsize=8.5)
ax.invert_yaxis()
ax.set_xscale("log")
ax.set_xlim(1, 200)
ax.set_xlabel("coste de atención relativo al texto solo")
titulo(ax, "Solo texto: 1x, con imagen: hasta 58x",
       "la atención va con el cuadrado de la secuencia total")
rejilla(ax, "x")
numeros(ax, "x")

guardar(fig, "multimodal-el-precio-en-tokens")
