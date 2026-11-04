"""microestructura-de-mercado-1.py — por qué una orden a mercado no se ejecuta a un precio
sino a un precio medio, y qué pasa cuando el libro no tiene bastante. Página de
microestructura (fase 9)."""

import numpy as np

from comun import *

estilo()

# El libro del ejemplo, agrandado a escala natural (precios a la derecha del spread)
bids = [(100.00, 400), (99.99, 700), (99.98, 900), (99.97, 1500)]
asks = [(100.01, 300), (100.02, 600), (100.03, 1200), (100.04, 2000)]

bid, ask = bids[0][0], asks[0][0]
mid = (bid + ask) / 2
q_bid, q_ask = bids[0][1], asks[0][1]
imbalance = (q_bid - q_ask) / (q_bid + q_ask)


def ejecutar(Q, niveles):
    """Recorre los niveles de arriba abajo: precio medio y cantidad que queda sin ejecutar."""
    resta, gastado = float(Q), 0.0
    for precio, cantidad in niveles:
        usa = min(resta, cantidad)
        gastado += usa * precio
        resta -= usa
        if resta == 0:
            break
    return gastado / (Q - resta), resta


medio800, resto800 = ejecutar(800, asks)
medio5000, resto5000 = ejecutar(5000, asks)

fig, (izq, der) = plt.subplots(1, 2, figsize=(7.0, 4.4))

# --- Izquierda: el libro y los niveles que se come una orden -----------------
ancho = 0.0028
for precio, cantidad in bids:
    izq.barh(precio, cantidad, height=ancho, color=AZUL)
for precio, cantidad in asks:
    izq.barh(precio, cantidad, height=ancho, color=NARANJA)

izq.barh(asks[0][0], 300, height=ancho, color=ROJO)
izq.barh(asks[1][0], 500, height=ancho, color=ROJO)

izq.annotate("el mid no es operable: nadie te vende a 100,005",
             xy=(mid, 100.062), xytext=(0.04, 0.93), textcoords="axes fraction",
             fontsize=8.5, color=TEXTO)
izq.annotate("comprar 800 a mercado:\n300 a 100,01 y 500 a 100,02\nprecio medio 100,01625",
             xy=(900, 100.016), xytext=(0.42, 0.28), textcoords="axes fraction",
             fontsize=8.5, color=ROJO,
             arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9, shrinkA=2, shrinkB=3))
izq.text(0.55, 0.66, "azul: compra\nnaranja: venta\nrojo: lo que consume tu orden",
         transform=izq.transAxes, fontsize=8.5, color=TEXTO)
izq.set_xlabel("títulos en el nivel")
izq.set_ylabel("precio (EUR)")
izq.set_xlim(0, 2600)
izq.set_ylim(99.955, 100.075)
izq.set_title("El libro, nivel a nivel")
rejilla(izq, eje="x")
numeros(izq)

# --- Derecha: el precio medio sube con el tamaño de la orden -----------------
tamanos = np.arange(100, 5200, 50)
medios = np.array([ejecutar(Q, asks)[0] for Q in tamanos])
restos = np.array([ejecutar(Q, asks)[1] for Q in tamanos])
impacto_pb = (medios - ask) / mid * 10000

der.plot(tamanos, impacto_pb, color=AZUL, linewidth=1.8)
der.axvline(q_ask, color=ROJO, linewidth=1.3, linestyle="--")
der.scatter([800], [(medio800 - ask) / mid * 10000], s=28, color=MORADO, zorder=4)
der.scatter([5000], [(medio5000 - ask) / mid * 10000], s=28, color=ROJO, zorder=4)
der.annotate("800 títulos: 0,63 pb",
             xy=(800, (medio800 - ask) / mid * 10000), xytext=(0.30, 0.42),
             textcoords="axes fraction", fontsize=8.5, color=MORADO,
             arrowprops=dict(arrowstyle="->", color=MORADO, linewidth=0.9, shrinkA=2, shrinkB=3))
der.annotate("5.000: el libro solo tiene 4.100,\nquedan 900 sin ejecutar",
             xy=(q_ask, impacto_pb[-1]), xytext=(0.42, 0.80), textcoords="axes fraction",
             fontsize=8.5, color=ROJO,
             arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9, shrinkA=2, shrinkB=3))
der.text(0.06, 0.06, "desequilibrio del libro: %+.3f  ·  spread %.2f pb"
         % (imbalance, (ask - bid) / mid * 10000), transform=der.transAxes, fontsize=8.5,
         color=TEXTO)
der.set_xlabel("tamaño de tu orden (títulos)")
der.set_ylabel("impacto sobre el mejor ask (puntos básicos)")
der.set_title("Cuanto más grande la orden, peor el precio medio")
rejilla(der)
numeros(der)

guardar(fig, "microestructura-libro-e-impacto")
