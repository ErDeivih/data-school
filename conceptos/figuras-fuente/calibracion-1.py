"""calibracion-1.py — el diagrama de fiabilidad de los cinco tramos del ejemplo y por qué
el AUC no distingue dos modelos con el mismo orden. Figura de la página de calibración de
probabilidades (fase 6)."""

import numpy as np

from comun import *

estilo()

# --- Panel izquierdo: los cinco tramos de la tabla del ejemplo. `casos` se usa para el
# tamaño del punto, para que se vea qué tramos pesan de verdad en el ECE.
confianza = np.array([0.12, 0.31, 0.52, 0.71, 0.88])
casos = np.array([300, 250, 200, 150, 100])
observada = np.array([0.10, 0.28, 0.55, 0.62, 0.74])
ece = float((casos / casos.sum() * np.abs(observada - confianza)).sum())

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.4))

ejes[0].plot([0, 1], [0, 1], color=TEXTO, linewidth=1.1, linestyle="--")
ejes[0].plot(confianza, observada, color=AZUL, linewidth=1.5)
ejes[0].scatter(confianza, observada, s=casos / 2.2, color=AZUL, zorder=3)
anotar(ejes[0], "aquí promete 0,88\ny cumple 0,74", xy=(0.88, 0.74), xytext=(0.52, 0.27),
       color=ROJO)
anotar(ejes[0], "la diagonal es la calibración perfecta", xy=(0.6, 0.6),
       xytext=(0.30, 0.10), color=TEXTO, flecha=False)
ejes[0].set_xlim(-0.02, 1.02)
ejes[0].set_ylim(-0.02, 1.02)
ejes[0].set_xlabel("lo que dijo el modelo (confianza media del tramo)")
ejes[0].set_ylabel("lo que pasó\n(frecuencia real de positivos)")
rejilla(ejes[0], "both")
numeros(ejes[0])
titulo(ejes[0], "Diagrama de fiabilidad: el tamaño es el nº de casos",
       f"ECE {ece:.3f}".replace(".", ",") + ": los puntos salen por debajo de la diagonal, sobre todo arriba")

# --- Panel derecho: dos modelos que ordenan exactamente igual. Elevar al cuadrado es una
# transformación creciente, así que el AUC no se mueve; la escala de las probabilidades,
# sí, y con ella el Brier.
p = np.linspace(0.02, 0.98, 200)
ejes[1].plot(p, p, color=TEXTO, linewidth=1.1, linestyle="--",
             label="calibrado: Brier 0,175")
ejes[1].plot(p, p ** 2, color=VERDE, linewidth=1.9,
             label="mismo orden, escala rota: Brier 0,210")
ejes[1].legend(loc="upper left")
anotar(ejes[1], "aquí dice 0,75 y la realidad es 0,56", xy=(0.75, 0.5625),
       xytext=(0.38, 0.12), color=VERDE)
ejes[1].set_xlim(-0.02, 1.02)
ejes[1].set_ylim(-0.02, 1.02)
ejes[1].set_xlabel("probabilidad que dice el modelo")
ejes[1].set_ylabel("probabilidad real\nde que sea positivo")
rejilla(ejes[1], "both")
numeros(ejes[1])
titulo(ejes[1], "Mismo orden, distinta escala",
       "el AUC de los dos es 0,816; solo uno de ellos sirve para decidir por coste")

guardar(fig, "calibracion-fiabilidad-y-brier")
