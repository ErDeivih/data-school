"""maldicion-de-la-dimensionalidad-1.py - el vecindario deja de ser local y las distancias
se igualan al crecer la dimensión. Figura de la pagina de la maldición de la
dimensionalidad (fase 6)."""

import numpy as np

from comun import *

estilo()

# --- Izquierda: lado del cubo que hace falta para cubrir el 10 % del volumen.
dimensiones = np.arange(1, 101)
lado10 = 0.1 ** (1.0 / dimensiones)          # de s^d = 0,1 con el cubo unidad

# --- Derecha: 150 puntos uniformes en el cubo unidad, distancia euclidea.
# Se calcula la distancia al vecino mas cercano y al mas lejano con productos matriciales
# (P @ P.T), que es mucho mas rapido que restar los pares uno a uno.
def contraste(d, n=150):
    azar = np.random.default_rng(7)
    P = azar.random((n, d))
    cuadrado = (P ** 2).sum(axis=1)
    distancia = np.sqrt(np.clip(cuadrado[:, None] + cuadrado[None, :] - 2 * P @ P.T, 0, None))
    np.fill_diagonal(distancia, np.nan)       # fuera la distancia de cada punto a si mismo
    return np.nanmean(np.nanmin(distancia, axis=1) / np.nanmax(distancia, axis=1))

medidas = [2, 3, 5, 8, 12, 20, 30, 50, 80, 120, 200, 350, 600, 1000]
contraste = np.array([contraste(d) for d in medidas])

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.2))

# --- Izquierda: el vecindario local se traga casi todo el rango con muy pocas variables.
ejes[0].plot(dimensiones, lado10, color=AZUL, linewidth=2.0)
ejes[0].axhline(0.1, color=TEXTO, linewidth=1.0, linestyle="--")
# La nota va en el hueco que queda a media altura, sin flecha: la curva pasa por encima y
# cualquier flecha hasta la esquina superior derecha la cruzaba.
anotar(ejes[0], "con 100 variables, el 10 % de los datos\nmas cercanos ocupa el 98 % de cada eje",
       xy=(100, lado10[-1]), xytext=(0.22, 0.24), color=VERDE, flecha=False)
titulo(ejes[0], "El vecindario deja de ser local",
       "lado necesario para cubrir el 10 % del volumen, con el cubo unidad")
ejes[0].set_xlabel("número de variables")
ejes[0].set_ylabel("lado del cubo (fracción del rango)")
ejes[0].set_xlim(0, 104)
ejes[0].set_xticks([1, 10, 20, 40, 60, 80, 100])
ejes[0].set_ylim(0, 1.12)
rejilla(ejes[0])
numeros(ejes[0])

# --- Derecha: el contraste entre el vecino mas cercano y el mas lejano desaparece.
ejes[1].plot(medidas, contraste, color=ROJO, linewidth=1.8, marker="o", markersize=4.2)
ejes[1].axhline(0.35, color=REJILLA, linewidth=1.2, linestyle=":")
ejes[1].set_xscale("log")
anotar(ejes[1], "por debajo de 0,35 el vecino más cercano\ny el más lejano se parecen: elegir\nentre ellos es casi azar",
       xy=(30, contraste[6]), xytext=(0.04, 0.83), color=ROJO)
titulo(ejes[1], "Cerca y lejos se vuelven lo mismo",
       "cociente entre la distancia al vecino más cercano y al más lejano")
ejes[1].set_xlabel("número de dimensiones (escala logaritmica)")
ejes[1].set_ylabel("cociente mínima / maxima")
ejes[1].set_ylim(0, 1.05)
rejilla(ejes[1])
numeros(ejes[1], ejes="x")

guardar(fig, "maldicion-vecindario-y-distancias")
