"""regularizacion-l1-l2-1.py — los caminos de los coeficientes al subir la penalización:
la restricción de L1 es un rombo con vértices en los ejes y la de L2 un círculo sin
esquinas; por eso Lasso llega a cero exacto y Ridge solo encoge (fase 6)."""

import numpy as np
from sklearn.linear_model import Lasso, LinearRegression, Ridge, lasso_path

from comun import *

estilo()
azar = np.random.default_rng(0)

# Las tres variables del ejemplo de la pagina: x1 con efecto real, x2 casi identica a x1
# (correlacion altisima) y x3 ruido puro.
n = 100
x1 = azar.normal(size=n)
x2 = 0.95 * x1 + azar.normal(scale=0.1, size=n)
x3 = azar.normal(size=n)
X = np.column_stack([x1, x2, x3])
y = 3 * x1 + azar.normal(scale=0.5, size=n)

# Sin estandarizar, la penalizacion castiga mas a la variable con menos escala.
X = (X - X.mean(axis=0)) / X.std(axis=0)
etiquetas = ["var 1 (real)", "var 2 (gemela)", "var 3 (ruido)"]
colores = [AZUL, NARANJA, VERDE]

# lasso_path devuelve los coeficientes para una rejilla de alpha EN ORDEN DECRECIENTE:
# por eso el flip, que deja la ruta de izquierda a derecha.
alphas = np.logspace(-2, 1.5, 90)
_, camino, _ = lasso_path(X, y, alphas=alphas)
alphas = alphas[::-1]
camino = camino[:, ::-1]

# Ridge no tiene ruta en sklearn: la formula cerrada (X^T X + alpha I)^-1 X^T y da el
# camino entero sin iterar nada.
camino_ridge = np.array([
    np.linalg.solve(X.T @ X + a * np.eye(3), X.T @ y) for a in alphas
])

# Dos filas y dos columnas: tres paneles en una sola fila se pisan. El hueco se borra.
fig, rejilla_ejes = plt.subplots(2, 2, figsize=(11.0, 7.4))
ejes = [rejilla_ejes[0][0], rejilla_ejes[0][1], rejilla_ejes[1][0]]
fig.delaxes(rejilla_ejes[1][1])

# --- (a) camino de Lasso ------------------------------------------------------
for j in range(3):
    ejes[0].plot(alphas, camino[j], color=colores[j], linewidth=1.8, label=etiquetas[j])
ejes[0].axvline(0.1, color=TEXTO, linewidth=1.0, linestyle=":")
ejes[0].set_xscale("log")
ejes[0].set_xlabel("α (escala logarítmica)")
ejes[0].set_ylabel("coeficiente")
ejes[0].set_ylim(-0.6, 3.7)
ejes[0].set_xlim(0.01, 34)
# Sin caja de leyenda: cada anotacion lleva el color de su curva.
ejes[0].text(0.12, 3.58, "λ = 0,1: aquí ya hay dos coeficientes", fontsize=8.5, va="top")
ejes[0].text(0.12, 3.34, "que valen cero exacto", fontsize=8.5, va="top")
anotar(ejes[0], "La gemela y el ruido caen a cero: Lasso elige", xy=(0.35, 0.0),
       xytext=(0.30, 0.34), color=NARANJA)
titulo(ejes[0], "L1: el camino se vacía en seco", "cada coeficiente descartado cae a cero exacto")
rejilla(ejes[0])
numeros(ejes[0], ejes="y")

# --- (b) camino de Ridge ------------------------------------------------------
for j in range(3):
    ejes[1].plot(alphas, camino_ridge[:, j], color=colores[j], linewidth=1.8,
                 label=etiquetas[j])
ejes[1].axvline(1.0, color=TEXTO, linewidth=1.0, linestyle=":")
ejes[1].set_xscale("log")
ejes[1].set_xlabel("α (escala logarítmica)")
ejes[1].set_ylabel("coeficiente")
ejes[1].set_ylim(-1.6, 4.4)
ejes[1].set_xlim(0.01, 45)
ejes[1].text(0.011, 2.23, "λ = 1,0: ningún coeficiente llega", fontsize=8.5, va="top")
ejes[1].text(0.011, 1.95, "a cero, solo se encogen", fontsize=8.5, va="top")
anotar(ejes[1], "La gemela conserva su parte del efecto", xy=(7.5, 0.95),
       xytext=(0.22, 0.06), color=NARANJA)
titulo(ejes[1], "L2: el camino se estrecha sin cortar", "ningún coeficiente es exactamente cero")
rejilla(ejes[1])
numeros(ejes[1], ejes="y")

# --- (c) qué se lleva cada método a la misma escala ---------------------------
ols = LinearRegression().fit(X, y).coef_
lasso = Lasso(alpha=0.1, max_iter=10000).fit(X, y).coef_
ridge = Ridge(alpha=1.0).fit(X, y).coef_
pos = np.arange(3)
ejes[2].barh(pos - 0.26, ols, 0.26, color=TEXTO, label="mínimos cuadrados")
ejes[2].barh(pos, lasso, 0.26, color=AZUL, label="Lasso (α = 0,1)")
ejes[2].barh(pos + 0.26, ridge, 0.26, color=NARANJA, label="Ridge (α = 1,0)")
ejes[2].axvline(0, color=TEXTO, linewidth=0.9)
ejes[2].set_yticks(pos)
ejes[2].set_yticklabels(etiquetas)
ejes[2].invert_yaxis()
ejes[2].set_xlim(-1.4, 3.9)
ejes[2].set_xlabel("coeficiente estimado")
# La leyenda va FUERA del área de datos (debajo del eje): así no compite con las barras
# ni con la anotación, que necesitan el poco hueco libre que queda a la derecha.
ejes[2].legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=3, fontsize=8,
               handlelength=1.2, columnspacing=1.0)
anotar(ejes[2], "Lasso pone dos variables en cero\nexacto; Ridge no anula ninguna",
       xy=(0.15, 1.85), xytext=(0.46, 0.10))
titulo(ejes[2], "Encojo, selecciono o no hago nada", "mismo ajuste, tres respuestas distintas")
rejilla(ejes[2], eje="x")
numeros(ejes[2], ejes="x")

guardar(fig, "regularizacion-caminos-l1-l2")
