"""algoritmos-de-join-1.py — el reparto por hash cuando una clave está sesgada y el coste de las
tres familias de join. Página de algoritmos de join (fase 10)."""

import zlib

import numpy as np

from comun import *

estilo()

# --- Izquierda: con una clave caliente, subir las particiones no arregla nada.
P_VALORES = [2, 4, 8, 16, 32, 64, 128, 256]
MEMORIA = 2000


def mayor_particion(filas, P):
    """Tamaño de la partición más cargada al repartir por hash de la clave."""
    partes = [0] * P
    for fila in filas:
        partes[zlib.crc32(str(fila[0]).encode()) % P] += 1
    return max(partes)


uniforme = [(i % 5000, i) for i in range(10000)]                    # 5.000 claves, 2 filas cada una
sesgado = [(42 if i % 2 == 0 else i % 5000, i) for i in range(10000)]   # la clave 42 en la mitad

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.5))
# Los formateadores se fijan ANTES de escribir las etiquetas a mano: al revés, el formateador
# automático pisa las etiquetas y los ejes logarítmicos salen como «1e+06».
numeros(ejes[0], ejes="both")
numeros(ejes[1], ejes="both")

mayor_u = [mayor_particion(uniforme, P) for P in P_VALORES]
mayor_s = [mayor_particion(sesgado, P) for P in P_VALORES]
ejes[0].loglog(P_VALORES, mayor_u, color=AZUL, linewidth=2.0, marker="o", markersize=5,
               label="claves uniformes")
ejes[0].loglog(P_VALORES, mayor_s, color=ROJO, linewidth=2.0, marker="s", markersize=5,
               label="una clave con la mitad de las filas")
ejes[0].axhline(MEMORIA, color=MORADO, linewidth=1.4, linestyle="--")
anotar(ejes[0], f"memoria disponible: {MEMORIA:,} filas".replace(",", "."),
       xy=(2, MEMORIA), xytext=(0.03, 0.44), color=MORADO, flecha=False)
anotar(ejes[0], f"con P = 256 sigue en {mayor_s[-1]:,} filas: el reparto\nno puede separar una misma clave".replace(",", "."),
       xy=(256, mayor_s[-1]), xytext=(0.03, 0.82), color=ROJO, flecha=False)
anotar(ejes[0], "la uniforme sí baja como n/P", xy=(64, mayor_u[5]),
       xytext=(0.30, 0.18), color=AZUL, flecha=False)
titulo(ejes[0], "El sesgo no se arregla con más particiones",
       "partición mayor al repartir 10.000 filas por hash")
ejes[0].set_xlabel("particiones P")
ejes[0].set_ylabel("filas en la partición mayor")
ejes[0].set_xticks(P_VALORES)
ejes[0].set_xticklabels([str(P) for P in P_VALORES])
ejes[0].set_yticks([100, 200, 500, 1000, 2000, 5000])
ejes[0].set_yticklabels(["100", "200", "500", "1.000", "2.000", "5.000"])
ejes[0].minorticks_off()
ejes[0].legend(loc="lower left", fontsize=9)
rejilla(ejes[0], eje="both")

# --- Derecha: el bucle anidado crece con el producto y los otros dos, en línea recta.
filas = np.logspace(4, 8, 60)                 # filas por tabla
b = filas / 100                               # bloques por tabla, con 100 filas por bloque


def ordenar_externo(bloques, M, k):
    """Bloques movidos al ordenar en disco: 2b por pasada, una por ronda más la inicial."""
    vueltas, rondas = -(-bloques // M), 0
    while vueltas > 1:
        vueltas = -(-vueltas // k)
        rondas += 1
    return 2 * bloques * (1 + rondas)


anidado = b + b * b
en_memoria = 2 * b
grace = 6 * b
con_orden = np.array([ordenar_externo(int(x), 5000, 10) for x in b]) * 2 + 2 * b

ejes[1].loglog(filas, anidado, color=ROJO, linewidth=2.0)
ejes[1].loglog(filas, con_orden, color=MORADO, linewidth=1.8, linestyle="--")
ejes[1].loglog(filas, grace, color=NARANJA, linewidth=2.0)
ejes[1].loglog(filas, en_memoria, color=AZUL, linewidth=2.2)
# Sin leyenda: cada nota lleva el color de su curva y así no tapa ninguna línea.
anotar(ejes[1], "el bucle anidado: 10¹² bloques\ncon 100 millones de filas", xy=(1e8, 1e12),
       xytext=(0.03, 0.95), color=ROJO, flecha=False)
anotar(ejes[1], "sort-merge: pagar la ordenación\nde las dos tablas", xy=(1e8, 1.4e7),
       xytext=(0.03, 0.80), color=MORADO, flecha=False)
anotar(ejes[1], "Grace hash: tres pasadas\ncuando no cabe en memoria", xy=(1e8, 6e6),
       xytext=(0.03, 0.65), color=NARANJA, flecha=False)
anotar(ejes[1], "hash join en memoria:\nuna pasada por tabla", xy=(1e8, 2e6),
       xytext=(0.03, 0.54), color=AZUL, flecha=False)
titulo(ejes[1], "Tres formas de unir, tres costes",
       "bloques movidos al unir dos tablas de n filas, con 100 filas por bloque")
ejes[1].set_xlabel("filas por tabla n")
ejes[1].set_ylabel("bloques movidos")
ejes[1].set_xticks([1e4, 1e5, 1e6, 1e7, 1e8])
ejes[1].set_xticklabels(["10.000", "100.000", "1 millón", "10 millones", "100 millones"])
ejes[1].set_yticks([1e4, 1e6, 1e8, 1e10, 1e12])
ejes[1].set_yticklabels(["10.000", "1 millón", "100 millones", "10.000 millones", "1 billón"])
ejes[1].set_ylim(1e2, 1e13)
ejes[1].minorticks_off()
rejilla(ejes[1], eje="both")

guardar(fig, "algoritmos-de-join-coste-y-sesgo")
