"""chi-cuadrado-1.py - de donde sale el estadístico chi-cuadrado y con que se compara.

Izquierda: la tabla 2x2 del ejemplo del portal (40/160 movil, 60/140 escritorio). Cada casilla
lleva el residuo (O - E)/raiz(E); el estadístico es la suma de esos residuos al cuadrado.
Derecha: la distribución chi-cuadrado con 1 grado de libertad y la cola que es el p-valor, con
encima la nula simulada con 4000 tablas al azar para comprobar que la teoria cae donde dice.
"""

import numpy as np
from scipy import stats

from comun import *

estilo()
azar = np.random.default_rng(7)

# --- La tabla del ejemplo del portal: filas movil/escritorio, columnas convierte/no convierte.
tabla = np.array([[40, 160],
                  [60, 140]])
total = tabla.sum()
esperado = tabla.sum(axis=1, keepdims=True) * tabla.sum(axis=0, keepdims=True) / total
residuo = (tabla - esperado) / np.sqrt(esperado)     # residuo estandarizado
chi2 = ((tabla - esperado) ** 2 / esperado).sum()    # el estadistico es la suma de los cuadrados
gl = 1
p_valor = float(stats.chi2.sf(chi2, gl))             # la cola a la derecha

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.3))

# ═══ Izquierda: quien empuja el estadistico ═══
ax = ejes[0]
mapa = ax.imshow(residuo, cmap="RdBu_r", vmin=-2.4, vmax=2.4)
ax.set_xticks([0, 1], labels=["convierte", "no convierte"])
ax.set_yticks([0, 1], labels=["móvil", "escritorio"])
ax.grid(False)
for i in range(2):
    for j in range(2):
        ax.text(j - 0.28, i + 0.09, f"{tabla[i, j]}", ha="center", va="center", fontsize=13,
                color=TEXTO, fontweight="bold")
        ax.text(j - 0.28, i - 0.19, f"({tabla[i, j]} − {esperado[i, j]:.0f})² / {esperado[i, j]:.0f}",
                ha="center", va="center", fontsize=8.5, color=TEXTO)
barra = fig.colorbar(mapa, ax=ax, fraction=0.046, pad=0.04)
barra.set_label("residuo estandarizado", fontsize=8.5)
titulo(ax, "χ² suma las cuatro casillas",
       "móvil convierte menos de lo esperado y escritorio más: la misma desviación, signo contrario")
anotar(ax, "cada casilla aporta (O − E)² / E:\n2,00 + 0,67 + 2,00 + 0,67",
       (1.34, 0.5), (0.02, 0.06), color=TEXTO)

# ═══ Derecha: con que se compara ese numero ═══
ax = ejes[1]
malla = np.linspace(0.0005, 12, 800)
densidad = np.exp(-malla / 2) / np.sqrt(2 * np.pi * malla)   # chi2 con 1 grado de libertad
ax.plot(malla, densidad, color=AZUL, linewidth=1.8)
ax.fill_between(malla, densidad, where=malla >= chi2, color=ROJO, alpha=0.22)
ax.axvline(chi2, color=ROJO, linewidth=1.8)

# La nula simulada: 4000 tablas 2x2 con 200 usuarios por grupo y la MISMA tasa de conversion
# del 25 % en los dos grupos. Si la teoria esta bien, esto cae encima de la curva.
a_conv = azar.binomial(200, 0.25, 4000)                 # convertidos en movil
b_conv = azar.binomial(200, 0.25, 4000)                 # convertidos en escritorio
dif = a_conv - b_conv                                   # las cuatro casillas se desvian igual
simulados = dif ** 2 / (a_conv + b_conv) + dif ** 2 / (400 - a_conv - b_conv)
ax.hist(simulados, bins=np.linspace(0, 12, 49), density=True, color=REJILLA, alpha=0.45,
        label="4000 tablas simuladas sin asociación")

altura = densidad[np.searchsorted(malla, chi2)]
ax.annotate(f"tu χ² = {chi2:.2f}\np = {p_valor:.4f}".replace(".", ","),
            xy=(chi2, altura), xytext=(0.24, 0.62), textcoords="axes fraction",
            fontsize=10, color=ROJO,
            arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=1.0))
ax.text(0.66, 0.44, "el área roja es el p-valor:\nla probabilidad de que el azar\nllegue tan lejos como tú",
        transform=ax.transAxes, fontsize=8.5, color=TEXTO, ha="center")
ax.set_xlim(0, 12)
ax.set_ylim(0, 1.25)
ax.set_xlabel("estadístico χ² con 1 grado de libertad")
ax.set_ylabel("densidad")
ax.legend(loc="upper center", bbox_to_anchor=(0.62, 1.0))
titulo(ax, "El p-valor es la cola a la derecha de tu χ²",
       "curva: nula teórica. Barras: la misma nula simulada tabla a tabla")
rejilla(ax)
numeros(ax, ejes="x")

guardar(fig, "chi-cuadrado-residuos-y-cola")
