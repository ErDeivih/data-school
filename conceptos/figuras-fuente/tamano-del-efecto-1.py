"""tamano-del-efecto-1.py — el mismo efecto estimado con dos muestras muy distintas y el
p-valor bajando solo porque crece n. Efecto real d = 0,55. Figura de la página del tamaño
del efecto."""

import numpy as np
from scipy import stats

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.1))

# --- Izquierda: la d estimada con 8 personas por grupo y con 200, mismo efecto real.
azar = np.random.default_rng(3)
filas = []
for n in (8, 200):
    a = azar.normal(0.55, 1.0, n)
    b = azar.normal(0.00, 1.0, n)
    sp = np.sqrt(((n - 1) * a.var(ddof=1) + (n - 1) * b.var(ddof=1)) / (2 * n - 2))
    d = (a.mean() - b.mean()) / sp
    ee = np.sqrt(1 / n + 1 / n + d**2 / (2 * 2 * n))
    filas.append((n, d, 1.96 * ee))

alto = [0.0, 1.0]
colores = [ROJO, VERDE]
for (n, d, margen), y, color in zip(filas, alto, colores):
    ejes[0].plot([d - margen, d + margen], [y, y], color=color, linewidth=2.6)
    ejes[0].plot([d], [y], "o", color=color, markersize=8, zorder=3)
    ejes[0].text(d + margen + 0.06, y, f"n = {n} por grupo: d = {d:+.2f}", fontsize=9,
                 color=color, va="center")
ejes[0].axvline(0, color=TEXTO, linewidth=1.2)
ejes[0].axvline(0.55, color=AZUL, linewidth=1.2, linestyle="--")
anotar(ejes[0], "sin efecto", xy=(0.0, 0.72), xytext=(0.02, 0.86), color=TEXTO)
anotar(ejes[0], "el efecto real, 0,55", xy=(0.55, 0.32), xytext=(0.24, 0.46), color=AZUL)
ejes[0].text(0.03, 0.10, "con 8 personas la estimación baila y el intervalo cruza el cero:\n"
             "no puedes descartar que no haya efecto",
             transform=ejes[0].transAxes, fontsize=8.5, color=ROJO)
ejes[0].set_xlabel("d de Cohen estimada")
ejes[0].set_ylim(-0.7, 1.7)
ejes[0].set_yticks([])
ejes[0].set_xlim(-1.35, 2.15)
titulo(ejes[0], "El mismo efecto estimado con dos muestras",
       "la d no cambia por tener más datos: lo que cambia es cuánto la conoces")
rejilla(ejes[0], eje="x")
numeros(ejes[0], ejes="x")

# --- Derecha: el p-valor baja al crecer n aunque el efecto sea el mismo.
grupos = np.arange(4, 320)
p = 2 * stats.t.sf(np.abs(0.55 * np.sqrt(grupos / 2)), 2 * grupos - 2)
p_pequeno = 2 * stats.t.sf(np.abs(0.20 * np.sqrt(grupos / 2)), 2 * grupos - 2)
ejes[1].plot(grupos, p, color=AZUL, linewidth=1.8, label="d = 0,55")
ejes[1].plot(grupos, p_pequeno, color=MORADO, linewidth=1.6, linestyle="--",
             label="d = 0,20: mismo umbral, n ≈ 193")
ejes[1].axhline(0.05, color=ROJO, linewidth=1.2, linestyle="--")
ejes[1].axvline(27, color=ROJO, linewidth=1.1, linestyle=":")
ejes[1].plot([27], [0.05], "o", color=ROJO, markersize=7, zorder=3)
ejes[1].plot([193], [0.05], "o", color=MORADO, markersize=7, zorder=3)
anotar(ejes[1], "con d = 0,55 el umbral del 5 %\nse cruza en n ≈ 27", xy=(27, 0.05),
       xytext=(0.06, 0.78), color=ROJO)
anotar(ejes[1], "con un efecto más pequeño (d = 0,20)\nhacen falta siete veces más datos",
       xy=(193, 0.05), xytext=(0.40, 0.30), color=MORADO)
ejes[1].set_xlabel("observaciones por grupo (n)")
ejes[1].set_ylabel("p-valor del contraste")
ejes[1].set_xlim(0, 330)
ejes[1].set_ylim(0, 1.05)
ejes[1].legend(loc="upper right")
titulo(ejes[1], "El p-valor baja con n aunque el efecto no cambie",
       "la d no cambia en ningún punto del eje: solo cambia cuántos datos hay")
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "efecto-mismo-d-distinta-muestra")
