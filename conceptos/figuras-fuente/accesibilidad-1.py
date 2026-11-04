"""accesibilidad-1.py — el contraste de tres colores del ejemplo y la curva del contraste de un
gris sobre blanco, con el corte exacto que separa lo que cumple el nivel AA. La figura de la
pagina de accesibilidad (fase 11)."""

import numpy as np

from comun import *

estilo()


def lineal(v):
    """Canal 0-255 linealizado con la gamma de la especificación WCAG."""
    v = v / 255
    return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4


def luminancia(c):
    """Luminancia relativa de un color RGB: el verde pesa mucho más que el azul."""
    return 0.2126 * lineal(c[0]) + 0.7152 * lineal(c[1]) + 0.0722 * lineal(c[2])


def contraste(c1, c2):
    """Cociente entre el color más claro y el más oscuro; siempre sale >= 1."""
    claro, oscuro = sorted([luminancia(c1), luminancia(c2)], reverse=True)
    return (claro + 0.05) / (oscuro + 0.05)


BLANCO = (255, 255, 255)
# Los tres casos que se comprueban en la pagina, con su contraste ya calculado.
nombres = ["#767676", "#999999", "#0057b8"]
valores = np.array([contraste((118, 118, 118), BLANCO),
                    contraste((153, 153, 153), BLANCO),
                    contraste((0, 87, 184), BLANCO)])
colores = [AZUL, ROJO, VERDE]

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 4.2))

# --- Izquierda: los tres colores frente a los umbrales de AA ------------------------------
barras = izq.barh(nombres, valores, color=colores, height=0.5)
izq.bar_label(barras, labels=[f"{coma(round(v, 2))}:1" for v in valores], padding=4, fontsize=9)
izq.axvline(4.5, color=ROJO, linewidth=1.5, linestyle="--")
izq.axvline(3.0, color=NARANJA, linewidth=1.4, linestyle=":")
anotar(izq, "texto normal: 4,5:1", xy=(4.5, 0.5), xytext=(0.52, 0.42), color=ROJO)
anotar(izq, "texto grande: 3:1", xy=(3.0, 1.72), xytext=(0.34, 0.66), color=NARANJA)
izq.set_xlim(0, 9)
izq.set_xlabel("cociente de contraste sobre blanco")
titulo(izq, "El gris que casi todo el mundo usa pasa por poco",
       "4,54 cumple; un punto más claro, 2,85, ya no")
rejilla(izq, eje="x")
numeros(izq, ejes="x")

# --- Derecha: la curva completa, para ver donde esta exactamente el corte ------------------
grises = np.arange(40, 211)
curva = np.array([contraste((int(g),) * 3, BLANCO) for g in grises])
der.plot(grises, curva, color=AZUL, linewidth=1.8)
der.plot([118, 153], [contraste((118,) * 3, BLANCO), contraste((153,) * 3, BLANCO)],
         "o", color=MORADO, markersize=5)
der.axhline(4.5, color=ROJO, linewidth=1.4, linestyle="--")
der.axhline(3.0, color=NARANJA, linewidth=1.3, linestyle=":")
der.axvline(119, color=TEXTO, linewidth=1.1, linestyle="--")
anotar(der, "a partir de #777777 el texto\nnormal ya no llega a 4,5:1",
       xy=(119, 4.5), xytext=(0.34, 0.86), color=TEXTO)
anotar(der, "#767676 (118)", xy=(118, 4.54), xytext=(0.03, 0.30), color=MORADO)
anotar(der, "#999999 (153)", xy=(153, 2.85), xytext=(0.58, 0.05), color=MORADO, flecha=False)
der.set_ylim(0, 12)
der.set_xlabel("nivel de gris (0 = negro, 255 = blanco)")
der.set_ylabel("contraste sobre blanco")
titulo(der, "El contraste no se estima a ojo: se calcula",
       "la frontera del nivel AA cae entre el gris 118 y el 119")
rejilla(der)
numeros(der)

guardar(fig, "accesibilidad-contraste")
