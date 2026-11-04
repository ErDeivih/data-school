"""precision-recall-y-pr.py — la curva precisión-exhaustividad con su línea base (la
prevalencia) y la misma cuenta mirada desde el eje de la ROC. Figura de la página de la
curva precisión-exhaustividad (fase 6)."""

import numpy as np

from comun import *

estilo()

# --- Panel izquierdo: 100 positivos entre 10.000 casos (el 1 % del ejemplo de la página).
# Las puntuaciones son las mismas que usa el código de la página, para que los números
# de la figura y los del texto sean los mismos.
pos = np.r_[np.linspace(0.80, 0.99, 90), np.linspace(0.10, 0.60, 10)]
neg = np.r_[np.linspace(0.80, 0.99, 495), np.linspace(0.00, 0.79, 9405)]
y = np.r_[np.ones(100), np.zeros(9900)]
score = np.r_[pos, neg]

# Recorriendo las puntuaciones de mayor a menor se obtienen todos los umbrales a la vez:
# `tp` son los positivos ya capturados y `fp` las falsas alarmas acumuladas.
orden = np.argsort(-score, kind="stable")
aciertos = np.cumsum(y[orden])
falsas = np.cumsum(1 - y[orden])
# Solo interesan los puntos en los que entra un positivo: entre uno y el siguiente, la
# exhaustividad no cambia y la precisión solo baja. Dibujarlos todos deja una especie de
# peine ilegible.
donde = np.flatnonzero(y[orden] == 1)
precision = (aciertos / (aciertos + falsas))[donde]
exhaustividad = (aciertos / aciertos[-1])[donde]

# La AP es la suma escalonada: cada tramo de exhaustividad pesa por la precisión que deja.
ap = float((np.diff(np.r_[0.0, exhaustividad]) * precision).sum())
prevalencia = float(y.mean())

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.4))

ejes[0].fill_between(exhaustividad, precision, step="post", color=AZUL, alpha=0.12)
ejes[0].plot(exhaustividad, precision, color=AZUL, linewidth=1.8, drawstyle="steps-post")
ejes[0].axhline(prevalencia, color=ROJO, linewidth=1.4, linestyle="--")
anotar(ejes[0], "la primera alerta acierta y a partir de ahí\ntodo se aplana en 0,15: nueve de cada\ndiez alertas son falsas",
       xy=(0.45, 0.15), xytext=(0.28, 0.72), color=AZUL)
anotar(ejes[0], "el azar: la precisión cae a la prevalencia (0,01)",
       xy=(0.9, prevalencia), xytext=(0.20, 0.42), color=ROJO, flecha=False)
ejes[0].set_xlim(-0.02, 1.02)
ejes[0].set_ylim(-0.03, 1.05)
ejes[0].set_xlabel("exhaustividad (positivos capturados)")
ejes[0].set_ylabel("precisión\n(alertas que eran reales)")
rejilla(ejes[0], "both")
numeros(ejes[0])
titulo(ejes[0], "La curva PR y su línea base honesta",
       f"AP ≈ {ap:.2f}".replace(".", ",") + " frente a un azar de 0,01: quince veces mejor")

# --- Panel derecho: la fórmula que une las dos curvas, dibujada. Con el mismo TPR, la
# precisión que se ve depende de cuántos negativos haya por cada positivo.
fpr = np.logspace(-3, 0, 300)
for pi, color in ((0.5, VERDE), (0.1, NARANJA), (0.01, ROJO)):
    curva = 0.9 * pi / (0.9 * pi + fpr * (1 - pi))
    ejes[1].plot(fpr, curva, color=color, linewidth=1.8)
    # El rótulo va al final de cada curva, fuera del dibujo: así no hay caja de leyenda
    # que tapar y se ve a qué prevalencia pertenece cada línea sin buscarla.
    ejes[1].text(1.25, curva[-1], f"prevalencia {pi:.0%}".replace("%", " %"), color=color,
                 fontsize=9, va="center", ha="left")
anotar(ejes[1], "con un 1 % de positivos, ni un FPR\ndel 1 % deja la precisión en 0,5",
       xy=(0.01, 0.476), xytext=(0.03, 0.14), color=ROJO)
ejes[1].set_xscale("log")
ejes[1].set_xlim(0.0008, 6.0)
ejes[1].set_ylim(-0.03, 1.05)
ejes[1].set_xlabel("tasa de falsos positivos (escala logarítmica)")
ejes[1].set_ylabel("precisión, con un TPR fijo de 0,90")
rejilla(ejes[1])
numeros(ejes[1], ejes="y")
titulo(ejes[1], "La misma cuenta mirada desde el FPR",
       "la precisión no depende solo del modelo: depende de cuántos negativos haya")

guardar(fig, "pr-curva-y-linea-base")
