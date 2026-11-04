"""ci-cd-1.py — el orden de las etapas no cambia lo que tarda el camino feliz, pero si lo que
tarda un desarrollador en enterarse de que ha roto algo. La figura de la pagina (fase 11)."""

import numpy as np

from comun import *

estilo()

# Las cuatro etapas del ejemplo de la pagina: duracion en segundos y probabilidad de fallo.
etapas = {"e2e": (600.0, 0.05), "integración": (240.0, 0.15),
          "unitarias": (40.0, 0.25), "lint": (5.0, 0.02)}
nombres = {"e2e": "extremo a extremo", "integración": "integración",
           "unitarias": "unitarias", "lint": "analisis estatico"}


def espera_hasta_fallo(orden):
    """Media del tiempo hasta el primer fallo, condicionada a que algo falle."""
    total, llega, acumulado = 0.0, 1.0, 0.0
    for nombre in orden:
        duracion, p_fallo = etapas[nombre]
        acumulado += duracion
        total += llega * p_fallo * acumulado
        llega *= 1 - p_fallo
    return total / (1 - llega)


actual = ["e2e", "integración", "unitarias", "lint"]
mejor = sorted(etapas, key=lambda n: etapas[n][0] / etapas[n][1])
e_actual, e_mejor = espera_hasta_fallo(actual), espera_hasta_fallo(mejor)
total = sum(d for d, _ in etapas.values())

fig, ejes = plt.subplots(1, 2, figsize=(11.6, 4.4))

# --- Izquierda: cuanto pesa cada etapa en la espera ---------------------------
filas = np.arange(len(mejor))
pesos = [etapas[n][0] * etapas[n][1] for n in mejor]      # coste por unidad de fallo
colores = [ROJO if n == "e2e" else NARANJA if n == "integración" else AZUL for n in mejor]
ejes[0].barh(filas, pesos, height=0.55, color=colores)
ejes[0].invert_yaxis()          # la etapa que mas pesa, arriba
for i, (n, peso) in enumerate(zip(mejor, pesos)):
    ejes[0].text(peso + 0.4, i, f"{etapas[n][0]:.0f} s x {etapas[n][1]:.2f} = {peso:.1f}",
                 va="center", fontsize=8, color=TEXTO)

ejes[0].set_yticks(filas)
ejes[0].set_yticklabels([nombres[n] for n in mejor], fontsize=9)
ejes[0].set_xlim(0, 62)
ejes[0].set_xlabel("segundos que aporta cada etapa a la espera")
titulo(ejes[0], "Lo que pesa no es lo que dura",
       "600 s con un 5 por ciento pesan solo el triple que 40 s con un 25 por ciento")
rejilla(ejes[0], "x")
numeros(ejes[0], "x")

# --- Derecha: la media hasta el fallo en los dos ordenes ----------------------
etiquetas = ["etapas lentas\nprimero", "etapas que fallan\nmucho primero"]
valores = [e_actual, e_mejor]
for i, (valor, color) in enumerate(zip(valores, [ROJO, VERDE])):
    ejes[1].bar(i, valor, width=0.5, color=color)
    ejes[1].text(i, valor + 25, f"{valor:.0f} s", ha="center", fontsize=10, color=TEXTO)
ejes[1].axhline(total, color=MORADO, linestyle="--", linewidth=1.3)
anotar(ejes[1], f"el pipeline completo son {total:.0f} s en los dos ordenes",
       xy=(0.35, total), xytext=(0.55, 0.50), color=MORADO)
anotar(ejes[1], "el caso frecuente mejora casi cinco veces",
       xy=(0.72, e_mejor), xytext=(0.50, 0.45), color=VERDE)

ejes[1].set_xticks(range(2))
ejes[1].set_xticklabels(etiquetas, fontsize=9)
ejes[1].set_xlim(-0.5, 1.5)
ejes[1].set_ylim(0, 1000)
ejes[1].set_ylabel("segundos de media hasta el primer fallo")
titulo(ejes[1], "Ordenar por coste partido por fallo",
       "no se acelera el camino feliz: se acorta el caso malo, que es el frecuente")
rejilla(ejes[1])
numeros(ejes[1], "y")

guardar(fig, "ci-cd-orden-de-etapas")
