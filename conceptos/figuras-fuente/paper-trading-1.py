"""paper-trading-1.py — por qué un resultado positivo en el simulador no dice si la
estrategia gana: el coste que la demo no cobra cambia el signo de la esperanza.
Figura de la página de paper trading (fase 9)."""

import numpy as np

from comun import *

estilo()

ganancia = 1.2        # % medio de las operaciones ganadoras
perdida = 1.0         # % medio de las perdedoras, en positivo
aciertos = 0.55       # proporción de aciertos del ejemplo
capital = 2_000.0     # EUR por operación

p = np.linspace(0.35, 0.70, 300)
costes = [(0.0, ROSA, "0 %: lo que te enseña el simulador"),
          (0.10, NARANJA, "0,10 %: valor muy líquido"),
          (0.25, AZUL, "0,25 %: valor de liquidez media")]

fig, ejes = plt.subplots(2, 1, figsize=(7.0, 5.8))

# ── Panel de arriba: donde la esperanza cambia de signo ────────────────────────
eje = ejes[0]
eje.axhline(0, color=TEXTO, linewidth=1.0)
for coste, color, etiqueta in costes:
    eje.plot(p, p * ganancia - (1 - p) * perdida - coste, color=color,
             linewidth=1.9, label=etiqueta)
    p_equilibrio = (perdida + coste) / (ganancia + perdida)
    eje.plot(p_equilibrio, 0.0, marker="o", color=color, markersize=5)
eje.axvline(aciertos, color=REJILLA, linewidth=1.0, linestyle=":")
titulo(eje, "El coste sube el acierto mínimo que hace falta para ganar",
       "Esperanza por operación según el porcentaje de aciertos; ganancia 1,2 % y pérdida 1,0 %")
eje.set_xlabel("proporción de operaciones ganadoras")
eje.set_ylabel("esperanza por operación (%)")
eje.set_xlim(0.35, 0.70)
eje.set_ylim(-0.55, 0.55)
rejilla(eje)
eje.legend(loc="upper left", fontsize=8)
anotar(eje, "con el 55 % de aciertos del ejemplo,\ncon 0,25 % de coste ya se pierde",
       (aciertos, 0.0), (0.06, 0.50), color=ROJO, flecha=True)

# ── Panel de abajo: lo que pasa al repetir la operación 200 veces ──────────────
eje = ejes[1]
n = 200
operaciones = np.arange(n + 1)
for coste, color, etiqueta in costes:
    esperanza_pct = aciertos * ganancia - (1 - aciertos) * perdida - coste
    eje.plot(operaciones, capital * esperanza_pct / 100 * operaciones,
             color=color, linewidth=1.9)
eje.axhline(0, color=TEXTO, linewidth=1.0)
titulo(eje, "En 200 operaciones, el coste decide el signo del resultado",
       "Resultado acumulado sobre 2.000 EUR por operación, sin componer")
eje.set_xlabel("número de operaciones")
eje.set_ylabel("resultado acumulado\n(EUR)")
eje.set_xlim(0, n)
rejilla(eje)
eje.text(4, capital * 0.40, "el simulador te enseña esta",
         fontsize=8, color=ROSA, va="center")
eje.text(4, -capital * 0.22, "esta es la que vas a tener",
         fontsize=8, color=AZUL, va="center")

numeros(ejes[0])
numeros(ejes[1])

guardar(fig, "paper-trading-el-coste-que-falta")
