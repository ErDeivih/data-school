"""p-valor-1.py — las dos caras del p-valor: la cola de la distribución nula (15 caras en
20 lanzamientos) y su distribución uniforme cuando H₀ es cierta frente a cuando hay efecto.
Figura de la página del p-valor."""

import numpy as np
from scipy import stats

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.1))

# --- Izquierda: el p-valor es area de cola, calculada suponiendo H0 cierta.
caras = np.arange(0, 21)
pmf = stats.binom.pmf(caras, 20, 0.5)
colores = [ROJO if k >= 15 or k <= 5 else AZUL for k in caras]
ejes[0].bar(caras, pmf, color=colores, width=0.75)
anotar(ejes[0], "P(X ≥ 15) = 0,0207", xy=(16, pmf[16]), xytext=(0.70, 0.62), color=ROJO)
anotar(ejes[0], "la cola simétrica,\nP(X ≤ 5) = 0,0207", xy=(4, pmf[4]), xytext=(0.03, 0.55),
       color=ROJO)
ejes[0].text(0.22, 0.86, "el contraste bilateral suma las dos colas: p = 0,0414\n"
             "(21.700 casos de 2²⁰ = 1.048.576)",
             transform=ejes[0].transAxes, fontsize=8.5, color=TEXTO)
ejes[0].set_xlabel("caras en 20 lanzamientos, si la moneda fuera justa")
ejes[0].set_ylabel("probabilidad")
ejes[0].set_ylim(0, 0.235)
titulo(ejes[0], "El p-valor es la cola, no el punto",
       "cuánto de raro es 15 caras contando todo lo más extremo que 15")
rejilla(ejes[0])
numeros(ejes[0], ejes="x")

# --- Derecha: bajo H0 el p-valor es uniforme; con efecto se apina a la izquierda.
azar = np.random.default_rng(0)
reps, n = 5000, 30
a = azar.normal(0.0, 1.0, size=(reps, n))
b = azar.normal(0.0, 1.0, size=(reps, n))
c = azar.normal(0.5, 1.0, size=(reps, n))
p_nulo = stats.ttest_ind(a, b, axis=1).pvalue
p_real = stats.ttest_ind(c, b, axis=1).pvalue

bordes = np.linspace(0, 1, 21)
ejes[1].axvspan(0, 0.05, color=ROJO, alpha=0.10, zorder=0)
ejes[1].axvline(0.05, color=ROJO, linewidth=1.2, linestyle="--", zorder=4)
ejes[1].hist(p_nulo, bins=bordes, color=AZUL, zorder=2)
ejes[1].hist(p_real, bins=bordes, histtype="step", color=VERDE, linewidth=2.0, zorder=3)
anotar(ejes[1], "sin ningún efecto, el 5,1 % de los 5.000 contrastes\ncae a la izquierda del umbral",
       xy=(0.05, 700), xytext=(0.14, 0.62), color=ROJO)
anotar(ejes[1], "con un efecto real (media 0,5 más alta),\nel 47,5 % se apina a la izquierda",
       xy=(0.025, 2370), xytext=(0.13, 0.90), color=VERDE)
ejes[1].text(0.30, 0.35, "bajo H₀ cada valor de p es igual de probable:\n"
             "el umbral del 5 % no es especial, solo está calibrado",
             transform=ejes[1].transAxes, fontsize=8.5, color=TEXTO)
ejes[1].set_xlabel("p-valor del contraste, en 5.000 simulaciones")
ejes[1].set_ylabel("contrastes")
ejes[1].set_xlim(0, 1)
titulo(ejes[1], "Bajo H₀ el p-valor es plano: el 5 % por azar",
       "la curva verde es el mismo contraste cuando sí hay efecto")
rejilla(ejes[1])
numeros(ejes[1], ejes="x")

guardar(fig, "p-valor-cola-y-uniformidad")
