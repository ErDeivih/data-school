"""testing-piramide-1.py — donde se va de verdad el tiempo de una suite: la proporción de la
piramide no la fija la elegancia, la fija la duración de las pruebas de extremo a extremo. La
figura de la pagina de la piramide de pruebas (fase 11)."""

import numpy as np

from comun import *

estilo()

# Los mismos numeros del ejemplo de la pagina: 800 unitarias, 120 de integracion y 8 de e2e.
capas = ["unitarias", "integración", "e2e"]
cantidades = np.array([800, 120, 8])
duraciones = np.array([0.002, 0.400, 12.0])
aportes = cantidades * duraciones              # producto elemento a elemento, no producto matricial
total = aportes.sum()
colores = [VERDE, AZUL, NARANJA]

# Dos filas: arriba el tiempo que pone cada nivel, abajo el reparto de pruebas frente al
# reparto de tiempo. Con los dos paneles anchos, las etiquetas de las barras no se salen.
fig, (arriba, abajo) = plt.subplots(2, 1, figsize=(10.2, 7.6))
fig.set_constrained_layout_pads(h_pad=0.12)   # aire entre los dos paneles (la leyenda va ahí)

# --- Arriba: cuanto pone cada nivel al tiempo total --------------------------------
barras = arriba.barh(capas, aportes, color=colores, height=0.6)
# El porcentaje va en la etiqueta: en segundos, 1,6 frente a 96 no se ve en una barra corta.
etiquetas = [f"{a:.1f} s  ({a / total:.0%})" for a in aportes]
arriba.bar_label(barras, labels=etiquetas, padding=4, fontsize=9)
arriba.invert_yaxis()                          # unitarias arriba: el orden en que se lee
arriba.set_xlim(0, aportes.max() * 1.40)       # margen para que quepa la etiqueta de la barra
titulo(arriba, "8 pruebas de e2e son el 66 % del tiempo")
arriba.set_xlabel("segundos de la suite completa")
rejilla(arriba, eje="x")
numeros(arriba)

# --- Abajo: reparto de pruebas contra reparto de tiempo ----------------------------
# Fila 0: que parte de las 928 pruebas es de cada nivel. Fila 1: que parte del tiempo.
for i, (capa, color) in enumerate(zip(capas, colores)):
    proporcion_pruebas = cantidades[i] / cantidades.sum()
    proporcion_tiempo = aportes[i] / total
    # Barra apilada: el desplazamiento left es la suma de los tramos anteriores.
    abajo.barh(0, proporcion_pruebas, left=sum(cantidades[:i]) / cantidades.sum(),
               color=color, height=0.5, label=capa)
    abajo.barh(1, proporcion_tiempo, left=sum(aportes[:i]) / total,
               color=color, height=0.5)
abajo.set_yticks([0, 1], ["pruebas\n(928 en total)", "tiempo\n(145,6 s en total)"])
abajo.set_xlim(0, 1)
abajo.invert_yaxis()                           # la fila de arriba es la de las pruebas
# La leyenda va debajo del eje para no tapar los tramos delgados (las unitarias son el 1 %).
abajo.legend(loc="upper center", ncols=3, bbox_to_anchor=(0.5, -0.13), fontsize=9)
titulo(abajo, "El 1 % de las pruebas se lleva dos tercios del tiempo")
abajo.set_xlabel("proporción del total (0 a 1)")
rejilla(abajo, eje="x")
# Solo el eje x: numeros(abajo) con los dos ejes sustituiria las etiquetas "pruebas" y "tiempo".
numeros(abajo, ejes="x")

guardar(fig, "testing-piramide-reparto-del-tiempo")
