"""eda-pasos-1.py — el paso 2 del método exploratorio, que es el que casi nadie comprueba:
qué es una fila. A la izquierda, tres claves candidatas sobre las mismas ocho filas y lo que
devuelve cada una; a la derecha, el ticket medio que sale según la clave elegida. Solo la
clave correcta cuadra con la verdad, y las otras dos fallan sin dar ningún error.

Página de análisis exploratorio (fase 5)."""

import numpy as np

from comun import *

estilo()

# Ocho líneas de pedido: cinco pedidos de tres clientes. El grano real es «una línea», y
# quien crea que es «un pedido» cambia el ticket medio sin que nada avise.
lineas = np.array([
    # pedido, linea, cliente, importe
    (1, 1, 10, 10.00),
    (1, 2, 10,  5.50),
    (2, 1, 11, 20.00),
    (3, 1, 12,  4.25),
    (3, 2, 12,  6.00),
    (4, 1, 13, 12.00),
    (5, 1, 13,  8.00),
    (5, 2, 13,  3.00),
])

pedido = lineas[:, 0].astype(int)
cliente = lineas[:, 2].astype(int)
importe = lineas[:, 3]
filas = lineas.shape[0]
total = importe.sum()

# Las tres claves candidatas: dos que se quedan cortas y la que identifica la fila.
claves = ["pedido_id", "cliente_id", "pedido_id + linea"]
distintos = np.array([np.unique(pedido).size, np.unique(cliente).size,
                      np.unique(pedido * 100 + lineas[:, 1].astype(int)).size])
ticket_medio = total / distintos
colores = [ROJO, NARANJA, VERDE]

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.4),
                         gridspec_kw={"width_ratios": [1.15, 1.0]})

# ── Izquierda: la comprobación del grano, clave por clave ─────────────────────
eje = ejes[0]
y = np.array([2, 1, 0])
eje.barh(y, distintos, height=0.5, color=colores, alpha=0.9)
eje.axvline(filas, color=TEXTO, linewidth=1.4, linestyle="--")
eje.text(filas, 2.72, f"{filas} filas", ha="right", va="bottom", fontsize=8.5, color=TEXTO)
for yi, n in zip(y, distintos):
    dentro = n == filas
    eje.text(n - 0.12 if dentro else n + 0.06, yi, f"{n}", va="center",
             ha="right" if dentro else "left", fontsize=9,
             color=VERDE if dentro else TEXTO)
titulo(eje, "El grano se comprueba contando, no mirando",
       "La clave candidata vale si sus valores distintos igualan las filas de la tabla")
eje.set_yticks(y)
eje.set_yticklabels(claves)
eje.set_ylim(-0.55, 3.05)
eje.set_xlabel("valores distintos de la clave")
eje.set_xlim(0, 9.4)
rejilla(eje, eje="x")
numeros(eje, "x")

# ── Derecha: lo que cuesta elegir mal la clave ────────────────────────────────
eje = ejes[1]
x = np.arange(3)
eje.bar(x, ticket_medio, width=0.55, color=colores, alpha=0.9)
eje.axhline(ticket_medio[2], color=VERDE, linewidth=1.4, linestyle="--")
for xi, tm, n, col in zip(x, ticket_medio, distintos, colores):
    eje.text(xi, tm + 0.5, f"{tm:.2f}".replace(".", ","), ha="center", fontsize=9, color=col)
eje.text(x[0], ticket_medio[0] / 2, f"×{filas / distintos[0]:.2f}".replace(".", ","),
         ha="center", va="center", fontsize=9, color=TEXTO)
anotar(eje, "solo la clave que identifica la fila\ndevuelve el ticket de verdad",
       xy=(2, float(ticket_medio[2])), xytext=(0.98, 0.94), color=VERDE, flecha=False,
       align="right")
titulo(eje, "La misma tabla, tres tickets medios",
       "Suma de las ocho líneas: 68,75 €")
eje.set_xticks(x)
eje.set_xticklabels(claves, fontsize=8.5)
eje.set_ylabel("ticket medio (€)")
eje.set_ylim(0, 21)
rejilla(eje)
numeros(eje, "y")

guardar(fig, "eda-pasos-grano-y-ticket-medio")
