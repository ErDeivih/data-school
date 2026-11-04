"""encoding-de-categoricas-1.py — el ordinal se inventa distancias y el target encoding
crudo se copia la etiqueta. La figura de la pagina de codificación de categoricas (fase 5)."""

import numpy as np

from comun import *

estilo()

# --- Panel izquierdo: tres ciudades, dos codificaciones ----------------------
ciudades = ["Madrid", "Lugo", "Sevilla"]
ordinal = np.array([1.0, 2.0, 3.0])
uno_caliente = [np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]), np.array([0.0, 0.0, 1.0])]

# --- Panel derecho: las seis filas del ejemplo de target encoding ------------
categorias = np.array(["A", "A", "A", "B", "B", "B"])
y = np.array([1.0, 0.0, 1.0, 0.0, 0.0, 1.0])
global_ = float(y.mean())
# La media de la categoria, tal cual, incluyendo la propia fila.
crudo = np.array([y[categorias == c].mean() for c in ("A", "B")])
# La misma media dejando fuera la fila que se esta codificando.
fuera = np.zeros(6)
for i in range(6):
    otras = (categorias == categorias[i])
    otras[i] = False
    fuera[i] = y[otras].mean()

fig, ejes = plt.subplots(1, 2, figsize=(8.4, 4.2), gridspec_kw={"width_ratios": [1.0, 1.05]})

# --- Izquierda: ordinal frente a one-hot -------------------------------------
ax = ejes[0]
for fila, ciudad in enumerate(ciudades):
    y_fila = float(2 - fila)
    if fila > 0:
        ax.annotate("", xy=(ordinal[fila], y_fila + 0.30), xytext=(0.0, y_fila + 0.30),
                    arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=1.2, shrinkA=0,
                                    shrinkB=0))
    ax.scatter(uno_caliente[fila] * 1.0, np.full(3, y_fila - 0.30), s=90, color=AZUL, zorder=3)
    ax.scatter(ordinal[fila], y_fila + 0.30, s=110, color=ROJO, zorder=3)
    ax.text(-0.12, y_fila, ciudad, ha="right", va="center", fontsize=9.5, color=TEXTO)
for tope in (1.0, 2.0, 3.0):
    ax.plot([tope, tope], [-0.5, 2.5], color=AZUL, linewidth=0.8, linestyle=":", zorder=1)
ax.text(-1.30, 2.86, "ordinal: un número por categoria", fontsize=9, color=ROJO, va="center")
ax.text(-1.30, 2.50, "one-hot: una columna por categoria", fontsize=9, color=AZUL, va="center")
ax.annotate("Sevilla = 3 y Madrid = 1,\ny la regresión se lo cree",
            xy=(2.0, 1.30), xycoords="data", xytext=(0.82, 0.14), textcoords="axes fraction",
            fontsize=8.5, color=ROJO, va="center", ha="right",
            arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9, shrinkA=2, shrinkB=2))
ax.set_xlim(-1.35, 3.45)
ax.set_ylim(-0.55, 3.05)
ax.set_yticks([])
ax.set_xticks([0, 1, 2, 3])
ax.set_xlabel("valor que ve el modelo")
ax.tick_params(axis="y", length=0)
titulo(ax, "El ordinal inventa un orden que no existe", "el one-hot solo dice cual es")
numeros(ax, ejes="x")

# --- Derecha: el encoding crudo copia la etiqueta ----------------------------
ax = ejes[1]
posiciones = np.arange(6.0)
etiquetas = [f"{c}\ny = {int(v)}" for c, v in zip(categorias, y)]
ax.scatter(posiciones, np.where(categorias == "A", crudo[0], crudo[1]), s=95, color=ROJO,
           zorder=3, label="target encoding crudo")
ax.scatter(posiciones, fuera, s=95, marker="D", color=VERDE, zorder=3,
           label="dejando fuera la propia fila")
ax.axhline(global_, color=MORADO, linewidth=1.0, linestyle="--")
ax.set_xticks(posiciones)
ax.set_xticklabels(etiquetas, fontsize=8.5, rotation=45)
ax.set_xlim(-0.7, 7.6)
ax.set_ylim(-0.22, 1.42)
ax.set_xlabel("las seis filas del ejemplo")
ax.set_ylabel("valor codificado")
ax.legend(loc="upper right")
ax.annotate("la linea morada es la media global, 0,50", xy=(4.6, global_), xycoords="data",
            xytext=(0.03, 0.30), textcoords="axes fraction", fontsize=8.5, color=MORADO,
            va="center",
            arrowprops=dict(arrowstyle="->", color=MORADO, linewidth=0.9, shrinkA=2, shrinkB=2))
ax.annotate("la fila con y = 1 aporta su 1 a su propio valor",
            xy=(2.0, crudo[0]), xycoords="data", xytext=(0.60, 0.74),
            textcoords="axes fraction", fontsize=8.5, color=ROJO, va="center",
            arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9, shrinkA=2, shrinkB=2))
ax.annotate("esta fila tiene y = 1 y le toca un 0,00",
            xy=(5.0, fuera[5]), xycoords="data", xytext=(0.03, 0.09),
            textcoords="axes fraction", fontsize=8.5, color=VERDE, va="center",
            arrowprops=dict(arrowstyle="->", color=VERDE, linewidth=0.9, shrinkA=2, shrinkB=2))
titulo(ax, "El encoding crudo ya trae la respuesta dentro",
       "cada fila aporta su propia etiqueta a su valor")
numeros(ax, ejes="y")

guardar(fig, "encoding-ordinal-onehot-y-target")
