"""rnn-lstm-gru-1.py — por qué la recurrencia se olvida y qué cuesta cada celda.

Izquierda: lo que sobrevive al retropropagar por el tiempo cuando cada paso multiplica el
gradiente por un factor. Con 0,25 la señal se apaga en veinte pasos; con 0,9 aguanta; con
1,5 se dispara. Es el producto lo que decide, no un error de cálculo.
Derecha: los parámetros que gasta cada celda con la misma entrada y el mismo estado. La GRU
hace casi lo mismo que la LSTM con tres puertas en vez de cuatro.
La figura de la página de RNN, LSTM y GRU (fase 7).
"""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.4))

# --- Izquierda: lo que sobrevive al retroceder n pasos -------------------------------
ax = ejes[0]
pasos = np.arange(0, 51)
for factor, color in ((0.25, ROJO), (0.9, AZUL), (1.5, VERDE)):
    ax.semilogy(pasos, factor ** pasos, color=color, linewidth=1.8)
# La línea del 1 separa lo que se apaga de lo que crece: es la referencia, no una curva.
ax.axhline(1.0, color=TEXTO, linewidth=0.8, alpha=0.45)
# En vez de leyenda, cada curva se nombra en su color en el hueco de abajo a la izquierda.
anotar(ax, "factor 0,25 por paso:  0,25^50 = 8·10⁻³¹, se apaga",
       xy=(50, 0.25 ** 50), xytext=(0.03, 0.21), color=ROJO, flecha=False)
anotar(ax, "factor 0,90 por paso:  0,90^50 = 5·10⁻³, sobrevive",
       xy=(50, 0.9 ** 50), xytext=(0.03, 0.12), color=AZUL, flecha=False)
anotar(ax, "factor 1,50 por paso:  1,50^50 = 6·10⁸, explota",
       xy=(50, 1.5 ** 50), xytext=(0.03, 0.03), color=VERDE, flecha=False)
titulo(ax, "El gradiente que sobrevive tras n pasos",
       "producto de un factor por paso, en escala logarítmica")
ax.set_xlabel("pasos hacia atrás (longitud de la secuencia)")
ax.set_ylabel("señal que llega al primer paso")
ax.set_xlim(0, 52)
ax.set_ylim(1e-32, 1e10)
rejilla(ax)
numeros(ax, ejes="x")

# --- Derecha: lo que cuesta cada tipo de celda ---------------------------------------
d, m = 10, 20                          # 10 entradas y 20 unidades de estado
etiquetas = ["RNN", "LSTM", "GRU"]
valores = [d * m + m * m + m,               # una matriz de entrada, una recurrente, un sesgo
           4 * (d * m + m * m) + 4 * m,     # cuatro puertas
           3 * (d * m + m * m) + 3 * m]     # tres puertas
ax = ejes[1]
barras = ax.bar(etiquetas, valores, color=[AZUL, MORADO, VERDE], width=0.6)
# El valor encima de cada barra: la altura no se lee bien de un vistazo.
ax.bar_label(barras, labels=[f"{v:,}".replace(",", ".") for v in valores], padding=4,
             fontsize=9)
anotar(ax, "tres puertas en vez de cuatro:\nun 25 % menos de parámetros",
       xy=(2.30, 1800), xytext=(0.97, 0.93), color=VERDE, align="right")
titulo(ax, "Lo que cuesta cada celda",
       "parámetros con 10 entradas y 20 unidades de estado")
ax.set_ylabel("parámetros que se aprenden")
ax.set_ylim(0, 3250)                   # deja aire encima para el valor y para la nota
rejilla(ax)
numeros(ax, ejes="y")

guardar(fig, "rnn-lstm-gru-gradiente-y-pesos")
