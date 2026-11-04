"""markowitz-y-frontera-1.py — la frontera eficiente y por qué se resiste en la práctica.

Izquierda: el plano riesgo-rentabilidad de tres activos. La nube son carteras con pesos
repartidos al azar; la curva es la frontera analítica de media-varianza y la recta verde es la
línea de asignación de capital, que sale del activo sin riesgo y toca la frontera en la cartera
tangente. Todo lo que está por debajo de la curva está mal combinado.
Derecha: el peso "óptimo" que sale al estimar con 36 meses de datos, repetido 2.000 veces. El
estimador rebota alrededor del valor verdadero y con una de cada tres muestras se va a pesos
negativos: es la maximización del error de la que habla la página.
La figura de la página de Markowitz y la frontera eficiente (fase 9).
"""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# Tres activos: rentabilidad esperada anual, volatilidad anual y correlaciones.
mu = np.array([0.08, 0.12, 0.05])
vol = np.array([0.15, 0.25, 0.10])
corr = np.array([[1.0, 0.3, 0.1],
                 [0.3, 1.0, 0.2],
                 [0.1, 0.2, 1.0]])
cov = np.outer(vol, vol) * corr
rf = 0.02
unos = np.ones(3)
inv = np.linalg.inv(cov)
porcentaje = FuncFormatter(lambda v, _p: f"{v:.0%}")

# Frontera analítica: w = Σ⁻¹ (a·μ + b·1), con a y b resueltos para cumplir wᵀμ = objetivo y wᵀ1 = 1.
A = np.array([[mu @ inv @ mu, mu @ inv @ unos],
              [mu @ inv @ unos, unos @ inv @ unos]])


def pesos_frontera(objetivo):
    a, b = np.linalg.solve(A, np.array([objetivo, 1.0]))
    return inv @ (a * mu + b * unos)


objetivos = np.linspace(mu.min() - 0.03, mu.max() + 0.06, 260)
pesos = np.array([pesos_frontera(o) for o in objetivos])
sigmas = np.sqrt(np.einsum("ij,jk,ik->i", pesos, cov, pesos))

# Cartera de mínima varianza y cartera tangente, las dos con fórmula cerrada.
w_mv = inv @ unos / (unos @ inv @ unos)
mu_mv, sigma_mv = float(w_mv @ mu), float(np.sqrt(w_mv @ cov @ w_mv))
w_tan = inv @ (mu - rf * unos)
w_tan = w_tan / w_tan.sum()
mu_tan, sigma_tan = float(w_tan @ mu), float(np.sqrt(w_tan @ cov @ w_tan))
sharpe_tan = (mu_tan - rf) / sigma_tan

# Carteras al azar con pesos no negativos que suman 1: la nube de lo alcanzable.
azar_pesos = azar.dirichlet(np.ones(3), size=1400)
ret_azar = azar_pesos @ mu
vol_azar = np.sqrt(np.einsum("ij,jk,ik->i", azar_pesos, cov, azar_pesos))

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.5))

# --- Izquierda: el plano riesgo-rentabilidad -----------------------------------------
ax = ejes[0]
ax.scatter(vol_azar, ret_azar, s=5, color=CIAN, alpha=0.16, linewidths=0, zorder=1)
# La parábola entera: la mitad de abajo también cumple las restricciones, pero es ineficiente.
ax.plot(sigmas, objetivos, color=REJILLA, linewidth=1.0, linestyle=":", zorder=2)
eficiente = objetivos >= mu_mv
ax.plot(sigmas[eficiente], objetivos[eficiente], color=AZUL, linewidth=2.4, zorder=3)
ax.scatter(vol, mu, s=52, color=ROJO, zorder=6, marker="o")
ax.scatter([sigma_mv], [mu_mv], s=130, color=NARANJA, marker="*", zorder=7)
# Línea de asignación de capital: mezcla del activo sin riesgo con la cartera tangente.
sig_cal = np.array([0.0, 0.32])
ax.plot(sig_cal, rf + sharpe_tan * sig_cal, color=VERDE, linewidth=1.7, linestyle="--", zorder=4)
ax.scatter([sigma_tan], [mu_tan], s=120, color=MORADO, marker="D", zorder=7)
for nombre, s, m in zip("ABC", vol, mu):
    ax.annotate(nombre, xy=(s, m), xytext=(s + 0.006, m + 0.008), fontsize=9, color=ROJO)
anotar(ax, "cada punto es una cartera distinta:\nlas de dentro están mal combinadas",
       xy=(0.20, 0.055), xytext=(0.42, 0.20), color=CIAN, flecha=False)
anotar(ax, "la frontera: para cada riesgo,\nla máxima rentabilidad posible",
       xy=(float(sigmas[150]), float(objetivos[150])), xytext=(0.05, 0.80), color=AZUL)
anotar(ax, "la tangente es la de máximo Sharpe",
       xy=(sigma_tan, mu_tan), xytext=(0.34, 0.95), color=MORADO)
anotar(ax, "el activo sin riesgo: 2 %", xy=(0.0, rf), xytext=(0.04, 0.07), color=VERDE)
titulo(ax, "La frontera, y la recta que sale del activo sin riesgo",
       "tres activos; la mitad punteada es ineficiente y nadie la elige")
ax.set_xlabel("volatilidad anual")
ax.set_ylabel("rentabilidad esperada anual")
ax.set_xlim(0.0, 0.32)
ax.set_ylim(0.0, 0.20)
ax.yaxis.set_major_formatter(porcentaje)
ax.xaxis.set_major_formatter(porcentaje)
rejilla(ax, eje="both")

# --- Derecha: qué peso sale al estimar con 36 meses de datos --------------------------
ax = ejes[1]
n_meses, n_muestras = 36, 2000
ret_mensual = azar.multivariate_normal(mu / 12, cov / 12, size=(n_muestras, n_meses))
medias = ret_mensual.mean(axis=1) * 12
centradas = ret_mensual - ret_mensual.mean(axis=1, keepdims=True)
cov_muestral = np.einsum("tki,tkj->tij", centradas, centradas) / (n_meses - 1) * 12
w_est = np.linalg.solve(cov_muestral, (medias - rf)[:, :, None])[:, :, 0]
w_est = w_est / w_est.sum(axis=1, keepdims=True)
peso_a = w_est[:, 0]
# El peso que saldría si μ y Σ fueran exactamente los verdaderos: la referencia.
peso_real = float(w_tan[0])
negativos = float((peso_a < 0).mean())
fuera = float(((peso_a < -1.0) | (peso_a > 2.0)).mean())
extremos = f"{peso_a.min() / 1000:,.0f} mil y {peso_a.max():,.0f}".replace(",", ".")

# range= deja fuera los pesos disparatados: se cuentan en la nota, no se dibujan.
ax.hist(peso_a, bins=48, range=(-1.0, 2.0), color=AZUL, alpha=0.75, zorder=2)
ax.axvline(0.0, color=TEXTO, linewidth=1.0, zorder=3)
ax.axvline(peso_real, color=ROJO, linewidth=1.8, linestyle="--", zorder=3)
anotar(ax, f"lo que pide la fórmula ({peso_real:.2f})".replace(".", ","),
       xy=(peso_real, 100), xytext=(0.51, 0.72), color=ROJO, flecha=False)
anotar(ax, f"en un {negativos:.0%} de las muestras".replace(".", ",")
       + "\nel peso «óptimo» sale negativo:\nvender en corto lo que no tienes",
       xy=(-0.28, 40), xytext=(0.03, 0.72), color=AZUL)
# Los que se quedan fuera del dibujo son la prueba más dura del problema.
anotar(ax, f"y un {fuera:.0%} ni cabe aquí: los pesos llegan a {extremos}",
       xy=(1.9, 20), xytext=(0.97, 0.92), color=TEXTO, flecha=False, align="right")
titulo(ax, "El peso óptimo rebota de muestra en muestra",
       "2.000 estimaciones con 36 meses de datos cada una")
ax.set_xlabel("peso del activo A que pide el optimizador")
ax.set_ylabel("número de muestras")
ax.set_ylim(0, 162)
rejilla(ax)
numeros(ax, ejes="x")

guardar(fig, "markowitz-frontera-y-ruido")
