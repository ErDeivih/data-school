"""validacion-temporal-1.py — por qué el K-fold barajado miente en una serie temporal y
qué mide de verdad el esquema hacia delante. La figura de la página de validación temporal (fase 5).

Los dos paneles usan los MISMOS datos y el MISMO modelo de vecino más cercano: la única
diferencia es qué filas caen en entrenamiento y cuáles en prueba."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# Serie con tendencia: y = 0.5·t + ruido de desviación 2 (la misma del ejemplo de la página)
n = 400
t = np.arange(n, dtype=float)
y = 0.5 * t + azar.normal(0.0, 2.0, n)
idx = np.arange(n)


def vecino(entrena, prueba):
    """Predice con el valor del punto de entrenamiento más cercano en el tiempo."""
    return y[entrena[np.abs(t[prueba][:, None] - t[entrena][None, :]).argmin(axis=1)]]


def rmse(entrena, prueba):
    return float(np.sqrt(np.mean((y[prueba] - vecino(entrena, prueba)) ** 2)))


# K-fold barajado: cada pliegue de prueba tiene vecinos temporales en el entrenamiento
pliegues = np.array_split(azar.permutation(idx), 5)
err_azar = np.array([rmse(np.setdiff1d(idx, p), p) for p in pliegues])

# Walk-forward: se entrena solo con lo anterior y se predice el bloque siguiente
bloques = np.array_split(idx, 5)[1:]
err_wf = np.array([rmse(idx[idx < b[0]], b) for b in bloques])

fig, ejes = plt.subplots(1, 2, figsize=(7.0, 4.4))

# --- Panel izquierdo: la prueba, sobre el dibujo de la serie ------------------
izq = ejes[0]
izq.plot(t, y, color=REJILLA, linewidth=1.0, zorder=1)

for p, color in zip(pliegues, [AZUL, NARANJA, VERDE, MORADO, ROJO]):
    izq.scatter(t[p], y[p], s=9, color=color, zorder=3)

corte = bloques[-1][0]
izq.axvline(corte, color=TEXTO, linewidth=1.1, linestyle="--", zorder=2)
izq.text(corte - 6, 175, "hasta aquí ve el modelo", rotation=90, ha="right", va="center",
         fontsize=8, color=TEXTO)
izq.annotate("ahí el modelo repite 161,3:\nel vecino más cercano no extrapola",
             xy=(390, 162), xytext=(0.03, 0.16), textcoords="axes fraction",
             fontsize=8.5, color=ROJO,
             arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=1.0, shrinkA=2, shrinkB=3))
izq.text(0.03, 0.94, "barajado: RMSE %.2f" % err_azar.mean(), transform=izq.transAxes,
         fontsize=9, color=TEXTO, va="top")
izq.set_title("Los puntos de prueba tienen vecinos a los lados")
izq.set_xlabel("instante t")
izq.set_ylabel("valor de la serie")
rejilla(izq)
numeros(izq)

# --- Panel derecho: los dos esquemas de partición ----------------------------
der = ejes[1]
filas = []
for i, p in enumerate(pliegues):
    filas.append(("barajado", i, np.sort(p)))
for i, b in enumerate(bloques):
    filas.append(("hacia delante", 5 + i, b))

for nombre, fila, prueba in filas:
    der.hlines(fila, 0, 400, color=AZUL, linewidth=6.5, zorder=2)
    der.hlines(fila, prueba.min(), prueba.max(), color=ROJO, linewidth=6.5, zorder=3)

der.axhline(4.6, color=REJILLA, linewidth=0.9, linestyle=":")
der.text(0, 10.1, "azul: entrena       rojo: prueba", fontsize=8.5, color=TEXTO, va="center")
der.text(0, 9.15, "hacia delante: RMSE %.2f" % err_wf.mean(), fontsize=9, color=TEXTO, va="center")
der.set_yticks([2, 7])
der.set_yticklabels(["K-fold\nbarajado", "hacia\ndelante"])
der.set_ylim(-0.8, 11.2)
der.set_xlim(-6, 406)
der.set_xlabel("instante t")
der.set_title("Qué filas entran en cada pliegue")
rejilla(der, eje="x")
numeros(der, ejes="x")

guardar(fig, "validacion-temporal-barajar-frente-a-avanzar")
