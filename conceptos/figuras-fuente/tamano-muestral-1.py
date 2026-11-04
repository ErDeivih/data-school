"""tamano-muestral-1.py - el efecto que quieres detectar manda, y el diseno lo encarece.

Izquierda: unidades por grupo segun el efecto estandarizado d = delta/sigma, con sigma = 11,2 s del
ejemplo del portal. Los tres puntos son los tres del ejemplo: 6,2 / 3,1 / 1,55 segundos, que son
d = 0,554 / 0,277 / 0,138, y cada uno cuesta el cuadruple que el anterior.
Derecha: el efecto de diseno 1 + (m-1)*rho que se aplica cuando las unidades van en conglomerados:
el mismo estudio, con tiendas de 20 usuarios y rho = 0,05, necesita casi el doble de gente.
"""

import numpy as np
from scipy import stats

from comun import *

estilo()

sigma, alfa, potencia = 11.2, 0.05, 0.80
z_a = stats.norm.ppf(1 - alfa / 2)
z_b = stats.norm.ppf(potencia)


def n_por_grupo(d):
    """Formula del portal con sigma^2 / delta^2 = 1 / d^2."""
    return 2 * (z_a + z_b) ** 2 / np.asarray(d, float) ** 2


fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.4))

# ═══ Izquierda: la mitad de efecto, el cuadruple de muestra ═══
ax = ejes[0]
d = np.linspace(0.10, 1.0, 400)
ax.plot(d, n_por_grupo(d), color=AZUL, linewidth=2.0)
ax.set_yscale("log")
deltas = np.array([1.55, 3.1, 6.2])          # de menor a mayor: el orden natural de la curva
ds = deltas / sigma
ns = n_por_grupo(ds)
ax.plot(ds, ns, color=ROJO, linewidth=0, marker="o", markersize=6)
for d_punto, n_punto, texto in zip(ds, ns, ["1,55 s", "3,1 s", "6,2 s"]):
    ax.annotate(texto, xy=(float(d_punto), float(n_punto)), xytext=(9, 0),
                textcoords="offset points", fontsize=8.5, color=ROJO, va="center")
ax.annotate("cada vez que partes el efecto por\ndos, la muestra se multiplica por 4:\n821 → 206 → 52 por grupo",
            xy=(float(ds[1]), float(ns[1])), xytext=(0.06, 0.76), textcoords="axes fraction",
            fontsize=8.5, color=TEXTO,
            arrowprops=dict(arrowstyle="->", color=TEXTO, linewidth=0.9))
ax.annotate("con 52 por grupo, el efecto\nde 1,55 s es invisible",
            xy=(float(ds[0]), float(ns[0])), xytext=(0.14, 0.28), textcoords="axes fraction",
            fontsize=8.5, color=NARANJA,
            arrowprops=dict(arrowstyle="->", color=NARANJA, linewidth=0.9))
ax.set_xlabel("efecto estandarizado d = δ / σ")
ax.set_ylabel("unidades por grupo (escala logarítmica)")
titulo(ax, "El tamaño muestral va con el cuadrado del efecto",
       "desviación típica 11,2 s, α = 0,05 y potencia del 80 %")
rejilla(ax)

# ═══ Derecha: el precio de asignar por conglomerados ═══
ax = ejes[1]
m = np.linspace(1, 60, 400)
ax.plot(m, 1 + (m - 1) * 0.05, color=MORADO, linewidth=1.6, label="ρ = 0,05")
ax.plot(m, 1 + (m - 1) * 0.10, color=CIAN, linewidth=1.6, label="ρ = 0,10")
ax.plot(m, 1 + (m - 1) * 0.02, color=VERDE, linewidth=1.6, label="ρ = 0,02")
ax.axhline(1.0, color=TEXTO, linewidth=1.1, linestyle=":")
ax.text(36, 1.10, "1,0: unidades independientes", color=TEXTO, fontsize=8.5)
ax.scatter([20], [1.95], s=70, color=ROJO, zorder=4)
ax.annotate("con tiendas de 20 usuarios y ρ = 0,05\nel DEFF es 1,95: 53 por grupo pasan a 103",
            xy=(20, 1.95), xytext=(0.30, 0.63), textcoords="axes fraction", fontsize=8.5,
            color=ROJO, arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9))
ax.set_xlabel("unidades por conglomerado, m")
ax.set_ylabel("efecto de diseño: multiplica la muestra")
ax.legend(loc="upper left", title="correlación intraclase", title_fontsize=8.5)
titulo(ax, "Los conglomerados cuestan casi el doble de muestra",
       "DEFF = 1 + (m − 1)·ρ es lo que hay que multiplicar al cálculo limpio")
rejilla(ax)

guardar(fig, "tamano-muestral-curva-y-conglomerados")
