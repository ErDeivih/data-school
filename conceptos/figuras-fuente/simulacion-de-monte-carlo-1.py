"""simulacion-de-monte-carlo-1.py — barajar y remuestrear responden a preguntas distintas: el
orden cambia el camino pero nunca el total, y el remuestreo sí cambia el total. Figura de la
página de Simulación de Monte Carlo (fase 9)."""

import numpy as np

from comun import *


def num(x, decimales=2):
    """Número con coma decimal, como se escribe en el portal."""
    return f"{x:.{decimales}f}".replace(".", ",")


def miles(n):
    """Entero con punto de millares, como se escribe en el portal."""
    return f"{n:,}".replace(",", ".")


def caida_maxima(curva):
    """Peor caída desde un máximo, en tanto por uno."""
    picos = np.maximum.accumulate(curva)
    return float(((picos - curva) / picos).max())


estilo()
azar = np.random.default_rng(7)

# Las diez operaciones de la página, en múltiplos de R, y un 2 % de riesgo por operación.
rs = np.array([2.0, 1.0, -1.0, 3.0, -1.0, 1.0, -1.0, 2.0, -1.0, 1.0])
riesgo = 0.02
replicas = 20_000
original = np.concatenate([[1.0], np.cumprod(1 + riesgo * rs)])
eje_x = np.arange(rs.size + 1)

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.6))

# --- Izquierda: barajar solo mueve el orden. Se dibujan 400 de las 20.000 réplicas para que se
# vea el abanico sin tapar la curva original.
for _ in range(400):
    barajado = np.concatenate([[1.0], np.cumprod(1 + riesgo * azar.permutation(rs))])
    ejes[0].plot(eje_x, barajado, color=REJILLA, linewidth=0.6, alpha=0.5, zorder=2)
ejes[0].plot(eje_x, original, color=AZUL, linewidth=2.4, zorder=4,
             label="el orden que te tocó")
ejes[0].axhline(1.0, color=TEXTO, linewidth=0.9, linestyle="--", zorder=3)
ejes[0].plot([rs.size], [float(original[-1])], marker="o", markersize=8, color=ROJO, zorder=5)
caidas = np.array([caida_maxima(np.concatenate(
    [[1.0], np.cumprod(1 + riesgo * azar.permutation(rs))])) for _ in range(replicas)])

anotar(ejes[0], f"las {miles(replicas)} réplicas acaban\n"
                f"todas en el mismo {num(100 * (original[-1] - 1))} %",
       xy=(rs.size, float(original[-1])), xytext=(0.97, 0.93), color=ROJO, align="right")
anotar(ejes[0], f"este orden cayó un {num(100 * caida_maxima(original))} %;\n"
                f"la mediana de los {miles(replicas)} es {num(100 * np.median(caidas))} %",
       xy=(3, 1.0), xytext=(0.02, 0.94), color=VERDE, flecha=False)
titulo(ejes[0], "Barajar cambia el camino, no el final",
       f"las mismas diez operaciones en {miles(replicas)} órdenes distintos")
ejes[0].set_xlabel("operaciones")
ejes[0].set_ylabel("capital (1 = capital inicial)")
ejes[0].set_xlim(0, rs.size + 0.6)
ejes[0].set_ylim(0.89, 1.28)
ejes[0].legend(loc="lower right", fontsize=8)
rejilla(ejes[0])
numeros(ejes[0], ejes="both")

# --- Derecha: remuestrear con reemplazo. Ahora el conjunto sí cambia (la peor operación puede
# salir cinco veces), así que se mueve el resultado final y no solo el camino.
muestras = azar.choice(rs, size=(replicas, rs.size), replace=True)
final = np.cumprod(1 + riesgo * muestras, axis=1)[:, -1] - 1
cuentas, bordes = np.histogram(100 * final, bins=70, range=(-20, 50))
centros = 0.5 * (bordes[:-1] + bordes[1:])
ancho = bordes[1] - bordes[0]
ejes[1].bar(centros, cuentas, width=ancho, color=[ROJO if c < 0 else AZUL for c in centros],
            alpha=0.82, zorder=2)
mediana, p5 = 100 * float(np.median(final)), 100 * float(np.percentile(final, 5))
ejes[1].axvline(mediana, color=AZUL, linewidth=1.3, linestyle=":")
ejes[1].axvline(p5, color=ROJO, linewidth=1.3, linestyle=":")
altura = float(cuentas.max())
ejes[1].set_ylim(0, altura * 1.34)
anotar(ejes[1], f"la mediana sale {num(mediana)} %: el remuestreo\nreproduce el centro del backtest",
       xy=(mediana, altura * 1.02), xytext=(0.98, 0.88), color=AZUL, align="right")
anotar(ejes[1], f"aquí empieza el 5 % peor:\npor debajo de {num(p5).replace('-', '−')} %",
       xy=(p5, altura * 0.55), xytext=(0.03, 0.86), color=ROJO)
titulo(ejes[1], "Remuestrear sí mueve el resultado",
       f"capital final de {miles(replicas)} réplicas sacadas al azar del histórico, con reemplazo")
ejes[1].set_xlabel("resultado final de la réplica (%)")
ejes[1].set_ylabel("número de réplicas")
ejes[1].set_xlim(-20, 50)
rejilla(ejes[1])
numeros(ejes[1], ejes="both")

guardar(fig, "monte-carlo-barajar-y-remuestrear")
