"""backtesting-por-eventos-1.py — la cola: 400 acciones en venta no llenan una orden de 500
detras de 300. La figura de la pagina de backtesting por eventos (fase 9)."""

import numpy as np

from comun import *

estilo()
cola_inicial = 300
orden = 500
# Las dos ventas que llegan contra nuestro nivel antes de que el precio se aleje y cancelemos lo
# que queda: son las del ejemplo de la pagina (con una tercera venta la orden acabaria llena).
ventas = np.array([400.0, 250.0])

# Cada venta que llega contra nuestro nivel consume primero lo que hay por delante.
cola, ejecutado = float(cola_inicial), 0.0
ejecutado_traza = [0.0]
cola_traza = [cola]
for venta in ventas:
    consume_cola = min(cola, venta)
    cola -= consume_cola
    disponible = venta - consume_cola
    ejecutado += min(orden - ejecutado, disponible)
    ejecutado_traza.append(ejecutado)
    cola_traza.append(cola)
eje_x = np.arange(ventas.size + 1)

fig, ejes = plt.subplots(2, 1, figsize=(7.0, 5.2), sharex=True)

# --- Arriba: lo que hay delante de tu orden, barrido venta a venta ---
ejes[0].step(eje_x, cola_traza, where="post", color=ROJO, linewidth=1.7)
ejes[0].axhline(0, color=TEXTO, linewidth=0.8, alpha=0.4)
titulo(ejes[0], "La cola de delante solo se llena al llegar a cero",
       "mientras quede cola, las ventas se la comen antes de tocarte")
ejes[0].set_ylabel("acciones por delante")
# Una sola linea: dos renglones no caben entre dos rayas de la rejilla (cada 50) sin rozarlas.
anotar(ejes[0], "la venta de 400 vacía los 300 de delante",
       xy=(1.0, 290), xytext=(0.60, 0.879), color=ROJO)
rejilla(ejes[0])
numeros(ejes[0], "y")

# --- Abajo: cuantas de tus 500 existen de verdad ---
ejes[1].plot(eje_x, ejecutado_traza, "o-", color=VERDE, markersize=4, linewidth=1.4)
ejes[1].axhline(orden, color=REJILLA, linewidth=1.2, linestyle="--")
ejes[1].axhline(ejecutado, color=AZUL, linewidth=1.2, linestyle=":")
ejes[1].set_ylim(0, 660)
ejes[1].set_xlim(-0.05, ventas.size + 0.4)
titulo(ejes[1], "Tu posición real: 350 de las 500 que pediste",
       "el backtest vectorizado da por hechas las 500 en cuanto el precio toca")
ejes[1].set_ylabel("acciones ejecutadas")
ejes[1].set_xlabel("ventas que llegan contra tu precio")
# Las tres notas se centran entre dos renglones de la rejilla (cada 100): a la altura natural de
# cada linea, la raya de 600, 300 y 100 les pasaba por encima del texto.
anotar(ejes[1], "el backtest vectorizado da por hecho: 500", xy=(1.75, orden),
       xytext=(0.03, 0.833), color=REJILLA)
anotar(ejes[1], "lo que de verdad se ejecuta: 350", xy=(1.75, ejecutado),
       xytext=(0.03, 0.682), color=AZUL)
anotar(ejes[1], "las 150 que faltan son beneficio imaginario si el precio sube",
       xy=(1.75, (orden + ejecutado) / 2), xytext=(0.98, 0.076), color=NARANJA, flecha=False,
       align="right")
rejilla(ejes[1])
numeros(ejes[1], "y")
ejes[1].set_xticks(np.arange(ventas.size + 1))
ejes[1].set_xticklabels(["inicio", "venta 1", "venta 2"])

guardar(fig, "backtesting-por-eventos-la-cola")
