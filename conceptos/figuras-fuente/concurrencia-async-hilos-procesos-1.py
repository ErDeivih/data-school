"""concurrencia-async-hilos-procesos-1.py — cuanto se tarda en hacer tres cosas a la vez y
por qué anadir nucleos deja de servir. La figura de la pagina de concurrencia (fase 11)."""

import numpy as np

from comun import *

estilo()

# Los tres tiempos del ejemplo de la pagina, en milisegundos.
tareas = ["a", "b", "c"]
duraciones = np.array([300.0, 200.0, 100.0])
inicio = np.concatenate([[0.0], np.cumsum(duraciones)[:-1]])   # donde empieza cada una en serie
suma_serie = duraciones.sum()                                 # 600 ms
suma_paralelo = duraciones.max()                              # 300 ms, la mas lenta

fig, ejes = plt.subplots(1, 2, figsize=(11.2, 4.3))

# --- Izquierda: las tres tareas, una tras otra y a la vez ---------------------
desplazamiento = 0.26
altura = 0.46
for fila, (tarea, d, arranque) in enumerate(zip(tareas, duraciones, inicio)):
    # Dos barras por tarea: arriba la serie (una tras otra) y abajo la concurrente (las tres
    # empezando en cero). Se ve de un golpe que en serie no se solapan.
    ejes[0].barh(fila + desplazamiento, d, left=arranque, height=altura, color=NARANJA)
    ejes[0].barh(fila - desplazamiento, d, left=0, height=altura, color=VERDE)
    ejes[0].text(arranque + d / 2, fila + desplazamiento, f"{d:.0f} ms", ha="center",
                 va="center", fontsize=8, color=TEXTO)
    ejes[0].text(d / 2, fila - desplazamiento, f"{d:.0f} ms", ha="center", va="center",
                 fontsize=8, color=TEXTO)

# Las dos lineas verticales marcan lo que tarda cada forma: la suma y el maximo.
ejes[0].axvline(suma_paralelo, color=MORADO, linestyle="--", linewidth=1.2)
ejes[0].axvline(suma_serie, color=ROJO, linestyle="--", linewidth=1.2)
anotar(ejes[0], f"a la vez: {suma_paralelo:.0f} ms", xy=(suma_paralelo, 1.55), xytext=(0.56, 0.62),
       color=MORADO)
anotar(ejes[0], f"una tras otra: {suma_serie:.0f} ms", xy=(suma_serie, -1.05), xytext=(0.55, 0.02),
       color=ROJO)

# Cada tarea arranca en un multiplo de 1,1 para dejar aire entre filas.
ejes[0].set_yticks([1.1 * i for i in range(len(tareas))])
ejes[0].set_yticklabels(tareas, fontsize=9)
ejes[0].set_ylim(-1.4, 3.9)
ejes[0].set_xlim(0, 660)
ejes[0].set_xlabel("milisegundos")
titulo(ejes[0], "Concurrencia: dejar de estar parado",
       "arriba de cada tarea, una tras otra; abajo, las tres a la vez")
rejilla(ejes[0], "x")
numeros(ejes[0], "x")

# --- Derecha: la ley de Amdahl, el techo que pone la parte que no se reparte ---
TOTAL, SERIE = 10.0, 2.0          # 10 s de trabajo, de los que 2 s no se pueden repartir
nucleos = np.arange(1, 65)
ganancia = TOTAL / (SERIE + (TOTAL - SERIE) / nucleos)
techo = TOTAL / SERIE             # con 2 s en serie, el maximo es 5x

ejes[1].axhline(techo, color=MORADO, linestyle="--", linewidth=1.3)
ejes[1].plot(nucleos, ganancia, color=AZUL, linewidth=2.0)
anotar(ejes[1], "techo: 10 s / 2 s en serie = 5x", xy=(56, techo), xytext=(0.55, 0.65),
       color=MORADO)
anotar(ejes[1], "de 1 a 4 nucleos se gana casi todo", xy=(4, ganancia[3]), xytext=(0.04, 0.18),
       color=AZUL)
anotar(ejes[1], "de 16 a 64, media vuelta para casi nada", xy=(16, ganancia[15]),
       xytext=(0.42, 0.24), color=AZUL)

ejes[1].set_xlabel("nucleos o procesos")
ejes[1].set_ylabel("veces más rapido que en serie")
ejes[1].set_xlim(1, 64)
ejes[1].set_ylim(1, 5.8)
titulo(ejes[1], "Los nucleos de más casi no se notan",
       "el 20 por ciento del trabajo que es serie pone el techo")
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "concurrencia-modelos-y-techo")
