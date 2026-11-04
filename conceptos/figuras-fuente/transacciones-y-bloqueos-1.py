"""transacciones-y-bloqueos-1.py — el intercalado que pierde una escritura y lo que cuesta
repetirlo. La figura de la pagina de transacciones, aislamiento y bloqueos (fase 3)."""

import numpy as np

from comun import *

estilo()

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 4.2))

# --- Izquierda: las dos cajas leen antes de que ninguna escriba ---------------------
# Un carril por sesion. Circulo = lee, cuadrado = escribe.
izq.axhline(1, color=REJILLA, linewidth=1.0, zorder=1)
izq.axhline(0, color=REJILLA, linewidth=1.0, zorder=1)
izq.scatter([1.0], [1], color=AZUL, s=95, zorder=3)
izq.scatter([3.0], [1], color=AZUL, s=95, marker="s", zorder=3)
izq.scatter([2.0], [0], color=NARANJA, s=95, zorder=3)
izq.scatter([4.0], [0], color=NARANJA, s=95, marker="s", zorder=3)

izq.text(1.0, 1.24, "lee 500", ha="center", fontsize=8.5, color=AZUL)
izq.text(3.0, 1.24, "escribe 600", ha="center", fontsize=8.5, color=AZUL)
izq.text(2.0, -0.30, "lee 500", ha="center", va="top", fontsize=8.5, color=NARANJA)
izq.text(4.0, -0.30, "escribe 550", ha="center", va="top", fontsize=8.5, color=NARANJA)

# La ventana entre la lectura y la escritura de la caja 2: ahi cabe la escritura ajena.
izq.annotate("", xy=(2.0, 0.5), xytext=(4.0, 0.5),
             arrowprops=dict(arrowstyle="<->", color=ROJO, linewidth=1.1))
izq.text(3.0, 0.62, "la ventana", ha="center", fontsize=8.5, color=ROJO)
anotar(izq, "las dos leen 500:\nuna escritura se pierde", xy=(1.0, 1.0), xytext=(0.04, 0.96),
       color=ROJO)

izq.set_xlim(0.2, 5.0)
izq.set_ylim(-0.95, 1.95)
izq.set_yticks([0, 1])
izq.set_yticklabels(["caja 2", "caja 1"])
izq.set_xticks([])
izq.set_xlabel("tiempo")
titulo(izq, "Las dos cajas leen el mismo 500",
       "el intercalado que produce la actualización pérdida")

# --- Derecha: el descuadre que deja detras cada dia ---------------------------------
dias = np.arange(1, 21)
# Cada dia entran dos ingresos: 100 por la manana y 50 por la tarde. La ultima escritura gana:
# la de la tarde calcula sobre la lectura vieja de la manana, asi que pisa el saldo con su
# propio incremento y el ingreso de la manana es el que no llega a la base.
registrado = 500.0 + 50.0 * dias
ingresado = 500.0 + 150.0 * dias

der.fill_between(dias, registrado, ingresado, color=ROJO, alpha=0.12)
der.plot(dias, ingresado, color=VERDE, linewidth=2.2, label="dinero que ha entrado")
der.plot(dias, registrado, color=ROJO, linewidth=2.2, label="saldo en la base")
der.set_xlabel("días")
der.set_ylabel("euros")
der.set_ylim(500, 3700)
der.legend(loc="upper left")
anotar(der, "100 euros al día\nde descuadre", xy=(11.0, 500.0 + 100.0 * 11),
       xytext=(0.42, 0.42), color=ROJO)
der.annotate("", xy=(20.0, ingresado[-1]), xytext=(20.0, registrado[-1]),
             arrowprops=dict(arrowstyle="<->", color=TEXTO, linewidth=1.0))
titulo(der, "El hueco crece 100 euros al día",
       "lo que figura en la base frente al dinero que entró")
rejilla(der)
numeros(der)

guardar(fig, "transacciones-lectura-perdida")
