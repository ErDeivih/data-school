"""imputacion-de-datos-1.py — lo que de verdad hace rellenar un hueco: el valor que
aparece, la varianza que se pierde y de quien se copia. La figura de la pagina de
imputación de datos (fase 5)."""

import numpy as np
from sklearn.impute import KNNImputer

from comun import *

estilo()

# --- Datos del panel de arriba a la izquierda --------------------------------
ingresos = np.array([1200.0, 1350.0, 1500.0, 1600.0, 1800.0,
                     np.nan, np.nan, np.nan, 9500.0])
faltan = np.isnan(ingresos)
puestos = np.flatnonzero(faltan)
media = float(np.nanmean(ingresos))
mediana = float(np.nanmedian(ingresos))

# --- Datos del panel de abajo a la izquierda ---------------------------------
datos = np.array([10.0, 12.0, 14.0, 16.0, 18.0, np.nan, np.nan])
huecos = np.flatnonzero(np.isnan(datos))
var_antes = float(np.nanvar(datos, ddof=1))
var_despues = float(np.where(np.isnan(datos), np.nanmean(datos), datos).var(ddof=1))

# --- Datos del panel de la derecha: KNN con uno y con dos vecinos -------------
X = np.array([[1.0, 10.0], [2.0, 12.0], [3.0, np.nan], [8.0, 90.0], [9.0, 95.0]])
k_uno = float(KNNImputer(n_neighbors=1).fit_transform(X)[2, 1])
k_dos = float(KNNImputer(n_neighbors=2).fit_transform(X)[2, 1])
media_columna = float(np.nanmean(X[:, 1]))

fig = plt.figure(figsize=(8.6, 5.8))
rej = fig.add_gridspec(2, 2, width_ratios=[1.5, 1.0])

# --- Arriba izquierda: los mismos huecos, dos rellenos -----------------------
ax = fig.add_subplot(rej[0, 0])
x = np.arange(1.0, 10.0)
ax.scatter(x[~faltan], ingresos[~faltan], s=150, color=AZUL, zorder=3)
ax.scatter(x[puestos], np.full(3, media), s=90, marker="D", color=ROJO, zorder=3,
           label=f"con la media ({media:,.0f})")
ax.scatter(x[puestos] + 0.22, np.full(3, mediana), s=90, marker="D", color=VERDE, zorder=3,
           label=f"con la mediana ({mediana:,.0f})")
ax.axhline(media, color=ROJO, linewidth=1.1, linestyle="--")
ax.axhline(mediana, color=VERDE, linewidth=1.1, linestyle=":")
ax.set_xticks(x)
ax.set_xticklabels([f"{int(v)}" if not np.isnan(v) else "falta" for v in ingresos],
                   fontsize=8, rotation=45)
ax.set_xlim(0.6, 11.4)
ax.set_ylim(0, 11_200)
ax.legend(loc="upper left")
anotar(ax, "inventa tres ingresos que aqui nadie tiene", (9.0, media), (0.24, 0.44),
       color=ROJO)
titulo(ax, "El metodo decide que valor aparece", "los tres huecos valen lo mismo que el resumen")
numeros(ax, ejes="y")
rejilla(ax)

# --- Abajo izquierda: la dispersion que se pierde ----------------------------
ax = fig.add_subplot(rej[1, 0])
ax.bar([0, 1], [var_antes, var_despues], width=0.34, color=AZUL, alpha=0.30)
ax.scatter([0, 1], [var_antes, var_despues], s=110, color=AZUL, zorder=3)
ax.set_xticks([0, 1])
ax.set_xticklabels(["antes", "después"], fontsize=9)
ax.set_ylabel("varianza muestral")
ax.set_xlim(-0.7, 2.9)
ax.set_ylim(0, 13.5)
anotar(ax, f"{var_antes:.2f}", (0, var_antes), (0.06, 0.90), color=AZUL, flecha=False)
anotar(ax, f"{var_despues:.2f}", (1, var_despues), (0.28, 0.62), color=ROJO, flecha=False)
anotar(ax, "los mismos 5 datos observados", (0, var_antes), (0.48, 0.86), color=TEXTO, flecha=False)
anotar(ax, "7 filas, pero los dos nuevos valen\njusto la media: no se separan", (1, var_despues),
       (0.48, 0.58), color=ROJO, flecha=False)
titulo(ax, "La varianza baja sin tocar un dato real", "un tercio de la dispersión, gratis")
numeros(ax, ejes="y")
rejilla(ax)

# --- Derecha: de quien copia el valor ----------------------------------------
ax = fig.add_subplot(rej[:, 1])
normal = X[~np.isnan(X[:, 1])]
ax.scatter(normal[:, 0], normal[:, 1], s=130, color=AZUL, zorder=3,
           label="filas completas")
ax.scatter([3.0], [media_columna], s=130, marker="x", color=REJILLA, linewidth=2.0, zorder=3,
           label=f"la media de la columna ({media_columna:.1f})")
ax.scatter([3.0, 3.0], [k_uno, k_dos], s=150, marker="D", color=ROJO, zorder=4)
for valor, vecinos in ((k_uno, 1), (k_dos, 2)):
    ax.plot([vecinos, 3.0], [valor, valor], color=ROJO, linewidth=1.0, linestyle=":", zorder=2)
ax.axvline(3.0, color=TEXTO, linewidth=0.9, alpha=0.4)
ax.set_xlabel("primera columna (siempre observada)")
ax.set_ylabel("segunda columna (con el hueco)")
ax.set_xlim(0, 10)
ax.set_ylim(0, 116)
ax.legend(loc="upper left")
anotar(ax, f"con k = 2: {k_dos:.0f}, copia de los dos vecinos", (3.0, k_dos), (0.22, 0.62),
       color=ROJO)
anotar(ax, f"con k = 1: {k_uno:.0f}, el vecino más cercano", (3.0, k_uno), (0.22, 0.47),
       color=ROJO)
anotar(ax, "la media de la columna, 51,8,\nno se parece a nada de aqui arriba",
       (3.0, media_columna), (0.98, 0.38), color=TEXTO, align="right")
titulo(ax, "El vecino manda, no el promedio",
       "KNN copia de quien se parece; la media, de nadie")
numeros(ax)
rejilla(ax)

guardar(fig, "imputacion-que-cambia-el-relleno")
