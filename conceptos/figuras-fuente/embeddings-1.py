"""embeddings-1.py — qué significa que la distancia signifique algo.

Izquierda: cuatro palabras dibujadas como flechas desde el origen, en dos dimensiones de un
espacio que en realidad tiene cientos. Los animales apuntan casi en la misma dirección y los
vehículos en otra casi perpendicular: el coseno dentro del grupo roza 1 y entre grupos roza 0.
Derecha: el mismo par de palabras medido con one-hot y con embeddings. Con one-hot todos los
pares dan 0, así que el modelo no tiene ninguna pista de parecido.
La figura de la página de embeddings (fase 7).
"""

import numpy as np

from comun import *

estilo()

# Cuatro vectores de dos dimensiones, inventados pero verosímiles: cada grupo apunta en su
# propia dirección. En un espacio real serían 300 números por palabra.
VECTORES = {
    "gato": (1.00, 0.03),
    "perro": (0.95, 0.14),
    "coche": (0.03, 1.00),
    "moto": (0.14, 0.86),
}
COLOR = {"gato": AZUL, "perro": AZUL, "coche": VERDE, "moto": VERDE}


def coseno(a, b):
    """Coseno entre dos vectores: 1 si apuntan igual, 0 si son perpendiculares."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def num(x, dec=2):
    """Número con coma decimal, como se escribe en el portal."""
    return f"{x:.{dec}f}".replace(".", ",")


fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.6))

# --- Izquierda: la geometría ----------------------------------------------------------
ax = ejes[0]
# Cada palabra es una flecha desde el origen: lo que se compara es la dirección, no el largo.
for palabra, (x, y) in VECTORES.items():
    ax.annotate("", xy=(x, y), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color=COLOR[palabra], linewidth=1.9))
# Las etiquetas van pegadas a la punta, cada una hacia el lado donde no hay nada.
ax.text(1.04, 0.06, "gato", color=AZUL, fontsize=9, ha="left", va="center")
ax.text(0.93, 0.22, "perro", color=AZUL, fontsize=9, ha="right", va="center")
ax.text(0.07, 1.05, "coche", color=VERDE, fontsize=9, ha="left", va="center")
ax.text(0.15, 0.80, "moto", color=VERDE, fontsize=9, ha="left", va="center")
anotar(ax, f"animales entre sí: {num(coseno(VECTORES['gato'], VECTORES['perro']))}\n"
           f"vehículos entre sí: {num(coseno(VECTORES['coche'], VECTORES['moto']))}\n"
           f"un animal y un vehículo: {num(coseno(VECTORES['gato'], VECTORES['coche']))}",
       xy=(0.5, 0.1), xytext=(0.30, 0.66), flecha=False)
titulo(ax, "Dos grupos, dos direcciones",
       "cada palabra es una dirección; el coseno mide el ángulo entre dos")
ax.set_xlim(-0.05, 1.40)
ax.set_ylim(-0.05, 1.30)
ax.set_xlabel("dimensión 1 (de las 300 que tendría de verdad)")
ax.set_ylabel("dimensión 2")
rejilla(ax, eje="both")
numeros(ax)

# --- Derecha: el mismo par medido de las dos maneras ----------------------------------
ax = ejes[1]
pares = ["gato\ny perro", "coche\ny moto", "gato\ny coche"]
similitud = [coseno(VECTORES["gato"], VECTORES["perro"]),
             coseno(VECTORES["coche"], VECTORES["moto"]),
             coseno(VECTORES["gato"], VECTORES["coche"])]
barras = ax.bar(pares, similitud, color=AZUL, width=0.5)
ax.bar_label(barras, labels=[num(v) for v in similitud], padding=4, fontsize=9)
# Con one-hot el coseno es 0 en TODOS los pares: no hay barra que dibujar, hay una raya.
ax.axhline(0.0, color=ROJO, linewidth=1.6, linestyle="--")
anotar(ax, "con one-hot el coseno es 0 en todos los pares:\n"
           "«perro» y «helicóptero» quedan igual de lejos",
       xy=(1.0, 0.0), xytext=(0.03, 0.90), color=ROJO, flecha=False)
titulo(ax, "One-hot frente a embeddings",
       "coseno entre pares de palabras: el one-hot no distingue ninguno")
ax.set_ylabel("coseno entre las dos palabras")
ax.set_ylim(0, 1.50)                    # aire arriba para la nota y los valores
rejilla(ax)
numeros(ax, ejes="y")                   # el eje x es de categorías: no lleva coma decimal

guardar(fig, "embeddings-geometria-y-coseno")
