"""map-reduce-1.py — añadir máquinas no acelera como uno cree (ley de Amdahl y coste de shuffle) y
el desbalanceo de particiones decide el tiempo total, no la media. Página de MapReduce y cómputo
distribuido (fase 10)."""

import hashlib

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.5))

# --- Izquierda: la aceleración al añadir trabajadores. Tres referencias: la ideal (lineal), la de
# Amdahl con una fracción serie del 5 % y una más realista que además paga el shuffle.
trabajadores = np.array([1, 2, 4, 8, 16, 32, 64])
serie, coste_shuffle = 0.05, 0.04


def amdahl(n, s):
    """Aceleración con una fracción s del trabajo que no se puede paralelizar."""
    return 1.0 / (s + (1 - s) / n)


aceleracion_ideal = trabajadores.astype(float)
aceleracion_amdahl = amdahl(trabajadores, serie)
# Cada trabajador añadido cuesta coordinación (arranque de tareas, barreras, shuffle): ese coste
# crece con el número de máquinas, y es lo que hace que la curva real acabe bajando.
aceleracion_real = 1.0 / (serie + (1 - serie) / trabajadores + coste_shuffle * (trabajadores - 1) / trabajadores)

ejes[0].plot(trabajadores, aceleracion_ideal, color=REJILLA, linewidth=1.2, linestyle="--",
             marker="o", markersize=4, label="ideal lineal")
ejes[0].plot(trabajadores, aceleracion_amdahl, color=AZUL, linewidth=2.0, marker="o",
             markersize=4, label=f"Amdahl con {serie:.0%} de trabajo en serie")
ejes[0].plot(trabajadores, aceleracion_real, color=NARANJA, linewidth=2.0, marker="s",
             markersize=4, label="con el coste del shuffle")
techo = 1 / serie
ejes[0].axhline(techo, color=AZUL, linewidth=1.0, linestyle=":")
mejor = int(np.argmax(aceleracion_real))
anotar(ejes[0], f"el techo es {techo:.0f}×: lo fija el {serie:.0%}\nque no se puede repartir",
       xy=(64.0, techo), xytext=(0.05, 0.74), color=AZUL)
anotar(ejes[0], f"con el coste de coordinación,\nel máximo está en {trabajadores[mejor]} trabajadores\n({aceleracion_real[mejor]:.1f}×) y luego baja",
       xy=(float(trabajadores[mejor]), float(aceleracion_real[mejor])), xytext=(0.30, 0.30),
       color=NARANJA)
titulo(ejes[0], "Añadir máquinas no acelera como uno cree",
       "aceleración frente al número de trabajadores")
ejes[0].set_xlabel("trabajadores (escala logarítmica)")
ejes[0].set_ylabel("aceleración respecto a uno")
ejes[0].set_xscale("log", base=2)
ejes[0].set_xticks(trabajadores)
ejes[0].set_xticklabels([str(t) for t in trabajadores])
ejes[0].legend(loc="upper left", fontsize=8)
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="y")

# --- Derecha: el desbalanceo. 200.000 registros cuyas claves siguen una ley de potencias: casi
# todo el tráfico se concentra en unas pocas claves, que es lo que pasa con los nulos, los robots
# o los usuarios muy activos.
REGISTROS, CLAVES, REDUCTORES = 200_000, 20_000, 10
claves = np.minimum(azar.zipf(1.3, REGISTROS), CLAVES) - 1


def reparto(numero_de_clave):
    """Hash determinista y estable: en un sistema distribuido la misma clave tiene que caer
    siempre en el mismo reductor, también al reejecutar una tarea caída."""
    resumen = hashlib.blake2b(str(int(numero_de_clave)).encode(), digest_size=8).digest()
    return int.from_bytes(resumen, "big") % REDUCTORES


# Se resuelve el hash una vez por clave distinta (20.000) y luego se busca por índice: recorrer
# los 200.000 registros uno a uno con el hash sería el doble de lento y no cambiaría nada.
reductor_de_clave = np.array([reparto(c) for c in range(CLAVES)])
carga = np.bincount(reductor_de_clave[claves], minlength=REDUCTORES)
ideal = REGISTROS / REDUCTORES

ejes[1].bar(range(REDUCTORES), carga, color=AZUL, width=0.62)
ejes[1].axhline(ideal, color=ROJO, linewidth=1.6, linestyle="--")
peor = int(np.argmax(carga))
ejes[1].bar([peor], [carga[peor]], color=NARANJA, width=0.62)
# Sin leyenda: cada referencia va rotulada donde está, que es lo que evita que el texto caiga
# encima de las barras. La etiqueta de la línea ideal lleva fondo blanco (el mismo del papel)
# para que se lea aunque la línea punteada le pase por debajo.
ejes[1].annotate(f"reparto ideal: {ideal:,.0f} cada uno".replace(",", "."), xy=(0.0, ideal),
                 xytext=(0.0, ideal + 0.04 * carga.max()), fontsize=8.5, color=ROJO,
                 bbox=dict(facecolor="white", edgecolor="none", pad=1.0))
anotar(ejes[1], f"el reductor más cargado lleva {carga[peor] / ideal:.1f} veces\nmás que la media: el trabajo dura lo que él",
       xy=(float(peor), float(carga[peor])), xytext=(0.36, 0.95), color=NARANJA)
anotar(ejes[1], "los demás terminan antes y esperan:\nnadie reparte el trabajo que sobra",
       xy=(float(int(np.argmin(carga))), float(carga.min())), xytext=(0.35, 0.68), color=AZUL)
titulo(ejes[1], "El desbalanceo manda sobre la media",
       f"{REGISTROS:,} registros y {CLAVES:,} claves con ley de potencias".replace(",", "."))
ejes[1].set_xlabel("número de reductor")
ejes[1].set_ylabel("registros asignados")
ejes[1].set_xticks(range(REDUCTORES))
rejilla(ejes[1], eje="y")
numeros(ejes[1], ejes="y")

guardar(fig, "map-reduce-aceleracion-y-desbalanceo")
