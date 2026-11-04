"""validacion-combinatoria-cpcv-1.py — todos los repartos posibles de bloques y la
dispersión de resultados que producen. Figura de la pagina de validación combinatoria (fase 9)."""

import numpy as np
from itertools import combinations

from comun import *

estilo()
azar = np.random.default_rng(0)

n_bloques, k, por_bloque = 6, 2, 120
combos = list(combinations(range(n_bloques), k))

# Una unica estrategia, exactamente la misma en todo el periodo: lo unico que cambia entre
# caminos es que bloques se usan para probar.
ret = azar.normal(0.0005, 0.01, size=n_bloques * por_bloque)
bloques = [ret[g * por_bloque:(g + 1) * por_bloque] for g in range(n_bloques)]


def sharpe_anual(x):
    return x.mean() / x.std(ddof=1) * np.sqrt(252)


srs = np.array([sharpe_anual(np.concatenate([bloques[g] for g in c])) for c in combos])
completo = sharpe_anual(ret)

fig, ejes = plt.subplots(2, 1, figsize=(7.2, 6.6))

# --- Arriba: el mapa de las C(6,2) = 15 formas de repartir ----------------------------
filas, columnas, colores = [], [], []
for j, c in enumerate(combos):
    for g in range(n_bloques):
        filas.append(j)
        columnas.append(g)
        colores.append(AZUL if g in c else REJILLA)
ejes[0].barh(filas, width=0.82, left=columnas, height=0.72, color=colores,
             alpha=0.9, edgecolor="none")
ejes[0].set_yticks(range(len(combos)))
ejes[0].set_yticklabels([f"({a + 1},{b + 1})" for a, b in combos], fontsize=7)
ejes[0].set_xticks(np.arange(n_bloques) + 0.41)
ejes[0].set_xticklabels([f"bloque {g + 1}" for g in range(n_bloques)], fontsize=8)
ejes[0].set_xlim(-0.1, n_bloques)
ejes[0].invert_yaxis()
titulo(ejes[0], "Las 15 formas de partir el histórico",
       "azul: los 2 bloques de prueba · gris: entrenamiento · se prueban todas, no la que más gusta")

# --- Abajo: la misma estrategia, 15 resultados distintos -------------------------------
ejes[1].hist(srs, bins=9, color=AZUL, alpha=0.75, edgecolor="none")
ejes[1].axvline(completo, color=ROJO, linewidth=1.6, linestyle="--")
ejes[1].axvline(srs.min(), color=MORADO, linewidth=1.2, linestyle=":")
ejes[1].axvline(srs.max(), color=MORADO, linewidth=1.2, linestyle=":")
ejes[1].set_ylim(0, 5.2)
ejes[1].set_xlabel("Sharpe anual de cada camino")
ejes[1].set_ylabel("nº de caminos")
titulo(ejes[1], f"La misma estrategia da de {srs.min():.2f} a {srs.max():.2f}".replace(".", ","),
       f"el recorrido de {srs.max() - srs.min():.2f} puntos no es habilidad: es dónde caen los cortes".replace(".", ","))
anotar(ejes[1], f"la serie completa: {completo:.2f}".replace(".", ","),
       xy=(completo, 3.0), xytext=(0.02, 0.90), color=ROJO)
anotar(ejes[1], "el peor y el mejor camino:\ndos veces el mismo backtest",
       xy=(srs.max(), 2.0), xytext=(0.98, 0.70), color=MORADO, align="right")
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "cpcv-caminos-y-dispersión")
