"""stacking-y-blending-1.py — el metamodelo aprende a quien creer, y de que predicciones
aprende lo cambia todo. Pagina de stacking y blending (fase 6)."""

import numpy as np

from comun import *

estilo()

# Dos modelos base, medidos de las dos formas del ejemplo de la pagina.
auc_en_muestra = np.array([0.95, 0.82])     # lo que dice cada base sobre los datos que vio
auc_fuera = np.array([0.87, 0.78])          # lo que hace de verdad en datos nuevos

# El metamodelo pondera cada base por su acierto menos el azar (tasa base 0,5).
pesos_en_muestra = (auc_en_muestra - 0.5) / (auc_en_muestra - 0.5).sum()
pesos_fuera = (auc_fuera - 0.5) / (auc_fuera - 0.5).sum()

auc_media_simple = auc_fuera.mean()
auc_stack_en_muestra = pesos_en_muestra @ auc_fuera
auc_stack_fuera = pesos_fuera @ auc_fuera

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.4))

# --- Izquierda: los pesos que aprende el metamodelo en cada caso.
ancho = 0.36
pos = np.arange(2)
ejes[0].bar(pos - ancho / 2, pesos_en_muestra, ancho, color=ROJO)
ejes[0].bar(pos + ancho / 2, pesos_fuera, ancho, color=VERDE)
for x, v in zip(pos - ancho / 2, pesos_en_muestra):
    ejes[0].text(x, v + 0.02, coma(round(v, 2)), ha="center", fontsize=8.5, color=ROJO)
for x, v in zip(pos + ancho / 2, pesos_fuera):
    ejes[0].text(x, v + 0.02, coma(round(v, 2)), ha="center", fontsize=8.5, color=VERDE)
# Las dos series se explican con texto en el propio gráfico: la leyenda tapaba las barras.
ejes[0].text(0.34, 1.10, "rojo: en muestra    verde: fuera de muestra", fontsize=8,
             color=ROJO)
anotar(ejes[0], "al base que memoriza se le da\ncasi todo el peso: 0,95",
       xy=(-ancho / 2, 0.97), xytext=(0.28, 0.60), color=ROJO)
anotar(ejes[0], "medido en datos nuevos, el reparto\nvuelve a ser razonable",
       xy=(1 + ancho / 2, 0.52), xytext=(0.29, 0.84), color=VERDE)
titulo(ejes[0], "El peso depende de cómo midas el base",
       "misma receta, mismas filas: solo cambia de dónde salen las predicciones")
ejes[0].set_xticks(pos)
ejes[0].set_xticklabels(["base que memoriza", "base que generaliza"])
ejes[0].set_ylabel("peso que aprende el metamodelo")
ejes[0].set_ylim(0, 1.15)
rejilla(ejes[0])
numeros(ejes[0], ejes="y")

# --- Derecha: el resultado final con cada forma de construir la matriz Z.
nombres = ["base que\nmemoriza", "base que\ngeneraliza", "promedio\nsimple",
           "stacking\nen muestra", "stacking\nfuera de muestra"]
valores = [auc_fuera[0], auc_fuera[1], auc_media_simple, auc_stack_en_muestra, auc_stack_fuera]
colores = [REJILLA, REJILLA, AZUL, ROJO, VERDE]
ejes[1].bar(np.arange(5), valores, 0.62, color=colores)
for x, v in enumerate(valores):
    ejes[1].text(x, v + 0.004, coma(round(v, 3)), ha="center", fontsize=8.5, color=TEXTO)
ejes[1].axhline(auc_fuera.max(), color=TEXTO, linewidth=1.2, linestyle="--")
anotar(ejes[1], "mejor base solo: 0,780",
       xy=(1.6, auc_fuera.max()), xytext=(0.06, 0.96), color=TEXTO)
titulo(ejes[1], "La métrica se decide en la primera capa",
       "AUC de cada base y del mismo ensemble según cómo se generó la matriz Z")
ejes[1].set_xticks(np.arange(5))
ejes[1].set_xticklabels(nombres, fontsize=7.5)
ejes[1].set_ylabel("AUC en datos nuevos")
ejes[1].set_ylim(0.70, 0.92)
rejilla(ejes[1])
numeros(ejes[1], ejes="y")

guardar(fig, "stacking-pesos-en-muestra-y-fuera")
