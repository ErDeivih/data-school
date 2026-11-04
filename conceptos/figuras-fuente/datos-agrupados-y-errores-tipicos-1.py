"""datos-agrupados-y-errores-tipicos-1.py - el error típico depende de las observaciones, no de las filas.

Izquierda: la tabla de 120 alumnos con 5 intervalos. La linea roja es el error típico correcto,
s / raiz(n) = 1,98, que no se mueve porque n es 120 y los intervalos que uses para presentar los
datos no cambian cuanta información tienes. La curva azul es el error que sale de dividir entre la
raiz del número de intervalos: con 5 filas da 9,70, casi cinco veces más, y encima se hace más
pequeno cuanto más troceas la tabla, que es justo lo contrario de lo que pasa de verdad.
Derecha: la varianza de los puntos medios frente a la anchura del intervalo. Los puntos son solo
la dispersión de las marcas de clase; la linea azul anade la variación de dentro de cada
intervalo, h^2/12, que es lo que la tabla se deja fuera.
"""

import numpy as np

from comun import *

estilo()

x = np.array([10.0, 30.0, 50.0, 70.0, 90.0])
f = np.array([8, 14, 42, 38, 18])
n = f.sum()
media = (f * x).sum() / n
s2_entre = (f * (x - media) ** 2).sum() / (n - 1)
s = np.sqrt(s2_entre)

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.6))

# --- Izquierda: el error tipico segun lo que pongas debajo de la raiz.
ax = ejes[0]
ks = np.arange(1, 41)
ax.plot(ks, np.full(ks.size, s / np.sqrt(n)), color=ROJO, linewidth=2.0,
        label="correcto: s / raiz(120) = 1,98")
ax.plot(ks, s / np.sqrt(ks), color=AZUL, linewidth=2.0,
        label="error: s / raiz(k)")
ax.plot([5], [s / np.sqrt(5)], marker="o", color=AZUL, markersize=7, zorder=5)
ax.annotate("con la tabla de 5 intervalos:\n9,70 (4,9 veces más)",
            xy=(5.0, s / np.sqrt(5)), xytext=(9.0, 6.6), fontsize=8.5, color=AZUL,
            arrowprops=dict(arrowstyle="->", color=AZUL, linewidth=0.9))
ax.annotate("el correcto no depende\nde como trocees la tabla",
            xy=(30.0, s / np.sqrt(n)), xytext=(12.0, 0.35), fontsize=8.5, color=ROJO)
ax.set_xlabel("número de intervalos de la tabla (k)")
ax.set_ylabel("error típico de la media")
ax.set_ylim(0.0, 11.0)
ax.legend(loc="upper right")
titulo(ax, "El error típico sale de n, no de las filas",
       "120 observaciones en los dos casos: solo cambia cómo se presentan")
rejilla(ax)
numeros(ax, ejes="y")

# --- Derecha: lo que se deja fuera la varianza de los puntos medios.
ax = ejes[1]
anchos = np.array([5.0, 10.0, 20.0, 40.0, 80.0, 160.0])
ax.plot(anchos, np.full(anchos.size, s2_entre), marker="o", color=MORADO, linewidth=1.6,
        markersize=6, label="varianza de los puntos medios")
ax.plot(anchos, s2_entre + anchos ** 2 / 12.0, marker="s", color=AZUL, linewidth=2.0,
        markersize=6, label="más la variación de dentro (h²/12)")
ax.fill_between(anchos, s2_entre, s2_entre + anchos ** 2 / 12.0, color=AZUL, alpha=0.12)
anotar(ax, "con intervalos de 20 puntos\nla tabla se deja fuera\n33,3 de varianza",
       (20.0, s2_entre + 400.0 / 24.0), (0.06, 0.34), color=AZUL, flecha=False)
ax.set_xlabel("anchura del intervalo, h")
ax.set_ylabel("varianza estimada")
ax.legend(loc="upper left")
titulo(ax, "Los intervalos anchos esconden varianza",
       "con 120 observaciones y s = 21,7: la curva azul es la varianza total")
rejilla(ax)
numeros(ax)

guardar(fig, "agrupados-error-tipico-y-varianza-de-dentro")
