"""preentrenamiento-y-escalado-1.py — de que esta hecha la pérdida y cuanto se gana
al escalar el modelo. La figura de la pagina de preentrenamiento (fase 8)."""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(9.2, 3.8))

# --- Panel izquierdo: la perdida no baja a cero, baja a L_inf -----------------
n = np.logspace(8, 12, 200)
L_inf, a, alfa = 1.6, 2.5, 0.05
perdida = L_inf + a * (n / 1e9) ** -alfa

ejes[0].fill_between(n, L_inf, perdida, color=AZUL, alpha=0.18)
ejes[0].plot(n, perdida, color=AZUL, linewidth=1.8)
ejes[0].axhline(L_inf, color=ROJO, linewidth=1.4, linestyle="--")
ejes[0].set_xscale("log")
# Los dos rotulos van en coordenadas del eje (0-1): en coordenadas de datos el de la
# pérdida irreducible caia encima de la linea roja.
anotar(ejes[0], "pérdida irreducible: ni con N infinito", xy=(1e12, L_inf),
       xytext=(0.24, 0.13), color=ROJO)
anotar(ejes[0], "lo que aporta tener más parámetros", xy=(1e10, 3.83),
       xytext=(0.30, 0.45), color=AZUL)
ejes[0].set_xlabel("parámetros N (escala logaritmica)")
ejes[0].set_ylabel("pérdida")
ejes[0].set_ylim(1.4, 4.7)
titulo(ejes[0], "El suelo de la pérdida no es cero",
       "es L infinito, y se alcanza antes de lo que parece")
rejilla(ejes[0])
numeros(ejes[0])

# --- Panel derecho: cuanto baja la perdida en cada salto de x10 ---------------
saltos = [1e8, 1e9, 1e10]
etiquetas = ["1e8 -> 1e9", "1e9 -> 1e10", "1e10 -> 1e11"]


def L(x):
    return L_inf + a * (x / 1e9) ** -alfa


bajadas = [L(x) - L(10 * x) for x in saltos]
pos = np.arange(3)

ejes[1].bar(pos, bajadas, width=0.55, color=[AZUL, MORADO, NARANJA])
for i, b in enumerate(bajadas):
    ejes[1].text(i, b + 0.006, f"{b:.4f}".replace(".", ","), ha="center", fontsize=8)
ejes[1].set_xticks(pos)
ejes[1].set_xticklabels(etiquetas, fontsize=8)
ejes[1].set_ylabel("lo que baja la pérdida")
ejes[1].set_ylim(0, max(bajadas) * 1.45)
ejes[1].set_yticks([0.00, 0.10, 0.20, 0.30])
# El aviso va en la franja vacia de arriba: pegado al eje se comia el titulo, y la flecha
# entra por el lado izquierdo de la barra para no tocar la etiqueta del valor.
anotar(ejes[1], "el mismo factor de escala,\ncada vez menos pérdida ganada",
       xy=(0.70, bajadas[1]), xytext=(0.28, 0.86), color=MORADO)
titulo(ejes[1], "Cada salto rinde menos que el anterior",
       "por eso el reparto se decide con una curva")
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "preentrenamiento-suelo-y-retorno-decreciente")
