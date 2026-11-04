"""seguimiento-de-experimentos-1.py — por qué una sola semilla no decide nada y cuantas hacen
falta. La figura de seguimiento de experimentos (fase 7)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

epocas = np.arange(1, 41)


def familia(final, ruido):
    """Cinco curvas de validación que acaban en el mismo sitio con distinta semilla."""
    curvas = []
    for _ in range(5):
        base = final - 0.03 * np.exp(-epocas / 7.0)
        curvas.append(base + azar.normal(0, ruido, epocas.size))
    return np.array(curvas)


A = familia(0.845, 0.004)      # configuracion lr-1e-3
B = familia(0.853, 0.003)      # configuracion lr-3e-4

fig, ejes = plt.subplots(1, 2, figsize=(8.4, 3.9))

# --- Izquierda: las dos configuraciones se solapan, asi que una sola semilla no decide ---
ax = ejes[0]
for datos, color, nombre in ((A, AZUL, "lr-1e-3"), (B, ROJO, "lr-3e-4")):
    media = datos.mean(axis=0)
    desv = datos.std(axis=0, ddof=1)
    ax.plot(epocas, media, color=color, linewidth=1.8, label=nombre)
    ax.fill_between(epocas, media - 2 * desv, media + 2 * desv, color=color, alpha=0.16,
                    linewidth=0)
ax.set_xlim(1, 40)
ax.set_ylim(0.80, 0.90)
ax.set_xlabel("época")
ax.set_ylabel("exactitud de validación")
ax.legend(loc="lower right", fontsize=8.5)
anotar(ax, "las bandas se solapan: una sola semilla\nde cada una no decide nada",
       (40, 0.850), (0.03, 0.84), color=TEXTO)
titulo(ax, "Dos configuraciones que se solapan", "cinco semillas por configuración, media y banda")
rejilla(ax)
numeros(ax, ejes="y")

# --- Derecha: el presupuesto de semillas crece con el cuadrado del ruido ---
ax = ejes[1]
delta = np.linspace(0.002, 0.020, 400)
for s, color, nombre in ((0.0045, AZUL, "dispersión 0,0045"), (0.009, NARANJA, "dispersión 0,009")):
    ax.plot(delta * 100, 8 * (s / delta) ** 2, color=color, linewidth=1.9, label=nombre)
ax.set_yscale("log")
ax.set_xlim(0.2, 2.0)
ax.set_ylim(1, 1000)
ax.set_xlabel("mejora que quieres detectar (puntos de exactitud)")
ax.set_ylabel("semillas por configuración")
ax.legend(loc="upper right", fontsize=8.5)
ax.axhline(5, color=REJILLA, linewidth=1.1, linestyle="--")
anotar(ax, "con la dispersión al doble,\nel presupuesto se multiplica por cuatro",
       (0.4, 41), (0.97, 0.55), color=NARANJA, align="right")
anotar(ax, "cinco semillas solo bastan\npara efectos grandes",
       (1.0, 5), (0.03, 0.72), color=TEXTO, flecha=False)
titulo(ax, "Semillas necesarias según el ruido", "para declarar una mejora con dos errores típicos")
rejilla(ax)
numeros(ax, ejes="x")

guardar(fig, "seguimiento-solape-y-semillas")
