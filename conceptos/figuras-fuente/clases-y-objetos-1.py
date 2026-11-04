"""clases-y-objetos-1.py — un atributo definido en la clase lo comparten todos los objetos;
uno definido en __init__ es de cada uno. La figura de la pagina de clases y objetos (fase 3)."""

import numpy as np

from comun import *

estilo()

dias = np.arange(1, 7)
# Lo que ingresa cada titular cada dia
ingresos_ana = np.array([10.0, 0.0, 25.0, 5.0, 0.0, 15.0])
ingresos_luis = np.array([0.0, 20.0, 0.0, 10.0, 30.0, 0.0])

# movimientos = [] escrito en la CLASE: hay una sola lista y los dos la comparten,
# asi que cada uno ve los ingresos del otro.
saldo_compartido = np.cumsum(ingresos_ana + ingresos_luis)
# self.movimientos = [] dentro de __init__: cada objeto estrena su lista.
saldo_ana = np.cumsum(ingresos_ana)
saldo_luis = np.cumsum(ingresos_luis)

fig, ejes = plt.subplots(1, 2, figsize=(9.4, 4.0), sharey=True)

ejes[0].plot(dias, saldo_compartido, color=AZUL, linewidth=2.2, marker="o", markersize=4)
ejes[0].plot(dias, saldo_compartido, color=NARANJA, linewidth=1.3, linestyle="--",
             marker="s", markersize=4)
titulo(ejes[0], "Una sola lista: los dos saldos coinciden",
       "el atributo está en la clase, no en cada objeto")
ejes[0].set_xlabel("día")
ejes[0].set_ylabel("saldo acumulado (euros)")
# El texto va debajo de la curva (que sube de izquierda a derecha), donde no hay nada.
anotar(ejes[0], "las dos líneas coinciden:\nno hay dos listas, hay una",
       xy=(3.1, saldo_compartido[2]), xytext=(0.30, 0.14))
rejilla(ejes[0])
numeros(ejes[0])

ejes[1].plot(dias, saldo_ana, color=AZUL, linewidth=2.2, marker="o", markersize=4,
             label="saldo de ana")
ejes[1].plot(dias, saldo_luis, color=NARANJA, linewidth=2.2, marker="s", markersize=4,
             label="saldo de luis")
titulo(ejes[1], "Dos listas: cada objeto acumula lo suyo",
       "el atributo se crea dentro de __init__")
ejes[1].set_xlabel("día")
# La leyenda va abajo a la derecha: arriba la cruzaría la línea roja de las 115.
ejes[1].legend(loc="lower right")
ejes[1].set_ylim(0, 132)
ejes[1].axhline(saldo_compartido[-1], color=ROJO, linewidth=1.1, linestyle="--")
# La banda entre las dos curvas (55-60) y la línea roja (115) está vacía: ahí cabe el texto.
anotar(ejes[1], "115: lo que vería ana si la lista fuera compartida",
       xy=(4.6, saldo_compartido[-1]), xytext=(0.10, 0.62), color=ROJO)
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "clases-y-objetos-atributo-compartido")
