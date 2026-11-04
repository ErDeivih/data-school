"""que-es-un-mercado-1.py — el precio del gráfico no es tu precio: comisión, diferencial e
impacto se comen el beneficio, y el tamaño de la posición decide cuánto. Página «Qué es un
mercado» (fase 9)."""

import numpy as np

from comun import *

estilo()

# Los dos recorridos del ejemplo: mismo movimiento por acción, posición diez veces mayor.
escenarios = ["200 acciones\norden límite", "2.000 acciones\na mercado"]
nominal = np.array([200 * 24.50, 2000 * 24.50])
bruto = np.array([200 * (25.10 - 24.50), 2000 * (25.10 - 24.50)])

f = 0.001                                            # 0,10 % con mínimo de 3 EUR por punta
comision = np.maximum(nominal * f, 3.0) * 2          # se paga al entrar y al salir
implicito = np.array([0.0, 2000 * 0.02 * 2])         # diferencial de 2 céntimos por punta
coste = comision + implicito
neto = bruto - coste

fig, (izq, der) = plt.subplots(1, 2, figsize=(7.0, 4.4))

pos = np.arange(2)
ancho = 0.34

# --- Izquierda: lo que gana el precio frente a lo que se llevan los demás -----
izq.bar(pos - ancho / 2, bruto, ancho, color=VERDE, label="lo que gana el precio")
izq.bar(pos + ancho / 2, coste, ancho, color=ROJO, label="bróker y diferencial")
for i in range(2):
    izq.text(pos[i] - ancho / 2, bruto[i] + 45, "%.0f €" % bruto[i], ha="center",
             fontsize=8.5, color=TEXTO)
    izq.text(pos[i] + ancho / 2, coste[i] + 45, "%.0f € = %.1f %%"
             % (coste[i], 100 * coste[i] / bruto[i]), ha="center", fontsize=8.5, color=ROJO)
izq.set_xticks(pos)
izq.set_xticklabels(escenarios, fontsize=8.5)
izq.set_ylabel("euros")
izq.set_ylim(0, 1620)
izq.set_title("Ganancia bruta frente a lo que se llevan")
izq.legend(loc="upper left")
rejilla(izq)
numeros(izq)

# --- Derecha: el porcentaje que sobrevive a los costes -----------------------
der.bar(pos, 100 * neto / bruto, 0.45, color=AZUL)
der.axhline(100, color=TEXTO, linewidth=1.0, linestyle="--")
for i in range(2):
    der.text(pos[i], 100 * neto[i] / bruto[i] + 3, "neto %.2f €" % neto[i], ha="center",
             fontsize=8.5, color=TEXTO)
der.set_xticks(pos)
der.set_xticklabels(escenarios, fontsize=8.5)
der.set_ylabel("% del beneficio bruto que sobrevive")
der.set_ylim(0, 122)
der.annotate("el mismo movimiento por acción:\ncon 2.000 títulos el coste pasa\ndel 8,3 % al 14,8 % del bruto",
             xy=(1, 85), xytext=(0.22, 0.40), textcoords="axes fraction",
             fontsize=8.5, color=ROJO,
             arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9, shrinkA=2, shrinkB=3))
der.set_title("El tamaño de la posición decide cuánto queda")
rejilla(der)
numeros(der)

guardar(fig, "mercado-notional-coste-y-tamano")
