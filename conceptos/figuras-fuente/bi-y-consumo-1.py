"""bi-y-consumo-1.py — coste de servir un cuadro en vivo o como extracto (fase 4).

Izquierda: las dos rectas de coste y su cruce. Derecha: como se mueve ese cruce segun los GB
que escanea cada consulta, que es lo que decide podar o no la partición.
"""

import numpy as np

from comun import *

estilo()

gb_por_tb = 1000.0
b = 2.0        # GB que escanea una consulta sin podar la particion
gran_tabla = 60.0   # GB que copia el extracto entero
refrescos = 30      # refrescos al mes
precio = 5.0        # euros por TB escaneado

consultas = np.linspace(0, 6000, 400)
viva = consultas * b / gb_por_tb * precio
extracto = np.full_like(consultas, refrescos * gran_tabla / gb_por_tb * precio)
cruce = refrescos * gran_tabla / b

fig, ejes = plt.subplots(1, 2, figsize=(7.6, 3.7))

eje = ejes[0]
eje.plot(consultas, viva, color=AZUL, linewidth=1.8)
eje.plot(consultas, extracto, color=VERDE, linewidth=1.8)
eje.axvline(cruce, color=MORADO, linewidth=1.1, linestyle=":")
eje.set_xlabel("consultas al mes")
eje.set_ylabel("coste mensual (EUR)")
titulo(eje, "El extracto empieza a ganar a las 900 consultas")
eje.text(0.55, 0.72, "consulta viva", transform=eje.transAxes, color=AZUL, fontsize=9)
eje.text(0.55, 0.10, "extracto nocturno", transform=eje.transAxes, color=VERDE, fontsize=9)
anotar(eje, "mismo coste en el cruce", xy=(cruce, extracto[0]), xytext=(0.30, 0.26), color=MORADO)
rejilla(eje)
numeros(eje)

eje = ejes[1]
escaneo = np.logspace(np.log10(0.01), np.log10(5), 200)
cruce_por_gb = refrescos * gran_tabla / escaneo
eje.plot(escaneo, cruce_por_gb, color=ROJO, linewidth=1.8)
eje.set_xscale("log")
eje.set_yscale("log")
eje.set_xlabel("GB escaneados por consulta")
eje.set_ylabel("consultas al mes en el cruce")
titulo(eje, "Podar la partición mueve el cruce cien veces")
anotar(eje, "con poda, el cruce sube a 90.000", xy=(0.02, refrescos * gran_tabla / 0.02),
       xytext=(0.34, 0.94), color=ROJO)
rejilla(eje, eje="both")
numeros(eje)

guardar(fig, "bi-y-consumo-coste-viva-y-extracto")
