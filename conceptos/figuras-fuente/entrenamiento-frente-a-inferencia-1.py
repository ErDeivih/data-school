"""entrenamiento-frente-a-inferencia-1.py — de dónde sale la discrepancia entre lo que el
modelo vio al entrenar y lo que ve al servir. La figura de la página de coherencia entre
entrenamiento e inferencia (fase 6).

Izquierda: el mismo dato bruto, dos veces normalizado. La línea gris usa la media y la
desviación aprendidas en el entrenamiento (lo correcto); la naranja recalcula los estadísticos
con el lote que llega (el error clásico). El modelo recibe números distintos para la misma
entrada.
Derecha: cuánto se desvía la predicción según el tamaño del lote, en escala logarítmica."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(3)   # la misma semilla que el bloque de la pagina
n = 1000
area = azar.lognormal(4.6, 0.55, n)
precio = 1.2 * area + azar.normal(0.0, 8.0, n)
corte = 700
X = area.reshape(-1, 1)

mu_entrena, sd_entrena = X[:corte].mean(), X[:corte].std()
z = (area - mu_entrena) / sd_entrena
pesos = np.linalg.lstsq(np.column_stack([np.ones(corte), z[:corte]]), precio[:corte],
                        rcond=None)[0]

fig, ejes = plt.subplots(1, 2, figsize=(7.4, 3.9))

# --- Panel izquierdo: la misma entrada, dos números distintos -----------------
ax = ejes[0]
muestras = z[corte:corte + 200]
z_ok = muestras
z_lote = (area[corte:corte + 200] - area[corte:corte + 200].mean()) / area[corte:corte + 200].std()

ax.plot(z_ok, color=AZUL, linewidth=1.4, label="estadísticos del entrenamiento")
ax.plot(z_lote, color=NARANJA, linewidth=1.4, label="estadísticos del lote que llega")
anotar(ax, "misma entrada,\notra escala", (60, z_ok[60]), (0.04, 0.06), color=NARANJA, flecha=False)
ax.set_xlabel("orden de la petición")
ax.set_ylabel("valor que recibe el modelo")
ax.legend(loc="upper right")
titulo(ax, "El modelo recibe otro número", "la media del lote mueve toda la escala")
rejilla(ax)
numeros(ax)

# --- Panel derecho: cuánto se desvía la predicción según el lote --------------
tamanos = [2, 5, 10, 20, 50, 100, 150, 200, 300]
desvios = []
for m in tamanos:
    d = []
    for i in range(corte, n - m + 1, m):
        lote = area[i:i + m]
        if len(lote) < 2:
            continue
        pred_ok = pesos[0] + pesos[1] * (lote - mu_entrena) / sd_entrena
        pred_mal = pesos[0] + pesos[1] * (lote - lote.mean()) / lote.std()
        d.append(np.mean(np.abs(pred_ok - pred_mal)))
    desvios.append(float(np.mean(d)) if d else float("nan"))

ax = ejes[1]
ax.plot(tamanos, desvios, "o-", color=ROJO, linewidth=1.6, markersize=5)
anotar(ax, "la escala se calcula\ncon el lote actual", (5, desvios[1]), (0.16, 0.42), color=ROJO,
       flecha=False, fondo=True)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlabel("tamaño del lote (escala logarítmica)")
ax.set_ylabel("desvío medio de la predicción")
titulo(ax, "Cuanto más pequeño el lote, peor", "el desvío cae al crecer el lote, no a cero")
rejilla(ax)
numeros(ax)

guardar(fig, "entrenamiento-inferencia-lote-y-escala")
