"""ordenacion-1.py — las comparaciones contadas de verdad frente a la cota inferior, y
cuándo deja de compensar contar valores en vez de compararlos. Página de ordenación (fase 10)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)


def mergesort(a):
    """Ordena por mezcla y devuelve (array ordenado, comparaciones hechas)."""
    if len(a) <= 1:
        return a, 0
    medio = len(a) // 2
    izq, c1 = mergesort(a[:medio])
    der, c2 = mergesort(a[medio:])
    salida, i, j, c3 = [], 0, 0, 0
    while i < len(izq) and j < len(der):
        c3 += 1
        if izq[i] <= der[j]:              # <= y no <: así la ordenación es estable
            salida.append(izq[i])
            i += 1
        else:
            salida.append(der[j])
            j += 1
    return salida + izq[i:] + der[j:], c1 + c2 + c3


def quicksort_lomuto(a, contador):
    """Quicksort con el pivote en el último elemento (partición de Lomuto)."""
    if len(a) <= 1:
        return a
    pivote = a[-1]
    i = 0
    for j in range(len(a) - 1):
        contador[0] += 1
        if a[j] <= pivote:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[-1] = a[-1], a[i]
    return quicksort_lomuto(a[:i], contador) + [a[i]] + quicksort_lomuto(a[i + 1:], contador)


tamanos = np.array([32, 64, 128, 256, 512])
azar_mrg, azar_qs, ordenado_qs = [], [], []
for n in tamanos:
    datos = azar.integers(0, 1000, size=int(n)).tolist()
    azar_mrg.append(mergesort(datos)[1])
    c = [0]
    quicksort_lomuto(datos[:], c)
    azar_qs.append(c[0])
    c = [0]
    quicksort_lomuto(sorted(datos), c)     # el peor caso: el array ya viene ordenado
    ordenado_qs.append(c[0])

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.5))
n = tamanos.astype(float)

# --- Izquierda: comparaciones medidas, no estimadas. El cuadrático no es una teoría: está
# medido sobre el mismo array ordenado que recibe cualquier consulta con ORDER BY.
ejes[0].loglog(n, n * np.log2(n), color=REJILLA, linewidth=1.6, linestyle=":",
               label="cota inferior: n · log₂ n")
ejes[0].loglog(n, n * (n - 1) / 2, color=MORADO, linewidth=1.6, linestyle="--",
               label="peor caso de quicksort: n(n−1)/2")
ejes[0].loglog(n, azar_mrg, color=AZUL, linewidth=2.0, marker="o", markersize=5,
               label="mergesort, array al azar")
ejes[0].loglog(n, azar_qs, color=VERDE, linewidth=2.0, marker="s", markersize=5,
               label="quicksort, array al azar")
ejes[0].loglog(n, ordenado_qs, color=ROJO, linewidth=2.2, marker="^", markersize=6,
               label="quicksort, array ya ordenado")
anotar(ejes[0], f"con 512 elementos ya ordenados, quicksort\nhace {ordenado_qs[-1]:,} comparaciones".replace(",", "."),
       xy=(512, ordenado_qs[-1]), xytext=(0.04, 0.88), color=ROJO, flecha=False)
titulo(ejes[0], "El cuadrático no es teoría: está medido",
       "comparaciones contadas en cada ejecución, con la semilla 7")
ejes[0].set_xlabel("elementos n")
ejes[0].set_ylabel("comparaciones")
ejes[0].legend(loc="lower right", fontsize=8)
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="both")
# Los tamaños son potencias de dos: con los ticks automáticos la escala logarítmica llena el
# eje de etiquetas raras («3 × 10¹»), así que se fijan a mano.
ejes[0].set_xticks(tamanos)
ejes[0].set_xticklabels([str(int(t)) for t in tamanos])
ejes[0].minorticks_off()

# --- Derecha: contar sale más barato que comparar, pero solo mientras el rango k sea pequeño.
n_fijo = 1e6
k = np.logspace(2, 13, 240)
cota = n_fijo * np.log2(n_fijo)                     # log2(n!) ≈ n·log2(n) − 1,44n
ejes[1].loglog(k, n_fijo + k, color=AZUL, linewidth=2.2, label="counting sort: n + k")
ejes[1].loglog(k, np.full(k.shape, cota), color=ROJO, linewidth=2.0,
               label="comparar: la cota inferior n · log₂ n")
cruce = cota - n_fijo
ejes[1].axvline(cruce, color=REJILLA, linewidth=1.1, linestyle=":")
anotar(ejes[1], f"con 1.000.000 de elementos, contar gana\nhasta k ≈ {cruce / 1e6:.0f} millones de valores distintos",
       xy=(cruce, cota), xytext=(0.03, 0.90), color=AZUL)
anotar(ejes[1], "un identificador de 64 bits tiene k = 1,8 · 10¹⁹:\nel array de conteo no cabe en ningún sitio",
       xy=(1e12, n_fijo + 1e12), xytext=(0.03, 0.72), color=MORADO, flecha=False)
titulo(ejes[1], "Contar gana solo si el rango es pequeño",
       "coste de ordenar un millón de elementos según el número de valores posibles k")
ejes[1].set_xlabel("valores distintos posibles k")
ejes[1].set_ylabel("operaciones")
ejes[1].legend(loc="lower right", fontsize=8)
rejilla(ejes[1], eje="both")
numeros(ejes[1], ejes="both")
ejes[1].set_yticks([1e6, 1e8, 1e10, 1e12])
ejes[1].set_yticklabels(["1 millón", "100 millones", "10.000 millones", "1 billón"])
ejes[1].minorticks_off()

guardar(fig, "ordenacion-comparaciones-y-cota")
