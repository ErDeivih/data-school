"""variable-aleatoria-1.py — masa frente a densidad, y por qué F(x) se lee en vertical.

Izquierda: la suma de dos dados, que solo toma 11 valores y cada uno tiene su probabilidad
(figura de barras). Derecha: el tiempo hasta un fallo, que es continuo: la densidad es una
altura, la probabilidad es un areas, y F(x) es la altura acumulada hasta ahi.
"""

import numpy as np

from comun import *

estilo()

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 4.4))   # mas alta: el titulo lleva subtitulo

# --- Panel izquierdo: variable discreta, funcion de masa --------------------------
# Las 36 parejas de dos dados, contadas a mano: la masa esta en la forma de la escalera.
sumas = np.arange(2, 13)
formas = np.array([1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1])
masa = formas / formas.sum()
assert abs(masa.sum() - 1.0) < 1e-12

izq.bar(sumas, masa, width=0.72, color=AZUL)
# Las notas van en coordenadas del eje (0-1) y en la franja que queda libre por encima de
# las barras: asi no pisan ni las barras ni la rejilla.
izq.set_ylim(0, 0.20)
anotar(izq, "aqui la altura ES la probabilidad\nP(X = 7) = 6/36 = 0,1667",
       xy=(7, masa[5]), xytext=(0.60, 0.93))
anotar(izq, "suma de todas\nlas barras = 1",
       xy=(11.5, masa[-1]), xytext=(0.03, 0.70), color=MORADO, flecha=False)
izq.set_xticks(sumas)
izq.set_xlabel("suma de los dos dados")
izq.set_ylabel("p(x) = P(X = x)")
titulo(izq, "Discreta: once valores exactos", "la altura de cada barra es su probabilidad")
numeros(izq, ejes="y")
rejilla(izq)

# --- Panel derecho: variable continua, densidad y funcion de distribucion ---------
lam = 0.5                                  # 0,5 fallos por hora: media de 2 horas
x = np.linspace(0, 8, 400)
densidad = lam * np.exp(-lam * x)
F = 1 - np.exp(-lam * x)                   # F(x) = P(X <= x)

der.plot(x, densidad, color=ROJO, linewidth=1.8)
der.fill_between(x[x <= 2], 0, densidad[x <= 2], color=ROJO, alpha=0.18)
der.plot(x, F, color=VERDE, linewidth=1.8, linestyle="--")
der.axhline(1.0, color=REJILLA, linewidth=0.9, linestyle=":")
der.set_ylim(0, 1.35)
# Las tres notas van en coordenadas del eje (0-1): la de la densidad en la franja que queda
# libre por encima de las dos curvas, y las otras dos apiladas en el hueco que dejan la
# densidad (abajo) y F(x) (arriba) a partir de x = 2.
anotar(der, "esta ALTURA es la densidad en 2:\n0,1839 no es la probabilidad de nada",
       xy=(2.0, lam * np.exp(-2)), xytext=(0.29, 0.90))
anotar(der, "esta AREA es P(X <= 2) = 0,6321", xy=(1.0, 0.20), xytext=(0.40, 0.42),
       color=ROJO)
anotar(der, "F(x) sube hasta 1: la lectura vertical\nde la linea verde da probabilidades",
       xy=(6.2, 1 - np.exp(-0.5 * 6.2)), xytext=(0.97, 0.22), color=VERDE, align="right")
der.set_xlabel("horas hasta el fallo")
der.set_ylabel("densidad f(x)  y  F(x)")
titulo(der, "Continua: la probabilidad es un áreas",
       "la densidad es una altura; F(x) se lee en vertical")
numeros(der)
rejilla(der)

guardar(fig, "variable-masa-densidad-y-acumulada")
