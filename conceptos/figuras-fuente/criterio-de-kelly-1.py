"""criterio-de-kelly-1.py — el crecimiento esperado tiene un máximo y un acantilado: pasarse de
la fracción óptima es tan malo como quedarse corto. Figura de la página del Criterio de Kelly
(fase 9)."""

import numpy as np

from comun import *


def num(x, decimales=2):
    """Número con coma decimal, como se escribe en el portal."""
    return f"{x:.{decimales}f}".replace(".", ",")


estilo()
azar = np.random.default_rng(7)

p, b = 0.55, 1.0                     # moneda cargada al 55 %, con cuota 1:1
q = 1 - p
fraccion = np.linspace(0.0, 0.45, 600)
# El crecimiento esperado por tirada es la media del logaritmo del capital: como el capital se
# multiplica, lo que manda a largo plazo es esta curva y no la esperanza aritmética.
crecimiento = 100 * (p * np.log(1 + fraccion * b) + q * np.log(1 - fraccion))

f_optima = float(fraccion[int(np.argmax(crecimiento))])
g_optima = float(crecimiento.max())
# El segundo corte con el cero es el punto a partir del cual se pierde dinero en promedio
# aunque la mayoría de las tiradas ganen.
cortes = np.where(np.diff(np.sign(crecimiento)))[0]
f_cero = float(fraccion[cortes[-1] + 1])

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.6))

ejes[0].axhline(0, color=TEXTO, linewidth=0.9)
ejes[0].plot(fraccion, crecimiento, color=AZUL, linewidth=2.2)
ejes[0].fill_between(fraccion, crecimiento, 0, where=crecimiento >= 0, color=VERDE, alpha=0.18)
ejes[0].fill_between(fraccion, crecimiento, 0, where=crecimiento < 0, color=ROJO, alpha=0.18)
ejes[0].axvline(f_optima, color=VERDE, linewidth=1.2, linestyle=":")
ejes[0].plot([f_optima], [g_optima], marker="o", markersize=7, color=VERDE, zorder=4)
anotar(ejes[0], f"el máximo está en f* = {num(f_optima)}:\n+{num(g_optima)} % por tirada",
       xy=(f_optima, g_optima), xytext=(0.15, 0.24), color=VERDE)
anotar(ejes[0], f"en f = {num(f_cero)} el crecimiento ya es negativo:\nla volatilidad se come la ventaja del 55 %",
       xy=(f_cero, 0.0), xytext=(0.98, 0.90), color=ROJO, align="right")
titulo(ejes[0], "Hay un tamaño y pasarse es peor",
       f"moneda que gana el {p:.0%} de las veces y paga 1 a 1: crecimiento esperado por tirada")
ejes[0].set_xlabel("f: fracción del capital apostada en cada tirada")
ejes[0].set_ylabel("crecimiento esperado por tirada (%)")
ejes[0].set_xlim(0, 0.45)
ejes[0].set_ylim(-2.6, 1.4)
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="both")

# --- Derecha: la misma apuesta jugada 400 veces con cuatro tamaños distintos. El eje vertical
# va en escala logarítmica porque el capital se multiplica: así cada camino sale casi recto y su
# pendiente es justo el crecimiento que mide la curva de la izquierda.
tiradas, caminos = 400, 15_000
resultados = azar.choice([1.0, -1.0], size=(caminos, tiradas), p=[p, q])
tipicos = {}
for f, color in zip((0.05, 0.10, 0.20, 0.30), [AZUL, VERDE, NARANJA, ROJO]):
    capital = 1000 * np.cumprod(1 + f * resultados, axis=1)
    # Media geométrica: la media de los logaritmos devuelta a euros. Es el «camino típico» que
    # Kelly maximiza, y en un producto de factores independientes no depende del orden.
    tipicos[f] = np.exp(np.mean(np.log(capital), axis=0))
    ejes[1].plot(np.arange(1, tiradas + 1), tipicos[f], color=color, linewidth=1.9,
                 label=f"f = {num(f)}")
ejes[1].axhline(1000, color=TEXTO, linewidth=0.9, linestyle="--")

anotar(ejes[1], f"con f = {num(0.30)} el capital típico se queda en "
                f"{num(tipicos[0.30][-1], 2)} € de cada 1.000:\nla ventaja del 55 % no llega a cobrarse",
       xy=(180, float(tipicos[0.30][179])), xytext=(0.04, 0.11), color=ROJO)
anotar(ejes[1], f"con f = {num(0.10)} el capital típico se multiplica por {num(tipicos[0.10][-1] / 1000, 1)}",
       xy=(tiradas, float(tipicos[0.10][-1])), xytext=(0.98, 0.93), color=VERDE, align="right")
titulo(ejes[1], "La misma apuesta, cuatro tamaños",
       "capital típico (media geométrica) de 15.000 caminos de 400 tiradas")
ejes[1].set_xlabel("tiradas jugadas")
ejes[1].set_ylabel("capital típico (EUR, escala logarítmica)")
ejes[1].set_yscale("log")
ejes[1].set_xlim(0, tiradas)
ejes[1].set_ylim(1, 30000)
ejes[1].legend(loc="upper left", fontsize=8)
rejilla(ejes[1], eje="both")
numeros(ejes[1], ejes="x")

guardar(fig, "kelly-crecimiento-y-sobreapuesta")
