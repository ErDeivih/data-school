"""anova-1.py - por qué el ANOVA compara dos variabilidades en vez de restar medias.

Izquierda: los tres metodos del ejemplo del portal. Las flechas rojas miden lo que se separan las
medias de grupo de la media general (SS_entre); las lineas grises, lo que se dispersa cada grupo
por dentro (SS_dentro). El estadístico F es el cociente de las dos, corregido por sus grados de
libertad.
Derecha: cuantas veces sale un falso positivo mirando los tres pares en vez de un solo ANOVA,
contado sobre 12000 experimentos simulados en los que NO hay ninguna diferencia entre grupos.
"""

import numpy as np
from scipy import stats

from comun import *

estilo()
azar = np.random.default_rng(7)

# --- Los tres metodos del ejemplo: cinco medidas de tiempo cada uno.
grupos = {"A": np.array([12., 14, 13, 15, 16]),
          "B": np.array([10., 11, 12, 9, 13]),
          "C": np.array([14., 16, 15, 13, 17])}
colores = {"A": AZUL, "B": NARANJA, "C": MORADO}
todas = np.concatenate(list(grupos.values()))
media_general = todas.mean()
ss_entre = sum(g.size * (g.mean() - media_general) ** 2 for g in grupos.values())
ss_dentro = sum(((g - g.mean()) ** 2).sum() for g in grupos.values())
gl_entre, gl_dentro = len(grupos) - 1, todas.size - len(grupos)
f_obs = (ss_entre / gl_entre) / (ss_dentro / gl_dentro)

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.4))

# ═══ Izquierda: las dos variabilidades, dibujadas ═══
ax = ejes[0]
for k, (nombre, g) in enumerate(grupos.items()):
    ax.scatter(np.full(g.size, k) + azar.uniform(-0.10, 0.10, g.size), g, s=26,
               color=colores[nombre], zorder=3)
    ax.hlines(g.mean(), k - 0.28, k + 0.28, color=colores[nombre], linewidth=2.4, zorder=4)
    # Lo de dentro: cada punto y su distancia a la media de su propio grupo.
    for valor in g:
        ax.annotate("", xy=(k + 0.33, valor), xytext=(k + 0.33, g.mean()),
                    arrowprops=dict(arrowstyle="-", color=REJILLA, linewidth=1.0,
                                    linestyle=(0, (2, 2))))
ax.axhline(media_general, color=ROJO, linewidth=1.6, linestyle="--", zorder=2)
for k, g in enumerate(grupos.values()):
    ax.annotate("", xy=(k - 0.45, g.mean()), xytext=(k - 0.45, media_general),
                arrowprops=dict(arrowstyle="<->", color=ROJO, linewidth=1.4))
ax.set_xticks(np.arange(3), labels=[f"método {n}\nmedia {g.mean():.0f} s"
                                    for n, g in grupos.items()])
ax.set_ylabel("tiempo de empaquetado (s)")
ax.set_xlim(-0.80, 2.80)
ax.set_ylim(8.2, 18.6)
ax.annotate("media general, 13,3 s", xy=(2.44, media_general), xytext=(1.30, media_general + 1.6),
            color=ROJO, fontsize=8.5,
            arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9))
anotar(ax, "flechas rojas: lo que se separan las medias\n(SS_entre = 43,3).  Líneas grises: lo que\nse dispersa cada grupo (SS_dentro = 30,0)",
       (0.35, media_general), (0.60, 0.04), color=TEXTO)
titulo(ax, "F compara la separación de las medias con el ruido de dentro")

# ═══ Derecha: el precio de mirar los pares ═══
ax = ejes[1]
reps, n = 12000, 20
x = azar.normal(0, 1, (reps, 3, n))                  # los tres grupos son el MISMO grupo
media, var = x.mean(axis=2), x.var(axis=2, ddof=1)


def p_welch(i, j):
    """p-valor del t-test de Welch entre los grupos simulados i y j, todo vectorizado."""
    ee2 = var[:, i] / n + var[:, j] / n
    t = (media[:, i] - media[:, j]) / np.sqrt(ee2)
    gl = ee2 ** 2 / ((var[:, i] / n) ** 2 / (n - 1) + (var[:, j] / n) ** 2 / (n - 1))
    return 2 * stats.t.sf(np.abs(t), gl)


pares = np.array([p_welch(0, 1), p_welch(0, 2), p_welch(1, 2)])
tasa_pares = float((pares.min(axis=0) < 0.05).mean())
f_sim = stats.f_oneway(x[:, 0, :], x[:, 1, :], x[:, 2, :]).statistic
tasa_anova = float((stats.f.sf(f_sim, 2, 3 * n - 3) < 0.05).mean())

ax.bar([0, 1], [tasa_pares, tasa_anova], width=0.5, color=[ROJO, AZUL])
ax.axhline(0.05, color=TEXTO, linewidth=1.4, linestyle="--")
ax.text(0.06, 0.055, "el 5 % que prometes", color=TEXTO, fontsize=8.5, va="bottom")
for k, valor in enumerate([tasa_pares, tasa_anova]):
    ax.text(k, valor + 0.006, f"{valor:.3f}".replace(".", ","), ha="center", fontsize=11,
            color=TEXTO)
ax.set_xticks([0, 1], labels=["peor de los 3 t-tests", "un solo ANOVA"])
ax.set_ylabel("proporción con algún falso positivo")
ax.set_ylim(0, tasa_pares * 1.40)
titulo(ax, "Mirar los pares multiplica por casi tres el falso positivo",
       "12000 experimentos simulados en los que las tres medias son idénticas")
rejilla(ax)
numeros(ax, ejes="y")

guardar(fig, "anova-entre-dentro-y-precio-de-los-pares")
