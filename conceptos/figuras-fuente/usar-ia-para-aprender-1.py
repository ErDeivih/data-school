"""usar-ia-para-aprender-1.py — las cuatro casillas de una respuesta de un modelo.

Cruza dos preguntas que se confunden todo el rato: ¿lo entiendes? y ¿lo has comprobado?
Solo la casilla de arriba a la derecha es codigo tuyo. Las otras tres son deuda con
distinto plazo: la hipotesis sin comprobar, el codigo que funciona y no sabes tocar y
el atajo que se paga en el primer cambio.
"""

from comun import *

estilo()

fig, ax = plt.subplots(figsize=(8.2, 5.4))

ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_xticks([])
ax.set_yticks([])

# Las dos lineas que parten el plano en cuatro casillas.
ax.axvline(0.5, color=REJILLA, linewidth=1.2)
ax.axhline(0.5, color=REJILLA, linewidth=1.2)

# Cada casilla lleva su titulo (el veredicto) y una linea de que hacer con ella.
# La x es «¿lo has comprobado?»: a la izquierda no, a la derecha si.
casillas = [
    (0.75, 0.75, "Lo entiendes y lo has comprobado", "Tuyo: puedes cambiarlo y defenderlo", VERDE),
    (0.75, 0.25, "Lo has comprobado y no lo entiendes", "Funciona hoy; pide la explicación antes de tocarlo", NARANJA),
    (0.25, 0.75, "Lo entiendes y no lo has comprobado", "Es una hipotesis: compruebala en tres lineas", AZUL),
    (0.25, 0.25, "No lo entiendes ni lo has comprobado", "El atajo que se paga en el primer cambio", ROJO),
]
for x, y, veredicto, que_hacer, color in casillas:
    ax.text(x, y + 0.055, veredicto, ha="center", va="center", fontsize=9.5, color=color,
            fontweight="bold", wrap=True)
    ax.text(x, y - 0.045, que_hacer, ha="center", va="center", fontsize=8.5, color=TEXTO)

ax.set_xlabel("¿lo has comprobado tú?   (izquierda: no   ·   derecha: sí)")
ax.set_ylabel("¿lo entiendes?\n(abajo: no   ·   arriba: sí)")
numeros(ax)

titulo(ax, "Una respuesta es tuya en una sola casilla",
       "entender y comprobar son dos preguntas distintas: contestar solo una deja deuda")

guardar(fig, "usar-ia-entender-frente-a-comprobar")
