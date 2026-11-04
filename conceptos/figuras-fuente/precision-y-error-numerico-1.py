"""precision-y-error-numerico-1.py — de dónde salen los errores de redondeo.

Izquierda: sumar 0,1 muchas veces. El error relativo no se queda quieto: crece con el
número de sumandos, porque cada suma vuelve a redondear al flotante más cercano.

Derecha: el hueco que hay entre dos números representables. No es constante: se duplica
cada vez que el número duplica su exponente. Por eso, pasado 2^53, sumar 1 a un número
grande no cambia nada.
"""

import numpy as np

from comun import *

estilo()

fig = plt.figure(figsize=(9.6, 4.2))
rejilla_paneles = fig.add_gridspec(1, 2)
izq = fig.add_subplot(rejilla_paneles[0, 0])
der = fig.add_subplot(rejilla_paneles[0, 1])

# --- Izquierda: error absoluto de acumular 0,1 ------------------------------------------------
tope = 100_000
acumulado = np.cumsum(np.full(tope, 0.1))
ns = np.unique(np.round(np.logspace(np.log10(8), np.log10(tope), 160)).astype(int))
ns = ns[(ns >= 8) & (ns <= tope)]

error = np.abs(acumulado[ns - 1] - ns / 10.0)
visibles = error > 0                  # en los primeros sumandos el resultado es exacto

izq.loglog(ns[visibles], error[visibles], color=AZUL, linewidth=1.5)
izq.axhline(2.0 ** -52, color=ROJO, linewidth=1.2, linestyle="--")
izq.set_ylim(1e-17, 1e-6)

anotar(izq, "cada suma vuelve a redondear\nsobre un total mayor",
       xy=(30_000, error[visibles][-1]), xytext=(0.30, 0.74), color=AZUL)
# La nota de la linea roja va al final de la propia linea, sin flecha: es su etiqueta.
anotar(izq, "2⁻⁵²: el hueco entre 1\ny el número siguiente",
       xy=(30_000, 2.0 ** -52), xytext=(0.66, 0.17), color=ROJO, flecha=False)

titulo(izq, "Sumar 0,1 no sale exacto y empeora",
       "mil sumandos: 1,4 · 10⁻¹² de error; cien mil: 1,9 · 10⁻⁸")
izq.set_xlabel("sumandos acumulados (escala logarítmica)")
izq.set_ylabel("error absoluto de la suma")
numeros(izq)
rejilla(izq)

# --- Derecha: distancia entre dos flotantes consecutivos --------------------------------------
exponentes = np.arange(30, 62)
huecos = np.array([np.log2(np.spacing(2.0 ** k)) for k in exponentes])

der.plot(exponentes, huecos, color=MORADO, linewidth=1.6)
der.axvline(53, color=VERDE, linewidth=1.2, linestyle="--")
der.set_xlim(29, 61.5)
der.set_ylim(-23, 10)
der.set_xticks([30, 40, 50, 53, 60])

anotar(der, "2⁵³: el hueco ya vale 2,\nsumar 1 no cambia el número",
       xy=(53, -12), xytext=(0.16, 0.34), color=VERDE)
anotar(der, "cada exponente de más\nduplica el hueco",
       xy=(58, 6), xytext=(0.36, 0.80), color=MORADO)

titulo(der, "El hueco entre números crece con el número",
       "el hueco se duplica con cada exponente: por eso 10¹⁶ + 1 sigue siendo 10¹⁶")
der.set_xlabel("exponente k, para el número 2ᵏ")
der.set_ylabel("hueco entre números consecutivos, como 2ˣ")
numeros(der)
rejilla(der)

guardar(fig, "precision-error-al-sumar")
