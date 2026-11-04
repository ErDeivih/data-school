"""supuestos-de-la-regresion-1.py — varianza constante frente a varianza creciente y lo
que eso le hace al error estandar: por qué los errores robustos HC3 dan un intervalo más
honesto sin mover el coeficiente (fase 6)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

n = 200
x = np.sort(azar.uniform(1, 10, size=n))

# Los dos juegos de datos del ejemplo de la pagina: en el segundo la desviacion del
# error crece como 0,3·x, asi que el embudo se abre hacia la derecha.
y_constante = 2 + 0.8 * x + azar.normal(0, 0.6, size=n)
y_creciente = 2 + 0.8 * x + azar.normal(0, 0.3 * x)

# Dos filas y dos columnas: tres paneles en una sola fila se pisan. El hueco se borra.
fig, rejilla_ejes = plt.subplots(2, 2, figsize=(10.4, 7.2))
ejes = [rejilla_ejes[0][0], rejilla_ejes[0][1], rejilla_ejes[1][0]]
fig.delaxes(rejilla_ejes[1][1])

# --- (a) Residuos con varianza constante: nube sin forma ----------------------
res_a = y_constante - (2 + 0.8 * x)
ejes[0].axhline(0, color=TEXTO, linewidth=0.9)
ejes[0].plot(x, res_a, "o", color=AZUL, markersize=3.2, alpha=0.7)
# Las dos bandas son el mismo +-2 sigma: si la nube las respeta, la varianza es constante.
ejes[0].axhline(1.2, color=REJILLA, linewidth=0.9, linestyle="--")
ejes[0].axhline(-1.2, color=REJILLA, linewidth=0.9, linestyle="--")
ejes[0].set_xlabel("valor de x")
ejes[0].set_ylabel("residuo")
anotar(ejes[0], "La nube respeta las dos bandas de\narriba abajo: la varianza es constante",
       xy=(5.6, -1.15), xytext=(0.04, 0.16))
titulo(ejes[0], "Varianza constante: nube sin forma", "los residuos no se estrechan ni se ensanchan")
rejilla(ejes[0])
numeros(ejes[0])

# --- (b) Residuos con varianza creciente: el embudo --------------------------
res_b = y_creciente - (2 + 0.8 * x)
ejes[1].axhline(0, color=TEXTO, linewidth=0.9)
ejes[1].plot(x, res_b, "o", color=ROJO, markersize=3.2, alpha=0.7)
# Las mismas bandas de (a) en valor absoluto, pero ahora proporcionales a x.
ejes[1].plot(x, 0.6 * x, color=NARANJA, linewidth=1.4, linestyle="--")
ejes[1].plot(x, -0.6 * x, color=NARANJA, linewidth=1.4, linestyle="--")
ejes[1].set_xlabel("valor de x")
ejes[1].set_ylabel("residuo")
ejes[1].set_ylim(-8.4, 8.4)   # la misma escala que en (a): si no, el embudo se disimula
anotar(ejes[1], "Las mismas bandas fijas dejaban puntos\nfuera: la dispersión crece con x, 25 veces\nde un extremo al otro",
       xy=(9.4, -4.3), xytext=(0.05, 0.15), color=ROJO)
titulo(ejes[1], "Varianza creciente: el embudo",
       "el error estándar clásico promedia lo que no es constante")
rejilla(ejes[1])
numeros(ejes[1])

# --- (c) El intervalo del coeficiente: clásico frente a HC3 -------------------
beta, se_clasico, se_robusto = 0.7435, 0.0288, 0.0316
ejes[2].axvline(0.8, color=TEXTO, linewidth=1.0, linestyle=":")
ejes[2].errorbar([0], [beta], yerr=[1.96 * se_clasico], fmt="o", color=AZUL,
                 markersize=8, capsize=8, linewidth=1.6)
ejes[2].errorbar([1], [beta], yerr=[1.96 * se_robusto], fmt="o", color=VERDE,
                 markersize=8, capsize=8, linewidth=1.6)
ejes[2].set_xticks([0, 1])
ejes[2].set_xticklabels(["clásico", "robusto HC3"])
ejes[2].set_xlim(-0.75, 1.75)
ejes[2].set_ylim(0.60, 0.875)
ejes[2].set_ylabel("β₁ con su intervalo del 95 %")
ejes[2].text(1.72, 0.865, "valor real, 0,8", color=TEXTO, fontsize=8.5,
             ha="right", va="top")
anotar(ejes[2], "El coeficiente no se mueve:\nlo que cambia es la anchura\ndel intervalo",
       xy=(0.06, 0.699), xytext=(0.04, 0.60), flecha=False)
titulo(ejes[2], "Mismo coeficiente, distinta confianza",
       "0,7435 ± 1,96 · SE, con el SE de cada método")
rejilla(ejes[2], eje="y")
numeros(ejes[2])

guardar(fig, "supuestos-embudo-y-error-estandar")
