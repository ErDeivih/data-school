"""gradient-boosting-1.py — la tasa de aprendizaje decide cuanto corrige cada árbol, y con
ella cuando el modelo empieza a sobreajustar. Pagina de gradient boosting (fase 6)."""

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import train_test_split

from comun import *

estilo()
azar = np.random.default_rng(7)

# Una señal suave (un seno) con ruido: la parte que el modelo no puede aprender.
X = azar.uniform(-3, 3, size=(300, 1))
y = np.sin(X[:, 0]) + azar.normal(scale=0.35, size=300)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4, random_state=7)

tasa_media = np.sqrt(((y_te - y_tr.mean()) ** 2).mean())   # RMSE de predecir siempre la media
pasos = np.arange(1, 301)

curvas = []          # (nu, iteraciones, rmse de validacion, indice del minimo)
for nu, color in ((0.05, VERDE), (0.15, AZUL), (0.6, ROJO)):
    modelo = GradientBoostingRegressor(n_estimators=300, learning_rate=nu, max_depth=2,
                                       random_state=0).fit(X_tr, y_tr)
    # staged_predict devuelve la prediccion tras cada arbol, uno a uno.
    val = np.array([np.sqrt(((y_te - p) ** 2).mean()) for p in modelo.staged_predict(X_te)])
    curvas.append((nu, val, int(np.argmin(val)), color))

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.8))

# --- Izquierda: la curva que hay que mirar, con su minimo marcado.
for nu, val, k, color in curvas:
    ejes[0].plot(pasos, val, color=color, linewidth=1.7, label=f"ν = {coma(nu)}")
    ejes[0].plot(k + 1, val[k], marker="o", markersize=7, color=color,
                 markeredgecolor="white", markeredgewidth=1.0, zorder=5)
anotar(ejes[0], "ν = 0,6 se pasa antes\nde 10 árboles",
       xy=(8, curvas[2][1][7]), xytext=(0.03, 0.90), color=ROJO)
anotar(ejes[0], "aquí ν = 0,6 ya solo empeora:\nparada temprana",
       xy=(60, curvas[2][1][59]), xytext=(0.30, 0.42), color=ROJO)
anotar(ejes[0], "al final de la ventana,\nν = 0,05 aún mejora",
       xy=(280, curvas[0][1][279]), xytext=(0.36, 0.92), color=VERDE)
titulo(ejes[0], "Tasa grande: antes mejora y antes se pasa",
       "error en datos no vistos; el punto marca dónde está el mínimo")
ejes[0].set_xlabel("árboles sumados (etapas de boosting)")
ejes[0].set_ylabel("RMSE en validación")
ejes[0].set_xlim(0, 300)
ejes[0].set_ylim(0.30, 0.82)
ejes[0].legend(loc="center right")
rejilla(ejes[0])
numeros(ejes[0], ejes="both")

# --- Derecha: lo mismo visto como presupuesto de corrección (curvas entrenamiento/prueba).
for nu, val, k, color in curvas:
    modelo = GradientBoostingRegressor(n_estimators=300, learning_rate=nu, max_depth=2,
                                       random_state=0).fit(X_tr, y_tr)
    tr = np.array([np.sqrt(((y_tr - p) ** 2).mean()) for p in modelo.staged_predict(X_tr)])
    ejes[1].plot(pasos, tr, color=color, linewidth=1.7, label=f"ν = {coma(nu)}: entrenamiento")
    ejes[1].plot(pasos, val, color=color, linewidth=1.2, linestyle="--", alpha=0.85,
                 label=f"ν = {coma(nu)}: validación")
ejes[1].axhline(tasa_media, color=TEXTO, linewidth=1.0, linestyle=":")
anotar(ejes[1], "predecir siempre la media:\nel listón a batir",
       xy=(150, tasa_media), xytext=(0.04, 0.55), color=TEXTO)
anotar(ejes[1], "el error de entrenamiento\nbaja siempre: no informa",
       xy=(200, 0.10), xytext=(0.08, 0.30), color=MORADO)
titulo(ejes[1], "El error de entrenamiento no informa de nada",
       "baja siempre; el que decide es el de validación (línea discontinua)")
ejes[1].set_xlabel("árboles sumados (etapas de boosting)")
ejes[1].set_ylabel("RMSE")
ejes[1].set_xlim(0, 300)
ejes[1].set_ylim(0, 0.85)
ejes[1].legend(loc="upper right", fontsize=7.6, ncol=2, bbox_to_anchor=(1.0, 0.96))
rejilla(ejes[1])
numeros(ejes[1], ejes="both")

guardar(fig, "boosting-tasa-de-aprendizaje-y-parada")
