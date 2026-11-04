"""arrays-y-listas-1.py — la memoria la paga el puntero y el tiempo lo paga la posición.

Izquierda: lo que ocupa lo mismo guardado en una lista de Python y en un array de NumPy. La
lista guarda 8 bytes de puntero por elemento y además el objeto entero, que vive aparte; el
array guarda los 8 bytes del número y nada más.
Derecha: el mismo trabajo hecho por el principio y por el final. Meter n elementos al
principio desplaza n(n−1)/2 elementos; añadirlos al final solo copia cuando se agota la
capacidad, y eso suma 2n. Es la diferencia entre O(n²) y O(n).
La figura de la página de arrays y listas (fase 10).
"""

import numpy as np

from comun import *

estilo()

n = np.logspace(3, 7, 60)            # de mil a diez millones de elementos

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.4))

# --- Izquierda: qué ocupa cada forma de guardar los mismos números ---------------
ax = ejes[0]
mem_lista = 8 * n + 28 * n            # puntero de 8 bytes + un objeto int de 28 por elemento
mem_array = 8 * n                     # int64 pegado, sin punteros
ax.loglog(n, mem_lista / 1e6, color=ROJO, linewidth=2.0)
ax.loglog(n, mem_array / 1e6, color=AZUL, linewidth=2.0)
# Las dos rectas son paralelas: la lista no es «un poco» más grande, es 4,5 veces más grande
# para cualquier tamaño. La distancia vertical es constante y ese es el mensaje.
ax.annotate("", xy=(4e6, 36.0), xytext=(4e6, 8.0),
            arrowprops=dict(arrowstyle="<->", color=MORADO, linewidth=1.4))
anotar(ax, "lista de Python:\n8 bytes de puntero + 28 del entero",
       xy=(1.2e4, 0.43), xytext=(0.06, 0.92), color=ROJO)
anotar(ax, "array de NumPy:\n8 bytes pegados",
       xy=(8e3, 0.064), xytext=(0.48, 0.20), color=AZUL)
anotar(ax, "×4,5 siempre:\nla distancia no se cierra",
       xy=(4e6, 20.0), xytext=(0.60, 0.62), color=MORADO, flecha=False)
titulo(ax, "La lista de Python pesa 4,5 veces más",
       "millones de bytes, en escala doble logarítmica, para los mismos enteros")
ax.set_xlabel("elementos guardados")
ax.set_ylabel("MB ocupados")
rejilla(ax, eje="both")
numeros(ax)

# --- Derecha: el mismo trabajo por el principio y por el final -------------------
ax = ejes[1]
def al_principio(k):
    """Insertar k elementos uno detrás de otro al principio de la lista."""
    return k * (k - 1) // 2

def al_final(k):
    """Añadir k elementos al final: solo se copia al duplicar la capacidad."""
    return 2 * k

k = np.logspace(2, 6, 80)
ax.loglog(k, [al_principio(int(x)) for x in k], color=ROJO, linewidth=2.0)
ax.loglog(k, [al_final(int(x)) for x in k], color=VERDE, linewidth=2.0)
anotar(ax, "al principio: O(n²)\nun desplazamiento por cada hueco",
       xy=(2e2, 2e4), xytext=(0.18, 0.26), color=ROJO)
anotar(ax, "al final: O(n)\n131.071 copias con 100.000 elementos",
       xy=(2e5, 2.5e5), xytext=(0.22, 0.74), color=VERDE)
anotar(ax, "de 100.000 a 1.000.000 de elementos,\nla brecha pasa de millones a billones",
       xy=(2e5, 2e10), xytext=(0.46, 0.16), color=MORADO, flecha=False)
titulo(ax, "Entrar por el principio condena el programa",
       "elementos desplazados al insertar n elementos, según por dónde entren")
ax.set_xlabel("elementos insertados")
ax.set_ylabel("desplazamientos acumulados")
rejilla(ax, eje="both")
numeros(ax)

guardar(fig, "arrays-memoria-y-coste-de-insertar")
