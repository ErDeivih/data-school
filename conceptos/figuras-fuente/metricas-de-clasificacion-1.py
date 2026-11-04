"""metricas-de-clasificacion-1.py - las métricas de un mismo detector cuentan historias
distintas, y todas dependen del umbral. Figura de la pagina de métricas de clasificación
(fase 6)."""

import numpy as np

from comun import *

estilo()

# --- Izquierda: el detector de fraude de la pagina. 1.000 operaciones, 20 fraudes reales,
# 30 alertas disparadas y 18 aciertos. Los cinco numeros salen de la misma matriz.
vp, fp, fn, vn = 18, 12, 2, 968
exactitud = (vp + vn) / (vp + fp + fn + vn)
precision = vp / (vp + fp)
exhaustividad = vp / (vp + fn)
especificidad = vn / (vn + fp)
f1 = 2 * precision * exhaustividad / (precision + exhaustividad)
balanced = (exhaustividad + especificidad) / 2
# El trivial que dice "no" a todo: su exactitud es la tasa de negativos de la poblacion, es
# decir, todos los que no son fraude (los verdaderos negativos mas los falsos positivos).
trivial = (vn + fp) / 1000

nombres = ["exactitud", "balanced\naccuracy", "F1", "precisión", "exhaustividad"]
valores = [exactitud, balanced, f1, precision, exhaustividad]

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.4))

colores = [ROJO, AZUL, AZUL, AZUL, AZUL]
# Las barras van sin etiqueta y los nombres se ponen a mano mas pequenos: con el tamano
# normal, "precisión" y "exhaustividad" se tocaban.
ejes[0].bar(range(5), valores, color=colores, width=0.6)
ejes[0].set_xticks(range(5))
ejes[0].set_xticklabels(nombres, fontsize=8)
# La exactitud del detector (0,986) es casi identica a la del modelo que no detecta nada
# (0,980): por eso la exactitud sola no permite elegir entre los dos.
ejes[0].axhline(trivial, color=ROJO, linewidth=1.2, linestyle="--")
for k, valor in enumerate(valores):
    ejes[0].text(k, valor + 0.02, "%.3f" % valor, ha="center", fontsize=9, color=TEXTO)
# La nota es un rotulo pegado a la linea de puntos, a la derecha: a media altura cae encima
# de las etiquetas de las barras y abajo a la izquierda, sobre la barra roja.
ejes[0].text(3.7, trivial + 0.022, "un modelo que dice «no» a todo:\n0,980 de exactitud y cero fraudes",
             ha="left", va="bottom", fontsize=8.5, color=ROJO)
titulo(ejes[0], "Todos los números salen del mismo detector",
       "18 fraudes cazados de 20, con 30 alertas: la exactitud no dice si el modelo sirve")
ejes[0].set_ylabel("valor de la métrica")
ejes[0].set_ylim(0, 1.16)
# Un poco de aire a los lados: el "0" del eje vertical se pegaba a la palabra "exactitud".
ejes[0].margins(x=0.04)
rejilla(ejes[0], eje="y")
numeros(ejes[0], ejes="y")

# --- Derecha: mover el umbral mueve las tres metricas en direcciones distintas. Un caso
# sintetico mas equilibrado (25 % de positivos) para que las curvas se lean.
azar = np.random.default_rng(7)
etiqueta = azar.random(800) < 0.25
puntuacion = np.where(etiqueta, azar.beta(5, 2.2, 800), azar.beta(2.2, 5, 800))
umbrales = np.linspace(0.05, 0.95, 91)      # paso de 0,01: asi el indice 54 es el umbral 0,59
curvas = []
for u in umbrales:
    marca = puntuacion >= u
    aciertos = int((marca & etiqueta).sum())
    falsos = int((marca & ~etiqueta).sum())
    perdidos = int((~marca & etiqueta).sum())
    p = aciertos / max(aciertos + falsos, 1)
    r = aciertos / max(aciertos + perdidos, 1)
    curvas.append((p, r, 2 * p * r / max(p + r, 1e-9)))
curvas = np.array(curvas)

ejes[1].plot(umbrales, curvas[:, 0], color=AZUL, linewidth=1.8, label="precisión")
ejes[1].plot(umbrales, curvas[:, 1], color=VERDE, linewidth=1.8, label="exhaustividad")
ejes[1].plot(umbrales, curvas[:, 2], color=MORADO, linewidth=1.8, label="F1")
# La nota va abajo a la izquierda: por alli la curva mas baja es la de precision (0,27) y
# el texto queda debajo de las tres.
anotar(ejes[1], "el mejor F1 (0,80) esta en 0,60:\nni el umbral más alto ni el más bajo",
       xy=(0.40, 0.57), xytext=(0.03, 0.22), color=MORADO)
titulo(ejes[1], "Cambiar el umbral mueve las tres",
       "precisión y exhaustividad tiran en direcciones opuestas; F1 recoge el equilibrio")
ejes[1].set_xlabel("umbral de decisión")
ejes[1].set_ylabel("valor de la métrica")
ejes[1].set_ylim(0, 1.3)
# La leyenda va dentro del panel, arriba a la derecha: es el hueco que dejan las curvas.
ejes[1].legend(loc="upper right", ncol=1)
rejilla(ejes[1])
numeros(ejes[1], ejes="x")

guardar(fig, "clasificacion-metricas-y-umbral")
