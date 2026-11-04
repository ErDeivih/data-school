"""autovalores-y-autovectores-1.py — qué es un autovector: la dirección que la matriz no gira.
Figura de la página de autovalores y autovectores (fase 1)."""

import numpy as np

from comun import *

estilo()

A = np.array([[2.0, 1.0], [1.0, 2.0]])
w, V = np.linalg.eigh(A)          # simétrica: autovalores reales, autovectores ortogonales
v1, v2 = V[:, 1], V[:, 0]         # eigh ordena de menor a mayor: v1 es el dominante

# --- Círculo unidad y su imagen: la matriz convierte el círculo en una elipse ---
t = np.linspace(0, 2 * np.pi, 400)
circulo = np.stack([np.cos(t), np.sin(t)])
elipse = A @ circulo              # A aplicada a CADA columna: (2, 2) @ (2, 400) -> (2, 400)

fig, (izq, der) = plt.subplots(1, 2, figsize=(10.0, 4.6))

izq.plot(circulo[0], circulo[1], color=REJILLA, linewidth=1.4, label="círculo unidad")
izq.plot(elipse[0], elipse[1], color=MORADO, linewidth=1.8, label="su imagen con A")

# Los dos autovectores: al transformarlos solo cambian de longitud, no de dirección.
for vec, lam, col in [(v1, w[1], ROJO), (v2, w[0], VERDE)]:
    izq.annotate("", xy=vec * lam, xytext=(0, 0),
                 arrowprops=dict(arrowstyle="-|>", color=col, linewidth=2.2, shrinkA=0, shrinkB=0))
    izq.annotate("", xy=vec, xytext=(0, 0),
                 arrowprops=dict(arrowstyle="-|>", color=col, linewidth=1.0, linestyle="--",
                                 alpha=0.6, shrinkA=0, shrinkB=0))
    izq.text(vec[0] * (lam + 0.30), vec[1] * (lam + 0.30),
             "$\\lambda$ = " + coma(lam), color=col, fontsize=9, ha="center", va="center")

# Las dos anotaciones van a las franjas libres de arriba y de abajo: la elipse solo llega a
# 2,24 de altura, asi que por encima y por debajo de esos extremos no hay nada.
anotar(izq, "estas dos direcciones no giran: solo se estiran",
       xy=(v1[0] * w[1] * 0.72, v1[1] * w[1] * 0.72), xytext=(0.02, 0.95), color=ROJO)
bajo = int(np.argmin(elipse[1]))          # el punto mas bajo de la elipse: la flecha es corta
anotar(izq, "cada flecha del círculo\nacaba en la elipse",
       xy=(elipse[0][bajo], elipse[1][bajo]), xytext=(0.02, 0.10), color=MORADO)
izq.plot(0, 0, marker="o", color=TEXTO, markersize=3)
izq.set_xlim(-3.5, 3.5)
izq.set_ylim(-3.1, 3.6)
izq.set_aspect("equal")
titulo(izq, "A gira casi todo salvo las direcciones propias",
       "los autovectores solo cambian de longitud")
izq.set_xlabel("primera coordenada")
izq.set_ylabel("segunda coordenada")
izq.legend(loc="lower right")
rejilla(izq, "both")
numeros(izq)

# --- Iteración de potencias: por qué manda el autovalor dominante ---
x = np.array([1.0, 0.0])
pasos = 20
traza = [x.copy()]
for _ in range(pasos):
    x = A @ x
    x = x / np.linalg.norm(x)
    traza.append(x.copy())
traza = np.array(traza)

dominante = v1 / np.linalg.norm(v1)
desvio = np.abs(1.0 - np.abs(traza @ dominante))     # 0.0 = la dirección ya es la dominante

der.semilogy(np.arange(pasos + 1), desvio, color=AZUL, linewidth=1.8, marker="o", markersize=3)
# La curva cae de arriba a la izquierda a abajo a la derecha: el hueco de arriba a la
# derecha lo ocupa la primera nota y la segunda va debajo de la curva, con el texto partido
# en tres lineas para que no llegue a cruzarla.
anotar(der, "al empezar, la dirección (1, 0) dista\nun " + coma(round(float(desvio[0]), 3))
       + " de la dominante", xy=(0, desvio[0]), xytext=(0.34, 0.87), color=AZUL)
anotar(der, "cada paso lo divide entre 3:\npor eso manda el autovalor 3\ny no el 1",
       xy=(9, desvio[9]), xytext=(0.02, 0.20), color=NARANJA)
der.set_ylim(1e-12, desvio[0] * 8)
titulo(der, "Iteración de potencias", "la distancia a la dirección dominante se desploma")
der.set_xlabel("número de multiplicaciones por A")
der.set_ylabel("distancia al autovector dominante (escala logarítmica)")
rejilla(der)
numeros(der)

guardar(fig, "autovalores-direcciones-propias")
