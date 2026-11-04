"""derivadas-y-reglas-1.py — la derivada es el límite del cociente incremental, y con h

demasiado pequeño la resta se come la respuesta.
Figura de la página de derivadas y reglas de derivación (fase 1)."""

import numpy as np

from comun import *

estilo()


def f(x):
    return 3 * x ** 2 - 2 * x + 1


def secante(x, h):
    return (f(x + h) - f(x)) / h


# --- Panel izquierdo: la secante se convierte en tangente ---
x = np.linspace(0.0, 4.2, 400)
izq_der = f(2.0)
izq_pen = 6 * 2.0 - 2                     # derivada exacta: f'(x) = 6x - 2

fig, (izq, der) = plt.subplots(1, 2, figsize=(10.6, 4.4))

izq.plot(x, f(x), color=AZUL, linewidth=1.8, label="f(x) = 3x² − 2x + 1")
izq.plot(x, f(2.0) + izq_pen * (x - 2.0), color=ROJO, linewidth=1.6,
         label="tangente en x = 2 (pendiente 10)")
for h, col in [(1.0, NARANJA), (0.5, VERDE), (0.1, CIAN)]:
    pend = secante(2.0, h)
    # La etiqueta se monta con % y NO con f-string: el corrector de tildes de las figuras
    # protege las expresiones {...} con un centinela que a veces deja dentro del texto, y
    # esos bytes salen luego como cuadraditos en el SVG (incidente del 2026-10-15).
    izq.plot(x, f(2.0) + pend * (x - 2.0), color=col, linewidth=1.0, linestyle="--",
             label="secante con h = %s (pendiente %s)" % (coma(h), coma(round(pend, 2))))
izq.plot([2.0], [f(2.0)], marker="o", color=TEXTO, markersize=5)
# La nota va por debajo de la leyenda, en la franja vacía que queda por encima de todas
# las rectas a la izquierda de x = 2, y señala el punto de tangencia.
anotar(izq, "al encoger h, la secante\nse pega a la tangente", xy=(2.0, f(2.0)),
       xytext=(0.03, 0.60), color=ROJO)
izq.set_xlim(0.0, 4.2)
izq.set_ylim(-1.0, 26.0)
titulo(izq, "La derivada es a donde van las secantes")
izq.set_xlabel("x")
izq.set_ylabel("f(x)")
izq.legend(loc="upper left")
rejilla(izq, "both")
numeros(izq)

# --- Panel derecho: el error de la diferencia hacia delante según h ---
hs = np.logspace(-16, 0, 300)
error = np.abs((f(2.0 + hs) - f(2.0)) / hs - izq_pen)


def error_en(h):
    return float(error[int(np.argmin(np.abs(hs - h)))])


der.loglog(hs, error, color=MORADO, linewidth=1.7)
mejor = int(np.argmin(error))
der.plot(hs[mejor], error[mejor], marker="o", markersize=9, markerfacecolor="none",
         markeredgecolor=ROJO, markeredgewidth=1.6)
# El mínimo se señala desde abajo a la derecha: la curva de la subida deja libre todo el
# hueco por debajo de ella, que es donde antes se pisaban las dos notas.
anotar(der, "el mejor h ronda %.0e:\naquí el error es %.0e" % (hs[mejor], error[mejor]),
       xy=(hs[mejor], error[mejor]), xytext=(0.56, 0.13), color=ROJO)
anotar(der, "con h grande manda el error\nde la fórmula: la curva se dobla",
       xy=(1e-1, error_en(1e-1)), xytext=(0.56, 0.93), color=NARANJA)
anotar(der, "con h diminuto manda el redondeo\nde la resta y el error vuelve a subir",
       xy=(1e-12, error_en(1e-12)), xytext=(0.02, 0.10), color=CIAN)
der.set_ylim(1e-12, 1e3)
titulo(der, "Hay un tamaño de paso óptimo",
       "encoger h sin mirar no ayuda: con h diminuto manda el redondeo de la resta")
der.set_xlabel("h: tamaño del paso en el cociente incremental")
der.set_ylabel("error frente a la derivada exacta")
rejilla(der, "both")
numeros(der)

guardar(fig, "derivadas-tangente-y-paso")
