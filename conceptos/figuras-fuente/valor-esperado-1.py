"""valor-esperado-1.py — donde esta la media y 43por qué multiplicar esperanzas enganna.

Izquierda: la masa de un dado y su centro de gravedad, que cae en 3,5 entre dos barras.
Derecha: la misma variable contra si misma. El rectángulo azul (media por media) es más
pequenio que la media de los productos, y esa diferencia es la covarianza.
"""

import numpy as np

from comun import *

estilo()

# Dos filas: cada panel necesita el ancho entero para que el texto no se cruce con las
# barras ni con las flechas.
fig, (izq, der) = plt.subplots(2, 1, figsize=(9.6, 8.0))
fig.set_constrained_layout_pads(h_pad=0.09)   # aire entre los dos paneles

# --- Panel de arriba: el valor esperado como centro de gravedad -------------------
caras = np.arange(1, 7, dtype=float)
masa = np.full(6, 1 / 6)
esperado = float((caras * masa).sum())
assert abs(esperado - 3.5) < 1e-12

izq.bar(caras, masa, width=0.7, color=AZUL)
izq.vlines(esperado, 0, 0.195, color=ROJO, linewidth=2.0)
izq.set_xticks(caras)
izq.set_xlim(0.4, 7.4)
izq.set_ylim(0, 0.20)
# Las barras llegan todas a 0,167: la franja de arriba está vacía y es donde caben la
# etiqueta y la nota sin pisar ninguna barra (antes el texto caía dentro de una).
izq.text(4.03, 0.187, "E[X] = 3,5", color=ROJO, fontsize=9.5, ha="center")
izq.annotate("cae entre el 3 y el 4:\nun valor que el dado nunca da",
             xy=(3.60, 0.186), xytext=(0.99, 0.88), textcoords="axes fraction",
             color=TEXTO, fontsize=9, ha="right", va="center",
             arrowprops=dict(arrowstyle="->", color=TEXTO, linewidth=0.9, shrinkA=2, shrinkB=2))
izq.set_xlabel("resultado del dado")
izq.set_ylabel("p(x)")
titulo(izq, "La media es un centro de gravedad, no un pronóstico")
numeros(izq, ejes="y")
rejilla(izq)

# --- Panel de abajo: E[X]*E[Y] frente a E[X*Y] con Y = X --------------------------
prod_esperanzas = esperado * esperado
media_productos = float((caras * caras * masa).sum())
covarianza = media_productos - prod_esperanzas
assert abs(media_productos - 91 / 6) < 1e-12 and covarianza > 0

etiquetas = ["E[X] · E[Y]\n(solo vale si son\nindependientes)", "E[X · Y]\n(aqui vale 91/6)"]
valores = [prod_esperanzas, media_productos]
der.bar([0, 1], valores, width=0.5, color=[REJILLA, AZUL])
for i, v in enumerate(valores):
    der.text(i, v + 0.35, f"{v:.4f}".replace(".", ","), ha="center", color=TEXTO, fontsize=10)
der.set_xticks([0, 1]); der.set_xticklabels(etiquetas)
der.set_ylim(0, 19.5)
der.set_ylabel("euros por tirada, en media")
titulo(der, "Multiplicar esperanzas se queda corto con dependencia")
# El texto va centrado en el hueco que queda entre las dos barras: ese hueco es justo la
# diferencia de la que habla, así que no hace falta ninguna flecha.
der.annotate(f"la diferencia, {covarianza:.4f}".replace(".", ",") + ",\nes la covarianza",
             xy=(0.5, 13.8), xytext=(0.5, 13.8), color=VERDE, fontsize=9.5,
             ha="center", va="bottom")
numeros(der, ejes="y")
rejilla(der)

guardar(fig, "esperado-centro-y-producto")
