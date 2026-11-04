"""q-learning-y-policy-gradient-1.py — qué aprende cada familia: una tabla de valores o
directamente la política. La figura de la página de Q-learning y gradiente de política (fase 7)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# --- Q-learning en un pasillo de 6 casillas con la meta en la 5 ---
n_estados, meta = 6, 5


def paso(s, a):
    """Devuelve el estado siguiente y la recompensa: 1 = derecha, 0 = izquierda."""
    s2 = min(max(s + (1 if a == 1 else -1), 0), n_estados - 1)
    return s2, (0.0 if s2 == meta else -1.0)     # -1 por cada paso que no llega


Q = np.zeros((n_estados, 2))
for _ in range(500):                             # 500 episodios de entrenamiento
    s = 0
    for _ in range(50):
        a = int(azar.integers(2)) if azar.random() < 0.2 else int(np.argmax(Q[s]))
        s2, r = paso(s, a)
        Q[s, a] += 0.5 * (r + 0.9 * Q[s2].max() - Q[s, a])   # error TD
        s = s2
        if s == meta:
            break

# Con la tabla aprendida, esta es la política avaricia paso a paso desde el estado 0.
camino = [0]
while camino[-1] != meta and len(camino) < 20:
    camino.append(paso(camino[-1], int(np.argmax(Q[camino[-1]])))[0])
print("recorrido avaricia:", camino)             # -> [0, 1, 2, 3, 4, 5]

fig, ejes = plt.subplots(1, 2, figsize=(8.4, 3.9))

# --- Izquierda: la tabla Q, que es lo único que se aprende ---
ax = ejes[0]
x = np.arange(n_estados)
ax.bar(x - 0.19, Q[:, 0], width=0.36, color=AZUL, label="izquierda")
ax.bar(x + 0.19, Q[:, 1], width=0.36, color=VERDE, label="derecha")
ax.axhline(0, color=TEXTO, linewidth=0.8, alpha=0.4)
ax.set_xticks(x)
ax.set_xlabel("estado (casilla del pasillo; la meta está en la 5)")
ax.set_ylabel("valor aprendido Q(s, a)")
ax.set_ylim(-4.9, 1.5)
ax.legend(loc="upper left", fontsize=8.5)
anotar(ax, "a la derecha siempre vale más:\nla decisión sale del signo",
       (2.2, -1.9), (0.55, 0.14), color=VERDE)
anotar(ax, "el valor del estado 0 es la suma\ndescontada de los 5 pasos hasta la meta",
       (0.19, -3.44), (0.02, 0.07), color=AZUL, flecha=False)
titulo(ax, "Q-learning aprende una tabla de valores",
       "y luego actúa eligiendo el número más alto")
rejilla(ax)
numeros(ax, ejes="y")

# --- Derecha: el gradiente de política mueve la probabilidad, no el valor ---
ax = ejes[1]
theta = np.linspace(-4, 6, 400)
p = 1 / (1 + np.exp(-theta))                     # probabilidad de la acción buena
premios = np.array([2.0, 0.5])
esperado = p * premios[0] + (1 - p) * premios[1]

ax.plot(theta, esperado, color=MORADO, linewidth=1.7, label="retorno esperado J(theta)")
ax.axhline(premios[1], color=REJILLA, linewidth=1.1, linestyle="--")
ax.axhline(premios[0], color=REJILLA, linewidth=1.1, linestyle=":")
ax.axvline(0.5, color=ROJO, linewidth=1.1, linestyle="--")
ax.plot([0.5], [1 / (1 + np.exp(-0.5)) * premios[0] + (1 - 1 / (1 + np.exp(-0.5))) * premios[1]],
        "o", color=ROJO, markersize=7)
ax.set_xlim(-4, 6)
ax.set_ylim(0.4, 2.12)
ax.set_xlabel("parámetro theta de la política")
ax.set_ylabel("retorno esperado por episodio")
ax.legend(loc="lower right", fontsize=8.5)
anotar(ax, "el teorema da el gradiente en theta = 0,5:\n0,3525, sin conocer la derivada del premio",
       (0.5, 1.433), (0.04, 0.82), color=ROJO, flecha=False)
anotar(ax, "exploración máxima\n(p = 0,5)", (0.0, 1.25), (0.04, 0.42), color=TEXTO)
titulo(ax, "El gradiente sube la probabilidad buena",
       "no hace falta saber cuánto vale cada acción")
rejilla(ax)
numeros(ax)

guardar(fig, "q-learning-tabla-y-gradiente")
