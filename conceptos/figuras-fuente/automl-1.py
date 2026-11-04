"""automl-1.py — lo que anuncia un buscador automático es un techo, no una promesa: el
ganador de cien configuraciones parece mucho mejor que el montón y su ventaja se deshincha
en datos nuevos. Figura de la página de AutoML (fase 6)."""

import numpy as np
from sklearn.datasets import make_regression
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score, train_test_split

from comun import *

estilo()
desvio = np.random.default_rng(7)

# Misma receta que el ejemplo de la página: señal débil (2 variables informan de 8) y mucho
# ruido, que es el escenario donde "el mejor de N" engaña.
X, y = make_regression(n_samples=150, n_features=8, n_informative=2, noise=45.0, random_state=0)

puntuaciones, pruebas = [], []
for semilla in range(3):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=semilla)
    azar = np.random.default_rng(semilla)
    alphas = 10 ** azar.uniform(-3, 3, size=100)         # 100 configuraciones al azar
    notas = np.array([cross_val_score(Ridge(alpha=a), X_tr, y_tr, cv=3,
                                      scoring="r2").mean() for a in alphas])
    puntuaciones.append(notas)
    pruebas.append(Ridge(alpha=alphas[int(np.argmax(notas))]).fit(X_tr, y_tr).score(X_te, y_te))
puntuaciones = np.array(puntuaciones)                    # 3 repartos x 100 configuraciones
pruebas = np.array(pruebas)

# El máximo acumulado es el número que el buscador va anunciando según gasta presupuesto.
mejor = np.maximum.accumulate(puntuaciones, axis=1)
intentos = np.arange(1, 101)

fig, ejes = plt.subplots(1, 2, figsize=(11.2, 4.4))

# --- Izquierda: los tres repartos, cada uno con sus 100 configuraciones. El desplazamiento
# horizontal es solo para que los puntos no se dibujen unos encima de otros.
for j in range(3):
    ejes[0].scatter(j + desvio.uniform(-0.16, 0.16, 100), puntuaciones[j], color=AZUL,
                    s=12, alpha=0.5, linewidths=0, zorder=3)
    # La mediana está donde estaría un intento cualquiera: el nivel real del montón.
    ejes[0].plot([j - 0.24, j + 0.24], [np.median(puntuaciones[j])] * 2, color=MORADO,
                 linewidth=1.8, zorder=4)
ganadores = puntuaciones.max(axis=1)
ejes[0].scatter(np.arange(3), ganadores, color=ROJO, s=70, zorder=5)
ejes[0].axhline(0, color=TEXTO, linewidth=1.0, linestyle="--")
anotar(ejes[0], "en rojo, el máximo de las 100:\nes lo que devuelve el buscador",
       xy=(2.0, ganadores[2]), xytext=(0.04, 0.86), color=ROJO)
anotar(ejes[0], "en morado, la mediana del montón", xy=(2.0, float(np.median(puntuaciones[2]))),
       xytext=(0.97, 0.055), color=MORADO, align="right")
ejes[0].set_xticks(np.arange(3), ["reparto 0", "reparto 1", "reparto 2"])
ejes[0].set_xlim(-0.45, 2.45)
ejes[0].set_ylim(-0.10, 0.15)
titulo(ejes[0], "Cien configuraciones por reparto",
       "regresión Ridge con 100 valores de alpha; la etiqueta tiene señal débil")
ejes[0].set_ylabel("puntuación en validación cruzada (R²)")
ejes[0].set_xlabel("reparto de los datos en entrenamiento y prueba")
rejilla(ejes[0])
numeros(ejes[0], ejes="y")

# --- Derecha: el mismo presupuesto, gastado poco a poco. Cada línea fina es un reparto.
for j in range(3):
    ejes[1].plot(intentos, mejor[j], color=ROJO, linewidth=1.0, alpha=0.4)
ejes[1].plot(intentos, mejor.mean(axis=0), color=ROJO, linewidth=2.0, label="media de los 3 repartos")
anotar(ejes[1], "el buscador solo puede subir:\nse queda con lo mejor que ha visto",
       xy=(20, mejor.mean(axis=0)[19]), xytext=(0.06, 0.90), color=ROJO)
ejes[1].legend(loc="lower right")
titulo(ejes[1], "El número sube con el presupuesto gastado",
       "aunque el modelo no mejore: es el máximo de 100 mediciones ruidosas")
ejes[1].set_xlabel("configuraciones probadas (presupuesto)")
ejes[1].set_ylabel("mejor puntuación vista hasta ahora")
rejilla(ejes[1])
numeros(ejes[1], ejes="y")

guardar(fig, "automl-el-mejor-de-n-engana")
print("mediana por reparto:", np.median(puntuaciones, axis=1).round(3).tolist())
print("ganador en validación:", ganadores.round(3).tolist())
print("el mismo en prueba:", pruebas.round(3).tolist())
print("mejor acumulado: primero %.3f, a los 100 %.3f" % (mejor.mean(axis=0)[0],
                                                         mejor.mean(axis=0)[-1]))
