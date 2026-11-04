"""exactamente-una-vez-1.py — el cobro duplicado y el contador que lo evita. La figura de la
pagina de entrega exactamente una vez (fase 11)."""

import numpy as np

from comun import *

estilo()

# Las cuatro entregas del ejemplo: la tercera es un reintento de la primera.
claves = ["m-77", "m-31", "m-77", "m-40"]
importes = np.array([10.0, 5.0, 10.0, 2.0])

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.6, 4.2))

# --- Izquierda: sin deduplicar se cobra de mas --------------------------------------
etiquetas = ["suma de todas\nlas entregas", "deduplicando\npor clave"]
totales = np.array([importes.sum(), importes[[0, 1, 3]].sum()])
barras = izq.bar(etiquetas, totales, color=[ROJO, VERDE], width=0.45)
izq.bar_label(barras, labels=[f"{t:.2f} EUR".replace(".", ",") for t in totales], padding=3,
              fontsize=9)
# El corchete marca exactamente el cobro de mas: los 10 EUR de la entrega repetida.
izq.annotate("", xy=(0.19, totales[0]), xytext=(0.19, totales[1]),
             arrowprops=dict(arrowstyle="<->", color=TEXTO, linewidth=1.1))
anotar(izq, "10,00 EUR de más:\nla entrega 3 es un reintento", xy=(0.35, 22), xytext=(0.42, 0.70),
       color=ROJO)
izq.set_ylim(0, 33)
izq.set_ylabel("importe cobrado (EUR)")
izq.set_xlabel("dos formas de sumar las cuatro entregas")
titulo(izq, "Sumar entregas cobra el mismo pago dos veces",
       "4 entregas, pero solo 3 mensajes lógicos")
rejilla(izq)
numeros(izq, ejes="y")

# --- Derecha: el contador de claves vistas, entrega a entrega -----------------------
# Se aplica la misma regla que el codigo de la pagina: si la clave ya esta, no se cobra.
vistas = set()
acumulado = []
for clave, importe in zip(claves, importes):
    if clave not in vistas:
        vistas.add(clave)
        acumulado.append(acumulado[-1] + importe if acumulado else importe)
    else:
        acumulado.append(acumulado[-1])
acumulado = np.array(acumulado)

x = np.arange(1, len(claves) + 1)
der.plot(x, acumulado, "o-", color=AZUL, linewidth=1.8, markersize=6)
# Cada entrega lleva su clave y, si es reintento, se marca en rojo.
for i, clave in enumerate(claves):
    repetida = claves.index(clave) < i
    # Las etiquetas van alternando altura (arriba y abajo de la linea) para no pisarse entre
    # ellas ni con la propia curva.
    altura = 0.90 if i % 2 == 0 else 0.24
    der.annotate(f"{clave}\n{importes[i]:.2f} EUR".replace(".", ","),
                 xy=(x[i], acumulado[i]), xycoords="data",
                 xytext=(0.04 + 0.24 * i, altura), textcoords="axes fraction",
                 fontsize=8.5, ha="left", color=ROJO if repetida else TEXTO,
                 arrowprops=dict(arrowstyle="->", color=ROJO if repetida else REJILLA,
                                 linewidth=0.9, shrinkA=2, shrinkB=3))
# El aviso del reintento apunta al tramo plano desde abajo: por arriba chocaria con la
# etiqueta de la propia entrega repetida.
anotar(der, "el reintento no suma nada", xy=(3, 14.4), xytext=(0.44, 0.20), color=ROJO)
der.set_xticks(x)
der.set_xlim(0.7, 4.3)
der.set_ylim(0, 23)
der.set_xlabel("entregas recibidas, en orden")
der.set_ylabel("cobrado acumulado (EUR)")
titulo(der, "El reintento encuentra la clave apuntada",
       "por eso no se cobra: el efecto ocurre una sola vez")
rejilla(der)
numeros(der, ejes="y")

guardar(fig, "exactamente-una-vez-deduplicar")
