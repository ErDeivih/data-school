"""probabilidad-condicional-1.py — condicionar no cambia los datos: reduce el espacio de
casos y reparte la probabilidad dentro del trozo que queda. Figura de la pagina de
probabilidad condicional."""

import numpy as np
from matplotlib.patches import Rectangle

from comun import *

estilo()
# Un poco mas alta que antes: entre el rotulo del eje x de arriba y el titulo del panel de
# abajo apenas quedaba aire.
fig, ejes = plt.subplots(2, 2, figsize=(9.6, 8.5))

# --- Panel 1: el espacio de casos y los dos sucesos, uno dentro del otro.
# Es un solo dado: seis caras equiprobables. 0 = ninguna, 1 = B (sale par), 2 = A (sale 6).
# Los dos sucesos se dibujan sobre las mismas seis celdas porque A esta dentro de B: el 6
# tambien es par. Antes eran dos dados y el rotulo de B pedia 18 casos sobre una sola columna.
S = np.array([[0, 1, 0, 1, 0, 2]])
ejes[0, 0].imshow(S, cmap="Blues", vmin=0, vmax=2, extent=(0, 6, 0, 1.6), aspect="auto")
for k in range(6):
    ejes[0, 0].text(k + 0.5, 0.8, str(k + 1), ha="center", va="center", fontsize=15,
                    color=TEXTO)
for k in (1, 3, 5):              # B: sale par -> las caras 2, 4 y 6
    ejes[0, 0].add_patch(Rectangle((k, 0), 1, 1.6, fill=False, edgecolor=VERDE, linewidth=2.0))
# A: sale 6 -> la ultima celda. El marco rojo va un poco por dentro para que se vean los dos.
ejes[0, 0].add_patch(Rectangle((5.07, 0.07), 0.86, 1.46, fill=False, edgecolor=ROJO,
                               linewidth=2.0))
ejes[0, 0].set_xticks([]); ejes[0, 0].set_yticks([])
for sp in ejes[0, 0].spines.values():
    sp.set_visible(True)
    sp.set_color(REJILLA)
# Arriba y abajo de la tira quedan dos franjas libres, una para cada rotulo.
ejes[0, 0].set_ylim(-0.9, 2.5)
anotar(ejes[0, 0], "A: sale 6 (la celda roja)", xy=(5.5, 1.7), xytext=(0.97, 0.93),
       color=ROJO, flecha=False, align="right")
anotar(ejes[0, 0], "B: sale par (las celdas 2, 4 y 6)", xy=(3, -0.4), xytext=(0.03, 0.07),
       color=VERDE, flecha=False)
titulo(ejes[0, 0], "6 casos, todos igual de probables")
ejes[0, 0].set_xlabel("cara del dado")

# --- Panel 2: los conjuntos, separados del resto.
ejes[0, 1].add_patch(Rectangle((0, 0), 6, 1.6, facecolor=REJILLA, alpha=0.15,
                               edgecolor=REJILLA, linewidth=1.0))
for k in range(6):
    ejes[0, 1].add_patch(Rectangle((k, 0), 1, 1.6, fill=False, edgecolor=REJILLA,
                                   linewidth=0.8))
for k in (1, 3, 5):              # B: 3 de los 6 casos, y dentro esta A
    ejes[0, 1].add_patch(Rectangle((k, 0), 1, 1.6, facecolor=AZUL, alpha=0.18,
                                   edgecolor=AZUL, linewidth=1.0))
ejes[0, 1].add_patch(Rectangle((5, 0), 1, 1.6, facecolor=ROJO, alpha=0.25,
                               edgecolor=ROJO, linewidth=2.0))
# Las cuatro notas se reparten entre las dos franjas libres: la de arriba de la caja y la de
# abajo. Antes las dos etiquetas de dentro caian sobre las celdas azules y no se sabia a cual
# apuntaban.
anotar(ejes[0, 1], "todo el espacio de casos: 6", xy=(3, 1.6), xytext=(0.04, 0.91),
       color=TEXTO, flecha=False)
anotar(ejes[0, 1], "A está dentro de B:\n1 caso de 3", xy=(5.5, 0.8), xytext=(0.97, 0.88),
       color=TEXTO, flecha=False, align="right")
anotar(ejes[0, 1], "A: sale 6\n1 caso", xy=(5.5, 0.8), xytext=(0.04, 0.16), color=ROJO)
anotar(ejes[0, 1], "B: sale par\n3 casos", xy=(3.5, 0.8), xytext=(0.42, 0.16), color=AZUL)
ejes[0, 1].set_xlim(-0.4, 6.4)
ejes[0, 1].set_ylim(-1.15, 2.2)
ejes[0, 1].set_xticks([]); ejes[0, 1].set_yticks([])
for sp in ejes[0, 1].spines.values():
    sp.set_visible(False)
titulo(ejes[0, 1], "Los dos sucesos, uno dentro del otro")

# --- Panel 3: con el dato, el espacio se encoge y hay que repartir.
# B tiene 3 casos, asi que el espacio condicional son 3 celdas iguales de 1/3, y A ocupa una.
for k in range(3):
    color_celda = ROJO if k == 2 else AZUL
    ejes[1, 0].add_patch(Rectangle((k, 0), 1, 1.6, facecolor=color_celda, alpha=0.20,
                                   edgecolor=color_celda, linewidth=1.4))
    ejes[1, 0].text(k + 0.5, 0.80, "1/3", ha="center", va="center", color=TEXTO, fontsize=13)
ejes[1, 0].set_xlim(0, 3)
ejes[1, 0].set_xticks([]); ejes[1, 0].set_yticks([])
for sp in ejes[1, 0].spines.values():
    sp.set_visible(True)
    sp.set_color(REJILLA)
# La formula que antes iba al pie de la figura (fig.text) y se escribia encima del rotulo del
# eje x; aqui cabe como linea pequena del titulo, que es su sitio.
anotar(ejes[1, 0], "los 6 casos se quedan en 3, los de B:\nvuelve a sumar 1",
       xy=(1.5, 1.6), xytext=(0.03, 0.86), color=TEXTO, flecha=False)
anotar(ejes[1, 0], "1 de esos 3 es A (el 6 también es par): P(A | B) = 1/3 = 0,333",
       xy=(2.5, 0.0), xytext=(0.03, 0.09), color=TEXTO, flecha=False)
ejes[1, 0].set_ylim(-1.2, 3.0)
titulo(ejes[1, 0], "Sabiendo que B ha pasado, solo queda B",
       "P(A | B) = P(A y B) / P(B)")

# --- Panel 4: la misma probabilidad condicional, movida por la prevalencia.
sensibilidad = 0.99
especificidad = 0.95
prevalencias = np.linspace(0.001, 0.10, 300)
posterior = sensibilidad * prevalencias / (sensibilidad * prevalencias
                                           + (1 - especificidad) * (1 - prevalencias))
ejes[1, 1].plot(prevalencias * 100, posterior, color=ROJO, linewidth=1.9)
ejes[1, 1].axhline(sensibilidad, color=MORADO, linewidth=1.2, linestyle="--")
ejes[1, 1].plot([1], [0.167], "o", color=ROJO, markersize=7, zorder=5)
ejes[1, 1].plot([5], [0.510], "o", color=ROJO, markersize=5, zorder=5)
# El nombre de la curva roja se va al eje y: como texto suelto caia sobre la propia curva.
ejes[1, 1].set_ylabel("P(enfermo | positivo)")
# Por encima de la linea de 0,99 no hay nada mas: alli cabe su rotulo sin pisarla.
anotar(ejes[1, 1], "P(positivo | enfermo) = 0,99: no se mueve", xy=(7.5, 0.99),
       xytext=(0.98, 0.955), color=MORADO, flecha=False, align="right")
# La esquina de arriba a la izquierda esta libre: la curva pasa muy por debajo.
anotar(ejes[1, 1], "con la enfermedad al 1 % acierta\nsolo el 16,7 % de los positivos",
       xy=(1.1, 0.167), xytext=(0.03, 0.72), color=TEXTO)
# Y la franja de abajo a la derecha tambien, porque la curva ya ha subido.
anotar(ejes[1, 1], "al 5 % ya pasa del 50 %", xy=(5, 0.510), xytext=(0.55, 0.20),
       color=TEXTO)
ejes[1, 1].set_xlim(0, 10)
ejes[1, 1].set_ylim(0, 1.12)
ejes[1, 1].set_xlabel("prevalencia de la enfermedad (%)")
titulo(ejes[1, 1], "El test no cambia: cambia la enfermedad")
rejilla(ejes[1, 1])
numeros(ejes[1, 1], "y")

guardar(fig, "condicional-encoge-el-espacio")
