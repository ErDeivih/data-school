"""causalidad-vs-correlacion-1.py — una correlación que no es una causa.

Izquierda: dos variables sin ninguna relación entre ellas se mueven juntas, porque las mueve
una tercera variable que no esta en el gráfico ni en los datos. Derecha: la misma pareja
después de descontar esa causa comun; la relación desaparece.
La figura de la pagina de causalidad frente a correlación (fase 2)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)
n = 400

z = azar.normal(0, 1, n)                    # la causa comun: no se mide, no se ve
x = z + azar.normal(0, 1, n)
y = z + azar.normal(0, 1, n)
bruta = float(np.corrcoef(x, y)[0, 1])

# Se quita de cada variable la parte que explica z. Lo que sobra ya no lleva su sombra.
sobra_x = x - np.polyval(np.polyfit(z, x, 1), z)
sobra_y = y - np.polyval(np.polyfit(z, y, 1), z)
limpia = float(np.corrcoef(sobra_x, sobra_y)[0, 1])

LIMITES = (-4.6, 4.6)


def nube(ax, hx, hy, color):
    """La nube con su recta ajustada: la pendiente se VE, que es lo que hay que comparar."""
    ax.scatter(hx, hy, s=13, color=color, alpha=0.40, edgecolors="none", zorder=2)
    pendiente, corte = np.polyfit(hx, hy, 1)
    xs = np.array(LIMITES)
    ax.plot(xs, pendiente * xs + corte, color=ROJO, linewidth=1.7, zorder=3)
    ax.axhline(0, color=REJILLA, linewidth=0.8, zorder=1)
    ax.set_xlim(*LIMITES)
    ax.set_ylim(*LIMITES)


fig, ejes = plt.subplots(1, 2, figsize=(9.8, 4.4), sharex=True, sharey=True)

nube(ejes[0], x, y, AZUL)
ejes[0].text(0.05, 0.96, ("correlación = %+.2f" % bruta).replace(".", ","),
             transform=ejes[0].transAxes, va="top", color=ROJO, fontsize=10.5)
ejes[0].text(0.97, 0.05, "ninguna causa a la otra:\nlas mueve una tercera variable que no ves",
             transform=ejes[0].transAxes, va="bottom", ha="right", color=TEXTO, fontsize=9)
titulo(ejes[0], "Dos variables que suben y bajan juntas",
       "la nube se aprieta en una recta aunque ninguna cause a la otra")
ejes[0].set_xlabel("x: una variable cualquiera")
ejes[0].set_ylabel("y: otra variable cualquiera")
numeros(ejes[0])
rejilla(ejes[0])

nube(ejes[1], sobra_x, sobra_y, MORADO)
ejes[1].text(0.05, 0.96, ("correlación = %+.2f" % limpia).replace(".", ","),
             transform=ejes[1].transAxes, va="top", color=ROJO, fontsize=10.5)
ejes[1].text(0.97, 0.05, "la recta ya es casi plana: lo que\nquedaba era la sombra de la que no mediste",
             transform=ejes[1].transAxes, va="bottom", ha="right", color=TEXTO, fontsize=9)
titulo(ejes[1], "Al descontar la causa común no queda nada",
       "quitando de cada variable lo que explicaba la tercera, la relación se va")
ejes[1].set_xlabel("x sin la parte que explicaba la causa común")
ejes[1].set_ylabel("y sin la parte que explicaba la causa común")
numeros(ejes[1])
rejilla(ejes[1])

guardar(fig, "confusor-correlacion-que-desaparece")
