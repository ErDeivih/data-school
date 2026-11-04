"""entropia-e-informacion-1.py - la entropia depende solo de las probabilidades (no de los
valores), y la divergencia KL no es simétrica."""

import numpy as np
from scipy import stats

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.2))

# --- Izquierda: entropia de una moneda segun su sesgo; 1 bit es el maximo.
p = np.linspace(0.001, 0.999, 600)
H = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
ejes[0].plot(p, H, color=AZUL, linewidth=1.8)
ejes[0].plot([0, 1], [1, 1], color=REJILLA, linewidth=0.9, linestyle="--")
for valor, color in ((0.9, NARANJA), (0.99, ROJO)):
    altura = stats.entropy([valor, 1 - valor], base=2)
    ejes[0].plot([valor], [altura], marker="o", markersize=5.5, color=color)
    ejes[0].vlines(valor, 0, altura, color=color, linewidth=1.0, linestyle=":")
# Las notas van en las dos esquinas que deja libres la curva: la de arriba a la izquierda
# (por debajo del maximo) y la franja de abajo, donde la entropia ya es baja. Pegadas a la
# rampa de subida el hueco se estrecha y el texto acabaria pisando la linea.
anotar(ejes[0], "moneda justa: 1 bit,\nel máximo posible", xy=(0.5, 1.0), xytext=(0.05, 0.90),
       color=AZUL, align="left")
anotar(ejes[0], "p = 0,9 -> 0,47 bits:\ncasi todo lo que sale ya lo sabias",
       xy=(0.88, 0.44), xytext=(0.30, 0.60), color=NARANJA, align="left")
anotar(ejes[0], "p = 0,99 -> 0,08 bits", xy=(0.965, 0.10), xytext=(0.30, 0.16),
       color=ROJO, align="left")
ejes[0].text(0.30, 0.045, "la tirada casi no informa", transform=ejes[0].transAxes,
             color=ROJO, fontsize=8.5, va="center", ha="left")
titulo(ejes[0], "La entropia depende de las probabilidades, no del valor")
ejes[0].set_xlabel("probabilidad de cara")
ejes[0].set_ylabel("entropia (bits)")
ejes[0].set_xlim(0, 1)
ejes[0].set_ylim(0, 1.12)
rejilla(ejes[0])
numeros(ejes[0], ejes="x")

# --- Derecha: la KL en los dos sentidos, con el modelo equivocado a la vista.
barras = np.array([0.7, 0.2, 0.1])
modelo = np.array([0.5, 0.4, 0.1])
categorias = np.arange(3)
ancho = 0.26
ejes[1].bar(categorias - ancho / 2, barras, ancho, color=AZUL)
ejes[1].bar(categorias + ancho / 2, modelo, ancho, color=NARANJA)
kl_pq = stats.entropy(barras, modelo, base=2)
kl_qp = stats.entropy(modelo, barras, base=2)
ejes[1].annotate("KL(p; q) = " + coma(round(kl_pq, 4)) + " bits  y  KL(q; p) = "
                 + coma(round(kl_qp, 4)) + " bits", xy=(0.95, 0.97),
                 xytext=(0.95, 0.97), textcoords="axes fraction", ha="right", va="top",
                 color=TEXTO, fontsize=8.5)
anotar(ejes[1], "datos p = 0,7 aqui", xy=(0.0 - ancho / 2, 0.71), xytext=(0.42, 0.87),
       color=AZUL, align="left")
anotar(ejes[1], "el modelo pone 0,4 en B", xy=(1.0 + ancho / 2, 0.42), xytext=(0.42, 0.69),
       color=NARANJA, align="left")
anotar(ejes[1], "categoria C: los dos\nmodelos coinciden", xy=(2.0, 0.13),
       xytext=(0.50, 0.42), color=TEXTO, align="left")
titulo(ejes[1], "La divergencia KL no es simétrica")
ejes[1].set_xticks(categorias)
ejes[1].set_xticklabels(["categoria A", "categoria B", "categoria C"])
ejes[1].set_ylabel("probabilidad")
ejes[1].set_ylim(0, 1.05)
rejilla(ejes[1])

guardar(fig, "entropia-bits-y-kl-no-simetrica")
