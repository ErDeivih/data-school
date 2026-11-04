"""confusores-y-dag-1.py — el mismo tercer nodo Z, tres papeles distintos.

Confusor (causa T y causa Y): hay que ajustar. Mediador (esta en medio del mecanismo): no hay
que ajustar si quieres el efecto total. Colisionador (consecuencia de T y de Y): no hay que
ajustar nunca, porque condicionar en el inventa una asociación.

Los tres paneles van en DOS FILAS (dos arriba y el colisionador ocupando el ancho de abajo):
en una sola fila los titulos y las anotaciones se pisan, y el comprobador de figuras lo avisa.
La figura de la pagina de confusores, mediadores y DAG (fase 2)."""

import numpy as np

from comun import *

estilo()


def nodo(ax, sitio, etiqueta, color):
    """Circulo HUECO con la letra dentro: el relleno blanco se veria mal en tema oscuro."""
    x, y = sitio
    ax.scatter([x], [y], s=1500, facecolors="none", edgecolors=color, linewidths=1.8, zorder=3)
    ax.text(x, y, etiqueta, ha="center", va="center", fontsize=13, color=color, zorder=4)


def flecha(ax, desde, hasta, color=TEXTO):
    ax.annotate("", xy=hasta, xytext=desde,
                arrowprops=dict(arrowstyle="-|>", color=color, linewidth=1.5,
                                shrinkA=24, shrinkB=24, mutation_scale=15))


def lienzo(ax):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_axis_off()


def veredicto(ax, frase, color, explicacion):
    ax.text(0.5, 0.15, frase, transform=ax.transAxes, ha="center", va="bottom",
            fontsize=10, color=color)
    ax.text(0.5, 0.02, explicacion, transform=ax.transAxes, ha="center", va="bottom",
            fontsize=8.2, color=TEXTO)


fig = plt.figure(figsize=(9.8, 7.4))
rejilla_paneles = fig.add_gridspec(2, 2)
ejes = [fig.add_subplot(rejilla_paneles[0, 0]),
        fig.add_subplot(rejilla_paneles[0, 1]),
        fig.add_subplot(rejilla_paneles[1, :])]
for ax in ejes:
    lienzo(ax)

# --- 1. Confusor: Z causa el tratamiento y tambien el resultado ---------------------
Z, T, Y = (0.50, 0.88), (0.15, 0.36), (0.85, 0.36)
flecha(ejes[0], Z, T)
flecha(ejes[0], Z, Y)
flecha(ejes[0], T, Y)
nodo(ejes[0], T, "T", AZUL)
nodo(ejes[0], Y, "Y", VERDE)
nodo(ejes[0], Z, "Z", NARANJA)
titulo(ejes[0], "Confusor: causa común de los dos",
       "Z empuja el tratamiento y también el resultado")
veredicto(ejes[0], "SÍ hay que ajustar",
          VERDE, "sin separarlo, su efecto\nse mezcla con el del tratamiento")

# --- 2. Mediador: el efecto del tratamiento pasa por Z ------------------------------
T, Z, Y = (0.13, 0.62), (0.50, 0.62), (0.87, 0.62)
flecha(ejes[1], T, Z)
flecha(ejes[1], Z, Y)
nodo(ejes[1], T, "T", AZUL)
nodo(ejes[1], Y, "Y", VERDE)
nodo(ejes[1], Z, "Z", CIAN)
titulo(ejes[1], "Mediador: está en medio del mecanismo",
       "el tratamiento actúa sobre el resultado a través de Z")
veredicto(ejes[1], "NO hay que ajustar",
          ROJO, "ajustar por el mediador\nbloquea parte del efecto que buscas")

# --- 3. Colisionador: Z es consecuencia de T y de Y ---------------------------------
T, Y, Z = (0.17, 0.78), (0.83, 0.78), (0.50, 0.32)
flecha(ejes[2], T, Y)
flecha(ejes[2], T, Z)
flecha(ejes[2], Y, Z)
nodo(ejes[2], T, "T", AZUL)
nodo(ejes[2], Y, "Y", VERDE)
nodo(ejes[2], Z, "Z", ROSA)
titulo(ejes[2], "Colisionador: consecuencia de los dos",
       "Z no causa nada: lo provocan T y Y a la vez")
veredicto(ejes[2], "NO ajustar NUNCA",
          ROJO, "mirar solo los que pasan por Z\ncrea una relación que no existe")

guardar(fig, "dag-tres-papeles-de-z")
