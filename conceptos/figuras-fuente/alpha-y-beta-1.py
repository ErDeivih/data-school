"""alpha-y-beta-1.py — dos carteras, el mismo 30 % y 12 %, y quien aporto algo.

Izquierda: la nube de cada cartera contra el mercado, con su recta. La pendiente es la beta; la
altura a la que cada recta corta al eje vertical es el alpha, y es el único trozo del resultado
que no es mercado. Derecha: una estrategia construida con beta 2 y alpha cero de verdad, al lado
de lo que se puede comprar para conseguir lo mismo: un ETF apalancado.
"""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# --- Izquierda: las dos carteras del ejemplo de la pagina ----------------------------------
mercado = np.array([2.0, -1.0, 3.0, 0.0, 1.0, -2.0, 2.5, 0.5, -1.5, 1.0])   # % en exceso
cartera_a = 1.5 * mercado + np.array([0.1, -0.2, 0.3, 0.0, -0.1, 0.2, -0.3, 0.1, 0.2, -0.3])
cartera_b = 0.5 * mercado + 2.0 + np.array([-0.3, 0.4, -0.2, 0.3, -0.4, 0.2, 0.3, -0.3, 0.4, -0.4])

beta_a, alpha_a = np.polyfit(mercado, cartera_a, 1)
beta_b, alpha_b = np.polyfit(mercado, cartera_b, 1)

fig, ejes = plt.subplots(1, 2, figsize=(9.8, 4.4), width_ratios=[1.25, 1.0])

recta = np.linspace(-2.4, 3.2, 40)
ejes[0].axhline(0, color=REJILLA, linewidth=0.9)
ejes[0].axvline(0, color=REJILLA, linewidth=0.9)
ejes[0].plot(recta, alpha_a + beta_a * recta, color=AZUL, linewidth=1.9)
ejes[0].plot(recta, alpha_b + beta_b * recta, color=VERDE, linewidth=1.9)
ejes[0].plot(mercado, cartera_a, "o", color=AZUL, markersize=6)
ejes[0].plot(mercado, cartera_b, "o", color=VERDE, markersize=6)
ejes[0].plot([0], [alpha_a], "o", color=AZUL, markersize=7, zorder=3)
ejes[0].plot([0], [alpha_b], "o", color=VERDE, markersize=7, zorder=3)

# El alpha es la distancia vertical entre las dos rectas en x = 0.
ejes[0].annotate("", xy=(0.0, alpha_b), xytext=(0.0, alpha_a),
                 arrowprops=dict(arrowstyle="<->", color=ROJO, linewidth=1.4))
ejes[0].text(0.10, (alpha_a + alpha_b) / 2 + 0.25,
             "el alpha vive aquí: la distancia vertical\nentre las dos rectas en el mercado = 0",
             color=ROJO, fontsize=8.5, va="center")
anotar(ejes[0], f"pendiente {beta_a:.2f}: solo acompaña al mercado,\nsu valor en el cero es 0",
       xy=(2.6, alpha_a + beta_a * 2.6), xytext=(0.03, 0.04), color=AZUL)
ejes[0].text(0.03, 0.38, f"pendiente {beta_b:.2f}: se mueve la mitad,\npero arranca {alpha_b:.2f} puntos por encima",
             transform=ejes[0].transAxes, color=VERDE, fontsize=8.5)
titulo(ejes[0], "La misma nube, dos historias distintas",
       "la pendiente es la beta; la altura en el cero es el alpha")
ejes[0].set_xlabel("exceso de retorno del mercado, en % mensual")
ejes[0].set_ylabel("exceso de retorno de la cartera, en %")
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="both")

# --- Derecha: una estrategia con beta 2 y alpha 0, y el ETF que la replica -------------------
meses = 120
mkt = azar.normal(0.008, 0.04, meses)
estrategia = 2.0 * mkt + azar.normal(0, 0.02, meses)

acum = lambda r: (np.prod(1 + r) - 1) * 100
valores = [acum(estrategia), acum(2.0 * mkt), acum(mkt)]
barras = ejes[1].bar(["estrategia\n(beta 2)", "ETF apalancado\n(beta 2)", "mercado\n(beta 1)"],
                     valores, color=[MORADO, NARANJA, AZUL], width=0.6, alpha=0.85)
for barra, valor in zip(barras, valores):
    altura = valor + 2.4 if valor >= 0 else valor - 2.4
    va = "bottom" if valor >= 0 else "top"
    ejes[1].text(barra.get_x() + barra.get_width() / 2, altura, f"{valor:.0f} %",
                 ha="center", va=va, color=TEXTO, fontsize=9.5)
b2, _a2 = np.polyfit(mkt, estrategia, 1)
ejes[1].text(0.47, 0.92, f"se construyó con alpha 0;\nsu beta estimada es {b2:.2f}",
             transform=ejes[1].transAxes, ha="right", va="top", color=MORADO, fontsize=8.5)
titulo(ejes[1], "Ganar más no es tener alpha",
       "el ETF apalancado consigue lo mismo sin ninguna habilidad")
ejes[1].set_ylabel("acumulado en 10 años, en %")
ejes[1].set_ylim(min(valores) * 1.22, max(valores) * 1.22)
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "alpha-y-beta-pendiente-y-altura")
