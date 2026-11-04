"""sesgo-varianza-1.py - las tres piezas del error esperado y por qué el mínimo no esta
en el modelo más flexible. Figura de la pagina del compromiso sesgo-varianza (fase 6)."""

import numpy as np

from comun import *

estilo()

# f(x) = sen(2 pi x) en 30 puntos con ruido de desviacion 0,3: el experimento de la pagina
def f(x):
    return np.sin(2 * np.pi * x)

azar = np.random.default_rng(7)
x = np.linspace(0, 1, 30)
sigma, replicas = 0.3, 300
grados = [0, 1, 2, 3, 4, 5, 6, 7, 9]

# 300 muestras distintas por grado: el sesgo y la varianza son propiedades del PROCEDIMIENTO
# de ajuste, no de un ajuste concreto, asi que hay que repetir el ajuste muchas veces.
pred = {g: np.zeros((replicas, x.size)) for g in grados}
for r in range(replicas):
    y = f(x) + azar.normal(0, sigma, x.size)
    for g in grados:
        pred[g][r] = np.polyval(np.polyfit(x, y, g), x)

sesgo2, varianza = [], []
for g in grados:
    media = pred[g].mean(axis=0)              # prediccion media sobre las 300 replicas
    sesgo2.append(np.mean((media - f(x)) ** 2))
    varianza.append(np.mean(pred[g].var(axis=0)))
sesgo2, varianza = np.array(sesgo2), np.array(varianza)
error = sesgo2 + varianza

# Una sola muestra, la primera de las 300: sirve para ensenar el sobreajuste a ojo
y_muestra = f(x) + azar.normal(0, sigma, x.size)
xs = np.linspace(0, 1, 400)

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.2))

# --- Izquierda: los tres sumandos, en la misma escala. El minimo esta en el grado 5.
ejes[0].plot(grados, sesgo2, color=AZUL, linewidth=1.8, marker="o", markersize=4.5,
             label="sesgo al cuadrado")
ejes[0].plot(grados, varianza, color=ROJO, linewidth=1.8, marker="s", markersize=4.5,
             label="varianza")
ejes[0].plot(grados, error, color=MORADO, linewidth=2.0, marker="D", markersize=4.5,
             label="error del estimador (su suma)")
ejes[0].set_yscale("log")
ejes[0].set_ylim(8e-5, 3)
# La nota va arriba a la izquierda: ahi el unico trazo que pasa es el del sesgo, y se lee
# sin tapar ninguna marca.
anotar(ejes[0], "del grado 5 al 9 el sesgo ya no baja\ny la varianza sube un 63 %",
       xy=(9, varianza[-1]), xytext=(0.06, 0.88), color=ROJO)
titulo(ejes[0], "El error se reparte en dos piezas",
       "el mínimo no esta ni en el modelo más simple ni en el más complejo")
ejes[0].set_xlabel("complejidad del modelo (grado del polinomio)")
ejes[0].set_ylabel("error cuadrático medio (escala logaritmica)")
ejes[0].set_xticks(grados)
ejes[0].legend(loc="lower left")
rejilla(ejes[0])
numeros(ejes[0])

# --- Derecha: que significa memorizar el ruido. Los mismos 30 datos con grado 3 y con grado 9.
ejes[1].plot(xs, f(xs), color=TEXTO, linewidth=1.4, linestyle="--", label="función verdadera")
ejes[1].plot(xs, np.polyval(np.polyfit(x, y_muestra, 3), xs), color=VERDE, linewidth=2.0,
             label="grado 3")
ejes[1].plot(xs, np.polyval(np.polyfit(x, y_muestra, 9), xs), color=ROJO, linewidth=1.6,
             label="grado 9")
ejes[1].plot(x, y_muestra, color=AZUL, linestyle="none", marker="o", markersize=4.2,
             label="30 datos")
anotar(ejes[1], "el grado 9 persigue el ruido:\nun dato distinto retuerce la curva\nentera",
       xy=(0.875, y_muestra[26]), xytext=(0.02, 0.16), color=ROJO)
titulo(ejes[1], "Mas flexible no es mejor",
       "el polinomio de grado 9 se pega a los datos y falla en los huecos")
ejes[1].set_xlabel("x")
ejes[1].set_ylabel("valor observado")
ejes[1].set_ylim(-2.2, 2.4)
ejes[1].legend(loc="upper right", ncol=2)
rejilla(ejes[1])
numeros(ejes[1], ejes="x")

guardar(fig, "sesgo-varianza-descomposicion-y-ajuste")
