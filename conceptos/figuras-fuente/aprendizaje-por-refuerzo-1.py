"""aprendizaje-por-refuerzo-1.py — cuánto cuesta no explorar y cuánto vale el futuro según
el descuento. La figura de la página de aprendizaje por refuerzo (fase 7)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# Bandido de tres brazos: probabilidad real de premio 0,3 / 0,5 / 0,4 (el segundo es el mejor).
medias = np.array([0.3, 0.5, 0.4])


def bandido(epsilon, pasos=2000):
    """Juega `pasos` veces con política epsilon-greedy y devuelve el premio medio por tirada."""
    q = np.zeros(3)                          # valor estimado de cada brazo
    n = np.zeros(3)                          # veces que se ha tirado de cada brazo
    premio = 0.0
    for _ in range(pasos):
        if azar.random() < epsilon:
            a = int(azar.integers(3))        # explorar: un brazo al azar
        else:
            a = int(np.argmax(q))            # explotar: el de más valor estimado
        r = float(azar.random() < medias[a])
        n[a] += 1
        q[a] += (r - q[a]) / n[a]            # media incremental, sin guardar el historial
        premio += r
    return premio / pasos


fig, ejes = plt.subplots(1, 2, figsize=(8.2, 3.9))

# --- Izquierda: la recompensa según cuánto se explora ---
ax = ejes[0]
epslons = np.array([0.0, 0.01, 0.05, 0.10, 0.20])
medias_medidas = np.array([bandido(e) for e in epslons])
ax.plot(epslons, medias_medidas, "o-", color=AZUL, markersize=6, linewidth=1.6)
# Dos referencias que no dependen de ninguna política aprendida.
ax.axhline(medias.mean(), color=REJILLA, linewidth=1.3, linestyle="--")
ax.axhline(medias.max(), color=ROJO, linewidth=1.3, linestyle=":")
ax.set_xlim(-0.015, 0.215)
ax.set_ylim(0.22, 0.58)
ax.set_xlabel("epsilon: fracción de tiradas al azar")
ax.set_ylabel("premio medio por tirada")
anotar(ax, "elegir al azar da 0,40", (0.20, medias.mean()), (0.36, 0.30), color=TEXTO)
anotar(ax, "el mejor brazo da 0,50", (0.20, medias.max()), (0.36, 0.85), color=ROJO)
anotar(ax, "sin explorar se queda en 0,29:\nni siquiera empata con el azar",
       (0.0, medias_medidas[0]), (0.30, 0.20), color=NARANJA, flecha=False)
titulo(ax, "Explorar un poco sube el premio", "y no explorar nada lo hunde")
rejilla(ax)
numeros(ax)

# --- Derecha: qué vale una recompensa según los pasos que tarda ---
ax = ejes[1]
pasos = np.arange(0, 31)
for gamma, color in ((0.9, NARANJA), (0.99, CIAN)):
    ax.plot(pasos, gamma ** pasos, color=color, linewidth=1.7, label=f"gamma = {gamma}")
ax.axhline(0.5, color=REJILLA, linewidth=1.1, linestyle=":")
ax.set_xlim(0, 30)
ax.set_ylim(0, 1.26)
ax.set_xlabel("pasos hasta cobrar la recompensa")
ax.set_ylabel("valor de 1 unidad de premio")
# Sin leyenda: el nombre de cada curva va dentro de su propia anotación, y el color lo ata.
anotar(ax, "gamma = 0,9: el futuro deja de contar\nen unos 7 pasos",
       (7, 0.9 ** 7), (0.02, 0.86), color=NARANJA, flecha=False)
anotar(ax, "con gamma = 0,99 el mismo premio a 30 pasos\naún vale 0,74 y el agente sigue mirando lejos",
       (30, 0.99 ** 30), (0.98, 0.30), color=CIAN, flecha=False, align="right")
titulo(ax, "El descuento decide cuánto mira el agente",
       "gamma es, en la práctica, el horizonte")
rejilla(ax)
numeros(ax)

guardar(fig, "refuerzo-explorar-y-descontar")
