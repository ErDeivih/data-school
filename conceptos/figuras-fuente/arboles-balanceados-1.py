"""arboles-balanceados-1.py — lo que se paga por mantener el orden con poca altura.

Izquierda: hasta dónde puede crecer la altura según la regla de equilibrado. El árbol perfecto
es la referencia (log2 n); un AVL admite hasta un 44 % más y un rojo-negro, hasta el doble.
Todo eso sigue siendo logarítmico: la diferencia entre 20 y 40 niveles es una constante.
Derecha: por qué las bases de datos usan B-árboles. Con orden 32, tres niveles guardan casi
31.000 claves y cuatro llegan a 954.300; un árbol binario tardaría veinte niveles en pasar
del millón.
La figura de la página de árboles balanceados (fase 10).
"""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.6))

# --- Izquierda: las tres cotas de altura ----------------------------------------
ax = ejes[0]
n = np.logspace(1, 9, 400)
perfecto = np.log2(n) + 1
avl = 1.4405 * np.log2(n + 2) - 0.3277          # cota de altura máxima de un AVL
rojo_negro = 2 * np.log2(n + 1)                 # cota de un rojo-negro
ax.loglog(n, rojo_negro, color=ROJO, linewidth=2.0)
ax.loglog(n, avl, color=NARANJA, linewidth=2.0)
ax.loglog(n, perfecto, color=AZUL, linewidth=2.0)
anotar(ax, "perfecto: log2(n)\nun millón de claves, 20 niveles",
       xy=(1e4, 14.3), xytext=(0.06, 0.10), color=AZUL)
anotar(ax, "AVL: hasta un 44 % más alto\nque el perfecto",
       xy=(1e6, 29.2), xytext=(0.30, 0.62), color=NARANJA)
anotar(ax, "rojo-negro: hasta el doble\ndel perfecto",
       xy=(1e8, 56.0), xytext=(0.60, 0.28), color=ROJO)
anotar(ax, "las tres crecen igual de despacio:\nun orden de magnitud más de claves\ncuesta tres o cuatro niveles",
       xy=(1e8, 1e2), xytext=(0.04, 0.36), color=MORADO, flecha=False)
titulo(ax, "Equilibrar no es allanar: cambia la constante",
       "altura máxima garantizada, en escala doble logarítmica")
ax.set_xlabel("claves guardadas")
ax.set_ylabel("niveles del árbol")
rejilla(ax, eje="both")
numeros(ax)

# --- Derecha: el B-árbol de orden 32 --------------------------------------------
ax = ejes[1]
orden = 32
claves_por_nodo = orden - 1                      # un nodo de orden 32 guarda hasta 31 claves
# Capacidad total de un B-árbol de orden m y altura h: suma de m^i − 1 en cada nivel.
niveles, total = [], 0.0
for h in range(5):
    # La suma de m^i − 1 es la capacidad de un B-árbol de altura h: 30, 990, 30.780,
    # 954.300 y 29.583.450 claves, y a partir de ahí el millón se queda muy atrás.
    total += claves_por_nodo ** (h + 1) - 1
    niveles.append(total)
niveles = np.array(niveles)
alturas = np.arange(niveles.size)

for h, capacidad in zip(alturas, niveles):
    # Cada barra es un nivel: su longitud dice cuántas claves caben en un árbol de esa altura.
    ax.barh(h, capacidad, height=0.62, color=CIAN if h < 3 else MORADO, alpha=0.88)
    texto = f"{capacidad:,.0f}".replace(",", ".")
    ax.text(capacidad * 1.35, h, f"{texto} claves", va="center", fontsize=8.5, color=TEXTO)
ax.axvline(1e6, color=ROJO, linewidth=1.6, linestyle="--")
anotar(ax, "un árbol binario necesitaría veinte\nniveles para pasar del millón;\naquí bastan cuatro",
       xy=(7e5, 2.45), xytext=(0.56, 0.13), color=ROJO)
titulo(ax, "Con 32 hijos por nodo, el árbol no crece",
       f"claves que caben según la altura ({claves_por_nodo} claves por nodo), en escala logarítmica")
ax.set_xscale("log")
ax.set_xlim(0.6, 1.8e12)
ax.set_ylim(-0.6, 4.6)
ax.set_yticks(alturas)
ax.set_yticklabels([f"{int(h)}" for h in alturas])
ax.set_xlabel("claves que caben como máximo")
ax.set_ylabel("niveles")
rejilla(ax, eje="x")
numeros(ax, ejes="x")

guardar(fig, "arboles-balanceados-altura-y-b-arbol")
