"""roc-auc-1.py — la escalera de la curva ROC con los ocho casos del ejemplo y el punto
donde el AUC se queda ciego: la precisión con un 1 % de positivos. Figura de la página
de la curva ROC y el AUC (fase 6)."""

import numpy as np

from comun import *

estilo()

# --- Panel izquierdo: los ocho casos del ejemplo de la página, ordenados de mayor a
# menor puntuación. Cada caso que entra al bajar el umbral mueve la curva un escalón.
y = np.array([1, 1, 1, 0, 0, 0, 0, 0])
score = np.array([0.95, 0.60, 0.40, 0.85, 0.55, 0.35, 0.20, 0.10])
orden = np.argsort(-score, kind="stable")     # de la puntuación más alta a la más baja
etiquetas = y[orden]
positivos, negativos = int(y.sum()), int((1 - y).sum())

# Al bajar el umbral se van acumulando casos: la tasa de aciertos y la de falsas alarmas
# son esas dos cuentas acumuladas divididas por el total de cada clase.
tpr = np.r_[0.0, np.cumsum(etiquetas) / positivos]
fpr = np.r_[0.0, np.cumsum(1 - etiquetas) / negativos]
auc = float(np.trapezoid(tpr, fpr))           # área bajo la escalera

# Los cuatro umbrales de la tabla de la página, con el punto de la curva que dejan.
umbrales = (0.95, 0.85, 0.60, 0.40)
puntos = [(fpr[k], tpr[k]) for k in (1, 2, 3, 5)]

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.4))

ejes[0].fill_between(fpr, tpr, step="post", color=AZUL, alpha=0.10)
ejes[0].plot(fpr, tpr, color=AZUL, linewidth=1.8, drawstyle="steps-post")
ejes[0].plot([0, 1], [0, 1], color=TEXTO, linewidth=1.0, linestyle="--")
ejes[0].plot(*zip(*puntos), "o", color=ROSA, markersize=6, zorder=3)
anotar(ejes[0], f"el área por debajo de la escalera es el AUC ({auc:.2f})".replace(".", ","),
       xy=(0.6, 0.1), xytext=(0.30, 0.10), color=AZUL, flecha=False)
anotar(ejes[0], "los cuatro umbrales de la tabla\nestán marcados en rosa",
       xy=(0.2, 0.667), xytext=(0.46, 0.34), color=ROSA)
ejes[0].set_xlim(-0.02, 1.02)
ejes[0].set_ylim(-0.02, 1.05)
ejes[0].set_xlabel("tasa de falsos positivos (negativos molestados)")
ejes[0].set_ylabel("tasa de verdaderos positivos\n(positivos capturados)")
rejilla(ejes[0], "both")
numeros(ejes[0])
titulo(ejes[0], "Cada umbral es un escalón",
       "la diagonal es ordenar al azar; la esquina de arriba a la izquierda es lo perfecto")

# --- Panel derecho: el mismo modelo del ejemplo grande, que trabaja capturando el 90 %
# de los positivos con un 5 % de falsos positivos. Su AUC es 0,92 en cualquier población,
# pero la precisión depende del porcentaje de positivos que haya.
tpr_op, fpr_op = 0.90, 0.05
prevalencias = np.logspace(-4, np.log10(0.5), 300)
precision = tpr_op * prevalencias / (tpr_op * prevalencias + fpr_op * (1 - prevalencias))
prec_1 = tpr_op * 0.01 / (tpr_op * 0.01 + fpr_op * 0.99)

ejes[1].plot(prevalencias, precision, color=MORADO, linewidth=1.9)
ejes[1].axhline(0.5, color=ROJO, linewidth=1.2, linestyle="--")
ejes[1].axvline(0.01, color=TEXTO, linewidth=1.0, linestyle=":")
ejes[1].plot([0.01], [prec_1], "o", color=ROJO, markersize=6)
anotar(ejes[1], f"con un 1 % de positivos: {prec_1:.2f}".replace(".", ","),
       xy=(0.01, prec_1), xytext=(0.06, 0.62), color=ROJO)
anotar(ejes[1], "la raya roja es el corte de 0,5\npor costumbre: solo se supera\nsi el positivo es común",
       xy=(0.3, 0.5), xytext=(0.66, 0.30), color=ROJO, flecha=False)
ejes[1].set_xscale("log")
ejes[1].set_ylim(-0.03, 1.05)
ejes[1].set_xlabel("prevalencia (proporción de positivos en la población)")
ejes[1].set_ylabel("precisión en el punto\nde trabajo")
rejilla(ejes[1])
numeros(ejes[1])
titulo(ejes[1], "El AUC no ve esto: 0,92 con cualquier prevalencia",
       "mismo punto de trabajo en todos los casos: captura el 90 % y molesta al 5 %")

guardar(fig, "roc-escalera-y-prevalencia")
