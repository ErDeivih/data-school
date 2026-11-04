"""tablas-hash-1.py — el factor de carga, medido.

Izquierda: sondas medias por búsqueda frente al factor de carga α = n/m. Con encadenamiento
el coste sube en línea recta (1 + α/2) y nunca estalla; con direccionamiento abierto y sondeo
lineal se dispara al acercarse a 1. Es la diferencia entre una tabla que aguanta llena y otra
que no.
Derecha: cómo se reparten 1.000 claves entre 1.024 cubetas al azar. De media toca a una por
cubeta, pero el reparto no es uniforme: hay cubetas vacías y alguna cadena de cuatro o cinco.
Por eso O(1) es un coste MEDIO y no una promesa.
La figura de la página de tablas hash (fase 10).
"""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.4))

# --- Izquierda: lo que cuesta una búsqueda según lo llena que esté la tabla -------
ax = ejes[0]
alfa = np.linspace(0.01, 0.97, 200)
ax.plot(alfa, 1 + alfa / 2, color=AZUL, linewidth=2.2)
ax.plot(alfa, 0.5 * (1 + 1 / (1 - alfa)), color=ROJO, linewidth=2.2)
ax.vlines(0.75, 2.6, 17.5, color=REJILLA, linewidth=1.1, linestyle=":")
ax.set_ylim(-0.6, 17.5)       # margen extra abajo: la nota del umbral cabe sin pisar las curvas
anotar(ax, "encadenamiento: 1 + α/2\nla cadena crece, pero de uno en uno",
       xy=(0.86, 14.8), xytext=(0.06, 0.88), color=AZUL)
anotar(ax, "sondeo lineal: se dispara\ncuando la tabla se llena",
       xy=(0.68, 2.2), xytext=(0.28, 0.24), color=ROJO)
anotar(ax, "a partir de α ≈ 0,75 conviene\nredimensionar al doble",
       xy=(0.75, 3.4), xytext=(0.55, 0.06), color=MORADO, flecha=False)
titulo(ax, "Llena, la tabla deja de ser O(1)",
       "sondas medias por búsqueda con éxito, frente al factor de carga α = n/m")
ax.set_xlabel("factor de carga α (claves / cubetas)")
ax.set_ylabel("sondas por búsqueda")
rejilla(ax)
numeros(ax)

# --- Derecha: el reparto real de las claves por cubeta ---------------------------
ax = ejes[1]
n, m = 1000, 1024
claves = azar.integers(0, m, n)              # una función de dispersión ideal, sin colisiones
ocupacion = np.bincount(claves, minlength=m)
largos, cuantos = np.unique(ocupacion, return_counts=True)
colores = [REJILLA if L == 0 else AZUL if L == 1 else NARANJA if L == 2 else ROJO for L in largos]
ax.bar(largos, cuantos, width=0.6, color=colores, alpha=0.9)
for L, c in zip(largos, cuantos):
    ax.text(L, c + 4, str(c), ha="center", fontsize=8.5, color=TEXTO)
anotar(ax, f"{cuantos[0]} cubetas vacías:\ncon 1.000 claves no se llenan ni 1.000 huecos",
       xy=(0, float(cuantos[0])), xytext=(0.04, 0.70), color=TEXTO)
anotar(ax, f"la cadena más larga tiene {int(largos.max())} claves:\n"
           "esa búsqueda no es O(1), es O(5)",
       xy=(4.7, 12.0), xytext=(0.30, 0.62), color=ROJO)
titulo(ax, "El azar no reparte por igual",
       f"{n} claves en {m} cubetas con una dispersión ideal")
ax.set_xlabel("claves que caen en una misma cubeta")
ax.set_ylabel("nº de cubetas")
ax.set_xticks(largos)
rejilla(ax)
numeros(ax, ejes="x")

guardar(fig, "tablas-hash-carga-y-colisiones")
