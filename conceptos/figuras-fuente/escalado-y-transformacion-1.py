"""escalado-y-transformacion-1.py — los mismos seis datos bajo cuatro escalados: lo
único que cambia es a quien aplasta el extremo. La figura de la pagina de escalado y
transformación (fase 5)."""

import numpy as np

from comun import *

estilo()

x = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 100.0])
cinco = x[:-1]
minmax = (x - x.min()) / (x.max() - x.min())
z = (x - x.mean()) / x.std(ddof=1)              # ddof=1: la desviacion muestral
robusto = (x - np.median(x)) / (np.percentile(x, 75) - np.percentile(x, 25))
log1p = np.log1p(x)

paneles = [
    (minmax, "Min-max: el extremo se come toda la escala",
     f"los cinco normales ocupan el {(minmax[4] - minmax[0]) * 100:.1f} % de la escala",
     "el 100 ocupa el 100 %"),
    (z, "Z-score: el extremo marca el paso",
     "cinco valores casi iguales y uno despegado",
     f"el 100 se queda en {z[-1]:+.2f}"),
    (robusto, "Robusto: el grupo respira, el extremo no",
     f"los cinco se reparten entre {robusto[0]:.1f} y {robusto[4]:.1f}",
     f"el 100 salta a {robusto[-1]:.1f}"),
    (log1p, "Logaritmo: no aplasta a nadie",
     f"los cinco se reparten entre {log1p[0]:.2f} y {log1p[4]:.2f}",
     f"el 100 solo llega a {log1p[-1]:.2f}"),
]

fig, ejes = plt.subplots(2, 2, figsize=(8.2, 5.2), sharex=True, sharey=True)

for indice, (valores, corto, subtitulo, nota) in enumerate(paneles):
    ax = ejes[indice // 2, indice % 2]
    normalizado = (valores - valores.min()) / (valores.max() - valores.min())
    ax.bar([10.0], [1.0], width=6.0, color=REJILLA, alpha=0.45)
    ax.scatter(normalizado[:-1], np.zeros(5), s=95, color=AZUL, zorder=3)
    ax.scatter(normalizado[-1], 0.0, s=110, color=ROJO, zorder=3)
    ax.axvline(1.0, color=ROJO, linewidth=1.1, linestyle="--")
    ax.set_xlim(-0.06, 1.06)
    ax.set_ylim(0, 2.2)
    ax.set_yticks([])
    anotar(ax, nota, (normalizado[-1], 0.0), (0.90, 0.80), color=ROJO, align="right")
    ax.text(0.04, 0.56, subtitulo, transform=ax.transAxes, fontsize=8.5, color=TEXTO,
            va="center", ha="left")
    titulo(ax, corto, "los seis valores del ejemplo, en su escala")
    numeros(ax, ejes="x")

ejes[0, 0].annotate("la barra gris es el extremo:\naqui ocupa todo el rango",
                    xy=(0.62, 0.75), xycoords="data", xytext=(0.03, 0.28),
                    textcoords="axes fraction", fontsize=8.5, color=REJILLA, va="center",
                    arrowprops=dict(arrowstyle="->", color=REJILLA, linewidth=0.9,
                                    shrinkA=2, shrinkB=2))
ejes[1, 1].annotate("las distancias entre valores\nsiguen teniendo sentido",
                    xy=(log1p[3] / log1p.max(), 0.0), xycoords="data", xytext=(0.30, 0.32),
                    textcoords="axes fraction", fontsize=8.5, color=VERDE, va="center",
                    arrowprops=dict(arrowstyle="->", color=VERDE, linewidth=0.9,
                                    shrinkA=2, shrinkB=2))
for ax in ejes[1]:
    ax.set_xlabel("valor escalado (0 a 1 para poder comparar)")

guardar(fig, "escalado-a-quien-aplasta-cada-metodo")
