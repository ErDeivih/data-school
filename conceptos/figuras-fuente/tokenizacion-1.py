"""tokenizacion-1.py — el compromiso de la tokenización por subpalabras y lo caros que son los números.

Izquierda: el corpus de juguete con el que la página sigue BPE paso a paso. «baja» aparece 5
veces y acaba en una sola pieza; «bajada» aparece 2 veces y acaba en cuatro. Lo frecuente se
comprime y lo raro se fragmenta, y eso es todo el algoritmo.
Derecha: cuántos tokens gasta cada palabra. Una palabra normal en español ronda 1,35 tokens;
una con dígitos se va a 4. Contar tokens como si fueran palabras subestima el consumo.
La figura de la página de tokenización (fase 7).
"""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.4))

# --- Izquierda: el corpus de juguete, antes y después de BPE --------------------------
ax = ejes[0]
palabras = ["baja", "bajo", "bajada"]
veces = [5, 3, 2]                       # frecuencia en el corpus de juguete
piezas = [1, 1, 4]                      # tokens en que queda cada palabra tras las fusiones
posiciones = np.arange(len(palabras))
ancho = 0.36
b1 = ax.bar(posiciones - ancho / 2, veces, ancho, color=AZUL)
b2 = ax.bar(posiciones + ancho / 2, piezas, ancho, color=NARANJA)
for barras in (b1, b2):
    ax.bar_label(barras, labels=[str(int(v)) for v in barras.datavalues], padding=3,
                 fontsize=9)
anotar(ax, "lo frecuente se comprime en una pieza;\nlo raro se queda en trozos pequeños",
       xy=(2.18, 4), xytext=(0.03, 0.93), flecha=False)
titulo(ax, "Lo frecuente se comprime; lo raro se parte",
       "corpus de juguete: «baja» 5 veces, «bajo» 3 y «bajada» 2")
ax.set_xticks(posiciones, palabras)
ax.set_ylabel("cuenta")
ax.set_ylim(0, 6.6)                     # aire arriba para las notas y los valores
rejilla(ax)
numeros(ax, ejes="y")                   # el eje x son palabras: no lleva coma decimal

# --- Derecha: lo que cuesta una palabra según lo que lleve dentro ---------------------
ax = ejes[1]
etiquetas = ["palabra\nnormal", "palabra con\ndígitos"]
coste = [1.35, 4.0]                     # tokens por palabra, del ejercicio de la página
barras = ax.bar(etiquetas, coste, color=[AZUL, NARANJA], width=0.5)
ax.bar_label(barras, labels=["1,35", "4,00"], padding=4, fontsize=9)
anotar(ax, "contar tokens como si fueran palabras\nsubestima el consumo alrededor de un 25 %",
       xy=(1.25, 3.7), xytext=(0.03, 0.93), color=NARANJA)
titulo(ax, "Los números gastan muchos más tokens",
       "tokens por palabra en español: texto normal frente a palabras con dígitos")
ax.set_ylabel("tokens por palabra")
ax.set_ylim(0, 5.3)                     # aire arriba para la nota
rejilla(ax)
numeros(ax, ejes="y")                   # el eje x son categorías: no lleva coma decimal

guardar(fig, "tokenizacion-bpe-y-coste")
