"""escalares-vectores-matrices-1.py — la forma (filas, columnas) y el eje que se colapsa"
deciden si una media significa algo. Figura de la pagina escalares-vectores-matrices."""

import numpy as np

from comun import *

estilo()

# Los numeros son los del ejemplo de la pagina (4 personas, 3 variables). No se sortean:
# la figura sale siempre igual y ademas coincide con lo que cuenta el texto.
datos = np.array([[34, 171, 68],
                  [51, 165, 71],
                  [28, 180, 84],
                  [45, 158, 57]])
variables = ["edad", "altura", "peso"]
unidades = ["años", "cm", "kg"]
personas = ["persona 1", "persona 2", "persona 3", "persona 4"]


def num(v, dec=1):
    """Numero con coma decimal, como se escribe en el portal."""
    return ("%.*f" % (dec, v)).replace(".", ",")


fig, (izq, der) = plt.subplots(1, 2, figsize=(10.6, 4.3))

# ---------------------------------------------------------------- izquierda: la tabla
izq.set_xlim(-2.3, 4.3)
izq.set_ylim(5.5, -2.9)
izq.axis("off")
izq.set_aspect("equal")

for i in range(4):
    for j in range(3):
        resalta = (i, j) == (1, 2)          # a_23 = 71, el que usa el texto
        izq.text(j, i, "%g" % datos[i, j], ha="center", va="center",
                 fontsize=11, color=TEXTO,
                 bbox=dict(boxstyle="round,pad=0.42", facecolor="none",
                           edgecolor=ROJO if resalta else REJILLA,
                           linewidth=1.8 if resalta else 0.9))

for j in range(3):
    izq.text(j, -1.05, variables[j], ha="center", va="center", fontsize=10, color=AZUL)
    izq.text(j, -1.62, unidades[j], ha="center", va="center", fontsize=8.5, color=REJILLA)

for i in range(4):
    izq.text(-0.55, i, personas[i], ha="right", va="center", fontsize=9, color=TEXTO)

izq.text(1.0, -2.35, "3 columnas = 3 variables  ·  4 filas = 4 observaciones",
         ha="center", va="center", fontsize=9.5, color=AZUL)
izq.text(1.0, 3.85, "Misma tabla, dos lecturas:  forma (4, 3)", ha="center",
         va="center", fontsize=11, color=TEXTO)
izq.text(1.0, 4.55, "Si la lees al revés, la media sale plausible y falsa",
         ha="center", va="center", fontsize=9.5, color=ROJO)

izq.annotate("en el texto: a₂₃\nen el código: A[1, 2]\n(el código empieza a contar en 0)",
             xy=(2.15, 1.0), xytext=(2.85, 2.35), fontsize=8.5, color=ROJO,
             ha="left", va="center", linespacing=1.5,
             arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=1.0))

# ------------------------------------------------- derecha: el eje que se colapsa
der.set_xlim(-0.4, 8.4)
der.set_ylim(-2.4, 3.6)
der.axis("off")

# El bloque de datos en pequeño: 4 filas y 3 columnas de cuadraditos.
for i in range(4):
    for j in range(3):
        der.plot([j * 0.5], [1.8 - i * 0.5], marker="s", linestyle="none",
                 markersize=11, color=AZUL, alpha=0.75)
der.text(0.5, -0.75, "los datos (4, 3)", ha="center", va="center", fontsize=9, color=TEXTO)

# Fila de arriba: axis=0 recorre las filas y deja una media por columna.
der.text(4.6, 3.05, "una media por variable: forma (3,)", ha="center", va="center",
         fontsize=9.5, color=VERDE)
der.text(2.3, 2.35, "axis=0", ha="center", va="center", fontsize=9.5, color=VERDE)
der.annotate("", xy=(3.1, 1.8), xytext=(1.5, 1.8),
             arrowprops=dict(arrowstyle="->", color=VERDE, linewidth=1.4))
for k, v in enumerate([39.5, 168.5, 70.0]):
    der.text(3.6 + k * 1.1, 1.8, num(v), ha="center", va="center", fontsize=9,
             color=TEXTO, bbox=dict(boxstyle="round,pad=0.35", facecolor="none",
                                    edgecolor=VERDE, linewidth=1.0))

# Fila de abajo: axis=1 recorre las columnas y deja una media por observacion.
der.text(5.0, 0.95, "una media por observación: forma (4,)", ha="center", va="center",
         fontsize=9.5, color=ROJO)
der.text(2.3, 0.35, "axis=1", ha="center", va="center", fontsize=9.5, color=ROJO)
der.annotate("", xy=(3.1, -0.05), xytext=(1.5, -0.05),
             arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=1.4))
for k, v in enumerate([91.0, 95.7, 97.3, 86.7]):
    der.text(3.6 + k * 0.95, -0.05, num(v), ha="center", va="center", fontsize=9,
             color=TEXTO, bbox=dict(boxstyle="round,pad=0.35", facecolor="none",
                                    edgecolor=ROJO, linewidth=1.0))
der.text(5.0, -0.80, "91,0 mezcla años con centímetros y kilos: no significa nada",
         ha="center", va="center", fontsize=8.5, color=ROJO)

der.text(4.3, -1.85, "El eje que escribes en axis= es el que se recorre y desaparece.",
         ha="center", va="center", fontsize=9.5, color=TEXTO)

guardar(fig, "matriz-filas-y-columnas")
