"""metricas-de-regresion-1.py — los residuos del ejemplo de las cinco viviendas y por qué
el RMSE castiga mucho más un error grande que el MAE. Figura de la página de métricas de
regresión (fase 6)."""

import numpy as np

from comun import *

estilo()

# --- Panel izquierdo: precio real frente a predicción en las cinco viviendas del ejemplo.
# Cada segmento vertical es un residuo, y lo que se resume es su valor absoluto.
real = np.array([100.0, 150.0, 200.0, 250.0, 300.0])
pred = np.array([110.0, 140.0, 210.0, 240.0, 320.0])
error = real - pred
mae = float(np.abs(error).mean())
rmse = float(np.sqrt((error ** 2).mean()))
r2 = 1 - float((error ** 2).sum() / ((real - real.mean()) ** 2).sum())

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.4))

ejes[0].plot([90, 330], [90, 330], color=TEXTO, linewidth=1.0, linestyle="--")
ejes[0].vlines(real, np.minimum(real, pred), np.maximum(real, pred), color=ROJO,
               linewidth=1.6, zorder=2)
ejes[0].plot(real, pred, "o", color=AZUL, markersize=7, zorder=3)
anotar(ejes[0], "cada raya roja es un residuo:\naquí el mayor se equivoca en 20",
       xy=(300, 320), xytext=(0.20, 0.86), color=ROJO)
anotar(ejes[0], f"MAE {mae:.1f}".replace(".", ",") + f" · RMSE {rmse:.1f}".replace(".", ",")
       + " (miles de €)",
       xy=(150, 140), xytext=(0.42, 0.12), color=AZUL, flecha=False)
ejes[0].set_xlim(85, 335)
ejes[0].set_ylim(85, 345)
ejes[0].set_xlabel("precio real")
ejes[0].set_ylabel("precio predicho")
rejilla(ejes[0], "both")
numeros(ejes[0])
titulo(ejes[0], "Los residuos del ejemplo, dibujados",
       f"la diagonal es acertar; el RMSE ({rmse:.1f})".replace(".", ",") +
       f" supera al MAE ({mae:.1f})".replace(".", ","))

# --- Panel derecho: qué pasa con las dos métricas cuando el error grande crece. Los otros
# cuatro errores se quedan en 1, así que el RMSE crece como el cuadrado de ese error
# mientras el MAE solo sube en línea recta.
grande = np.linspace(1.0, 20.0, 200)
mae_curva = (4 * 1.0 + grande) / 5
rmse_curva = np.sqrt((4 * 1.0 ** 2 + grande ** 2) / 5)

ejes[1].plot(grande, mae_curva, color=AZUL, linewidth=1.9, label="MAE")
ejes[1].plot(grande, rmse_curva, color=ROJO, linewidth=1.9, label="RMSE")
ejes[1].plot([10], [(4 + 10) / 5], "o", color=AZUL, markersize=6)
ejes[1].plot([10], [np.sqrt((4 + 100) / 5)], "o", color=ROJO, markersize=6)
anotar(ejes[1], "con el error de 10: MAE 2,8 y RMSE 4,6", xy=(10, 4.56),
       xytext=(0.38, 0.88), color=ROJO)
anotar(ejes[1], "el MAE sube en línea recta;\nel RMSE se dispara al cuadrado",
       xy=(15, 6.9), xytext=(0.50, 0.16), color=TEXTO, flecha=False)
ejes[1].set_xlim(0.5, 20.5)
ejes[1].set_ylim(0.6, 9.5)
ejes[1].set_xlabel("tamaño del error grande (los otros cuatro valen 1)")
ejes[1].set_ylabel("valor de la métrica")
ejes[1].legend(loc="upper left")
rejilla(ejes[1], "both")
numeros(ejes[1])
titulo(ejes[1], "Uno grande contra cuatro pequeños",
       "las dos métricas coinciden solo si todos los errores miden exactamente lo mismo")

guardar(fig, "regresion-mae-y-rmse")
