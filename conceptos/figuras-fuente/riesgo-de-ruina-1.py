"""riesgo-de-ruina-1.py — la probabilidad de quedarse a cero cae en picado al reducir el tamaño
de la apuesta, y con el mismo sistema. Figura de la página de Riesgo de ruina (fase 9)."""

import numpy as np

from comun import *


def num(x, decimales=2):
    """Número con coma decimal, como se escribe en el portal."""
    return f"{x:.{decimales}f}".replace(".", ",")


estilo()
azar = np.random.default_rng(7)

p, q = 0.55, 0.45
riesgo = np.linspace(0.01, 0.25, 400)
# Capital medido en unidades de riesgo: N = 1 / riesgo. La probabilidad de arruinarse alguna
# vez es (q/p)^N, y el exponente es lo que hace que la curva sea un acantilado y no una recta.
ruina_pct = 100 * (q / p) ** (1 / riesgo)
riesgos_marcados = np.array([0.01, 0.02, 0.05, 0.10, 0.20])
valores_marcados = 100 * (q / p) ** (1 / riesgos_marcados)

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.6))

ejes[0].semilogy(riesgo * 100, ruina_pct, color=AZUL, linewidth=2.2)
ejes[0].plot(riesgos_marcados * 100, valores_marcados, linestyle="none", marker="o",
             markersize=5, color=AZUL, zorder=4)
veces = f"{valores_marcados[3] / valores_marcados[1]:,.0f}".replace(",", ".")
anotar(ejes[0], f"con el 2 % la ruina es del {num(valores_marcados[1], 4)} %",
       xy=(2, valores_marcados[1]), xytext=(0.02, 0.94), color=VERDE)
anotar(ejes[0], f"con el 10 % sube al {num(valores_marcados[3])} %:\n"
                f"unas {veces} veces más, con la misma ventaja",
       xy=(10, valores_marcados[3]), xytext=(0.98, 0.30), color=ROJO, align="right")
titulo(ejes[0], "El tamaño decide el riesgo de ruina",
       f"misma ventaja del {p:.0%} y apuesta fija: P(ruina) = (q/p) elevado a 1/riesgo")
ejes[0].set_xlabel("riesgo por operación, en % del capital")
ejes[0].set_ylabel("probabilidad de ruina (%, escala logarítmica)")
ejes[0].set_xlim(1, 25)
ejes[0].set_ylim(1e-7, 1e2)
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="x")

# --- Derecha: la misma simulación de la página, con la misma semilla. 20.000 caminos de 200
# operaciones y apuesta de tamaño fijo: cada operación suma o resta el riesgo en unidades del
# capital inicial, que es el modelo del que sale la fórmula de la izquierda.
n_ops, n_caminos = 200, 20_000
resultados = azar.choice([1.0, -1.0], size=(n_caminos, n_ops), p=[p, q])

etiquetas, ruinas, mitades = [], [], []
for riesgo_i in (0.02, 0.10):
    capital = 1 + riesgo_i * np.cumsum(resultados, axis=1)
    etiquetas.append(f"riesgo del {riesgo_i:.0%}")
    ruinas.append(100 * (capital <= 0).any(axis=1).mean())
    mitades.append(100 * (capital <= 0.5).any(axis=1).mean())

posiciones = np.arange(2)
ejes[1].bar(posiciones - 0.19, ruinas, width=0.36, color=ROJO, alpha=0.85,
            label="se queda a cero", zorder=2)
ejes[1].bar(posiciones + 0.19, mitades, width=0.36, color=NARANJA, alpha=0.85,
            label="llega a perder la mitad", zorder=2)
for xi, valor in zip(posiciones - 0.19, ruinas):
    ejes[1].text(xi, valor + 0.9, f"{num(valor)} %", ha="center", fontsize=9, color=ROJO)
for xi, valor in zip(posiciones + 0.19, mitades):
    ejes[1].text(xi, valor + 0.9, f"{num(valor)} %", ha="center", fontsize=9, color=NARANJA)
ejes[1].set_xticks(posiciones)
ejes[1].set_xticklabels(etiquetas)
ejes[1].set_xlim(-0.65, 1.65)
ejes[1].set_ylim(0, 52)
anotar(ejes[1], f"con el 2 % no se arruina ningún camino\ny solo el {num(mitades[0])} % toca la mitad",
       xy=(-0.19, 0.0), xytext=(0.04, 0.66), color=VERDE, flecha=False)
anotar(ejes[1], f"con el 10 % se arruina el {num(ruinas[1])} %\ny el {num(mitades[1])} % pasa por la mitad",
       xy=(1.37, mitades[1]), xytext=(0.97, 0.90), color=ROJO, align="right")
titulo(ejes[1], "Lo que cuesta en 200 operaciones",
       "20.000 caminos simulados con el mismo porcentaje de aciertos")
ejes[1].set_ylabel("caminos que pasan por ahí (%)")
ejes[1].legend(loc="upper left", fontsize=8)
rejilla(ejes[1])
numeros(ejes[1], ejes="y")

guardar(fig, "riesgo-ruina-tamano-y-acantilado")
