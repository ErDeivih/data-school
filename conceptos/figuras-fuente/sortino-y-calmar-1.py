"""sortino-y-calmar-1.py — dos decisiones que cambian el número sin tocar la estrategia:
entre cuanto se divide la desviación bajista y desde donde se mide el Calmar. Figura de la
pagina de Sortino y Calmar (fase 9)."""

import numpy as np

from comun import *


def pct(x, decimales=1):
    """Porcentaje con coma decimal, como se escribe en el portal."""
    return f"{x * 100:.{decimales}f} %".replace(".", ",")


def num(x, decimales=2):
    return f"{x:.{decimales}f}".replace(".", ",")


estilo()


def medir(x):
    """Retorno anualizado, caida maxima y Calmar de una serie de retornos."""
    capital = np.cumprod(1 + x)
    picos = np.maximum.accumulate(capital)
    mdd = float(((picos - capital) / picos).max())
    anual = float(capital[-1] ** (12 / x.size) - 1)
    return capital, anual, mdd, anual / mdd


# --- izquierda: la misma serie con las dos convenciones del Sortino
r6 = np.array([0.03, -0.02, 0.04, -0.05, 0.01, 0.02])
exceso = r6 - 0.0
raiz = np.sqrt(12)
vol = exceso.std(ddof=1)
cuadrados = (np.minimum(exceso, 0) ** 2).sum()
bajista_n = np.sqrt(cuadrados / exceso.size)
bajista_k = np.sqrt(cuadrados / (exceso < 0).sum())
sharpe = exceso.mean() / vol * raiz
sortino_n = exceso.mean() / bajista_n * raiz
sortino_k = exceso.mean() / bajista_k * raiz

# --- derecha: la misma estrategia con dos ventanas
r24 = np.array([0.05, 0.04, -0.12, -0.08, 0.06, 0.05, 0.03, 0.04, 0.02, 0.03, 0.04, 0.03,
                0.005, 0.01, -0.015, 0.005, 0.01, 0.005, 0.005, 0.00, 0.01, 0.005, 0.005, 0.005])
capital24, anual24, mdd24, calmar24 = medir(r24)
capital12, anual12, mdd12, calmar12 = medir(r24[-12:])
meses = np.arange(1, r24.size + 1)

fig, ejes = plt.subplots(1, 2, figsize=(9.6, 4.4))

nombres = ["Sharpe\n(toda la\nvolatilidad)", "Sortino\n/ n = 6\n(seis meses)", "Sortino\n/ k = 2\n(dos meses malos)"]
valores = [sharpe, sortino_n, sortino_k]
colores = [AZUL, VERDE, NARANJA]
ejes[0].bar(np.arange(3), valores, width=0.55, color=colores, alpha=0.8, zorder=2)
for xi, v in zip(np.arange(3), valores):
    ejes[0].text(xi, v + 0.02, num(v), ha="center", fontsize=10, color=TEXTO)
ejes[0].set_ylim(0, 1.18)
ejes[0].set_xticks(np.arange(3))
ejes[0].set_xticklabels(nombres, fontsize=8.5)
titulo(ejes[0], "La misma serie de seis meses, tres ratios",
       "lo único que cambia entre la barra verde y la naranja es entre cuanto se divide")
anotar(ejes[0], "dividir entre los dos meses malos\nen vez de entre los seis\nbaja el ratio por debajo del Sharpe",
       xy=(2, sortino_k), xytext=(0.97, 0.86), color=NARANJA, align="right")
ejes[0].set_ylabel("ratio anualizado")
rejilla(ejes[0])
numeros(ejes[0], "y")

# --- derecha: el Calmar depende de la ventana
ejes[1].axvspan(1, 12, color=REJILLA, alpha=0.18, zorder=0)
ejes[1].plot(meses, 100 * capital24, color=AZUL, linewidth=1.8, zorder=2)
ejes[1].axvline(12.5, color=TEXTO, linewidth=1.0, linestyle="--", zorder=1)
ejes[1].set_xlim(1, 24)
ejes[1].set_ylim(87, 140)
titulo(ejes[1], "El Calmar depende de donde empieces",
       "la caida del 19 % vive en los primeros doce meses")
ejes[1].set_xlabel("meses")
ejes[1].set_ylabel("capital (base 100)")
ejes[1].text(2, 134.5, f"24 meses: caida {pct(mdd24)} y Calmar {num(calmar24)}",
             ha="left", fontsize=8.5, color=AZUL)
ejes[1].text(2, 128.5, f"ultimos 12: caida {pct(mdd12)} y Calmar {num(calmar12)}",
             ha="left", fontsize=8.5, color=ROJO)
rejilla(ejes[1])
numeros(ejes[1], "y")

guardar(fig, "sortino-convencion-y-ventana")
