"""protocolo-fix-1.py — una sesión FIX es un ida y vuelta de mensajes, y lo que la tumba no
es el mensaje raro: es un número de secuencia que no cuadra. El diagrama sigue una sesión
normal en la que el broker detecta un hueco en su contador de entrada, pide el reenvío con
35=2 y recibe la orden repetida con la marca 43=Y.

Página del protocolo FIX (fase 9)."""

import numpy as np

from comun import *
from matplotlib.patches import Rectangle

estilo()

fig, eje = plt.subplots(figsize=(9.6, 5.2))

# Dos participantes y sus contadores. El tag 34 es POR DIRECCIÓN: el 7 de la izquierda y
# el 12 de la derecha conviven sin ningún problema.
izq, der = 0.06, 0.94
eje.add_patch(Rectangle((izq - 0.05, -0.25), 0.10, 8.1, color=REJILLA, alpha=0.25, zorder=0))
eje.add_patch(Rectangle((der - 0.05, -0.25), 0.10, 8.1, color=REJILLA, alpha=0.25, zorder=0))
eje.plot([izq, izq], [-0.25, 7.85], color=REJILLA, linewidth=1.2, zorder=1)
eje.plot([der, der], [-0.25, 7.85], color=REJILLA, linewidth=1.2, zorder=1)
eje.text(izq, 8.05, "Sistema cliente", ha="center", va="bottom", fontsize=9.5, color=TEXTO)
eje.text(der, 8.05, "Bróker o mercado", ha="center", va="bottom", fontsize=9.5, color=TEXTO)

# (y, llega_a_la_derecha, etiqueta del mensaje). Las secuencias son las del ejemplo: la
# izquierda envía 6 y 7, la derecha responde 12 (Logon) y 13 (ejecución).
mensajes = [
    (7.20, True, "35=A  Logon  · 34=6"),
    (6.10, False, "35=A  Logon  · 34=12"),
    (5.00, True, "35=D  orden nueva  · 34=7"),
    (3.50, False, "35=2  ResendRequest  · 34=12"),
    (2.00, True, "35=D  reenvío  · 34=7  · 43=Y"),
    (0.50, False, "35=8  ejecución  · 34=13"),
]
for y, hacia_la_derecha, etiqueta in mensajes:
    color = AZUL if hacia_la_derecha else MORADO
    eje.annotate("", xy=(der if hacia_la_derecha else izq, y),
                 xytext=(izq if hacia_la_derecha else der, y),
                 arrowprops=dict(arrowstyle="->", color=color, linewidth=1.5,
                                 shrinkA=2, shrinkB=2))
    eje.text((izq + der) / 2, y + 0.14, etiqueta, ha="center", va="bottom",
             fontsize=9, color=color)

# La banda marca lo que el broker esperaba y no llegó: si su contador va por el 11 y le
# entra un 13, sabe que se ha perdido un mensaje y lo pide.
eje.add_patch(Rectangle((izq, 2.65), der - izq, 1.55, color=ROJO, alpha=0.08, zorder=0))
eje.plot([(izq + der) / 2, (izq + der) / 2], [2.65, 4.20], color=ROJO, linewidth=1.1,
         linestyle="--")
eje.text((izq + der) / 2 - 0.015, 4.02, "el 13 llegó cuando esperaba el 12", fontsize=8.5,
         color=ROJO, ha="right", va="center")

eje.text(0.01, -0.62, "El tag 34 es un contador por dirección: el 7 de la izquierda y el 12 "
                      "de la derecha\nconviven en la misma sesión sin chocar",
         fontsize=8.5, color=TEXTO, va="top")
eje.text(0.99, -0.62, "Un hueco no se arregla ignorándolo: si el mensaje perdido era\nuna "
                      "ejecución, tu posición ya no cuadra", fontsize=8.5, color=ROJO,
         va="top", ha="right")

eje.set_xlim(-0.02, 1.02)
eje.set_ylim(-1.70, 8.45)
eje.set_xticks([])
eje.set_yticks([])
for lado in ("top", "right", "left", "bottom"):
    eje.spines[lado].set_visible(False)
titulo(eje, "La sesión FIX no se rompe por un mensaje raro",
       "Se rompe cuando el contador de secuencia no cuadra: una orden pérdida y su reenvío")
eje.text(0.5, -1.28, "tiempo (cada flecha es un mensaje de la sesión)", ha="center",
         va="top", fontsize=9, color=TEXTO)

guardar(fig, "protocolo-fix-sesion-y-hueco-de-secuencia")
