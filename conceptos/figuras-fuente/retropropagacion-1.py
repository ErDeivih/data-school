"""retropropagacion-1.py — cuánto cuesta el paso hacia atrás y cuánto gradiente llega abajo.

Izquierda: el coste de un paso, en operaciones, frente al número de parámetros. El paso hacia
atrás va en paralelo al de ida (un factor constante), mientras que comprobar el gradiente
perturbando cada peso cuesta P pasos hacia delante. Por eso las diferencias finitas sirven
para verificar, no para entrenar.
Derecha: la norma del gradiente en cada capa de una red de cinco, relativa a la última. Con
sigmoide el error se apaga por el camino; con ReLU se mantiene.
La figura de la página de retropropagación (fase 7).
"""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.4))

# --- Izquierda: lo que cuesta cada forma de obtener el gradiente ---------------------
ax = ejes[0]
P = np.logspace(3.0, 8.0, 200)
ax.plot(P, P, color=AZUL, linewidth=1.8)
ax.plot(P, 2.0 * P, color=VERDE, linewidth=1.8)
# Perturbar cada peso arriba y abajo son dos pasadas completas por cada parámetro
ax.plot(P, 2.0 * P ** 2, color=ROJO, linewidth=1.8, linestyle="--")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_ylim(1e2, 3e17)
# Sin leyenda: cada curva se nombra con una nota de su color, en el hueco que deja libre.
anotar(ax, "paso hacia delante", xy=(2e5, 2e5), xytext=(0.62, 0.22), color=AZUL)
anotar(ax, "paso hacia atrás\n(retropropagación)", xy=(6e6, 1.2e7), xytext=(0.62, 0.32),
       color=VERDE)
anotar(ax, "comprobar peso a peso:\n10¹⁶ pasadas hacia delante",
       xy=(2e6, 8e12), xytext=(0.10, 0.72), color=ROJO)
titulo(ax, "El paso hacia atrás cuesta lo mismo que el de ida",
       "operaciones por paso, en escala logarítmica, frente al número de parámetros")
ax.set_xlabel("parámetros del modelo")
ax.set_ylabel("operaciones por paso")
rejilla(ax)
numeros(ax)


def normas_por_capa(activacion, derivada, capas=5, ancho=32, n=64):
    """Norma del gradiente de la pérdida respecto a los pesos de cada capa.

    La red es una pila de capas de `ancho` unidades y la pérdida es la media de la salida,
    así que el delta de la última capa vale 1/n. Todo se calcula a mano: es exactamente el
    mismo encadenado de deltas que explica la página.
    """
    rng = np.random.default_rng(7)
    pesos = [rng.normal(0.0, 1.0 / np.sqrt(ancho), (ancho, ancho)) for _ in range(capas)]
    a = [rng.normal(size=(n, ancho))]           # las entradas, capa 0
    zs = []                                     # preactivaciones, para poder usar φ'(z)
    for W in pesos:
        zs.append(a[-1] @ W)
        a.append(activacion(zs[-1]))

    delta = np.full((n, ancho), 1.0 / n)        # δ de la salida con L = media de las salidas
    normas = []
    for capa in range(capas - 1, -1, -1):
        normas.append(float(np.linalg.norm(a[capa].T @ delta)))     # ∂L/∂W de esa capa
        if capa > 0:                            # (W)ᵀ reparte el error hacia atrás
            delta = (delta @ pesos[capa].T) * derivada(zs[capa - 1])
    return np.array(normas[::-1])               # de la primera capa a la última


sigmoide = lambda z: 1.0 / (1.0 + np.exp(-z))
d_sigmoide = lambda z: sigmoide(z) * (1.0 - sigmoide(z))
relu = lambda z: np.maximum(0.0, z)
d_relu = lambda z: (z > 0).astype(float)

norm_sig = normas_por_capa(sigmoide, d_sigmoide)
norm_relu = normas_por_capa(relu, d_relu)
capas = np.arange(1, len(norm_sig) + 1)

# --- Derecha: cuánto gradiente llega a cada capa -------------------------------------
ax = ejes[1]
ax.semilogy(capas, norm_sig / norm_sig[-1], color=AZUL, linewidth=1.8, marker="o",
            markersize=5, label="activación sigmoide")
ax.semilogy(capas, norm_relu / norm_relu[-1], color=VERDE, linewidth=1.8, marker="o",
            markersize=5, label="activación ReLU")
cociente = f"{norm_sig[0] / norm_sig[-1]:.1e}".replace(".", ",")   # coma decimal, como el portal
anotar(ax, f"con sigmoide la primera capa recibe\n{cociente} de lo que recibe la última",
       xy=(1.0, norm_sig[0] / norm_sig[-1]), xytext=(0.40, 0.10), color=AZUL)
anotar(ax, "con ReLU el gradiente llega\ndel mismo orden a todas las capas",
       xy=(4.0, norm_relu[3] / norm_relu[-1]), xytext=(0.42, 0.92), color=VERDE)
titulo(ax, "El gradiente de las primeras capas se apaga",
       "norma del gradiente de cada capa, relativa a la última, en escala logarítmica")
ax.set_xlabel("capa (1 = la más cercana a la entrada)")
ax.set_ylabel("norma del gradiente, relativa")
ax.set_ylim(1e-3, 3.0)          # el hueco de arriba queda libre para la nota
ax.set_xticks(capas)
ax.legend(loc="upper left")
rejilla(ax)
numeros(ax, ejes="x")

guardar(fig, "retropropagacion-coste-y-desvanecimiento")
