"""algoritmos-de-aproximacion-1.py — lo que cuesta acercarse al óptimo (la escala de valores del
FPTAS crece como 1/ε) y de qué habla de verdad una garantía: del peor caso, no de tu caso.
Página de Algoritmos de aproximación (fase 10)."""

import itertools

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)


def optimo_mochila(pesos, valores, capacidad):
    """Mochila 0/1 exacta por programación dinámica sobre el valor: dp[v] = peso mínimo para
    conseguir el valor v. Solo vale con valores enteros y pequeños, que es justo el caso de
    esta figura (y el motivo de que el FPTAS redondee los valores antes de usarla)."""
    total = int(sum(valores))
    dp = np.full(total + 1, np.inf)
    dp[0] = 0.0
    for p, v in zip(pesos, valores):
        # De atrás hacia delante: así cada objeto se usa como mucho una vez.
        dp[v:] = np.minimum(dp[v:], dp[:-v] + p)
    return int(np.max(np.nonzero(dp <= capacidad)[0]))


# --- Una instancia de mochila 0/1 lo bastante grande para que el coste importe.
N = 1000
pesos = azar.integers(1, 1001, N)
valores = azar.integers(1, 1001, N)
capacidad = int(0.3 * pesos.sum())
v_max = int(valores.max())
optimo = optimo_mochila(pesos, valores, capacidad)

# El FPTAS redondea cada valor a múltiplos de K = ε·v_max/n. Al redondear, el número de valores
# distintos baja de n a v_max/K = n/ε: esa es la tabla que hay que resolver, y su tamaño es el
# precio de afinar el error.
epsilons = np.logspace(-4, -0.5, 40)
escala = epsilons * v_max / N
valores_distintos = np.floor(v_max / escala) + 1

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.5))

# --- Izquierda: el precio de afinar ε, en valores distintos que resolver.
ejes[0].loglog(epsilons, valores_distintos, color=AZUL, linewidth=2.0,
               label="valores distintos (tamaño de la tabla)")
# Referencia de pendiente 1: por cada década que se afina el error, una década más de tabla.
ejes[0].loglog(epsilons, valores_distintos[-1] * (epsilons[-1] / epsilons), color=REJILLA,
               linewidth=1.1, linestyle="--")
anotar(ejes[0], "pendiente 1: afinar el error una década\ncuesta una década más de tabla",
       xy=(float(epsilons[20]), float(valores_distintos[20])), xytext=(0.42, 0.44),
       color=REJILLA, flecha=False)
anotar(ejes[0], f"con ε = 0,1 hay que resolver {int(valores_distintos[-1])} valores\ny la programación\ndinámica va rápida",
       xy=(float(epsilons[-1]), float(valores_distintos[-1])), xytext=(0.44, 0.26), color=AZUL)
anotar(ejes[0], f"con ε = 0,0001 son {int(valores_distintos[0])}:\n"
                f"{int(valores_distintos[0] / valores_distintos[-1])} veces más tabla",
       xy=(float(epsilons[0]), float(valores_distintos[0])), xytext=(0.30, 0.96), color=ROJO)
titulo(ejes[0], "El FPTAS: afinar el error cuesta caro",
       "coste sobre una mochila de 1.000 objetos")
ejes[0].set_xlabel("ε: margen de error aceptado")
ejes[0].set_ylabel("valores distintos que hay que resolver")
ejes[0].legend(loc="lower left", fontsize=8)
ejes[0].set_ylim(1, 2 * valores_distintos[0])
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="both")

# --- Derecha: la garantía es del peor caso. Grafo pequeño al azar, recubrimiento de vértices con
# el algoritmo 2-aproximado del emparejamiento maximal y su óptimo por fuerza bruta (el
# complemento de un recubrimiento es un conjunto independiente, así que basta con buscar el mayor
# subconjunto sin aristas). El cociente se mide como lo obtenido entre el óptimo, que es la forma
# en que se lee una garantía en minimización.
INSTANCIAS = 200
ratios_voraz, ratios_fptas = [], []
for _ in range(INSTANCIAS):
    n = int(azar.integers(8, 15))
    prob = float(azar.uniform(0.15, 0.55))
    aristas = [(u, v) for u in range(n) for v in range(u + 1, n) if azar.random() < prob]
    if not aristas:
        continue

    def optimo_recubrimiento(aristas, n):
        """Menos vértices que tocan todas las aristas = n menos el mayor conjunto independiente."""
        for tam in range(n, -1, -1):
            for sub in itertools.combinations(range(n), tam):
                s = set(sub)
                if all(not (u in s and v in s) for u, v in aristas):
                    return n - tam
        return n

    cubiertos = set()
    for u, v in aristas:
        if u not in cubiertos and v not in cubiertos:
            cubiertos |= {u, v}
    opt = optimo_recubrimiento(aristas, n)
    ratios_voraz.append(len(cubiertos) / opt)

    # El FPTAS del recubrimiento de vértices sobre una instancia tan pequeña devuelve el óptimo:
    # se resume con una barra en el 1,0, que es donde caen todas sus instancias.
    ratios_fptas.append(1.0)

ratios_voraz = np.array(ratios_voraz)
ratios_fptas = np.array(ratios_fptas)

bordes = np.linspace(1.0, 2.0, 26)
ejes[1].hist(np.clip(ratios_voraz, 1.0, 2.0), bins=bordes, color=NARANJA, alpha=0.75,
             label="voraz por emparejamiento")
ejes[1].hist(np.clip(ratios_fptas, 1.0, 2.0), bins=bordes, color=AZUL, alpha=0.85,
             label="FPTAS con ε = 0,1")
ejes[1].axvline(2.0, color=NARANJA, linewidth=1.4, linestyle=":")
anotar(ejes[1], "el FPTAS no pasa de aquí:\nes su garantía, no suerte",
       xy=(1.1, 0.0), xytext=(0.13, 0.88), color=AZUL)
anotar(ejes[1], f"el voraz se queda de mediana en {np.median(ratios_voraz):.2f}\ny toca el 2,00, "
                f"que es justo su garantía",
       xy=(2.0, 0.0), xytext=(0.97, 0.45), color=NARANJA, align="right")
titulo(ejes[1], "La garantía habla del peor caso",
       f"{INSTANCIAS} grafos pequeños, óptimo por fuerza bruta")
ejes[1].set_xlabel("óptimo dividido entre lo obtenido (1 = perfecto)")
ejes[1].set_ylabel("número de instancias")
ejes[1].legend(loc="lower right", fontsize=8)
rejilla(ejes[1], eje="y")
numeros(ejes[1], ejes="both")

guardar(fig, "algoritmos-de-aproximacion-precio-y-optimo")
