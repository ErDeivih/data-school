"""retornos-logaritmicos-1.py — sumar log-retornos es exacto y sumar porcentajes no, y
los logaritmos son simétricos mientras que los porcentajes no. Figura de la página de
retornos logarítmicos (fase 9)."""

import matplotlib.pyplot as plt
import numpy as np

from comun import *

estilo()
plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9,
                     "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 7.5})

# ── Panel de arriba: quién se puede sumar para acumular el retorno ─────────────
azar = np.random.default_rng(7)
n = 60
diarios = azar.normal(0.0008, 0.011, n)      # log-retornos diarios inventados
simples = np.exp(diarios) - 1
instante = np.arange(n + 1)

verdadero = np.concatenate([[0.0], np.cumprod(1 + simples) - 1])
suma_simples = np.concatenate([[0.0], np.cumsum(simples)])

fig, ejes = plt.subplots(2, 1, figsize=(7.0, 5.4))

eje = ejes[0]
eje.plot(instante, 100 * suma_simples, color=NARANJA, linewidth=1.7,
         label="sumando los retornos simples, uno a uno")
eje.plot(instante, 100 * verdadero, color=VERDE, linewidth=2.6,
         label="multiplicando los factores (1 + R): el resultado real")
titulo(eje, "La acumulación correcta no es una suma de porcentajes",
       "Sesenta sesiones inventadas: lo que de verdad gana el capital frente a lo que sale de sumar")
eje.set_xlabel("sesión")
eje.set_ylabel("retorno acumulado (%)")
eje.set_xlim(0, n)
eje.set_ylim(-21, 11)
rejilla(eje)
eje.legend(loc="lower left", fontsize=7.5)
anotar(eje, f"la suma de porcentajes se queda en {100*suma_simples[-1]:.2f} %",
       (n, 100 * suma_simples[-1]), (0.04, 0.90), color=NARANJA, flecha=False)
anotar(eje, f"el capital acaba en {100*verdadero[-1]:.2f} %: la suma se queda "
            f"{100*(suma_simples[-1]-verdadero[-1]):.2f} puntos por debajo",
       (n, 100 * verdadero[-1]), (0.04, 0.69), color=VERDE, flecha=False)

# ── Panel de abajo: la simetría que sí tienen los logaritmos ───────────────────
eje = ejes[1]
movimiento = np.linspace(0.01, 0.50, 300)
nivel_log = 100 * np.ones_like(movimiento)                   # +x % y −x % en log: 100
nivel_simple = 100 * (1 + movimiento) * (1 - movimiento)     # +x % y −x % en simple

eje.plot(100 * movimiento, nivel_log, color=AZUL, linewidth=2.0,
         label="log-retornos: +x % y después −x %: siempre 100")
eje.plot(100 * movimiento, nivel_simple, color=ROJO, linewidth=2.0,
         label="retornos simples: (1 + x) · (1 − x) = 1 − x²")
eje.axhline(100, color=TEXTO, linewidth=0.9, linestyle="--")
titulo(eje, "Los logaritmos son simétricos; los porcentajes, no",
       "Nivel final tras una subida del x % y una bajada del mismo x %, partiendo de 100")
eje.set_xlabel("tamaño del movimiento, arriba y luego abajo (%)")
eje.set_ylabel("nivel final")
eje.set_xlim(1, 50)
eje.set_ylim(72, 104)
rejilla(eje)
eje.legend(loc="lower left", fontsize=7.5)
for valor, color in [(0.05, NARANJA), (0.20, VERDE), (0.50, ROJO)]:
    eje.plot(100 * valor, 100 * (1 - valor ** 2), marker="o", color=color, markersize=5)
anotar(eje, "con un 20 % arriba y abajo se pierde un 4 %:\n"
            "y con un 50 %, un 25 % del capital",
       (50, 100 * (1 - 0.25)), (0.97, 0.70), color=ROJO, align="right")

numeros(ejes[0])
numeros(ejes[1])

guardar(fig, "retornos-log-aditivos-y-error")
