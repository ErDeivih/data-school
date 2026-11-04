"""atencion-1.py — por qué hay que dividir las puntuaciones entre la raíz de d_k.

Izquierda: el mismo reparto de peso en dos casos. Con puntuaciones [8, 0, -8] el softmax sin
escalar da 0,9997 a una sola clave y deja las otras dos a cero: el modelo ha dejado de
mezclar. Dividiendo entre la raíz de d_k las tres claves reciben señal.
Derecha: eso no es un caso extremo elegido a mano. Al crecer la dimensión, el producto punto
de vectores aleatorios tiene desviación típica raíz de d_k, así que el peso máximo sin escalar
se va a 1 y con el escalado se mantiene.
La figura de la página de mecanismos de atención (fase 7).
"""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)


def softmax(z):
    """Softmax estable: restar el máximo no cambia el resultado y evita desbordar exp()."""
    e = np.exp(z - z.max())
    return e / e.sum()


fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.4))

# --- Izquierda: el mismo caso contado dos veces ---------------------------------------
ax = ejes[0]
# d_k = 64: la desviación típica de los productos punto es raíz de 64 = 8, y de ahí salen
# las puntuaciones 8, 0 y -8 en las que se fija el ejemplo de la página.
sin_escalar = softmax(np.array([8.0, 0.0, -8.0]))          # sin dividir
escalado = softmax(np.array([8.0, 0.0, -8.0]) / np.sqrt(64))   # dividiendo entre 8
posiciones = np.arange(3)
ancho = 0.36
b1 = ax.bar(posiciones - ancho / 2, sin_escalar, ancho, color=ROJO)
b2 = ax.bar(posiciones + ancho / 2, escalado, ancho, color=VERDE)
for barras in (b1, b2):                 # el valor encima: las barras diminutas no se ven
    ax.bar_label(barras, labels=[f"{v:.4f}".replace(".", ",") for v in barras.datavalues],
                 padding=3, fontsize=8)
# Las dos notas van arriba a la derecha, donde las barras de la clave 3 dejan hueco.
anotar(ax, "sin escalar: una clave se lleva\ncasi todo el peso", xy=(0.0, 0.9997),
       xytext=(0.52, 0.90), color=ROJO)
anotar(ax, "escalado: las tres claves\nreciben señal", xy=(2.18, 0.05),
       xytext=(0.52, 0.66), color=VERDE)
titulo(ax, "El softmax se satura sin el 1/√d_k",
       "peso de atención sobre tres claves con puntuaciones 8, 0 y −8")
ax.set_xticks(posiciones, ["clave 1", "clave 2", "clave 3"])
ax.set_ylabel("peso de atención (suman 1)")
ax.set_ylim(0, 1.22)                    # aire arriba para las notas y los valores
rejilla(ax)
numeros(ax, ejes="y")                   # el eje x es de categorías: no lleva coma decimal


def peso_maximo(d_k, escalar, n_claves=256, repeticiones=40):
    """Peso de atención más alto, promediado, sobre `n_claves` claves al azar.

    Consulta y claves se sortean con media 0 y varianza 1, que es el supuesto del que sale
    el factor 1/√d_k. `escalar` decide si se divide o no.
    """
    maximos = []
    for _ in range(repeticiones):
        q = azar.normal(size=d_k)
        K = azar.normal(size=(n_claves, d_k))
        puntos = K @ q                          # un producto punto por clave
        if escalar:
            puntos = puntos / np.sqrt(d_k)
        maximos.append(float(softmax(puntos).max()))
    return float(np.mean(maximos))


# --- Derecha: lo que pasa al crecer la dimensión --------------------------------------
ax = ejes[1]
dimensiones = np.array([2, 4, 8, 16, 32, 64, 128, 256, 512])
crudo = [peso_maximo(int(d), False) for d in dimensiones]
escalado_d = [peso_maximo(int(d), True) for d in dimensiones]
ax.semilogx(dimensiones, crudo, color=ROJO, linewidth=1.8, marker="o", markersize=5,
            base=2)
ax.semilogx(dimensiones, escalado_d, color=VERDE, linewidth=1.8, marker="o", markersize=5,
            base=2)
anotar(ax, "sin dividir: el peso máximo\nse pega a 1", xy=(512, crudo[-1]),
       xytext=(0.03, 0.78), color=ROJO)
anotar(ax, "dividiendo entre √d_k\nel reparto se mantiene", xy=(512, escalado_d[-1]),
       xytext=(0.42, 0.22), color=VERDE)
titulo(ax, "Más dimensión, más se satura",
       "peso máximo medio sobre 256 claves, según d_k, en escala logarítmica")
ax.set_xlabel("dimensión de claves y consultas (d_k)")
ax.set_ylabel("peso de atención máximo")
ax.set_ylim(0, 1.10)
ax.set_xticks(dimensiones, [str(d) for d in dimensiones])
rejilla(ax)
numeros(ax, ejes="both")

guardar(fig, "atencion-escalado-de-puntuaciones")
