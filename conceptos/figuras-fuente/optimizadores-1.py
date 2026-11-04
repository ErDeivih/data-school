"""optimizadores-1.py — la misma pérdida y el mismo gradiente con cuatro reglas de paso.

El valle estrecho f(x, y) = 0,5·(x² + 100·y²) desde el punto (1, 1): cien veces más curvatura
en y que en x. Izquierda: por dónde pasa cada regla. Derecha: la pérdida en cada iteración, en
escala logarítmica, que es donde se ve que SGD con η = 0,025 diverge.
La figura de la página de optimizadores (fase 7).
"""

import numpy as np

from comun import *

estilo()

PASOS = 20


def valle(eta, beta=None, pasos=PASOS):
    """SGD puro (beta=None) o con momento. Devuelve la trayectoria completa, no solo el final."""
    q = np.array([1.0, 1.0])
    v = np.zeros(2)
    traza = [q.copy()]
    for _ in range(pasos):
        g = np.array([q[0], 100.0 * q[1]])      # gradiente de 0,5·(x² + 100·y²)
        if beta is None:
            q = q - eta * g
        else:
            v = beta * v + g                    # la velocidad acumula el gradiente
            q = q - eta * v
        traza.append(q.copy())
    return np.array(traza)


def adam(eta, pasos=PASOS):
    """Adam con sus valores por defecto y la corrección de sesgo de las medias."""
    q = np.array([1.0, 1.0])
    m, v = np.zeros(2), np.zeros(2)
    traza = [q.copy()]
    for t in range(1, pasos + 1):
        g = np.array([q[0], 100.0 * q[1]])
        m = 0.9 * m + 0.1 * g                   # media del gradiente
        v = 0.999 * v + 0.001 * g ** 2          # media del gradiente al cuadrado
        q = q - eta * (m / (1 - 0.9 ** t)) / (np.sqrt(v / (1 - 0.999 ** t)) + 1e-8)
        traza.append(q.copy())
    return np.array(traza)


t_sgd = valle(0.015)
t_mom = valle(0.015, 0.9)
t_adam = adam(0.05)
t_mal = valle(0.025)                            # dos milésimas más y no converge

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.4))

# --- Izquierda: por dónde pasa cada regla en el valle --------------------------------
ax = ejes[0]
xx, yy = np.meshgrid(np.linspace(-0.4, 1.4, 400), np.linspace(-1.3, 1.3, 400))
zz = 0.5 * (xx ** 2 + 100.0 * yy ** 2)
# Niveles geométricos: con niveles lineales las elipses se saldrían del encuadre
ax.contour(xx, yy, zz, levels=np.logspace(-1.5, 1.0, 10), colors=[REJILLA], linewidths=0.6)
ax.plot(t_sgd[:, 0], t_sgd[:, 1], color=AZUL, linewidth=1.6, marker="o", markersize=3,
        label="SGD, η = 0,015")
ax.plot(t_adam[:, 0], t_adam[:, 1], color=MORADO, linewidth=1.6, marker="o", markersize=3,
        label="Adam, η = 0,05")
ax.scatter([0.0], [0.0], s=55, color=TEXTO, marker="*", zorder=5)
# La trayectoria del momento se deja fuera de este panel: su zigzag cruza todo el valle y
# tapa las otras dos. En el panel de la derecha se ve lo que hace con la pérdida.
anotar(ax, "SGD avanza en x y se queda\npegado al fondo del valle:\nen y no puede dar un paso mayor",
       xy=(0.72, 0.02), xytext=(0.10, 0.38), color=AZUL)
anotar(ax, "Adam llega al centro con el mismo\npaso en las dos direcciones",
       xy=(0.11, 0.11), xytext=(0.25, 0.88), color=MORADO)
titulo(ax, "El valle estrecho castiga al descenso de gradiente",
       "curvas de nivel de 0,5·(x² + 100·y²), cien veces más curvatura en y")
ax.set_xlabel("x (curvatura 1)")
ax.set_ylabel("y (curvatura 100)")
ax.set_xlim(-0.35, 1.35)
ax.set_ylim(-1.25, 1.20)
ax.legend(loc="lower left")
rejilla(ax)
numeros(ax)

# --- Derecha: la pérdida en cada iteración -------------------------------------------
ax = ejes[1]
perdida = lambda t: 0.5 * (t[:, 0] ** 2 + 100.0 * t[:, 1] ** 2)
for traza, color, etiqueta in ((t_sgd, AZUL, "SGD, η = 0,015"),
                               (t_mal, ROJO, "SGD, η = 0,025"),
                               (t_mom, VERDE, "momento, β = 0,9"),
                               (t_adam, MORADO, "Adam, η = 0,05")):
    ax.semilogy(np.arange(len(traza)), perdida(traza), color=color, linewidth=1.6,
                marker="o", markersize=3, label=etiqueta)
ax.axhline(perdida(t_sgd)[-1], color=REJILLA, linewidth=0.9, linestyle=":")
# El eje arranca por debajo de todas las curvas: así la banda de abajo queda libre para las notas.
ax.set_ylim(1e-2, 1e9)
anotar(ax, "dos milésimas más de η:\nel error ×1,5 en cada paso",
       xy=(18.0, perdida(t_mal)[18]), xytext=(0.42, 0.93), color=ROJO)
anotar(ax, "Adam baja de forma sostenida,\nsin aprovechar la curvatura a su favor",
       xy=(19.0, perdida(t_adam)[-1]), xytext=(0.24, 0.05), color=MORADO)
titulo(ax, "Cuatro reglas, cuatro finales distintos",
       "la misma pérdida y el mismo gradiente desde (1, 1), en escala logarítmica")
ax.set_xlabel("iteración")
ax.set_ylabel("pérdida")
ax.legend(loc="upper left")
rejilla(ax)
numeros(ax, ejes="x")

guardar(fig, "optimizadores-valle-y-perdida")
