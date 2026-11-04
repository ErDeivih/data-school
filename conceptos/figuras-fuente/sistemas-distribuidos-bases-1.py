"""sistemas-distribuidos-bases-1.py — el abanico multiplica la cola y el reparto decide cuanto se
mueve al crecer. La figura de la pagina de sistemas distribuidos (fase 11)."""

import numpy as np

from comun import *

estilo()

# --- Izquierda: la cola se amplifica con el abanico ---------------------------------
abanico = np.arange(1, 151)
# 0.99 es la probabilidad de que UN servidor responda a tiempo: el p99 de cada pieza.
afectadas = 1 - 0.99 ** abanico

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.6, 4.2))

izq.plot(abanico, 100 * afectadas, color=AZUL, linewidth=1.8)
# Los dos puntos que cita la pagina: 10 servicios (9,6 %) y 100 (63,4 %).
for n, color in ((10, NARANJA), (100, ROJO)):
    valor = 100 * (1 - 0.99 ** n)
    izq.plot([n], [valor], "o", color=color, markersize=5)
    izq.annotate(f"{n} servicios: {valor:.1f} %".replace(".", ","),
                 xy=(n, valor), xycoords="data",
                 xytext=(0.10, 0.86 if n == 10 else 0.66), textcoords="axes fraction",
                 fontsize=8.5, color=color, va="center",
                 arrowprops=dict(arrowstyle="->", color=color, linewidth=0.9, shrinkA=2, shrinkB=2))
# La raya del 50 % es la conclusion incomoda de la curva: la mitad de las peticiones esperan.
izq.axhline(50, color=REJILLA, linewidth=1.0, linestyle="--")
izq.text(148, 52, "la mitad de las peticiones", color=REJILLA, fontsize=8.5, ha="right")
izq.set_ylim(0, 100)
izq.set_xlabel("servicios que hay que consultar (n)")
izq.set_ylabel("% de peticiones lentas")
titulo(izq, "Basta con que uno esté en su cola",
       "cada servicio cae en su p99 el 1 % del tiempo")
rejilla(izq)
numeros(izq)

# --- Derecha: repartir bien decide si crecer es barato ------------------------------
estrategias = ["hash mod N\n(4 a 5 nodos)", "anillo consistente\n(4 a 5 nodos)"]
movidas = np.array([80, 20])
colores = [ROJO, VERDE]
barras = der.bar(estrategias, movidas, color=colores, width=0.45)
der.bar_label(barras, labels=[f"{v} % de las claves" for v in movidas], padding=3, fontsize=9)
anotar(der, "casi todo el conjunto\nde datos por la red", xy=(0.05, 78), xytext=(0.40, 0.84),
       color=ROJO)
# La anotacion de la derecha apunta al barra verde, pero el texto se queda a su izquierda:
# encima de la barra chocaria con la etiqueta del valor.
anotar(der, "solo el tramo\ndel nodo nuevo", xy=(0.88, 22), xytext=(0.52, 0.44), color=VERDE)
der.set_ylim(0, 100)
der.set_ylabel("% de claves que cambian de nodo")
titulo(der, "Añadir un nodo: lo que se mueve",
       "el reparto con el resto de la división castiga cada cambio")
rejilla(der)
numeros(der, ejes="y")

guardar(fig, "sistemas-distribuidos-abanico-y-reparto")
