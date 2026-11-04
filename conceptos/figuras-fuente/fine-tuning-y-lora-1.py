"""fine-tuning-y-lora-1.py — donde va el presupuesto de parámetros y como el rango r
recorta la corrección que LoRA puede aprender. La figura de la pagina de ajuste fino y
LoRA (fase 7)."""

import numpy as np

from comun import *

estilo()
rng = np.random.default_rng(7)

fig, ejes = plt.subplots(1, 2, figsize=(9.4, 4.1))

# --- Panel 1: parametros entrenables, completo frente a LoRA ---
# Cuatro barras: cada bloque de dos es una capa, y dentro del bloque, completo y adaptador.
posiciones = np.array([0.0, 1.0, 2.6, 3.6])
alturas = [589824, 12288, 2359296, 30720]
colores = [AZUL, NARANJA, AZUL, NARANJA]
for x, alto, color in zip(posiciones, alturas, colores):
    ejes[0].bar(x, alto, width=0.62, color=color)
    # La etiqueta va girada porque el eje esta en escala logaritmica y hay poco hueco.
    ejes[0].text(x, alto * 1.4, f"{alto:,}".replace(",", "."), ha="center", fontsize=8, rotation=90)
ejes[0].set_yscale("log")
ejes[0].set_ylim(2000, 2e8)
ejes[0].set_xticks([0.6, 3.6])
ejes[0].set_xticklabels(["atención 768 x 768", "MLP 768 x 3072"])
titulo(ejes[0], "El adaptador es un 2 % de los parámetros",
       "la matriz base sigue ahi, pero congelada")
ejes[0].set_ylabel("parámetros entrenables (escala logaritmica)")
# La leyenda se dibuja a mano: asi no depende de que bar() etiquete una sola barra.
ejes[0].plot([], [], color=AZUL, linewidth=6, label="ajuste completo")
ejes[0].plot([], [], color=NARANJA, linewidth=6, label="LoRA r = 8")
ejes[0].legend(loc="upper center", ncol=2)
anotar(ejes[0], "2,08 % en la atención y 1,30 % en el MLP", xy=(3.6, 30720), xytext=(0.26, 0.45), color=NARANJA)
rejilla(ejes[0])
numeros(ejes[0])

# --- Panel 2: la correccion vive en un subespacio de dimension r ---
d, k, r, alpha = 8, 8, 2, 16
A = rng.normal(size=(r, k))
B = rng.normal(size=(d, r))
delta = (alpha / r) * (B @ A)                   # lo unico que LoRA puede sumar a la base
s = np.linalg.svd(delta, compute_uv=False)      # solo los r primeros valores singulares son > 0
indices = np.arange(1, d + 1)
colores = [NARANJA if v > 1e-10 else REJILLA for v in s]
ejes[1].bar(indices, s, color=colores, width=0.62)
ejes[1].set_xticks(indices)
ejes[1].axvline(r + 0.5, color=ROJO, linewidth=1.4, linestyle="--")
titulo(ejes[1], "Cuanta corrección cabe en el adaptador",
       "de 8 valores singulares solo 2 no son cero")
ejes[1].set_xlabel("índice del valor singular")
ejes[1].set_ylabel("valor singular de la corrección")
anotar(ejes[1], "cero exacto: esas direcciones no se tocan", xy=(6, 2.0), xytext=(0.42, 0.44), color=ROJO)
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "fine-tuning-y-lora-presupuesto-y-rango")
