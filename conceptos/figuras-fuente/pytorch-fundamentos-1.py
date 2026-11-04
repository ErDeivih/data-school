"""pytorch-fundamentos-1.py — el bucle de entrenamiento a mano y de dónde salen los lotes.

Izquierda: el mismo bucle de cinco pasos sobre y = 2x. Con η = 0,1 la pérdida baja de 30 a
3·10⁻⁷; con η = 0,13 el factor por paso supera 1 en valor absoluto y la pérdida acaba en 10²⁸.
Derecha: lo que hace el DataLoader con 1000 muestras y batch_size = 32: 31 lotes completos y un
lote corto de 8 muestras que también cuenta.
La figura de la página de PyTorch: fundamentos (fase 7).
"""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.4))

# --- Izquierda: la misma pérdida con dos tasas de aprendizaje -------------------------
ax = ejes[0]
x = np.array([[1.0], [2.0], [3.0], [4.0]])
y = np.array([[2.0], [4.0], [6.0], [8.0]])      # la relacion exacta es y = 2x

for lr, color, etiqueta in ((0.10, AZUL, "η = 0,10"), (0.13, ROJO, "η = 0,13")):
    w, b = np.zeros((1, 1)), 0.0
    perdidas = []
    for _ in range(200):
        prediccion = x @ w + b                  # 1. hacia delante
        perdidas.append(float(np.mean((prediccion - y) ** 2)))   # 2. la perdida
        error = prediccion - y                  # 3. hacia atras, a mano
        w -= lr * (2 * x.T @ error / len(x))    # 4. paso del optimizador
        b -= lr * (2 * error.mean())
    ax.semilogy(np.arange(200), perdidas, color=color, linewidth=1.9, label=etiqueta)

anotar(ax, "η = 0,13: la pérdida acaba en 10²⁸", xy=(200.0, 5.9e28), xytext=(0.26, 0.91),
       color=ROJO)
anotar(ax, "η = 0,10: el modelo recupera y = 2x", xy=(199.0, 3.5e-7), xytext=(0.30, 0.07),
       color=AZUL)
titulo(ax, "La misma pérdida y dos tasas de aprendizaje",
       "MSE de y = 2x con cuatro puntos, en escala logarítmica")
ax.set_xlabel("paso del bucle")
ax.set_ylabel("pérdida")
ax.set_ylim(1e-9, 1e32)
ax.legend(loc="upper left")
rejilla(ax)
numeros(ax, ejes="x")

# --- Derecha: cómo reparte el DataLoader 1000 muestras en lotes de 32 ------------------
ax = ejes[1]
muestras, tamano = 1000, 32
cortes = np.arange(0, muestras, tamano)
en_lote = np.minimum(tamano, muestras - cortes)          # el ultimo lote va corto
colores = [ROJO if n < tamano else AZUL for n in en_lote]
ax.bar(np.arange(en_lote.size), en_lote, width=0.72, color=colores, zorder=3)
ax.axhline(tamano, color=REJILLA, linewidth=1.1, linestyle="--")
anotar(ax, "31 lotes de 32 muestras", xy=(14.0, tamano), xytext=(0.02, 0.92), color=AZUL)
anotar(ax, "el último lleva 8", xy=(31.0, 8.0), xytext=(0.68, 0.92), color=ROJO)
titulo(ax, "1000 muestras en lotes de 32: 32 lotes, no 31",
       "muestras que lleva cada lote de una época")
ax.set_xlabel("índice del lote")
ax.set_ylabel("muestras en el lote")
ax.set_ylim(0, 42)
ax.set_xlim(-0.9, 32.4)
rejilla(ax)
numeros(ax)

guardar(fig, "pytorch-fundamentos-bucle-y-lotes")
