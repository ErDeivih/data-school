"""multiplicidad-y-fdr-1.py - que hace cada corrección con la misma lista de p-valores.

Izquierda: los diez p-valores ordenados del ejemplo del portal. Los puntos negros son los
p-valores y las lineas son los umbrales: la recta creciente k*alfa/m de Benjamini-Hochberg y la
recta plana alfa/m de Bonferroni. El círculo verde marca los cuatro hallazgos que declara BH y el
rojo, el único que sobrevive a Bonferroni.
Derecha: que le pasa al error de tipo I cuando contrastas 1, 5, 20, 100 o 1000 hipotesis que son
todas ciertas. La probabilidad de colar al menos un falso positivo sube hacia 1.
"""

import numpy as np

from comun import *

estilo()

p = np.array([0.001, 0.009, 0.011, 0.019, 0.031, 0.048, 0.120, 0.340, 0.510, 0.880])
m, alfa = p.size, 0.05

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.4))

# ═══ Izquierda: donde corta cada correccion ═══
ax = ejes[0]
k = np.arange(1, m + 1)
umbral_bh = k / m * alfa
k_corte = int(np.max(np.where(p <= umbral_bh)[0])) + 1   # BH rechaza TODO hasta ese k
ax.plot(k, umbral_bh, color=AZUL, linewidth=1.8, marker="o", markersize=4,
        label="umbral de BH: k · α / m")
ax.axhline(alfa / m, color=ROJO, linewidth=1.8, linestyle="--",
           label="umbral de Bonferroni: α / m = 0,005")
ax.scatter(k[1:], p[1:], s=34, color=TEXTO, zorder=4)
ax.scatter(k[1:k_corte], p[1:k_corte], s=130, facecolor="none", edgecolor=VERDE, linewidth=1.9,
           zorder=5, label=f"los {k_corte} hallazgos de BH")
ax.scatter(k[:1], p[:1], s=230, facecolor="none", edgecolor=ROJO, linewidth=1.7, zorder=5,
           label="el único hallazgo de Bonferroni")
ax.axhline(alfa, color=REJILLA, linewidth=1.0, linestyle=":")
ax.text(7.4, alfa + 0.014, "α = 0,05", color=REJILLA, fontsize=8.5)
ax.axvline(4.5, color=MORADO, linewidth=1.4)
ax.annotate("BH corta en el cuarto: el quinto\np (0,031) ya supera su umbral\n(0,025), y a partir de ahí se para",
            xy=(4.5, 0.16), xytext=(0.33, 0.40), textcoords="axes fraction", fontsize=8.5,
            color=MORADO, arrowprops=dict(arrowstyle="->", color=MORADO, linewidth=0.9))
ax.set_xlabel("p-valor ordenado (k de 10)")
ax.set_ylabel("valor del p-valor")
ax.legend(loc="upper left", fontsize=8.2)
titulo(ax, "Los dos umbrales sobre la misma lista de p-valores",
       "BH compara cada p con una fracción creciente de α; Bonferroni, todos con la misma")

# ═══ Derecha: el error que crece con el numero de pruebas ═══
ax = ejes[1]
pruebas = np.array([1, 2, 5, 10, 20, 50, 100, 1000])
fwer = 1 - 0.95 ** pruebas
ax.plot(pruebas, fwer, color=ROJO, linewidth=2.0, marker="o", markersize=5)
ax.axhline(0.05, color=TEXTO, linewidth=1.3, linestyle="--")
ax.text(1.05, 0.075, "el 5 % que crees que controlas", color=TEXTO, fontsize=8.5)
for n, desplazamiento in ((20, 0.16), (100, 0.14)):
    valor = 1 - 0.95 ** n
    ax.annotate(f"{valor:.2f}".replace(".", ","), xy=(n, valor),
                xytext=(n * 0.55, valor - desplazamiento), fontsize=9, color=ROJO)
ax.annotate("con 100 pruebas que no dependen de nada,\nla probabilidad de colar al menos\nun falso positivo es del 99,4 %",
            xy=(100, 0.994), xytext=(0.06, 0.62), textcoords="axes fraction", fontsize=8.5,
            color=TEXTO, arrowprops=dict(arrowstyle="->", color=TEXTO, linewidth=0.9))
ax.set_xscale("log")
ax.set_ylim(0, 1.08)
ax.set_xlabel("número de hipótesis que contrastas (escala logarítmica)")
ax.set_ylabel("probabilidad de al menos un falso positivo")
titulo(ax, "El 5 % por prueba no es el 5 % del estudio",
       "todas las hipótesis son ciertas: cada test aporta su 5 % y se acumulan")
rejilla(ax)
numeros(ax, ejes="x")

guardar(fig, "multiplicidad-umbrales-y-fwer")
