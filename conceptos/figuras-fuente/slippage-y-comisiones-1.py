"""slippage-y-comisiones-1.py — los tres costes de la ida y vuelta y cómo el impacto
por raíz cuadrada se come la ventaja bruta al crecer el nominal. Figura de la página
de deslizamiento y comisiones (fase 9)."""

import numpy as np

from comun import *

estilo()

comision_pb = 4.0          # por punta: se paga al entrar y al salir
diferencial_pb = 4.0       # cruzar a mercado una vez por vuelta
ventaja_bruta_pb = 15.0
k = 1.0                    # impacto en pb con el nominal de referencia
V = 25_000                 # nominal de referencia

nominal = np.linspace(5_000, 350_000, 400)
impacto = k * np.sqrt(nominal / V)
coste = 2 * comision_pb + diferencial_pb + impacto
neta = ventaja_bruta_pb - coste

# Donde la ventaja neta se anula: por encima, la estrategia no existe
cruce = int(np.argmax(neta < 0))
nominal_cruce = nominal[cruce]

fig, ejes = plt.subplots(2, 1, figsize=(7.0, 5.6))

# ── Panel de arriba: de qué está hecho el coste ────────────────────────────────
eje = ejes[0]
eje.fill_between(nominal, 2 * comision_pb, color=AZUL, alpha=0.30,
                 label="comisión · 2 puntas")
eje.fill_between(nominal, 2 * comision_pb, 2 * comision_pb + diferencial_pb,
                 color=NARANJA, alpha=0.35, label="diferencial · una vez por vuelta")
eje.fill_between(nominal, 2 * comision_pb + diferencial_pb, coste,
                 color=ROJO, alpha=0.35, label="impacto · crece con la raíz del tamaño")
eje.axhline(ventaja_bruta_pb, color=VERDE, linewidth=1.6, linestyle="--")
titulo(eje, "La ventaja es fija y el coste crece con el tamaño",
       "Los tres costes se suman por operación; la línea verde es lo que gana la señal antes de costes")
eje.set_ylabel("puntos básicos")
eje.set_xlim(nominal[0], nominal[-1])
eje.set_ylim(0, 22.5)
eje.legend(loc="upper left", ncol=2, fontsize=8, handlelength=1.2, columnspacing=1.0)
anotar(eje, "la señal gana 15 pb brutos, siempre", (300_000, ventaja_bruta_pb),
       (0.97, 0.63), color=VERDE, align="right")
anotar(eje, "la comisión se paga al entrar y al salir", (40_000, 2 * comision_pb),
       (0.05, 0.26), color=AZUL)
rejilla(eje)

# ── Panel de abajo: la resta que decide si la estrategia existe ────────────────
eje = ejes[1]
eje.plot(nominal, neta, color=MORADO, linewidth=1.9)
eje.axhline(0, color=TEXTO, linewidth=1.0)
eje.fill_between(nominal, neta, 0, where=(neta > 0), color=VERDE, alpha=0.16)
eje.fill_between(nominal, neta, 0, where=(neta <= 0), color=ROJO, alpha=0.16)
eje.axvline(nominal_cruce, color=ROJO, linewidth=1.1, linestyle=":")
titulo(eje, "El tamaño de la orden decide si la estrategia vive",
       "Ventaja neta por operación: ventaja bruta menos los tres costes")
eje.set_xlabel("nominal de la orden, en EUR")
eje.set_ylabel("ventaja neta (pb)")
eje.set_xlim(nominal[0], 350_000)
eje.set_ylim(-1.4, 5.0)
rejilla(eje)
anotar(eje, f"con {nominal_cruce/1000:.0f} mil EUR la ventaja neta llega a cero",
       (nominal_cruce, 0.0),
       (0.62, 0.85), color=ROJO)
anotar(eje, "aquí la señal aún paga, pero el margen es fino",
       (30_000, float(np.interp(30_000, nominal, neta))),
       (0.05, 0.62), color=VERDE, flecha=False)

numeros(ejes[0])
numeros(ejes[1])

guardar(fig, "slippage-coste-y-tamano")
