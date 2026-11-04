"""order-book-y-spread-1.py — leer el libro: el spread como coste inmediato, el desequilibrio
según la profundidad que mires y el precio medio que se paga de verdad. Página «Libro de
órdenes y diferencial» (fase 9)."""

import numpy as np

from comun import *

estilo()

bids = [(50.00, 1200), (49.99, 3000), (49.98, 6000), (49.97, 9000)]
asks = [(50.01, 900), (50.02, 2500), (50.03, 4000), (50.04, 8000)]

bid, ask = bids[0][0], asks[0][0]
mid = (bid + ask) / 2
niveles = [1, 2, 3, 4]
desequilibrio = []
for k in niveles:
    q_b = sum(q for _, q in bids[:k])
    q_a = sum(q for _, q in asks[:k])
    desequilibrio.append((q_b - q_a) / (q_b + q_a))

q_bid = np.array([q for _, q in bids])
q_ask = np.array([q for _, q in asks])
profundidad = np.cumsum(q_ask)


def ejecutar(Q, niveles_libro):
    """Recorre los niveles de arriba abajo: precio medio y cantidad sin ejecutar."""
    resta, gastado = float(Q), 0.0
    for precio, cantidad in niveles_libro:
        usa = min(resta, cantidad)
        gastado += usa * precio
        resta -= usa
        if resta == 0:
            break
    return gastado / (Q - resta), resta


medio, _ = ejecutar(10000, asks)
impacto_pb = (medio - ask) / mid * 10000

fig, (izq, der) = plt.subplots(1, 2, figsize=(7.0, 4.4))

# --- Izquierda: el libro como escalera, con los dos lados frente a frente -----
alto = 0.0028
izq.barh([p for p, _ in bids], -q_bid, alto, color=AZUL)
izq.barh([p for p, _ in asks], q_ask, alto, color=NARANJA)
izq.axvline(0, color=TEXTO, linewidth=0.9, zorder=3)
izq.annotate("el spread (2 pb) separa los dos lados", xy=(mid, 100.0065),
             xytext=(0.30, 0.90), textcoords="axes fraction", fontsize=8.5, color=TEXTO,
             arrowprops=dict(arrowstyle="->", color=TEXTO, linewidth=0.9, shrinkA=2, shrinkB=3))
izq.annotate("mirar más niveles suaviza el desequilibrio:\n+0,143 con uno, +0,159 con tres",
             xy=(4000, 50.03), xytext=(0.03, 0.72), textcoords="axes fraction",
             fontsize=8.5, color=MORADO,
             arrowprops=dict(arrowstyle="->", color=MORADO, linewidth=0.9, shrinkA=2, shrinkB=3))
izq.text(0.03, 0.05, "desequilibrio %+.3f  ·  la barra mide el tamaño del nivel"
         % desequilibrio[-1], transform=izq.transAxes, fontsize=8.5, color=TEXTO)
izq.set_yticks([99.97, 99.98, 99.99, 100.00, 100.01, 100.02, 100.03, 100.04])
izq.set_ylim(99.958, 100.055)
izq.set_xlabel("títulos visibles (a la izquierda, compra; a la derecha, venta)")
izq.set_ylabel("precio (EUR)")
izq.set_title("Diferencial estrecho no es libro profundo")
rejilla(izq, eje="x")
numeros(izq, ejes="y")

# --- Derecha: el coste de cruzar, nivel a nivel ------------------------------
der.step(np.concatenate([[0], profundidad]), [ask] + [p for p, _ in asks], where="post",
         color=NARANJA, linewidth=1.8)
der.axhline(mid, color=TEXTO, linewidth=1.0, linestyle="--")
der.vlines(10000, mid, medio, color=MORADO, linewidth=1.6)
der.scatter([10000], [medio], s=30, color=MORADO, zorder=4)
der.text(0.03, 0.97, "mid 50,005: no es un precio operable", transform=der.transAxes,
         fontsize=8.5, color=TEXTO, va="top")
der.annotate("900 títulos: solo el primer nivel",
             xy=(1400, 50.015), xytext=(0.30, 0.66), textcoords="axes fraction",
             fontsize=8.5, color=NARANJA,
             arrowprops=dict(arrowstyle="->", color=NARANJA, linewidth=0.9, shrinkA=2, shrinkB=3))
der.text(0.42, 0.06, "10.000 títulos: medio 50,0283\n%.2f pb sobre el mejor ask" % impacto_pb,
         transform=der.transAxes, fontsize=8.5, color=MORADO)
der.set_xlabel("títulos acumulados en el lado de venta")
der.set_ylabel("precio (EUR)")
der.set_xlim(-200, 17000)
der.set_title("Cruzar cuesta más cuanto más grande")
rejilla(der)
numeros(der)

guardar(fig, "order-book-spread-y-profundidad")
