"""ratio-de-sharpe-1.py — dos caminos con el mismo capital final y el mismo Sharpe mal
medido: cuanto baila la métrica segun cuantas observaciones la sostienen. Figura de la
pagina del Ratio de Sharpe (fase 9)."""

import numpy as np

from comun import *


def pct(x, decimales=1):
    """Porcentaje con coma decimal, como se escribe en el portal."""
    return f"{x * 100:.{decimales}f} %".replace(".", ",")


def num(x, decimales=1):
    return f"{x:.{decimales}f}".replace(".", ",")


estilo()

# --- el mismo resultado por dos caminos muy distintos
tranquilo = np.array([0.02, 0.03, -0.01, 0.04, 0.01, 0.02,
                      -0.02, 0.03, 0.00, 0.02, 0.01, 0.01])
base = np.array([0.09, -0.07, 0.10, -0.08, 0.09, -0.06,
                 0.10, -0.08, 0.09, -0.07, 0.10, -0.06])
# Se ajusta la segunda serie para que acabe EXACTAMENTE en el mismo capital.
factor = (np.prod(1 + tranquilo) / np.prod(1 + base)) ** (1 / base.size)
brusco = (1 + base) * factor - 1

capital_t = 100 * np.cumprod(1 + tranquilo)
capital_b = 100 * np.cumprod(1 + brusco)
rf = 0.002
sigma_t = (tranquilo - rf).std(ddof=1)
sigma_b = (brusco - rf).std(ddof=1)
sharpe_t = (tranquilo - rf).mean() / sigma_t * np.sqrt(12)
sharpe_b = (brusco - rf).mean() / sigma_b * np.sqrt(12)
meses = np.arange(1, tranquilo.size + 1)

fig, ejes = plt.subplots(1, 2, figsize=(9.6, 4.2))

# --- izquierda: que mide el Sharpe
ejes[0].plot(meses, capital_t, color=AZUL, linewidth=1.8, marker="o", markersize=3.5,
             label="meses tranquilos")
ejes[0].plot(meses, capital_b, color=ROJO, linewidth=1.8, marker="o", markersize=3.5,
             label="meses con sobresaltos")
ejes[0].legend(loc="upper left")
ejes[0].set_ylim(70, 135)
titulo(ejes[0], "Mismo capital final, distinto camino",
       f"las dos acaban en {num(capital_t[-1])}: eso es todo lo que dice el beneficio")
ejes[0].set_xlabel("meses")
ejes[0].set_ylabel("capital (base 100)")
ejes[0].text(0.35, 0.30, f"la azul se mueve un {pct(sigma_t)} al mes:\nSharpe anual {num(sharpe_t)}",
             transform=ejes[0].transAxes, fontsize=8.5, color=AZUL)
ejes[0].text(0.35, 0.12, f"la roja se mueve un {pct(sigma_b)} al mes:\nSharpe anual {num(sharpe_b)}",
             transform=ejes[0].transAxes, fontsize=8.5, color=ROJO)
rejilla(ejes[0])
numeros(ejes[0], "y")

# --- derecha: cuanto baila el Sharpe medido cuando no hay ninguna ventaja
repeticiones = 4000
bines = np.linspace(-3.2, 3.2, 65)
ancho = bines[1] - bines[0]
azar = np.random.default_rng(7)
for meses_medidos, color, nombre in ((12, CIAN, "estimado con 12 meses"),
                                     (240, MORADO, "estimado con 240 meses")):
    muestra = azar.normal(0.0, 0.03, size=(repeticiones, meses_medidos))
    sr = muestra.mean(axis=1) / muestra.std(axis=1, ddof=1) * np.sqrt(12)
    ejes[1].hist(sr, bins=bines, color=color, alpha=0.55, label=nombre)
    if meses_medidos == 12:
        exagerados = float((sr >= 2.2).mean() * 100)

ejes[1].axvline(2.2, color=ROJO, linewidth=1.3, linestyle="--")
ejes[1].set_xlim(-3.2, 3.2)
titulo(ejes[1], "Cuanto baila el Sharpe medido",
       "misma estrategia SIN ninguna ventaja (Sharpe verdadero 0), 4.000 simulaciones")
ejes[1].set_xlabel("Sharpe anual que sale al medirlo")
ejes[1].set_ylabel("simulaciones")
ejes[1].legend(loc="upper left")
ejes[1].text(2.1, ejes[1].get_ylim()[1] * 0.55, f"2,2: con 12 meses se supera\nen el {f'{exagerados:.1f}'.replace('.', ',')} % de las veces",
             color=ROJO, fontsize=8.5, ha="right")
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "sharpe-caminos-y-ruido")
