"""glm-y-logistica-1.py — la sigmoide, el logit, los datos del ejemplo y la
verosimilitud: cuatro vistas de la misma función de enlace (fase 6)."""

import numpy as np

from comun import *

estilo()

# Las doce observaciones del ejemplo de la pagina: horas de estudio y aprobado (1/0).
x = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0, 7.0])
y = np.array([0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1])

# Coeficientes que se obtienen al ajustar la logistica (estan en la pagina).
b0, b1 = -4.774, 1.271
eta = np.linspace(-6, 6, 400)
sigmoide = 1 / (1 + np.exp(-eta))

# Dos filas y dos columnas: tres paneles en una sola fila se pisan (esta medido en
# _comprobar-figuras.mjs). El cuarto hueco se borra.
fig, rejilla_ejes = plt.subplots(2, 2, figsize=(10.6, 7.2))
ejes = [rejilla_ejes[0][0], rejilla_ejes[0][1], rejilla_ejes[1][0]]
fig.delaxes(rejilla_ejes[1][1])

# --- (a) El predictor lineal contra la probabilidad ---------------------------
ejes[0].axvspan(-6, 0, color=AZUL, alpha=0.06)
ejes[0].axvspan(0, 6, color=VERDE, alpha=0.06)
ejes[0].plot(eta, sigmoide, color=AZUL, linewidth=2.0)
ejes[0].axhline(0.5, color=REJILLA, linewidth=1.0, linestyle="--")
ejes[0].axvline(0, color=ROJO, linewidth=0.9, linestyle=":")
ejes[0].set_xlabel("predictor lineal η")
ejes[0].set_ylabel("probabilidad estimada")
ejes[0].set_ylim(-0.05, 1.05)
ejes[0].text(0.15, 0.505, "umbral 0,5", color=ROJO, fontsize=8.5, va="bottom")
anotar(ejes[0], "Lejos del centro la curva se pega\na 0 o a 1: una unidad más de η\ncasi no mueve la probabilidad",
       xy=(4.6, 0.93), xytext=(0.04, 0.72))
titulo(ejes[0], "La sigmoide aplasta cualquier valor",
       "η puede valer ±∞; la probabilidad se queda en [0, 1]")
rejilla(ejes[0])
numeros(ejes[0])

# --- (b) El logit: la escala en la que el modelo sí es lineal -----------------
# Mezclo dos rejillas: fina cerca de 0,5 (donde el logit es casi lineal) y gruesa en
# las colas (donde se dispara). Por eso hay dos leyendas.
probs_cerca = np.linspace(0.42, 0.58, 160)
probs_colas = np.concatenate([np.linspace(0.01, 0.42, 80), np.linspace(0.58, 0.99, 80)])
ejes[1].plot(probs_cerca, np.log(probs_cerca / (1 - probs_cerca)), color=AZUL,
             linewidth=1.6, label="zona central: casi una recta")
ejes[1].plot(probs_colas, np.log(probs_colas / (1 - probs_colas)), color=ROJO,
             linewidth=1.8, label="colas: el logit se dispara")
# Las etiquetas van por encima de la curva y a la izquierda del punto: dentro del hueco
# caerian sobre la propia linea del logit.
for p, nom, dx, dy in ((0.5, "logit 0", 0.10, 0.30),
                       (0.9, "logit 2,20", 0.08, 0.15),
                       (0.99, "logit 4,60", 0.07, 0.55)):
    valor = np.log(p / (1 - p))
    ejes[1].plot([p], [valor], "o", color=TEXTO, markersize=5)
    ejes[1].text(p - dx, valor + dy, nom, color=TEXTO, fontsize=8, ha="right", va="bottom")
ejes[1].set_xlabel("probabilidad p")
ejes[1].set_ylabel("logit(p) = ln(p / (1 − p))")
ejes[1].set_ylim(-5.6, 6.2)
ejes[1].legend(loc="upper left", fontsize=8)
anotar(ejes[1], "Un coeficiente suma lo mismo en logit,\npero mueve la probabilidad mucho más\nen el centro que en los extremos",
       xy=(0.965, 3.5), xytext=(0.02, 0.62))
titulo(ejes[1], "El logit estira los extremos",
       "de 0,01 a 0,99 el logit recorre de −4,6 a 4,6")
rejilla(ejes[1])
numeros(ejes[1])

# --- (c) Los datos del ejemplo y la curva ajustada ----------------------------
horas = np.linspace(0.8, 7.3, 300)
prob = 1 / (1 + np.exp(-(b0 + b1 * horas)))
# Separo un poco los ceros y los unos para que se vean los dos grupos de puntos.
ejes[2].plot(x[y == 0], np.full((y == 0).sum(), -0.045), "o", color=MORADO,
             markersize=6, label="suspende (0)")
ejes[2].plot(x[y == 1], np.full((y == 1).sum(), 1.045), "o", color=VERDE,
             markersize=6, label="aprueba (1)")
ejes[2].plot(horas, prob, color=AZUL, linewidth=2.0, label="probabilidad ajustada")
ejes[2].axhline(0.5, color=REJILLA, linewidth=1.0, linestyle="--")
ejes[2].axvline((0.5 - b0) / b1, color=ROJO, linewidth=0.9, linestyle=":")
ejes[2].set_xlabel("horas de estudio")
ejes[2].set_ylabel("resultado y probabilidad")
ejes[2].set_ylim(-0.18, 1.35)
ejes[2].legend(loc="lower right", fontsize=8)
# Una sola linea, a la izquierda de la frontera: el cruce con el 0,5 se lee en el punto
# donde la curva corta la raya de puntos, y la explicacion larga va en el pie.
ejes[2].text(1.0, 0.78, "la frontera del 0,5, en\n3,76 horas", fontsize=8.5, va="bottom")
titulo(ejes[2], "Una recta no vale para un 0/1",
       "con 4 horas la probabilidad ya es 0,576")
rejilla(ejes[2])
numeros(ejes[2])

guardar(fig, "glm-sigmoide-y-logit")
