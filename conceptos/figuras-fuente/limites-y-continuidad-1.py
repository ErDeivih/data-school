"""limites-y-continuidad-1.py — el límite no mira el valor en el punto; la continuidad sí.

Figura de la página de límites y continuidad (fase 1)."""

import numpy as np

from comun import *

estilo()


def f(x):
    return x + 1.0          # (x^2 - 1)/(x - 1) simplificado para x != 1


def s(x):
    return np.sign(x)       # la función signo: su límite en 0 no existe


x = np.linspace(-2.6, 3.6, 600)

fig, (arr, aba) = plt.subplots(2, 1, figsize=(7.6, 6.8))

# --- Panel de arriba: la función, su hueco y lo que vale el límite ---
arr.plot(x, f(x), color=AZUL, linewidth=1.8)
arr.plot([1.0], [2.0], marker="o", markersize=7, markerfacecolor="white",
         markeredgecolor=AZUL, markeredgewidth=1.6)
arr.plot([1.0], [1.0], marker="o", color=ROJO, markersize=6)
arr.plot([0.9, 0.99], [1.9, 1.99], color=NARANJA, linewidth=1.6, linestyle="--")
arr.plot([1.01, 1.1], [2.01, 2.1], color=NARANJA, linewidth=1.6, linestyle="--")
# La recta sube de izquierda a derecha: la esquina de arriba a la izquierda y la de abajo a
# la derecha son las dos zonas libres, y cada nota se queda en la suya.
anotar(arr, "el límite vale 2 y no depende del hueco", xy=(1.0, 2.0),
       xytext=(0.03, 0.90), color=AZUL)
anotar(arr, "f(1) no existe: aquí hay 0/0,\npero los valores se acercan a 2", xy=(1.0, 1.0),
       xytext=(0.56, 0.12), color=ROJO)
arr.set_xlim(-2.6, 3.6)
arr.set_ylim(-0.2, 3.9)
titulo(arr, "El límite no mira el valor en el punto",
       "f(1) no existe, pero los valores se acercan a 2")
arr.set_xlabel("x")
arr.set_ylabel("f(x) = (x² − 1)/(x − 1)")
rejilla(arr, "both")
numeros(arr)

# --- Panel de abajo: el salto, donde el límite no existe ---
aba.plot(x[x <= -0.1], s(x[x <= -0.1]), color=MORADO, linewidth=1.8)
aba.plot(x[x >= 0.1], s(x[x >= 0.1]), color=MORADO, linewidth=1.8)
aba.plot([-0.1, 0.0], [-1, -1], color=MORADO, linewidth=1.8)
aba.plot([0.0, 0.1], [1, 1], color=MORADO, linewidth=1.8)
aba.plot([0.0], [0.0], marker="o", color=MORADO, markersize=6)
aba.plot([0.0], [1.0], marker="o", markersize=7, markerfacecolor="white",
         markeredgecolor=MORADO, markeredgewidth=1.5)
aba.plot([0.0], [-1.0], marker="o", markersize=7, markerfacecolor="white",
         markeredgecolor=MORADO, markeredgewidth=1.5)
# Las dos mesetas dejan libre la banda de arriba y la de abajo: una nota en cada una.
anotar(aba, "el límite no existe: los dos laterales\nno coinciden y la función da un salto",
       xy=(0.0, 0.05), xytext=(0.03, 0.88), color=ROJO, flecha=False)
anotar(aba, "lateral derecho: +1", xy=(1.2, 1.0), xytext=(0.60, 0.90), color=MORADO)
anotar(aba, "lateral izquierdo: −1", xy=(-1.2, -1.0), xytext=(0.03, 0.08), color=MORADO)
aba.set_xlim(-2.6, 3.6)
aba.set_ylim(-2.3, 2.3)
titulo(aba, "Aquí sí se rompe: los laterales no coinciden",
       "los dos existen, pero no apuntan al mismo valor")
aba.set_xlabel("x")
aba.set_ylabel("signo de x")
rejilla(aba, "both")
numeros(aba)

guardar(fig, "limites-hueco-y-salto")
