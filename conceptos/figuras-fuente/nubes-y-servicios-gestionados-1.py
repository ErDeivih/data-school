"""nubes-y-servicios-gestionados-1.py — los tres modelos de cobro del computo gestionado.
Por consulta pagas solo lo que usas: barato en rafagas, carisimo con carga estable. La
reserva es una cuota fija que sale a cuenta en cuanto la carga pasa cierto umbral. El
consumo puro (sin servidor) factura por uso, pero el proveedor le pone un techo de
capacidad: pasado ese punto, el trabajo se multiplica y la curva se dispara.
"""

import numpy as np

from comun import *

estilo()

consulta = 6.0        # coste por cada 1000 consultas
reserva = 100.0       # cuota mensual fija de la capacidad reservada
techo = 150.0         # coste de consumo cuando el trafico llega al techo de capacidad
tope = 700.0          # consultas al mes (en miles) a las que el sin servidor toca techo

q = np.linspace(0, 1000, 800)          # consultas al mes, en miles
por_consulta = consulta * q
con_reserva = np.full_like(q, reserva)
# Hasta el techo, el consumo crece con el trafico; despues, el exceso se paga multiplicado.
sin_servidor = techo * (1 + 2.6 * np.maximum(q - tope, 0) / (1000 - tope))

fig, ax = plt.subplots()

ax.plot(q, por_consulta, color=ROJO, linewidth=1.6, label="pago por consulta")
ax.plot(q, con_reserva, color=MORADO, linewidth=1.8, label="capacidad reservada")
ax.plot(q, sin_servidor, color=VERDE, linewidth=2.0, label="sin servidor (por uso)")
ax.axvline(tope, color=REJILLA, linewidth=0.9, linestyle="--")

alto = float(por_consulta[-1])         # coste de pagar por consulta con el trafico maximo
ax.set_ylim(0, alto * 1.06)
ax.set_xlim(0, 1030)

# Cruce entre pagar por consulta y reservar: el umbral que hay que calcular.
cruce = reserva / consulta
ax.plot([cruce], [reserva], marker="o", color=TEXTO, markersize=5, zorder=5)

# Las tres anotaciones se escriben en coordenadas del eje (0-1), no en coordenadas de
# datos: asi cada una cae en una zona vacia (arriba a la izquierda, arriba en el centro y
# en la banda que queda por debajo de la recta roja) y ninguna toca una curva ni otra.
anotar(ax, "pagar por consulta\nsolo gana con ráfagas", xy=(250, float(consulta * 250)),
       xytext=(0.04, 0.60), color=ROJO)
anotar(ax, "el techo de capacidad\nencarece el pico diario",
       xy=(880, float(sin_servidor[np.argmin(np.abs(q - 880))])),
       xytext=(0.44, 0.74), color=VERDE)
anotar(ax, "desde " + str(int(round(cruce))) + " mil consultas al mes,\n"
       "reservar es más barato que pagar",
       xy=(cruce, reserva), xytext=(0.33, 0.19), color=TEXTO)

ax.set_xlabel("consultas al mes (miles)")
ax.set_ylabel("coste mensual del computo")
titulo(ax, "Con carga estable, el volumen no es lo caro",
       "pagar por consulta solo compensa con ráfagas")
ax.legend(loc="upper left")
numeros(ax)
rejilla(ax)

guardar(fig, "nubes-modelos-de-cobro")
