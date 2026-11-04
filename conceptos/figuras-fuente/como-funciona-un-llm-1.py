"""como-funciona-un-llm-1.py — la temperatura decide como de repartida sale la
probabilidad, y la ley de potencia decide cuanto se gana al crecer. pagina f08."""

import numpy as np

from comun import *

estilo()


def softmax(z, temperatura):
    """Misma cuenta que en la pagina: reparte los logits segun la temperatura."""
    z = np.asarray(z, dtype=float) / temperatura
    e = np.exp(z - z.max())
    return e / e.sum()


fig, ejes = plt.subplots(1, 2, figsize=(9.2, 4.0))

# --- Panel izquierdo: el mismo logit, tres temperaturas ---------------------
logits = np.array([2.0, 1.0, 0.1])
temperaturas = [0.5, 1.0, 2.0]
colores = [AZUL, MORADO, NARANJA]
barras = np.arange(3)
ancho = 0.26

for j, (t, color) in enumerate(zip(temperaturas, colores)):
    p = softmax(logits, t)
    pos = barras + (j - 1) * ancho
    ejes[0].bar(pos, p, width=ancho, color=color, label=f"T = {t:.1f}".replace(".", ","))

ejes[0].set_xticks(barras)
ejes[0].set_xticklabels(["logit 2,0", "logit 1,0", "logit 0,1"])
titulo(ejes[0], "La temperatura reparte la misma terna",
       "no cambia lo que el modelo sabe")
ejes[0].set_ylabel("probabilidad del token")
ejes[0].set_ylim(0, 1.05)
ejes[0].legend(loc="upper right")
# El hueco libre es el centro del panel, por encima de las barras bajas del tercer logit.
anotar(ejes[0], "con T alta la cola\ndeja de ser improbable",
       xy=(2.13, 0.20), xytext=(0.50, 0.42), color=NARANJA)
rejilla(ejes[0])
# Solo el eje y: el x lleva el nombre de cada logit y `numeros` lo borraría.
numeros(ejes[0], ejes="y")

# --- Panel derecho: la ley de potencia de la perdida ------------------------
n = np.logspace(8, 12, 120)
perdida = 2.5 * (n / 1e9) ** -0.05 + 1.6

ejes[1].semilogx(n, perdida, color=VERDE, linewidth=1.8)
ejes[1].axhline(1.6, color=ROJO, linewidth=1.2, linestyle="--")
ejes[1].set_ylim(1.45, 5.35)
for x in (1e8, 1e9, 1e10):
    centro = np.sqrt(x * 10 * x)          # punto medio del salto, en escala log
    y = 2.5 * (centro / 1e9) ** -0.05 + 1.6
    ejes[1].annotate("x10", xy=(centro, y), xytext=(centro, y + 0.22),
                     ha="center", fontsize=8, color=MORADO,
                     arrowprops=dict(arrowstyle="->", color=MORADO, linewidth=0.8))
titulo(ejes[1], "Cada salto de x10 baja menos",
       "la curva se aplana contra la pérdida irreducible")
# La banda entre la curva y el suelo está vacía: el texto va dentro, sin pisar la raya.
anotar(ejes[1], "suelo irreducible", xy=(1.2e8, 1.6), xytext=(0.03, 0.14), color=ROJO)
ejes[1].set_xlabel("parámetros N (escala logaritmica)")
ejes[1].set_ylabel("pérdida")
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "como-funciona-un-llm-temperatura-y-perdida")
