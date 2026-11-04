"""integrales-1.py — la integral es un limite de sumas: los rectangulos se afinan hasta que
el error desaparece. La figura de la pagina de integrales."""

import numpy as np

from comun import *

estilo()
p = lambda t: 2 * np.exp(-2 * t)      # densidad exponencial de tasa 2 (solo tiene sentido en t >= 0)
exacta = 1 - np.exp(-10)              # area exacta entre 0 y 5

fig, ejes = plt.subplots(2, 1, figsize=(7.6, 6.2), sharex=True)
tt = np.linspace(0, 5, 400)

for ax, n in ((ejes[0], 8), (ejes[1], 40)):
    bordes = np.linspace(0, 5, n + 1)
    ancho = 5.0 / n
    izquierda = bordes[:-1]
    ax.plot(tt, p(tt), color=AZUL, linewidth=1.8)
    ax.bar(izquierda, p(izquierda), width=ancho, align="edge",
           color=NARANJA, alpha=0.25, edgecolor=NARANJA, linewidth=0.6)
    suma = float(p(izquierda).sum() * ancho)
    ax.axhline(0, color=TEXTO, linewidth=0.7, alpha=0.4)
    # El recuento va en la esquina de arriba a la derecha: la curva y las barras se quedan
    # a la izquierda y ahi no hay nada que tapar.
    anotar(ax, f"{n} rectángulos suman {coma(round(suma, 5))}\n"
               f"el área exacta es {coma(round(exacta, 5))}: faltan {coma(round(exacta - suma, 5))}",
           xy=(2.6, 0.55), xytext=(0.42, 0.80), flecha=False)
    rejilla(ax)
    numeros(ax)

titulo(ejes[0], "Pocos rectángulos: la suma se queda corta",
       "el escalón de cada rectángulo se ve a simple vista")
titulo(ejes[1], "Muchos rectángulos: la suma ya es el área",
       "la diferencia entre las dos es de 0,13 y no se aprecia")
ejes[1].set_xlabel("x")
ejes[1].set_ylabel("densidad p(x)")

guardar(fig, "integrales-suma-de-riemann")
