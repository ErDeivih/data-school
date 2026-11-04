"""cointegracion-1.py — dos series que divagan juntas no estan atadas, y la resta lo delata.

Arriba, dos pares con el mismo aspecto: en los dos casos las lineas se mueven juntas y la
regresión de niveles da un R2 respetable. Abajo, la resta ponderada de cada par: la del par
independiente se instala lejos de cero y no vuelve (su residuo tiene raiz unitaria), mientras la
del par cointegrado oscila alrededor de una media constante. La correlación se mira arriba; la
cointegración, abajo.
"""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)
n = 250

# --- Par A: dos paseos aleatorios INDEPENDIENTES. Se parecen, y se separan para siempre.
xa = np.cumsum(azar.normal(0, 1, n)) + 100
ya = np.cumsum(azar.normal(0, 1, n)) + 100
ba, aa = np.polyfit(xa, ya, 1)
res_a = ya - (aa + ba * xa)
r2_a = np.corrcoef(xa, ya)[0, 1] ** 2

# --- Par B: mismo aspecto, pero y esta atada a x: el desvio es estacionario (AR(1) con phi 0,85).
z = np.zeros(n)
for t in range(1, n):
    z[t] = 0.85 * z[t - 1] + azar.normal(0, 0.5)
xb = np.cumsum(azar.normal(0, 1, n)) + 300
yb = 2.0 * xb + 5 + z
bb = np.polyfit(xb, yb, 1)[0]
res_b = yb - (np.polyfit(xb, yb, 1)[1] + bb * xb)
vida_media = -np.log(2) / np.log(0.85)

fig, ejes = plt.subplots(2, 1, figsize=(7.4, 6.2), sharex=True)

# --- Arriba: los dos pares, el mismo dibujo -------------------------------------------------
ejes[0].plot(xa, color=AZUL, linewidth=1.6)
ejes[0].plot(ya, color=CIAN, linewidth=1.3, alpha=0.85)
ejes[0].plot(xb, color=ROJO, linewidth=1.4)
ejes[0].plot(yb, color=NARANJA, linewidth=1.3, linestyle="--")
ejes[0].text(0.02, 0.80, f"par independiente (azul y cian): R² = {r2_a:.2f} y β = {ba:.2f}",
             transform=ejes[0].transAxes, color=CIAN, fontsize=8.5)
ejes[0].text(0.32, 0.50, f"par cointegrado (rojo y naranja): R² = {r2_a:.2f} y β = {bb:.2f}",
             transform=ejes[0].transAxes, color=NARANJA, fontsize=8.5)
ejes[0].set_ylim(0, 660)
titulo(ejes[0], "Los dos pares «van juntos» y la recta ajusta en los dos",
       "los dos pares están separados en el eje solo para poder dibujarlos juntos")
ejes[0].set_ylabel("nivel")
rejilla(ejes[0])
numeros(ejes[0])

# --- Abajo: la resta, que es lo unico que distingue un caso del otro -------------------------
ejes[1].axhline(0, color=TEXTO, linewidth=0.9)
ejes[1].plot(res_a, color=CIAN, linewidth=1.5)
ejes[1].plot(res_b, color=ROJO, linewidth=1.5)
ejes[1].text(0.02, 0.04, "residuo del par independiente: raíz unitaria, se va y no vuelve",
             transform=ejes[1].transAxes, color=CIAN, fontsize=8.5)
ejes[1].text(0.02, 0.26, "residuo del par cointegrado: oscila alrededor de cero y vuelve",
             transform=ejes[1].transAxes, color=ROJO, fontsize=8.5)
titulo(ejes[1], "La resta y − α̂ − β̂·x es lo que decide",
       "solo el residuo del par cointegrado se comporta como una serie estable")
ejes[1].set_xlabel("día")
ejes[1].set_ylabel("diferencial")
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "cointegracion-diferencial-estacionario")
