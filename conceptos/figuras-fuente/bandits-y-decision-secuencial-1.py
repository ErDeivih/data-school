"""bandits-y-decision-secuencial-1.py — cuánto pierde cada política de bandit frente al brazo
que nadie conoce de antemano, y por qué UCB deja de insistir en un brazo que ya ha probado.
Figura de la página de bandits y decisión secuencial (fase 6)."""

import numpy as np

from comun import *

estilo()

# Cinco brazos con recompensa binaria (éxito o fracaso). Estas medias son la realidad que el
# algoritmo no conoce: solo las descubre tirando del brazo.
medias = np.array([0.30, 0.60, 0.45, 0.35, 0.50])
mejor = float(medias.max())
T = 2000
REPS = 40


def simula(politica, rng, eps=0.0):
    """Devuelve el arrepentimiento acumulado en cada paso y las tiradas por brazo."""
    n = np.zeros(medias.size)
    suma = np.zeros(medias.size)
    alfa = np.ones(medias.size)          # prior Beta(1, 1) de Thompson: no sabe nada
    beta = np.ones(medias.size)
    reg = np.empty(T)
    acum = 0.0
    for t in range(T):
        if politica == "thompson":
            i = int(np.argmax(rng.beta(alfa, beta)))       # sortea una media y actúa
        elif n.min() == 0:
            i = int(np.argmin(n))                          # UCB necesita un tiro por brazo
        elif politica == "ucb":
            i = int(np.argmax(suma / n + np.sqrt(2 * np.log(t) / n)))
        elif politica == "eps" and rng.random() < eps:
            i = int(rng.integers(medias.size))
        else:
            i = int(np.argmax(suma / n))                   # explota la media observada
        premio = 1.0 if rng.random() < medias[i] else 0.0
        n[i] += 1
        suma[i] += premio
        alfa[i] += premio
        beta[i] += 1.0 - premio
        acum += mejor - medias[i]
        reg[t] = acum
    return reg, n


politicas = [("codicioso", "greedy", TEXTO), ("épsilon = 0,1", "eps", ROJO),
             ("UCB1", "ucb", AZUL), ("Thompson", "thompson", VERDE)]
curvas = {}
for nombre, clave, _ in politicas:
    acumulada = np.zeros(T)
    for r in range(REPS):
        reg, _ = simula(clave, np.random.default_rng(1000 + r))
        acumulada += reg
    curvas[nombre] = acumulada / REPS

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.2))

# --- Panel izquierdo: el arrepentimiento son los premios que no ganas por no tirar del mejor.
for nombre, _, color in politicas:
    ejes[0].plot(np.arange(1, T + 1), curvas[nombre], color=color, linewidth=1.7, label=nombre)
anotar(ejes[0], f"el codicioso se deja\n{curvas['codicioso'][-1]:.0f} premios por el camino",
       xy=(1500, curvas["codicioso"][1499]), xytext=(0.28, 0.70), color=TEXTO)
anotar(ejes[0], "UCB y Thompson ya casi\nno se equivocan tras 500 tiros",
       xy=(900, curvas["UCB1"][899]), xytext=(0.34, 0.14), color=AZUL)
ejes[0].set_xlabel("tiradas acumuladas")
ejes[0].set_ylabel("arrepentimiento acumulado\n(premios que no ganas)")
ejes[0].legend(loc="upper left")
rejilla(ejes[0])
numeros(ejes[0])
titulo(ejes[0], "El codicioso paga un arrepentimiento lineal",
       f"media de {REPS} repeticiones, 5 brazos, {T} tiradas")

# --- Panel derecho: el bono de UCB no depende solo del brazo, también del tiempo.
nn = np.arange(1, 1201)
hueco = mejor - float(medias.min())
for t_ref, color in ((200, MORADO), (2000, AZUL)):
    ejes[1].plot(nn, np.sqrt(2 * np.log(t_ref) / nn), color=color, linewidth=1.8,
                 label=f"con {t_ref} tiradas acumuladas")
ejes[1].axhline(hueco, color=ROJO, linewidth=1.3, linestyle="--")
cruce = int(nn[np.argmax(np.sqrt(2 * np.log(2000) / nn) < hueco)])
anotar(ejes[1], f"a las {cruce} tiradas de ese brazo\nel bono ya no tapa el hueco",
       xy=(cruce, hueco), xytext=(0.38, 0.60), color=ROJO)
ejes[1].text(0.30, 0.06, f"el peor brazo está {hueco:.2f} por debajo del mejor",
             transform=ejes[1].transAxes, fontsize=8.5, color=TEXTO)
ejes[1].set_xlabel("veces que ya has tirado de ese brazo")
ejes[1].set_ylabel("bono que UCB le suma\na su media observada")
ejes[1].legend(loc="upper right")
rejilla(ejes[1])
numeros(ejes[1])
titulo(ejes[1], "El bono se encoge con cada tiro",
       "nadie decide explorar: lo hace el bono del brazo olvidado")

guardar(fig, "bandits-y-decision-secuencial-arrepentimiento")
