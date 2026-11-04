"""concurrencia-algoritmica-1.py — los dos números que mandan en un programa concurrente.

Izquierda: la ley de Amdahl. La aceleración no la limita el número de núcleos, la limita la
fracción de trabajo que no se puede repartir: con la mitad en serie (p = 0,5) ni con 64
núcleos se pasa de 2 veces.
Derecha: cuántos entrelazados admite un programa de n hilos con tres acciones cada uno
(leer, sumar, escribir) y cuántos de ellos acaban con el resultado correcto. Se enumeran
todos para 2, 3 y 4 hilos; para 5 y 6 se usa la fórmula, porque son cientos de millones.
La figura de la página de concurrencia y paralelismo (fase 10).

Los dos paneles son cálculo exacto (la ley de Amdahl y el recuento de entrelazados
enumerados), así que no hay nada que sortear: la figura no necesita semilla aleatoria.
"""

import math

import numpy as np

from comun import *

estilo()


def num(x, dec=2):
    """Números con coma decimal, como se escriben en el portal."""
    return ("%.*f" % (dec, x)).replace(".", ",")


fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.4))

# --- Izquierda: ley de Amdahl --------------------------------------------------------
nucleos = np.arange(1, 65)
ax = ejes[0]
for p, color, altura in [(0.5, ROJO, 0.10), (0.8, AZUL, 0.245), (0.9, VERDE, 0.44),
                         (0.95, MORADO, 0.78)]:
    ax.plot(nucleos, 1 / ((1 - p) + p / nucleos), color=color, linewidth=1.9)
    ax.axhline(1 / (1 - p), color=color, linewidth=0.9, linestyle=":", alpha=0.6)
    # Etiqueta directa al final de cada curva: no hace falta leyenda y se ve de un golpe
    # dónde está el techo de cada una.
    anotar(ax, "p = {} % (techo {}×)".format(num(100 * p, 0), num(1 / (1 - p), 0)),
           xy=(64.0, 1 / ((1 - p) + p / 64)), xytext=(0.97, altura), color=color,
           flecha=False, align="right")
ax.set_xscale("log", base=2)
ax.set_xticks([1, 2, 4, 8, 16, 32, 64])
ax.set_xticklabels(["1", "2", "4", "8", "16", "32", "64"])
ax.set_ylim(0.5, 21.0)
ax.scatter([4.0], [1 / ((1 - 0.8) + 0.8 / 4)], s=32, color=AZUL, zorder=5)
anotar(ax, "el techo lo pone la fracción en serie,\nno el número de núcleos",
       xy=(10.0, 1 / ((1 - 0.95) + 0.95 / 10)), xytext=(0.03, 0.92), color=TEXTO,
       flecha=False)
anotar(ax, "con 4 núcleos, p = 80 % da {} veces".format(num(1 / ((1 - 0.8) + 0.8 / 4))),
       xy=(4.0, 1 / ((1 - 0.8) + 0.8 / 4)), xytext=(0.03, 0.66), color=AZUL)
titulo(ax, "El techo lo pone la parte que no se reparte",
       "aceleración S(n) = 1 / ((1 − p) + p/n) frente al número de núcleos")
ax.set_xlabel("núcleos o trabajadores (escala logarítmica)")
ax.set_ylabel("veces más rápido que con uno")
rejilla(ax)
numeros(ax, ejes="y")


# --- Derecha: cuántos entrelazados hay y cuántos salen bien --------------------------
def entrelazados_validos(n):
    """Enumera los entrelazados de n hilos con tres acciones (leer, sumar, escribir).

    Cada hilo hace un incremento sobre un contador compartido que empieza en 0. Devuelve
    cuántos entrelazados hay y cuántos acaban con el valor n, que es lo correcto.
    """
    total = correctos = 0

    def recorrer(progreso, leido, valor):
        nonlocal total, correctos
        if all(p == 3 for p in progreso):         # 3 = ya ha escrito
            total += 1
            if valor == n:
                correctos += 1
            return
        for h in range(n):
            if progreso[h] == 0:                  # leer el contador compartido
                recorrer(progreso[:h] + (1,) + progreso[h + 1:],
                         leido[:h] + (valor,) + leido[h + 1:], valor)
            elif progreso[h] == 1:                # sumar en local: no toca memoria compartida
                recorrer(progreso[:h] + (2,) + progreso[h + 1:], leido, valor)
            elif progreso[h] == 2:                # escribir: pisa lo que haya
                recorrer(progreso[:h] + (3,) + progreso[h + 1:], leido, leido[h] + 1)

    recorrer(tuple([0] * n), (None,) * n, 0)
    return total, correctos


hilos = np.arange(2, 7)
validos, correctos = [], []
for n in hilos:
    if n <= 4:
        # Hasta 4 hilos se pueden enumerar todos: 369.600 en el peor caso, y así el
        # «solo 24 acaban bien» está contado, no supuesto.
        total, bien = entrelazados_validos(int(n))
    else:
        total = math.factorial(3 * n) // math.factorial(3) ** n
        bien = math.factorial(n)                  # solo los totalmente en serie
    validos.append(total)
    correctos.append(bien)

ax = ejes[1]
ax.semilogy(hilos, validos, color=AZUL, linewidth=1.9, marker="o", markersize=5)
ax.semilogy(hilos, correctos, color=VERDE, linewidth=1.9, marker="s", markersize=5)
ax.set_ylim(0.6, 1e15)
anotar(ax, "entrelazados posibles", xy=(6.0, validos[-1]), xytext=(0.97, 0.80),
       color=AZUL, flecha=False, align="right")
anotar(ax, "los que dan el resultado correcto", xy=(6.0, correctos[-1]),
       xytext=(0.97, 0.24), color=VERDE, flecha=False, align="right")
anotar(ax, "con 2 hilos: 20 entrelazados y 18 pierden una actualización;\n"
           "con 4: {} entrelazados y solo {} acaban bien"
       .format(num(validos[2], 0), num(correctos[2], 0)),
       xy=(3.0, validos[1]), xytext=(0.03, 0.88), color=TEXTO)
titulo(ax, "Casi ningún entrelazado sale bien",
       "entrelazados de n hilos con 3 acciones cada uno (contados: 2 a 4 · calculados: 5 y 6)")
ax.set_xlabel("hilos, cada uno con un incremento del contador")
ax.set_ylabel("cuántos entrelazados hay (escala logarítmica)")
ax.set_xticks(hilos)
rejilla(ax)
numeros(ax, ejes="x")

guardar(fig, "amdahl-y-entrelazados")
