"""maximo-drawdown-1.py — la caida maxima de una curva de capital: cuanto cayo, desde que
pico, hasta que mínimo y cuanto tardo en volver. Figura de la pagina de Caida maxima
(fase 9)."""

import numpy as np

from comun import *


def miles(x):
    """Enteros con punto de millares, como se escribe en el portal."""
    return f"{x:,.0f}".replace(",", ".")


def pct(x, decimales=2):
    """Porcentaje con coma decimal."""
    return f"{x * 100:.{decimales}f} %".replace(".", ",")


estilo()

capital = np.array([10000, 10500, 11200, 10800, 10100, 9500,
                    10200, 11000, 11600, 11400, 12100, 12400], dtype=float)
meses = np.arange(1, capital.size + 1)

picos = np.maximum.accumulate(capital)
caidas = (picos - capital) / picos
i_fondo = int(caidas.argmax())
i_pico = int(capital[:i_fondo + 1].argmax())
vuelta = int(np.flatnonzero(capital[i_fondo:] >= capital[i_pico])[0]) + i_fondo
mdd = float(caidas[i_fondo])
recuperar = capital[i_pico] / capital[i_fondo] - 1

fig, ejes = plt.subplots(2, 1, figsize=(7.0, 6.0), sharex=True)

# --- arriba: la curva, el pico movil y el hueco que queda debajo
ejes[0].fill_between(meses, capital, picos, where=capital < picos, color=ROJO, alpha=0.16,
                     zorder=1)
ejes[0].plot(meses, capital, color=AZUL, linewidth=1.9, marker="o", markersize=4, zorder=3)
ejes[0].plot(meses, picos, color=REJILLA, linewidth=1.1, linestyle="--", zorder=2)
ejes[0].axhline(capital[i_pico], color=ROJO, linewidth=1.0, linestyle="--", zorder=2)
ejes[0].plot(meses[i_pico], capital[i_pico], marker="o", markersize=7, color=ROJO, zorder=4)
ejes[0].plot(meses[i_fondo], capital[i_fondo], marker="o", markersize=7, color=ROJO, zorder=4)
ejes[0].set_ylim(8600, 13400)
anotar(ejes[0], f"pico: {miles(capital[i_pico])} EUR (mes {meses[i_pico]})",
       xy=(meses[i_pico], capital[i_pico]), xytext=(0.02, 0.94), color=ROJO)
anotar(ejes[0], f"el máximo no se recupera hasta el mes {meses[vuelta]}: {meses[vuelta] - meses[i_pico]} meses por debajo del pico",
       xy=(meses[vuelta], capital[vuelta]), xytext=(0.98, 0.94), color=TEXTO, align="right")
anotar(ejes[0], f"fondo: {miles(capital[i_fondo])} EUR (mes {meses[i_fondo]}): un {pct(mdd)} por debajo del pico\ny para volver a {miles(capital[i_pico])} hace falta un {pct(recuperar)}",
       xy=(meses[i_fondo], capital[i_fondo]), xytext=(0.02, 0.07), color=ROJO)
titulo(ejes[0], "La caida no es el resultado: es el camino",
       "la cuenta acaba el ano un 24 % arriba y aun así paso medio ano sin recuperar su máximo")
ejes[0].set_ylabel("capital (EUR)")
rejilla(ejes[0])
numeros(ejes[0], "y")

# --- abajo: la caida de cada mes (lo que se llama la curva bajo el agua)
ejes[1].fill_between(meses, 0, caidas * 100, color=ROJO, alpha=0.25, zorder=1)
ejes[1].plot(meses, caidas * 100, color=ROJO, linewidth=1.6, marker="o", markersize=4, zorder=3)
ejes[1].plot(meses[i_fondo], mdd * 100, marker="o", markersize=7, color=TEXTO, zorder=4)
ejes[1].set_ylim(-0.6, max(caidas * 100) * 1.45)
titulo(ejes[1], "Cuanto estabas por debajo del máximo, mes a mes",
       "el máximo de esta curva es el número que se pública como caida maxima")
ejes[1].set_xlabel("meses")
ejes[1].set_ylabel("caida (%)")
ejes[1].text(meses[i_fondo] + 0.25, mdd * 100 - 0.35, pct(mdd),
            color=TEXTO, fontsize=9)
rejilla(ejes[1])
numeros(ejes[1], "y")

guardar(fig, "drawdown-profundidad-y-duración")
