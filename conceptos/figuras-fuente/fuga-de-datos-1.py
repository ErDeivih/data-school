"""fuga-de-datos-1.py — cuatro formas de fuga y la huella que deja cada una: métrica
perfecta, un coeficiente que lo absorbe todo, un valor extremo domesticado y un reparto
aleatorio que interpola. La figura de la pagina de fuga de datos."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# --- 1. La variable que es consecuencia del objetivo ------------------------------
n = 300
clase = azar.integers(0, 2, n)
senal = azar.normal(0, 1, n)                  # variable legitima, sin relacion con la clase
fuga = clase + azar.normal(0, 0.1, n)         # se conoce DESPUES de la etiqueta

mitad = n // 2


def exactitud(X, y):
    """Exactitud de una regresión lineal usada como clasificador de umbral 0,5."""
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    return float(np.mean((X @ b > 0.5) == y))


acc_fuga = exactitud(np.column_stack([np.ones(mitad), senal[:mitad], fuga[:mitad]]), clase[:mitad])
acc_senal = exactitud(np.column_stack([np.ones(mitad), senal[:mitad]]), clase[:mitad])

# Pesos estandarizados: con la variable de fuga dentro, la senal legitima se queda sin peso.
def pesos_estandarizados(X, y):
    Z = (X - X.mean(0)) / X.std(0)
    b, *_ = np.linalg.lstsq(np.column_stack([np.ones(Z.shape[0]), Z]), y, rcond=None)
    return b[1:]


pesos = pesos_estandarizados(np.column_stack([senal, fuga]), clase.astype(float))
peso_senal, peso_fuga = pesos[0], pesos[1]

# --- 2. El escalador ajustado con todo el conjunto --------------------------------
datos = np.array([2.0, 4.0, 6.0, 8.0, 998.0])
mal = (998.0 - datos.mean()) / datos.std()            # media 203,6 y desviacion 397,6
bien = (998.0 - datos[:4].mean()) / datos[:4].std()   # media 5 y desviacion 2,58

# --- 3. Reparto aleatorio en una serie temporal -----------------------------------
n4 = 300
t4 = np.arange(n4)
y4 = np.sin(2 * np.pi * t4 / 50) + azar.normal(0, 0.3, n4)
reparto = azar.integers(0, 5, n4)                      # pliegue asignado al azar
bloques = np.array_split(np.arange(n4), 5)

fig, ejes = plt.subplots(2, 2, figsize=(11.0, 7.6))

# Panel 1: la metrica que no se cree
eje = ejes[0, 0]
barras = eje.bar([1, 2], [acc_fuga, acc_senal], width=0.5, color=[ROJO, VERDE], alpha=0.85)
for x, v in zip([1, 2], [acc_fuga, acc_senal]):
    eje.text(x, v + 0.03, f"{v:.2f}".replace(".", ","), color=TEXTO, fontsize=10, ha="center")
eje.axhline(0.5, color=TEXTO, linewidth=1.0, linestyle="--")
eje.text(0.55, 0.53, "el azar acierta el 50 %", color=TEXTO, fontsize=8.5)
eje.set_ylim(0, 1.18)
eje.set_xticks([1, 2])
eje.set_xticklabels(["con la variable\nde fuga", "solo con la\nsenal legitima"])
eje.set_title("Un acierto perfecto delata la fuga")
eje.set_ylabel("exactitud en prueba")
anotar(eje, "esta columna solo existe si el\nimpago ya ha ocurrido: en el\nmomento de predecir vale cero",
       (1.0, acc_fuga), (0.55, 0.62), ROJO)
rejilla(eje)
numeros(eje)

# Panel 2: que variable se lleva el peso
eje = ejes[0, 1]
pesos = [peso_fuga, peso_senal]
eje.barh([1, 0], pesos, height=0.45, color=[ROJO, AZUL])
eje.text(pesos[0] - 0.03, 1, f"{pesos[0]:.1f}", color=TEXTO, fontsize=9.5, ha="right", va="center")
eje.set_yticks([0, 1])
eje.set_yticklabels(["senal legitima", "variable de fuga"])
eje.set_xlim(-0.35, max(pesos) * 1.18)
eje.set_title("La fuga se lleva todo el peso del modelo")
eje.set_xlabel("peso de cada variable, en desviaciones tipicas")
anotar(eje, "la senal legitima casi no\nrecibe peso: el modelo\nno ha aprendido nada",
       (max(pesos[1], 0.0), 0.0), (0.34, 0.44), AZUL)
eje.axvline(0, color=TEXTO, linewidth=0.8, alpha=0.5)
rejilla(eje, eje="x")
numeros(eje, ejes="x")

# Panel 3: el mismo valor, dos escalados
eje = ejes[1, 0]
eje.scatter([mal, bien], [1, 0], color=[ROJO, VERDE], s=80, zorder=5)
eje.plot([mal, bien], [1, 0], color=REJILLA, linewidth=1.0, linestyle=":")
eje.set_xscale("log")
eje.set_xlim(0.5, 2000)
eje.set_ylim(-0.7, 1.7)
eje.set_yticks([1, 0])
eje.set_yticklabels(["escalador ajustado\ncon las 5 filas",
                     "escalador ajustado\ncon 4 filas"])
eje.set_title("El mismo 998, domesticado o enorme")
eje.set_xlabel("valor que le llega al modelo (escala logaritmica)")
eje.text(mal, 1.28, f"{mal:.2f}".replace(".", ","), color=ROJO, fontsize=10, ha="center")
eje.text(bien, 0.28, f"{bien:.1f}".replace(".", ","), color=VERDE, fontsize=10, ha="center")
anotar(eje, "con la media contaminada, un 998\nparece un valor casi normal:\n2,0 desviaciones",
       (mal, 1.0), (0.02, 0.60), ROJO)
rejilla(eje, eje="x")
numeros(eje, ejes="x")

# Panel 4: reparto aleatorio frente a reparto por bloques
eje = ejes[1, 1]
entrenamiento = reparto != 0
prueba = reparto == 0
eje.scatter(t4[entrenamiento], y4[entrenamiento], color=AZUL, s=16, label="entrenamiento")
eje.scatter(t4[prueba], y4[prueba], color=ROJO, s=20, marker="s", label="prueba")
eje.axvspan(bloques[0][-1], n4, color=REJILLA, alpha=0.22, zorder=0)
eje.text(295, -1.95, "la prueba es la parte\nsombreada: el futuro",
         color=TEXTO, fontsize=9, va="bottom", ha="right")
eje.set_ylim(-2.1, 2.3)
eje.set_title("Barajar mezcla prueba entre el entrenamiento")
eje.set_xlabel("dia")
eje.set_ylabel("la serie")
eje.legend(loc="lower left", fontsize=8)
eje.annotate("puntos de prueba rodeados de dias\nque el modelo ya ha visto:\nacierta interpolando",
             xy=(t4[prueba][3], y4[prueba][3]), xycoords="data",
             xytext=(0.02, 0.97), textcoords="axes fraction", fontsize=8.5, color=ROJO,
             va="top", ha="left",
             arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9, shrinkA=2, shrinkB=2))
rejilla(eje)
numeros(eje)

guardar(fig, "fuga-de-datos-cuatro-huellas")
