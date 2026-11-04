"""almacenamiento-de-objetos-1.py — la clase de almacenamiento que minimiza el coste no
depende del volumen guardado, sino de cuantas veces lees cada GB. Tres clases con el mismo
modelo de coste: almacen por GB y mes fijo, más un precio por operación de lectura.
Solo la envolvente inferior (la linea gruesa) es una elección sensata.
"""

import numpy as np

from comun import *

estilo()

# Coste por GB y mes de cada clase y coste por operacion de lectura.
# Unidades relativas: lo que importa es la FORMA de las curvas, no que coincidan con
# la tarifa de ningun proveedor concreto. Cambia estos seis numeros y la decision cambia.
clases = [
    ("acceso frecuente", 1.00, 0.0005, ROJO),
    ("acceso poco frecuente", 0.50, 0.005, NARANJA),
    ("archivo", 0.20, 0.020, CIAN),
]
n = np.logspace(0, 3.02, 500)          # lecturas por GB y mes, de 1 a ~1050

fig, ax = plt.subplots(figsize=(8.8, 4.8))

# Punto en el que dos clases cuestan exactamente lo mismo: ahi cambia la decision.
cortes = []
for (n1, a1, c1, _), (n2, a2, c2, _) in zip(clases[:-1], clases[1:]):
    corte = (a2 - a1) / (c1 - c2)
    cortes.append((corte, n1, n2))
    ax.axvline(corte, color=REJILLA, linewidth=0.9, linestyle="--")

costes = []
for nombre, almacen, lectura, color in clases:
    coste = almacen + lectura * n
    costes.append(coste)
    ax.plot(n, coste, color=color, linewidth=1.5, label=nombre)
costes = np.array(costes)

# La envolvente inferior: para cada frecuencia de lectura, la clase mas barata.
ax.plot(n, costes.min(axis=0), color=AZUL, linewidth=3.0, solid_capstyle="round",
        label="clase más barata en cada caso")

ax.set_xscale("log")
ax.set_ylim(0, float(costes.min(axis=0).max()) * 1.95)

# Etiquetas de las clases: cada una pegada a su curva, en la franja de la izquierda, donde
# las tres estan separadas y por encima de ellas no pasa nada.
niveles = [(1.5, 1.12), (1.5, 0.66), (1.5, 0.36)]
for (nombre, almacen, lectura, color), (ex, ey) in zip(clases, niveles):
    ax.annotate(nombre, xy=(ex, ey), xytext=(0, 0), textcoords="offset points",
                ha="left", va="center", color=color, fontsize=9.5)

# Los dos cambios de decision van a la banda vacia de arriba, en coordenadas del eje: el
# texto lleva el color de la clase que deja de compensar, asi que no hace falta una flecha
# que cruce media figura.
for k, (corte, _, _) in enumerate(cortes):
    anotar(ax, f"deja de compensar a partir de\n{corte:.0f} lecturas por GB y mes",
           xy=(corte, clases[k][1] + clases[k][2] * corte),
           xytext=(0.03, 0.93 - 0.15 * k), color=clases[k][3], flecha=False)

ax.set_xlabel("lecturas por GB y mes")
ax.set_ylabel("coste por GB y mes")
titulo(ax, "El precio por GB no decide: deciden las lecturas",
       "lo que decide es cuántas veces lees cada GB")
ax.set_xticks([1, 10, 100, 1000])
ax.set_xticklabels(["1", "10", "100", "1000"])
# La leyenda baja debajo del eje: dentro solo cabia en la banda que ahora usan los textos.
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=2, fontsize=9)
numeros(ax, ejes="y")
rejilla(ax)

guardar(fig, "almacenamiento-de-objetos-clase-segun-acceso")
