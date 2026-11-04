"""algoritmos-greedy-1.py — dónde acierta el voraz y cuánto pierde cuando falla.
La figura de la página de algoritmos voraces (fase 10).

Izquierda: los once intervalos del ejemplo, con la selección del criterio «la que antes acaba»
en azul (4 actividades) y la del criterio «la que antes empieza» en rojo (3). Los dos son
voraces; solo uno es óptimo.
Derecha: 3.000 mochilas 0/1 pequeñas resueltas con el voraz por densidad y con fuerza bruta.
El voraz acierta en la mayoría, pero hay instancias donde se queda muy corto.
"""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)          # semilla fija: las cuentas salen siempre igual

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.6))

# --- Izquierda: selección de actividades, con los dos criterios -----------------------
intervalos = [("A", 0, 6), ("B", 1, 4), ("C", 3, 5), ("D", 5, 7), ("E", 3, 9), ("F", 5, 9),
              ("G", 6, 10), ("H", 8, 11), ("I", 8, 12), ("J", 2, 14), ("K", 12, 16)]
por_inicio_orden = sorted(intervalos, key=lambda t: (t[1], t[2]))


def elegir(orden):
    """El voraz de la página: coge todo lo compatible con la última elegida."""
    elegidas, fin_ultimo = [], -1
    for nombre, ini, fin in orden:
        if ini >= fin_ultimo:
            elegidas.append(nombre)
            fin_ultimo = fin
    return elegidas


por_fin = elegir(sorted(intervalos, key=lambda t: (t[2], t[1])))
por_ini = elegir(por_inicio_orden)

ax = ejes[0]
for fila, (nombre, ini, fin) in enumerate(por_inicio_orden):
    en_fin, en_ini = nombre in por_fin, nombre in por_ini
    color = AZUL if en_fin else (ROJO if en_ini else REJILLA)
    ax.add_patch(plt.Rectangle((ini, fila - 0.32), fin - ini, 0.64, facecolor=color,
                               alpha=0.75 if (en_fin or en_ini) else 0.35,
                               edgecolor=color, linewidth=1.1))
    ax.text(ini - 0.35, fila, nombre, ha="right", va="center", fontsize=8.5, color=TEXTO)
    ax.text(fin + 0.25, fila, f"[{ini}, {fin})", ha="left", va="center", fontsize=7.5,
            color=TEXTO)
ax.plot([], [], marker="s", markersize=9, linestyle="none", color=AZUL,
        label=f"criterio «la que antes acaba»: {len(por_fin)} actividades")
ax.plot([], [], marker="s", markersize=9, linestyle="none", color=ROJO,
        label=f"criterio «la que antes empieza»: {len(por_ini)} actividades")
ax.plot([], [], marker="s", markersize=9, linestyle="none", color=REJILLA,
        label="descartada por los dos")
anotar(ax, "el mismo problema y el mismo tipo de algoritmo:\ncambiar el criterio cuesta una actividad",
       xy=(7.0, 6.0), xytext=(0.02, 0.94), color=TEXTO, flecha=False)
titulo(ax, "Un voraz acierta y el otro no",
       "once intervalos [inicio, fin) y lo que elige cada criterio, ordenados por inicio")
ax.set_xlabel("hora")
ax.set_ylabel("actividad")
ax.set_yticks([])
ax.set_xlim(-1.4, 18.6)
ax.set_ylim(-2.9, 12.2)
ax.legend(loc="lower right", fontsize=8.5)
rejilla(ax, eje="x")
numeros(ax, ejes="x")


# --- Derecha: cuánto se aleja el voraz del óptimo en mochilas pequeñas ----------------
def mochila_voraz(pesos, valores, cap):
    orden = sorted(range(len(pesos)), key=lambda i: valores[i] / pesos[i], reverse=True)
    peso = valor = 0
    for i in orden:
        if peso + pesos[i] <= cap:
            peso += pesos[i]; valor += valores[i]
    return valor


def mochila_optima(pesos, valores, cap):
    mejor = 0
    for mascara in range(1 << len(pesos)):
        peso = valor = 0
        for i in range(len(pesos)):
            if mascara >> i & 1:
                peso += pesos[i]; valor += valores[i]
        if peso <= cap and valor > mejor:
            mejor = valor
    return mejor


ratios = []
for _ in range(3000):
    pesos = list(azar.integers(1, 30, size=6))
    valores = list(azar.integers(1, 30, size=6))
    cap = int(0.5 * sum(pesos))
    optimo = mochila_optima(pesos, valores, cap)
    ratios.append(mochila_voraz(pesos, valores, cap) / optimo if optimo else 1.0)
ratios = np.array(ratios)
optimas = 100 * float((ratios == 1).mean())
peor = float(ratios.min())

ax = ejes[1]
bordes = np.arange(0.5, 1.001, 0.025)
ax.hist(ratios, bins=bordes, color=AZUL, alpha=0.85, edgecolor=REJILLA, linewidth=0.6)
ax.axvline(peor, color=ROJO, linewidth=1.6, linestyle="--")
ax.axvline(30 / 48, color=MORADO, linewidth=1.6, linestyle=":")
anotar(ax, f"en el {optimas:.0f} % de las instancias el voraz da el óptimo",
       xy=(1.0, 1.0), xytext=(0.30, 0.90), color=AZUL, flecha=False)
anotar(ax, f"la peor de esta muestra:\n{100 * peor:.0f} % del óptimo",
       xy=(peor, 300), xytext=(0.02, 0.70), color=ROJO)
anotar(ax, "el contraejemplo de la página\n(30 de 48) cae aquí, en el 62,5 %",
       xy=(30 / 48, 300), xytext=(0.34, 0.42), color=MORADO)
titulo(ax, "El voraz casi siempre acierta, pero no siempre",
       "3.000 mochilas 0/1 de seis objetos: valor del voraz dividido entre el óptimo")
ax.set_xlabel("valor conseguido por el voraz, en fracción del óptimo")
ax.set_ylabel("número de instancias")
ax.set_xlim(0.5, 1.02)
rejilla(ax)
numeros(ax)

guardar(fig, "voraces-intervalos-y-mochila")
