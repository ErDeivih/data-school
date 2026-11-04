"""divide-y-venceras-1.py — de qué depende el coste cuando se parte el problema en trozos.
La figura de la página de divide y vencerás (fase 10).

Izquierda: comparaciones contadas de verdad, mergesort frente a ordenación por inserción, con
arrays aleatorios de 64 a 4.096 elementos. La distancia entre las dos curvas se abre con n: es
la diferencia entre n log₂ n y n².
Derecha: el coste de multiplicar dos números de n cifras. El método escolar es cuadrático,
Karatsuba lo baja a n^1,585 y la FFT a n log₂ n; con cuatro cifras da igual, con un millón no.
"""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)


# --- Izquierda: comparaciones medidas de los dos algoritmos de ordenación -------------
def mergesort_contando(v):
    if len(v) <= 1:
        return v, 0
    medio = len(v) // 2
    izq, c1 = mergesort_contando(v[:medio])
    der, c2 = mergesort_contando(v[medio:])
    salida, i, j, c3 = [], 0, 0, 0
    while i < len(izq) and j < len(der):
        c3 += 1
        if izq[i] <= der[j]:
            salida.append(izq[i]); i += 1
        else:
            salida.append(der[j]); j += 1
    return salida + izq[i:] + der[j:], c1 + c2 + c3


def insercion_contando(v):
    v = list(v)
    comparaciones = 0
    for i in range(1, len(v)):
        actual, j = v[i], i - 1
        while j >= 0:
            comparaciones += 1
            if v[j] > actual:
                v[j + 1] = v[j]; j -= 1
            else:
                break
        v[j + 1] = actual
    return v, comparaciones


tamanos = np.array([64, 128, 256, 512, 1024, 2048, 4096])
repes = 3                                  # se mide varias veces y se queda la media
c_merge, c_insercion = [], []
for n in tamanos:
    cm = ci = 0
    for _ in range(repes):
        datos = list(azar.integers(0, 10 * n, size=int(n)))
        _, a = mergesort_contando(datos)
        _, b = insercion_contando(datos)
        cm += a / repes
        ci += b / repes
    c_merge.append(cm)
    c_insercion.append(ci)
c_merge = np.array(c_merge)
c_insercion = np.array(c_insercion)

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.4))

ax = ejes[0]
ax.loglog(tamanos, c_insercion, color=ROJO, linewidth=1.9, marker="o", markersize=5,
          label="ordenación por inserción: Θ(n²)")
ax.loglog(tamanos, c_merge, color=AZUL, linewidth=1.9, marker="s", markersize=5,
          label="mergesort: Θ(n log₂ n)")
ax.set_xticks(tamanos)
numeros(ax)
# Las etiquetas llevan el punto de millar, como el resto del portal.
ax.set_xticklabels([f"{n:,}".replace(",", ".") for n in tamanos], fontsize=8)
ax.set_xlim(50, 6e3)
ax.set_ylim(1e2, 2e7)
anotar(ax, f"con 4.096 elementos: {c_merge[-1]:,.0f} comparaciones\n"
           f"frente a {c_insercion[-1]:,.0f} de la inserción".replace(",", "."),
       xy=(4096, float(c_insercion[-1])), xytext=(0.03, 0.72), color=ROJO, flecha=False)
anotar(ax, "la pendiente de la recta roja es 2:\ncada vez que n se duplica, se cuadruplica",
       xy=(2048, float(c_insercion[-2])), xytext=(0.30, 0.16), color=NARANJA)
titulo(ax, "Combinar bien cambia el orden del coste",
       "comparaciones medidas ordenando arrays aleatorios, en escala logarítmica")
ax.set_xlabel("elementos del array")
ax.set_ylabel("comparaciones")
ax.legend(loc="upper left")
rejilla(ax)

# --- Derecha: el coste de multiplicar, según cómo se parta ----------------------------
ax = ejes[1]
cifras = np.logspace(1, 6, 200)
escolar = cifras ** 2
karatsuba = cifras ** 1.585
fft = cifras * np.log2(cifras)
ax.loglog(cifras, escolar, color=ROJO, linewidth=1.9, label="método escolar: n²")
ax.loglog(cifras, karatsuba, color=AZUL, linewidth=1.9, label="Karatsuba: n^1,585")
ax.loglog(cifras, fft, color=VERDE, linewidth=1.9, label="FFT: n log₂ n")
ax.set_xlim(8, 3e6)
ax.set_ylim(2e1, 3e13)
anotar(ax, "un millón de cifras: 10¹² operaciones\nfrente a 3,2 · 10⁹ de Karatsuba",
       xy=(1e6, 1e12), xytext=(0.02, 0.24), color=ROJO, flecha=False)
anotar(ax, "con pocas cifras las tres curvas se\nconfunden: dividir paga cuando n crece",
       xy=(30, float(30 * np.log2(30))), xytext=(0.02, 0.88), color=MORADO, flecha=False)
titulo(ax, "Partir en trozos baja el exponente",
       "operaciones para multiplicar dos números de n cifras, en escala logarítmica")
ax.set_xlabel("cifras de cada número")
ax.set_ylabel("operaciones")
ax.legend(loc="lower right")
rejilla(ax)
numeros(ax)

guardar(fig, "divide-y-venceras-comparaciones-y-exponentes")
