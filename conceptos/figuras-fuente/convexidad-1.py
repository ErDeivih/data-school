"""convexidad-1.py — convexo significa «la cuerda va por encima» y «la tangente va por
debajo». Figura de la pagina de convexidad."""

import numpy as np

from comun import *

estilo()

# Tres paneles: en dos filas (2x2) cada uno es el doble de ancho que en una fila de tres,
# que es lo que hacía falta para que quepan los rótulos sin pisarse. El cuarto hueco se deja
# apagado.
fig, ejes = plt.subplots(2, 2, figsize=(9.6, 6.6))
ejes[1, 1].set_visible(False)
x = np.linspace(-3, 3, 400)

# --- Panel 1: la definicion, dibujada.
f = x**2
ejes[0, 0].plot(x, f, color=AZUL, linewidth=1.8)
ejes[0, 0].plot([-2, 2], [f[0], f[-1]], color=ROJO, linewidth=1.6)
ejes[0, 0].plot([-2, 2], [4, 4], "o", color=TEXTO, markersize=5)
ejes[0, 0].plot([0], [0], "o", color=AZUL, markersize=5)
ejes[0, 0].vlines(0, 0, 5.5, color=TEXTO, linewidth=0.8, linestyles=":")
anotar(ejes[0, 0], "el punto medio de la cuerda vale 4", xy=(0, 4), xytext=(0.34, 0.87),
       color=ROJO)
anotar(ejes[0, 0], "f en ese punto vale 0", xy=(0, 0), xytext=(0.58, 0.07), color=AZUL)
anotar(ejes[0, 0], "cuerda", xy=(-1.5, 4), xytext=(0.05, 0.40), color=ROJO)
anotar(ejes[0, 0], "f(x) = x^2", xy=(2.1, 4.4), xytext=(0.76, 0.30), color=AZUL)
titulo(ejes[0, 0], "Cuerda por encima: 0 <= 4, se cumple")
ejes[0, 0].set_ylim(-1.8, 9.5)
ejes[0, 0].set_xlabel("x")
ejes[0, 0].set_ylabel("f(x)")
rejilla(ejes[0, 0])
numeros(ejes[0, 0])

# --- Panel 2: el criterio de la tangente, que es el que se usa para optimizar.
t = np.linspace(-3, 3, 400)
g = t**2
x0 = -1.5
tangente = 2 * x0 * (t - x0) + x0**2       # f(x0) + f'(x0)(x - x0)
ejes[0, 1].plot(t, g, color=AZUL, linewidth=1.8)
ejes[0, 1].plot(t, tangente, color=VERDE, linewidth=1.4, linestyle="--")
ejes[0, 1].plot([x0], [x0**2], "o", color=TEXTO, markersize=5)
anotar(ejes[0, 1], "tangente en x = -1,5", xy=(x0, x0**2), xytext=(0.13, 0.86), color=VERDE)
anotar(ejes[0, 1], "toca la curva y se queda\npor debajo en todo lo demás", xy=(x0, x0**2),
       xytext=(0.30, 0.52), color=TEXTO)
titulo(ejes[0, 1], "Tangente por debajo: no sobreestima")
ejes[0, 1].set_ylim(-1.8, 9.5)
ejes[0, 1].set_xlabel("x")
ejes[0, 1].set_ylabel("f(x)")
rejilla(ejes[0, 1])
numeros(ejes[0, 1])

# --- Panel 3: sin convexidad, la cuerda corta la grafica.
h = x**3 - 3 * x
ejes[1, 0].plot(x, h, color=MORADO, linewidth=1.8)
ejes[1, 0].plot([-2, 2], [-2, 2], color=ROJO, linewidth=1.6)
ejes[1, 0].plot([-2, 2], [-2, 2], "o", color=TEXTO, markersize=5)
ejes[1, 0].plot([-1], [2], "o", color=ROJO, markersize=5)
ejes[1, 0].vlines(-1, -1, 2, color=ROJO, linewidth=1.0, linestyles=":")
anotar(ejes[1, 0], "la cuerda vale -1,\nla curva vale 2: falla", xy=(-1, 2),
       xytext=(0.22, 0.62), color=ROJO)
anotar(ejes[1, 0], "f(x) = x^3 - 3x", xy=(-2.4, -6.6), xytext=(0.06, 0.10), color=MORADO)
titulo(ejes[1, 0], "Cuerda por debajo: no es convexa")
ejes[1, 0].set_ylim(-20, 22)
ejes[1, 0].set_xlabel("x")
ejes[1, 0].set_ylabel("f(x)")
rejilla(ejes[1, 0])
numeros(ejes[1, 0])

guardar(fig, "convexidad-cuerda-y-tangente")
