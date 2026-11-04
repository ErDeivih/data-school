"""grafos-representacion-1.py — la decisión que decide el coste de todos los algoritmos de
grafos: qué ocupa la matriz de adyacencia y qué ocupa la lista. Página de representación de
grafos (fase 10)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# Grafo disperso típico: cada vértice conecta con unos pocos. Es el caso de una red social,
# de un mapa de carreteras y de las dependencias entre tareas, y es la inmensa mayoría de
# los grafos que te vas a encontrar.
n = np.unique(np.logspace(1, 5, 80).astype(int)).astype(float)
grado = 5.0
celdas = n ** 2                        # la matriz reserva n² celdas pase lo que pase
entradas = n + grado * n               # la lista: n listas y 2m pares (vecino, peso), con 2m = grado·n

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.4))

# --- Izquierda: la memoria de las dos representaciones, en escala logarítmica. Sin el log
# las dos curvas no caben juntas: con n = 10.000 hay seis órdenes de magnitud de diferencia.
ejes[0].loglog(n, celdas, color=ROJO, linewidth=2.0, label="matriz: n² celdas")
ejes[0].loglog(n, entradas, color=AZUL, linewidth=2.0, label="lista: n + 2m entradas")

# Doce grafos al azar, con su tamaño y su grado medio, medidos con la misma fórmula: sirven
# para ver que la recta de la lista no describe un caso de laboratorio, sino lo corriente.
n_azar = azar.integers(60, 60000, size=12).astype(float)
grado_azar = azar.uniform(2.0, 9.0, size=12)
ejes[0].scatter(n_azar, n_azar * (1 + grado_azar), s=24, color=MORADO, zorder=5,
                label="12 grafos dispersos al azar")

anotar(ejes[0], "con 10.000 vértices la matriz pide\n100 millones de celdas y la lista 60.000",
       xy=(1e4, 1e8), xytext=(0.04, 0.80), color=ROJO)
anotar(ejes[0], "la lista solo guarda lo que existe:\ncrece con las aristas, no con n²",
       xy=(1e4, 6e4), xytext=(0.30, 0.30), color=AZUL)
titulo(ejes[0], "La matriz crece con n² y la lista con n + m",
       "grafo no dirigido con 5 vecinos por vértice de media, en escala logarítmica")
ejes[0].set_xlabel("vértices n")
ejes[0].set_ylabel("celdas o entradas guardadas")
ejes[0].legend(loc="lower right", fontsize=8)
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="both")

# --- Derecha: cuánto de la matriz se usa de verdad. La ocupación es 2m/n² y con grado medio
# d vale d/n: la matriz solo deja de desperdiciar cuando el grafo es denso.
n_fijo = 1000
grado_eje = np.logspace(0, 3, 240)
ocupado = 100 * grado_eje / n_fijo
ejes[1].semilogx(grado_eje, ocupado, color=MORADO, linewidth=2.0)
ejes[1].axhline(100, color=REJILLA, linewidth=1.0, linestyle=":")
ejes[1].axvline(5, color=AZUL, linewidth=1.2, linestyle=":")
anotar(ejes[1], "una red social: 5 vecinos de 1.000\nposibles usan el 0,5 % de las celdas",
       xy=(5, 0.5), xytext=(0.05, 0.62), color=AZUL)
anotar(ejes[1], "grafo denso: 500 vecinos\nya usa la mitad de la tabla",
       xy=(500, 50), xytext=(0.44, 0.30), color=MORADO)
titulo(ejes[1], "Con 5 vecinos, la matriz está vacía al 99,5 %",
       "celdas ocupadas de una matriz de 1.000 × 1.000 según el grado medio")
ejes[1].set_xlabel("vecinos por vértice (grado medio)")
ejes[1].set_ylabel("celdas de la matriz que se usan (%)")
ejes[1].set_ylim(-5, 118)
rejilla(ejes[1], eje="both")
numeros(ejes[1], ejes="both")

guardar(fig, "grafos-representacion-matriz-y-lista")
