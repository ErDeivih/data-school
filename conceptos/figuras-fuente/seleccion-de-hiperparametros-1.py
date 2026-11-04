"""seleccion-de-hiperparametros-1.py — por qué la búsqueda aleatoria sondea mejor el espacio
que la rejilla con el mismo presupuesto, y por qué el mejor de N intentos no es una
estimación insesgada. Figura de la página de búsqueda de hiperparámetros (fase 6)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# Los dos hiperparámetros del ejemplo de la página: C entre 0,1 y 10 y gamma entre 0,01 y 1,
# los dos en escala logarítmica porque son multiplicativos.
C_rejilla = np.array([0.1, 1.0, 10.0])
g_rejilla = np.array([0.01, 0.1, 1.0])
C_aleatoria = 10 ** azar.uniform(-1, 1, 9)
g_aleatoria = 10 ** azar.uniform(-2, 0, 9)

fig, ejes = plt.subplots(1, 2, figsize=(11.2, 4.4))

# --- Izquierda: los dos diseños de muestreo sobre el mismo presupuesto de 9 intentos.
# Las líneas de puntos marcan los tres valores que la rejilla usa en cada eje: fuera de esas
# tres rectas no hay ni un punto, y ahí está la mitad del espacio de búsqueda.
for c in C_rejilla:
    ejes[0].axvline(c, color=REJILLA, linewidth=0.8, linestyle=":", zorder=0)
for g in g_rejilla:
    ejes[0].axhline(g, color=REJILLA, linewidth=0.8, linestyle=":", zorder=0)
malla_C, malla_g = np.meshgrid(C_rejilla, g_rejilla)
ejes[0].scatter(malla_C.ravel(), malla_g.ravel(), marker="s", s=52, color=AZUL,
                zorder=4, label="rejilla: 3 valores por eje")
ejes[0].scatter(C_aleatoria, g_aleatoria, marker="o", s=52, color=ROJO,
                zorder=5, label="aleatoria: 9 valores por eje")
anotar(ejes[0], "los nueve puntos de la aleatoria\nno comparten ni una coordenada",
       xy=(C_aleatoria[3], g_aleatoria[3]), xytext=(0.36, 0.86), color=ROJO)
anotar(ejes[0], "la rejilla repite\nlas mismas tres columnas", xy=(10.0, 0.1),
       xytext=(0.44, 0.16), color=AZUL)
ejes[0].legend(loc="lower left")
titulo(ejes[0], "Nueve intentos, dos diseños",
       "cada punto es una combinación probada; los dos ejes van en escala logarítmica")
ejes[0].set_xscale("log")
ejes[0].set_yscale("log")
ejes[0].set_xlabel("C (escala logarítmica)")
ejes[0].set_ylabel("gamma (escala logarítmica)")
rejilla(ejes[0], "both")
numeros(ejes[0])

# --- Derecha: sesenta configuraciones EQUIVALENTES (misma puntuación media, mismo ruido).
# El máximo acumulado sube con los intentos aunque no haya nada mejor que encontrar; la
# mediana, que sí estima el nivel real, se queda quieta.
media, ruido = 0.850, 0.012
puntuaciones = media + azar.normal(0, ruido, 60)
mejor_hasta_ahora = np.maximum.accumulate(puntuaciones)   # el número que reporta la búsqueda
intentos = np.arange(1, puntuaciones.size + 1)

ejes[1].axhline(media, color=TEXTO, linewidth=1.2, linestyle="--")
ejes[1].plot(intentos, mejor_hasta_ahora, color=ROJO, linewidth=1.9,
             label="mejor encontrado hasta ahora")
ejes[1].scatter(intentos, puntuaciones, color=REJILLA, s=10, zorder=3,
                label="cada intento")
anotar(ejes[1], "la media real es 0,850:\nninguna configuración es mejor que otra",
       xy=(52, media), xytext=(0.30, 0.22), color=TEXTO, flecha=False)
anotar(ejes[1], "el máximo sube %.3f por puro ruido" % (mejor_hasta_ahora[-1] - media),
       xy=(60, mejor_hasta_ahora[-1]), xytext=(0.06, 0.93), color=ROJO)
ejes[1].legend(loc="lower right")
titulo(ejes[1], "El mejor de N intentos siempre parece mejor",
       "sesenta configuraciones idénticas en calidad, con el ruido de la validación")
ejes[1].set_xlabel("configuraciones probadas (presupuesto gastado)")
ejes[1].set_ylabel("puntuación en validación")
ejes[1].set_ylim(0.80, 0.90)
rejilla(ejes[1])
numeros(ejes[1], ejes="y")

guardar(fig, "seleccion-de-hiperparametros-rejilla-vs-aleatoria")
