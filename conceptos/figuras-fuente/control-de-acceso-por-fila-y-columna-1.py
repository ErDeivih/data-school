"""control-de-acceso-por-fila-y-columna-1.py — una sola tabla fisica y lo que ve cada rol
celda a celda. La figura de la pagina de control de acceso por fila y columna (fase 4)."""

import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import Patch

from comun import *

estilo()

columnas = ["pais", "comercial", "importe", "cliente"]
filas = [
    ["ES", "ana", "1000", "ACME"],
    ["ES", "luis", "250", "PEREZ SL"],
    ["FR", "ana", "4000", "ACME"],
    ["DE", "luis", "150", "GARCIA"],
    ["ES", "ana", "3200", "ACME"],
]

# La politica de cada rol: un predicado de fila y una lista de columnas permitidas.
filas_ana = {0, 1, 4}          # pais = ES
filas_luis = {1, 3}            # comercial = luis
columnas_ana = {"pais", "comercial", "importe"}
columnas_luis = {"pais", "importe", "cliente"}

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 4.2))

# --- Izquierda: la tabla fisica, que es una sola para todos --------------------------
izq.imshow(np.zeros((5, 4, 3)) + np.array(to_rgb(REJILLA)) * 0.25 + 0.72, aspect="auto")
for i, fila in enumerate(filas):
    for j, valor in enumerate(fila):
        izq.text(j, i, valor, ha="center", va="center", fontsize=9, color=TEXTO)
izq.set_xticks(range(4))
izq.set_xticklabels(columnas, fontsize=8.5)
izq.set_yticks(range(5))
izq.set_yticklabels([f"fila {i + 1}" for i in range(5)], fontsize=8.5)
izq.set_xlabel("columnas")
izq.set_ylabel("filas")
titulo(izq, "Una sola tabla en el disco",
       "nadie ve la politica mirando los datos: está en el motor")

# --- Derecha: quien ve cada celda, con las dos politicas a la vez --------------------
# 0 = nadie, 1 = solo ana, 2 = solo luis, 3 = los dos.
quien = np.zeros((5, 4))
for i in range(5):
    for j, col in enumerate(columnas):
        ve_ana = i in filas_ana and col in columnas_ana
        ve_luis = i in filas_luis and col in columnas_luis
        quien[i, j] = 3 if (ve_ana and ve_luis) else (1 if ve_ana else (2 if ve_luis else 0))

paleta = {0: np.array(to_rgb(REJILLA)) * 0.55 + 0.35, 1: np.array(to_rgb(NARANJA)),
          2: np.array(to_rgb(MORADO)), 3: np.array(to_rgb(AZUL))}
colores = np.zeros((5, 4, 3))
etiquetas = {0: "no", 1: "ana", 2: "luis", 3: "ana\nluis"}
for i in range(5):
    for j in range(4):
        colores[i, j] = paleta[quien[i, j]]
der.imshow(colores, aspect="auto")
for i in range(5):
    for j in range(4):
        der.text(j, i, etiquetas[quien[i, j]], ha="center", va="center", fontsize=8.5,
                 color=TEXTO if quien[i, j] == 0 else "white")
der.set_xticks(range(4))
der.set_xticklabels(columnas, fontsize=8.5)
der.set_yticks(range(5))
der.set_yticklabels([f"fila {i + 1}" for i in range(5)], fontsize=8.5)
der.set_xlabel("columnas")
der.legend(handles=[Patch(facecolor=paleta[3], label="la ven los dos"),
                    Patch(facecolor=paleta[1], label="solo ana"),
                    Patch(facecolor=paleta[2], label="solo luis"),
                    Patch(facecolor=paleta[0], label="nadie")],
           loc="upper center", bbox_to_anchor=(0.5, -0.16), ncols=4, fontsize=8.5)
titulo(der, "Qué ve cada rol, celda a celda",
       "ana filtra por pais; luis, por comercial y sin la columna comercial")
# La rejilla la dibujan los bordes de las celdas de imshow: no hace falta rejilla() aqui.

guardar(fig, "acceso-fila-y-columna")
