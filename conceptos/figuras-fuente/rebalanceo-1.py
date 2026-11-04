"""rebalanceo-1.py — cuánto se desvía una cartera 60/40 y cuándo merece la pena tocarla.

Izquierda: la historia de una sola cartera 60/40 a lo largo de cinco años. En azul, el peso de la
bolsa si no se toca nada: se va solo, sin que nadie decida nada. En naranja, la misma cartera con
una banda de 5 puntos: solo se opera cuando el desvío cruza la banda, y cada operación devuelve el
peso al objetivo (los puntos marcan las veces que se operó).
Derecha: cuántos rebalanceos hacen falta según el ancho de la banda, en escala logarítmica. La
referencia punteada baja con pendiente −2: doblar la banda no tarda el doble en cruzarse, tarda
unas cuatro veces más.
La figura de la página de rebalanceo (fase 9).
"""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

n_caminos, n_meses = 200, 60
# Retornos mensuales: bolsa en torno al 0,8 % con mucha dispersión, bonos en torno al 0,2 %.
r_bolsa = azar.normal(0.008, 0.045, size=(n_caminos, n_meses))
r_bonos = azar.normal(0.002, 0.006, size=(n_caminos, n_meses))
OBJETIVO, COSTE = 0.60, 0.001        # 60 % en bolsa, 10 puntos básicos por unidad negociada


def recorrer(umbral, r_bol, r_bon):
    """Devuelve (rebalanceos, coste, valor final, serie de pesos, meses en que se operó).

    Con umbral = 1 nunca se cruza la banda: esa es la política de no tocar nada.
    """
    v_bol = np.full(r_bol.shape[0], 60000.0)
    v_bon = np.full(r_bol.shape[0], 40000.0)
    ops = np.zeros(r_bol.shape[0])
    pagado = np.zeros(r_bol.shape[0])
    pesos = [np.full(r_bol.shape[0], OBJETIVO)]
    toca_serie = []
    for t in range(r_bol.shape[1]):
        v_bol *= 1 + r_bol[:, t]
        v_bon *= 1 + r_bon[:, t]
        total = v_bol + v_bon
        toca = np.abs(v_bol / total - OBJETIVO) >= umbral
        negociado = np.abs(OBJETIVO * total - v_bol) * toca
        total = total - negociado * COSTE          # el coste sale de la cartera
        v_bol = np.where(toca, OBJETIVO * total, v_bol)
        v_bon = np.where(toca, (1 - OBJETIVO) * total, v_bon)
        ops += toca
        pagado += negociado * COSTE
        pesos.append(v_bol / (v_bol + v_bon))
        toca_serie.append(toca)
    return ops, pagado, v_bol + v_bon, np.array(pesos), np.array(toca_serie)


fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.5))

# --- Izquierda: una cartera concreta, con banda y sin ella ----------------------------
ax = ejes[0]
meses = np.arange(n_meses + 1)
_, _, _, peso_quieta, _ = recorrer(1.0, r_bolsa[:1], r_bonos[:1])
ops_banda, _, _, peso_banda, toca_banda = recorrer(0.05, r_bolsa[:1], r_bonos[:1])
cuando = np.flatnonzero(toca_banda[:, 0]) + 1

ax.axhspan(0.55, 0.65, color=REJILLA, alpha=0.18, zorder=0)
ax.axhline(OBJETIVO, color=TEXTO, linewidth=1.0, linestyle=":", zorder=1)
ax.axhline(0.55, color=ROJO, linewidth=1.1, linestyle="--", zorder=2)
ax.axhline(0.65, color=ROJO, linewidth=1.1, linestyle="--", zorder=2)
ax.plot(meses, peso_quieta[:, 0], color=AZUL, linewidth=2.0, zorder=3)
ax.plot(meses, peso_banda[:, 0], color=NARANJA, linewidth=1.8, zorder=4)
ax.plot(cuando, peso_banda[cuando, 0], "o", color=NARANJA, markersize=6, zorder=5)
anotar(ax, f"sin tocarla, el peso se va solo:\nacaba en el {peso_quieta[-1, 0]:.0%}"
       .replace(".", ","),
       xy=(n_meses, float(peso_quieta[-1, 0])), xytext=(0.98, 0.93), color=AZUL,
       align="right", flecha=False)
anotar(ax, f"solo se opera al cruzar la banda:\n{int(ops_banda[0])} veces en cinco años",
       xy=(float(cuando[0]), OBJETIVO), xytext=(0.02, 0.93), color=NARANJA)
titulo(ax, "Sin rebalancear, el riesgo lo decide el mercado",
       "peso de la bolsa en una cartera 60/40 a lo largo de cinco años")
ax.set_xlabel("meses")
ax.set_ylabel("peso de la bolsa")
ax.set_ylim(0.44, 0.78)
ax.set_xlim(0, n_meses + 1)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{v:.0%}"))
rejilla(ax)

# --- Derecha: cuántas veces hay que operar según el ancho de la banda -----------------
ax = ejes[1]
bandas = np.array([0.01, 0.015, 0.02, 0.03, 0.05, 0.07, 0.10, 0.15])
media_ops = np.array([recorrer(b, r_bolsa, r_bonos)[0].mean() for b in bandas])
# Referencia de pendiente −2: el tiempo hasta cruzar la banda crece con su cuadrado.
referencia = media_ops[0] * (bandas[0] / bandas) ** 2

ax.loglog(bandas * 100, media_ops, color=AZUL, linewidth=2.0, marker="o", markersize=6,
          zorder=4)
ax.loglog(bandas * 100, referencia, color=ROJO, linewidth=1.4, linestyle="--", zorder=3)
anotar(ax, "la línea de puntos es la referencia 1/b²:\ndoblar la banda tarda cuatro veces más",
       xy=(10.0, float(referencia[-3])), xytext=(0.98, 0.93), color=ROJO, align="right",
       flecha=False)
anotar(ax, f"de 1 a 5 puntos se pasa de {media_ops[0]:.0f}\nrebalanceos a {media_ops[4]:.0f} "
       "en cinco años",
       xy=(1.0, float(media_ops[0])), xytext=(0.03, 0.14), color=AZUL)
titulo(ax, "Cuanto más ancha la banda, menos se opera",
       "rebalanceos en cinco años, media de 200 carteras simuladas")
ax.set_xlabel("ancho de la banda (puntos porcentuales)")
ax.set_ylabel("rebalanceos en cinco años")
ax.set_xticks([1, 2, 5, 10, 15])
ax.set_xticklabels(["1", "2", "5", "10", "15"])
ax.set_yticks([0.2, 1, 5, 20])
ax.set_yticklabels(["0,2", "1", "5", "20"])
ax.set_ylim(0.12, 45)
ax.set_xlim(0.8, 20)
rejilla(ax, eje="both")

guardar(fig, "rebalanceo-deriva-y-bandas")
