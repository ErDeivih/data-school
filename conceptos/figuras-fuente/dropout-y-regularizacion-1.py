"""dropout-y-regularizacion-1.py — qué conserva el dropout y qué destruye el decaimiento.

Izquierda: los 16 resultados posibles de una máscara sobre una capa de cuatro unidades. Ninguno
tiene por qué caer en la media original (1,125), pero el promedio de todos cae exactamente ahí:
eso es lo que arregla el reescalado 1/(1 − p).
Derecha: un peso que no recibe gradiente ninguno, solo empujado por la penalización L2. Con
λ = 0,01 sobrevive; con λ = 0,1 el factor por paso cambia de 0,999 a 0,99 y el peso desaparece.
La figura de la página de dropout y regularización (fase 7).
"""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.4))

# --- Izquierda: el dropout conserva la esperanza, no cada sorteo ----------------------
ax = ejes[0]
h = np.array([2.0, -1.0, 0.5, 3.0])
p = 0.5
# Las 2^4 mascaras posibles, cada una con probabilidad 1/16.
mascaras = ((np.arange(16)[:, None] >> np.arange(h.size)) & 1).astype(float)
salidas = (h * mascaras / (1 - p)).mean(axis=1)      # media de la capa en cada sorteo
valores, cuantas = np.unique(salidas, return_counts=True)
# El sorteo del ejemplo de la pagina: mascara [1, 1, 1, 0], que da una media de 0,75.
ejemplo = (h * np.array([1.0, 1.0, 1.0, 0.0]) / (1 - p)).mean()
colores = [ROJO if abs(v - ejemplo) < 1e-9 else AZUL for v in valores]
ax.bar(valores, cuantas / 16.0, width=0.16, color=colores, zorder=3)
ax.axvline(h.mean(), color=VERDE, linewidth=1.6, linestyle="--")
anotar(ax, "el sorteo del ejemplo da 0,75", xy=(ejemplo, cuantas[valores == ejemplo][0] / 16.0),
       xytext=(0.06, 0.90), color=ROJO)
anotar(ax, "los 16 sorteos\npromedian 1,125", xy=(1.125, 0.135), xytext=(0.71, 0.74),
       color=VERDE)
titulo(ax, "El dropout mueve cada sorteo y no la esperanza",
       "media de la capa en las 16 máscaras posibles")
ax.set_xlabel("media de la salida de la capa en ese sorteo")
ax.set_ylabel("probabilidad del sorteo")
ax.set_ylim(0, 0.19)
ax.set_xlim(-0.4, 4.9)
rejilla(ax)
numeros(ax)

# --- Derecha: el decaimiento de pesos encoge aunque no haya gradiente ------------------
ax = ejes[1]
pasos = np.arange(0, 1001)
eta = 0.1
for lam, color in ((0.01, VERDE), (0.1, ROJO)):
    ax.semilogy(pasos, (1 - eta * lam) ** pasos, color=color, linewidth=1.9,
                label=f"λ = {lam:.2f}".replace(".", ","))
anotar(ax, "λ = 0,01:\nel peso acaba en 0,368", xy=(1000.0, 0.368), xytext=(0.68, 0.70),
       color=VERDE)
anotar(ax, "λ = 0,1:\nel peso queda borrado", xy=(1000.0, (1 - eta * 0.1) ** 1000),
       xytext=(0.36, 0.28), color=ROJO)
titulo(ax, "Diez veces más λ pasa de encoger a borrar",
       "un peso sin ningún gradiente, con η = 0,1")
ax.set_xlabel("paso de entrenamiento")
ax.set_ylabel("valor del peso")
ax.set_ylim(1e-6, 3.0)
ax.legend(loc="lower left")
rejilla(ax)
numeros(ax, ejes="x")

guardar(fig, "dropout-y-regularizacion-esperanza-y-encogimiento")
