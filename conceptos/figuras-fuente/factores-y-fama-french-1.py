"""factores-y-fama-french-1.py — el factor valor y el alpha que aparece cuando lo olvidas.

Izquierda: la misma estrategia del codigo de la pagina, construida SIN habilidad (alpha cero),
estimada con dos modelos. Si no metes el factor valor, la prima de ese factor se va al termino
independiente y aparece un alpha que no existe: sesgo por variable omitida. Derecha: las cargas
que la estrategia si llevaba, que es lo que de verdad la explica.
"""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# La estrategia de la pagina: alpha CERO de verdad, beta de mercado 0,8 y carga de valor 0,5.
n = 240
mkt = azar.normal(0.006, 0.04, n)
hml = azar.normal(0.005, 0.03, n)
hml = hml - hml.mean() + 0.005
y = 0.8 * mkt + 0.5 * hml + azar.normal(0, 0.006, n)


def resumen(y, X):
    """MCO con errores tipicos: devuelve coeficientes, errores, t y R²."""
    X = np.column_stack([np.ones(len(y)), X])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ coef
    n, k = X.shape
    s2 = resid @ resid / (n - k)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    r2 = 1 - (resid @ resid) / ((y - y.mean()) @ (y - y.mean()))
    return coef, se, r2


coef_c, se_c, r2_c = resumen(y, np.column_stack([mkt, hml]))     # con el factor valor
coef_s, se_s, r2_s = resumen(y, mkt.reshape(-1, 1))              # sin el factor valor

fig, ejes = plt.subplots(1, 2, figsize=(9.8, 4.3), width_ratios=[1.1, 1.0])

# --- Izquierda: el alpha de los dos modelos, con su barra de error --------------------------
alphas = [coef_s[0] * 100, coef_c[0] * 100]          # en % mensual
errores = [se_s[0] * 100, se_c[0] * 100]
tstats = [coef_s[0] / se_s[0], coef_c[0] / se_c[0]]
barras = ejes[0].bar(["modelo solo con\nel mercado", "modelo con mercado\ny factor valor"],
                     alphas, yerr=errores, color=[ROJO, VERDE], width=0.52, alpha=0.85,
                     error_kw=dict(ecolor=TEXTO, linewidth=1.2, capsize=5))
for barra, valor, t, err in zip(barras, alphas, tstats, errores):
    ejes[0].text(barra.get_x() + barra.get_width() / 2,
                 valor + err * 1.5 if valor >= 0 else valor - err * 1.5,
                 f"{valor:+.2f} %\nt = {t:+.2f}", ha="center",
                 va="bottom" if valor >= 0 else "top", color=TEXTO, fontsize=9)
ejes[0].axhline(0, color=TEXTO, linewidth=1.0)
ejes[0].set_ylim(-0.20, 0.52)
ejes[0].text(0.5, 0.96, "la estrategia se construyó con alpha = 0",
             transform=ejes[0].transAxes, ha="center", va="top", color=TEXTO, fontsize=8.5)
ejes[0].text(0.02, 0.04, "ese +0,21 % no es habilidad: es la prima\ndel valor que no metiste en la regresión",
             transform=ejes[0].transAxes, ha="left", va="bottom", color=ROJO, fontsize=8.5)
titulo(ejes[0], "Quitar un factor no quita su rentabilidad",
       "la prima del factor omitido se muda al término independiente")
ejes[0].set_ylabel("alpha estimado, en % mensual")
rejilla(ejes[0])
numeros(ejes[0])

# --- Derecha: las cargas del modelo completo, que es lo que si la explica --------------------
cargas = [coef_c[1], coef_c[2]]
t_cargas = [coef_c[1] / se_c[1], coef_c[2] / se_c[2]]
barras = ejes[1].bar(["mercado", "valor\n(HML)"], cargas, color=[AZUL, NARANJA],
                     width=0.5, alpha=0.85)
for barra, valor, t in zip(barras, cargas, t_cargas):
    ejes[1].text(barra.get_x() + barra.get_width() / 2, valor + 0.025,
                 f"{valor:.2f}\n(t = {t:.0f})", ha="center", color=TEXTO, fontsize=9.5)
ejes[1].text(0.5, 0.06, f"con las dos cargas dentro, el R² sube de {r2_s:.2f} a {r2_c:.2f}\ny el término independiente se queda en cero",
             transform=ejes[1].transAxes, ha="center", va="bottom", color=TEXTO, fontsize=8.5)
titulo(ejes[1], "Lo que la estrategia llevaba de verdad",
       "0,8 de mercado y 0,5 de valor: eso es la estrategia, no el alpha")
ejes[1].set_ylabel("carga estimada (beta del factor)")
ejes[1].set_ylim(0, 1.05)
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "factores-alpha-que-era-una-carga")
