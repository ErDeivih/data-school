"""purged-kfold-1.py — que se lleva la purga y que se lleva el embargo en una validación
cruzada de series temporales. Figura de la pagina de K-fold con purga y embargo (fase 9)."""

import numpy as np

from comun import *

estilo()

# 100 observaciones cuyas etiquetas duran 10 barras: la i ocupa [i, i + 10).
n = 100
t0 = np.arange(n, dtype=float)
t1 = t0 + 10.0
prueba = np.array_split(np.arange(n), 5)[2]            # tercer pliegue: indices 40 a 59
inicio, fin = t0[prueba].min(), t1[prueba].max()       # ventana de prueba [40, 69)
entreno = np.setdiff1d(np.arange(n), prueba)

# Purga: fuera toda etiqueta de entrenamiento que toque la ventana de prueba.
contaminado = entreno[(t1[entreno] >= inicio) & (t0[entreno] <= fin)]
# Embargo: fuera ademas el tramo inmediatamente posterior al pliegue.
span = t1.max() - t0.min()
embargadas = entreno[(t0[entreno] > fin) & (t0[entreno] <= fin + 0.02 * span)]
limpio = np.setdiff1d(entreno, np.concatenate([contaminado, embargadas]))
sanos = np.setdiff1d(entreno, contaminado)

fig, ejes = plt.subplots(2, 1, figsize=(7.2, 5.8), sharex=True)

# --- Arriba: el K-fold de manual, con parte del entrenamiento contaminado -------------
ejes[0].broken_barh([(i, 10) for i in sanos], (0.05, 0.9), facecolors=VERDE, alpha=0.35)
ejes[0].broken_barh([(i, 10) for i in contaminado], (0.05, 0.9), facecolors=ROJO, alpha=0.75)
ejes[0].broken_barh([(i, 10) for i in prueba], (0.05, 0.9), facecolors=AZUL, alpha=0.95)
ejes[0].axvspan(inicio, fin, color=AZUL, alpha=0.10)
ejes[0].set_ylim(-0.15, 2.55)
ejes[0].set_yticks([])
ejes[0].set_ylabel("etiquetas")
titulo(ejes[0], f"K-fold normal: {contaminado.size} de las {entreno.size} de entrenamiento comparten precios",
       "cada barra es la vida de una etiqueta y la franja azul es la ventana de prueba")
anotar(ejes[0], "en rojo, etiquetas que el modelo usaría para entrenar\ny que solapan con lo que luego se le pide predecir",
       xy=(float(contaminado.min()), 1.45), xytext=(0.02, 0.80), color=ROJO)

# --- Abajo: la misma particion, con purga y embargo -----------------------------------
ejes[1].broken_barh([(i, 10) for i in limpio], (0.05, 0.9), facecolors=VERDE, alpha=0.8)
ejes[1].broken_barh([(i, 10) for i in contaminado], (0.05, 0.9), facecolors=ROSA, alpha=0.5)
ejes[1].broken_barh([(i, 10) for i in embargadas], (0.05, 0.9), facecolors=NARANJA, alpha=0.9)
ejes[1].broken_barh([(i, 10) for i in prueba], (0.05, 0.9), facecolors=AZUL, alpha=0.95)
ejes[1].axvspan(inicio, fin, color=AZUL, alpha=0.10)
ejes[1].axvspan(fin, fin + 0.02 * span, color=NARANJA, alpha=0.18)
ejes[1].set_ylim(-0.15, 2.55)
ejes[1].set_yticks([])
ejes[1].set_ylabel("etiquetas")
ejes[1].set_xlabel("observación (orden temporal, sin barajar)")
titulo(ejes[1], f"Con purga y embargo: {limpio.size} de {n} entrenan, 0 contaminan",
       "la estimación sale más pesimista y es la única que no se engaña a sí misma")
anotar(ejes[1], f"purga: {contaminado.size} etiquetas fuera", xy=(float(contaminado.min()), 0.98),
       xytext=(0.02, 0.88), color=ROSA)
anotar(ejes[1], f"embargo: {embargadas.size} más, justo después", xy=(fin + 0.5, 1.75),
       xytext=(0.02, 0.72), color=NARANJA)
anotar(ejes[1], "hueco ciego: las variables\ntodavía miran a la prueba", xy=(fin + 0.01 * span, 1.0),
       xytext=(0.62, 0.58), color=NARANJA, align="right")

guardar(fig, "purgado-purga-y-embargo")
