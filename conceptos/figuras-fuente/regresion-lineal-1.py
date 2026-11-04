"""regresion-lineal-1.py — la recta de mínimos cuadrados con sus residuos y el aviso de
la extrapolación: el mismo ajuste que se calcula a mano en la pagina, dibujado (fase 6)."""

import numpy as np

from comun import *

estilo()

# Los cinco alumnos del ejemplo de la pagina: horas de estudio y nota.
x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
y = np.array([4.0, 5.0, 6.0, 8.0, 9.0])

# Minimos cuadrados en forma cerrada: b1 = Sxy / Sxx.
xm, ym = x.mean(), y.mean()
b1 = ((x - xm) * (y - ym)).sum() / ((x - xm) ** 2).sum()
b0 = ym - b1 * xm
pred = b0 + b1 * x
residuos = y - pred
r2 = 1 - (residuos ** 2).sum() / ((y - ym) ** 2).sum()

linea = np.linspace(1.0, 6.0, 80)

fig, ejes = plt.subplots(1, 2, figsize=(9.8, 4.2))

# --- Izquierda: la recta, los residuos y el hueco de la extrapolacion -----------
ejes[0].axvspan(5.0, 6.35, color=NARANJA, alpha=0.10)
ejes[0].plot(linea, b0 + b1 * linea, color=AZUL, linewidth=1.9, label="recta ajustada")
ejes[0].plot(x, y, "o", color=TEXTO, markersize=6, label="alumnos observados")
# Cada palo vertical es un residuo: la distancia que la recta no explica.
for xi, yi, pi in zip(x, y, pred):
    ejes[0].plot([xi, xi], [yi, pi], color=ROJO, linewidth=1.4, zorder=1)
ejes[0].plot([], [], color=ROJO, linewidth=1.4, label="residuos")
ejes[0].plot([6.0], [b0 + b1 * 6.0], "o", color=NARANJA, markersize=7, zorder=3)
ejes[0].set_xlabel("horas de estudio")
ejes[0].set_ylabel("nota")
ejes[0].set_xlim(0.6, 6.35)
ejes[0].set_ylim(2.6, 11.6)
ejes[0].legend(loc="upper left")
anotar(ejes[0], "Con 6 horas predice 10,3: es\nuna extrapolación, no una\npredicción fiable",
       xy=(6.0, 10.3), xytext=(0.30, 0.28), color=NARANJA)
titulo(ejes[0], "La recta que deja los residuos mínimos",
       "nota = 2,5 + 1,3 · horas   ·   R² = 0,9826")
rejilla(ejes[0])
numeros(ejes[0])

# --- Derecha: residuo contra prediccion, la comprobacion que si avisa ----------
ejes[1].axhline(0, color=TEXTO, linewidth=0.9)
# Los puntos van en orden de x, no de prediccion: asi el patron (una curva suave) se ve.
ejes[1].plot(pred, residuos, "o", color=MORADO, markersize=7, label="un alumno")
ejes[1].plot([], [], color=REJILLA, linewidth=1.0, linestyle="--", label="banda de ruido típico, ±0,4")
for xi, r in zip(pred, residuos):
    ejes[1].plot([xi, xi], [0, r], color=MORADO, linewidth=1.2, alpha=0.5)
ejes[1].axhline(0.4, color=REJILLA, linewidth=1.0, linestyle="--")
ejes[1].axhline(-0.4, color=REJILLA, linewidth=1.0, linestyle="--")
ejes[1].set_xlabel("predicción de la recta, en orden de las horas")
ejes[1].set_ylabel("residuo (nota − predicción)")
ejes[1].set_ylim(-0.62, 0.66)
ejes[1].legend(loc="lower right", fontsize=8)
anotar(ejes[1], "El patrón sube y baja sin ordenar los\nerrores por tamaño: sin más datos, esto\nno basta para dudar del modelo",
       xy=(7.7, 0.3), xytext=(0.04, 0.86))
titulo(ejes[1], "Los residuos, uno a uno", "su suma es cero por construcción: la recta pasa por (x̄, ȳ)")
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "regresion-lineal-recta-y-residuos")
