"""regla-de-la-cadena-1.py — derivar una composición es multiplicar las pendientes de sus

etapas; en una cadena larga ese producto se desploma (o explota).
Figura de la página de regla de la cadena (fase 1)."""

import numpy as np

from comun import *

estilo()


def g(x):
    return 3 * x + 1          # etapa interna
def f(u):
    return u ** 4             # etapa externa


x0 = 2.0
u0 = g(x0)
pend_g = 3.0                  # g'(x) = 3
pend_f = 4 * u0 ** 3          # f'(u) = 4u^3 evaluada en u = 7
total = pend_f * pend_g

fig, (izq, der) = plt.subplots(2, 1, figsize=(9.6, 8.2))
fig.set_constrained_layout_pads(h_pad=0.09)   # aire entre los dos paneles

# --- Panel de arriba: la composición, paso a paso ---
x = np.linspace(0.5, 3.0, 300)

izq.plot(x, g(x), color=AZUL, linewidth=1.9, label="etapa interna: u = 3x + 1")
izq.plot(x0, u0, marker="o", color=TEXTO, markersize=5)
# El punto (x=2, u=7) se señala desde la esquina de arriba a la izquierda, que es la única
# zona del panel sin curva, sin triángulo y sin leyenda.
izq.annotate(f"aquí x = {coma(x0)} y la interna está en u = {coma(u0)}",
             xy=(x0, u0), xytext=(0.04, 0.93), textcoords="axes fraction",
             fontsize=9, color=AZUL, va="center", ha="left",
             arrowprops=dict(arrowstyle="->", color=AZUL, linewidth=0.9, shrinkA=2, shrinkB=2))
# El triangulo: 1 de avance en x, 3 de subida en u. Esa es la pendiente de la etapa.
izq.plot([x0, x0 + 1.0], [u0, u0], color=NARANJA, linewidth=1.4)
izq.plot([x0 + 1.0, x0 + 1.0], [u0, u0 + pend_g], color=NARANJA, linewidth=1.4)
izq.annotate(f"1 unidad de x sube {coma(pend_g)} de u:\nésa es la primera pendiente",
             xy=(x0 + 0.5, u0 + 1.4), xytext=(0.62, 0.20), textcoords="axes fraction",
             fontsize=9, color=NARANJA, va="center", ha="left",
             arrowprops=dict(arrowstyle="->", color=NARANJA, linewidth=0.9, shrinkA=2, shrinkB=2))
izq.set_xlim(0.5, 3.0)
izq.set_ylim(2.0, 11.5)
titulo(izq, f"De x a u: la primera etapa multiplica por {coma(pend_g)}")
izq.set_xlabel("x")
izq.set_ylabel("u")
izq.legend(loc="upper right")
rejilla(izq, "both")
numeros(izq)

# --- Panel de abajo: la misma idea en una cadena de 30 etapas ---
pasos = np.arange(0, 31)
der.semilogy(pasos, 0.7 ** pasos, color=AZUL, linewidth=1.9, label="cada etapa multiplica por 0,7")
der.semilogy(pasos, 1.4 ** pasos, color=ROJO, linewidth=1.9, label="cada etapa multiplica por 1,4")
der.axhline(1.0, color=REJILLA, linewidth=1.0, linestyle="--")
# Cada nota va en la franja vacía que le toca: la azul, en el hueco de abajo a la
# izquierda; la roja, en el de arriba a la izquierda, por debajo de la leyenda. En escala
# logarítmica el texto ocupa mucho alto, así que hay que dejarle margen de sobra.
anotar(der, f"tras 20 etapas queda {0.7 ** 20:.1e}:\n"
            f"el gradiente de las primeras capas\nya no mueve nada (se desvanece)",
      xy=(20, 0.7 ** 20), xytext=(0.05, 0.22), color=AZUL)
anotar(der, "si cada etapa multiplica por más de 1,\nel producto explota",
      xy=(26, 1.4 ** 26), xytext=(0.05, 0.68), color=ROJO)
der.set_ylim(1e-10, 1e9)
titulo(der, "Cadena larga: la pendiente total se multiplica")
der.set_xlabel("número de etapas encadenadas")
der.set_ylabel("pendiente acumulada (escala logarítmica)")
der.legend(loc="upper left")
rejilla(der)
numeros(der)

guardar(fig, "cadena-multiplicar-pendientes")
