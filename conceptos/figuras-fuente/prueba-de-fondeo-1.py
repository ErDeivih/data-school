"""prueba-de-fondeo-1.py — por qué subir el riesgo no aprueba una prueba de fondeo.

Izquierda: probabilidad de aprobar y de morir, según el riesgo por operación, con las reglas de la
página (objetivo del 6 %, límite diario del 3 %, drawdown móvil del 6 %, tres operaciones al día,
45 % de aciertos y ratio 2:1). Con riesgo diminuto casi todo el mundo aprueba, pero tarda mucho;
según sube el riesgo, el límite diario se lleva por delante a más de la mitad de los intentos.
Derecha: quince intentos reales simulados con un 1 % de riesgo, uno por línea, parados en el
momento en que se deciden. Se ve que la mayoría muere en el primer día, antes de acercarse al
objetivo, y que morir es cuestión de tres pérdidas seguidas.
La figura de la página de pruebas de fondeo (fase 9).
"""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

CAPITAL, OBJETIVO = 100000.0, 6000.0
LIMITE_DIA, PERDIDA_MAX = 3000.0, 6000.0
P, R, OPS_DIA = 0.45, 2.0, 3
APRUEBA, MUERE_DIA, MUERE_TOTAL, CENSURADO = 0, 1, 2, 3


def simular(riesgo, n_sim, max_ops=400):
    """Replica la prueba con tandas de OPS_DIA operaciones y drawdown móvil.

    Devuelve el código de resultado de cada intento y cuántas operaciones duró.
    """
    r = CAPITAL * riesgo
    pasos = np.where(azar.random((n_sim, max_ops)) < P, R * r, -r)
    equity = CAPITAL + np.cumsum(pasos, axis=1)
    # El máximo se actualiza DESPUÉS de comprobar el drawdown: el pico no incluye el valor de hoy.
    anteriores = np.concatenate([np.full((n_sim, 1), CAPITAL), equity[:, :-1]], axis=1)
    pico = np.maximum.accumulate(anteriores, axis=1)
    # Equity al empezar cada día: el del primer día es el capital; luego, el cierre del día anterior.
    cierres = np.concatenate([np.full((n_sim, 1), CAPITAL), equity[:, OPS_DIA - 1::OPS_DIA]],
                             axis=1)
    inicio_dia = cierres[:, np.arange(max_ops) // OPS_DIA]

    exito = equity - CAPITAL >= OBJETIVO
    fallo_dia = inicio_dia - equity >= LIMITE_DIA
    fallo_total = pico - equity >= PERDIDA_MAX
    primero = lambda m: np.where(m.any(axis=1), m.argmax(axis=1), max_ops)
    t_exito, t_dia, t_total = primero(exito), primero(fallo_dia), primero(fallo_total)

    aprueba = (t_exito <= t_dia) & (t_exito <= t_total) & (t_exito < max_ops)
    muere_dia = (~aprueba) & (t_dia <= t_total) & (t_dia < max_ops)
    muere_total = (~aprueba) & (~muere_dia) & (t_total < max_ops)
    resultado = np.where(aprueba, APRUEBA,
                         np.where(muere_dia, MUERE_DIA,
                                  np.where(muere_total, MUERE_TOTAL, CENSURADO)))
    return resultado, t_exito + 1, equity


fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.5))

# --- Izquierda: probabilidad de aprobar y de morir según el riesgo --------------------
ax = ejes[0]
riesgos = np.linspace(0.002, 0.035, 16)
N_SIM = 1500
frecuencias = np.array([np.bincount(simular(r, N_SIM, 400)[0], minlength=4) / N_SIM
                        for r in riesgos])

ax.plot(riesgos * 100, frecuencias[:, APRUEBA], color=AZUL, linewidth=2.2, marker="o",
        markersize=4.5, zorder=4)
ax.plot(riesgos * 100, frecuencias[:, MUERE_DIA], color=ROJO, linewidth=1.8, marker="s",
        markersize=4, zorder=3)
ax.plot(riesgos * 100, frecuencias[:, MUERE_TOTAL], color=NARANJA, linewidth=1.8, marker="^",
        markersize=4.5, zorder=3)
anotar(ax, "el límite diario se lleva por delante\na más de la mitad de los intentos",
       xy=(3.0, float(frecuencias[-3, MUERE_DIA])), xytext=(0.98, 0.93), color=ROJO,
       align="right")
anotar(ax, "morir por el drawdown total:\nsolo pasa con riesgo pequeño",
       xy=(float(riesgos[3]) * 100, float(frecuencias[3, MUERE_TOTAL])), xytext=(0.40, 0.20),
       color=NARANJA)
titulo(ax, "Más riesgo no aprueba la prueba: la entierra antes",
       "1.500 intentos por punto; con riesgo diminuto se tarda 60 operaciones")
ax.set_xlabel("riesgo por operación (% del capital)")
ax.set_ylabel("probabilidad")
ax.set_ylim(-0.03, 1.05)
ax.set_xlim(0.0, 3.7)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{v:.0%}"))
rejilla(ax)

# --- Derecha: quince intentos con un 1 % de riesgo, parados al decidirse ---------------
ax = ejes[1]
resultado, duracion, equity = simular(0.01, 15, 30)
colores = {APRUEBA: VERDE, MUERE_DIA: ROJO, MUERE_TOTAL: NARANJA, CENSURADO: REJILLA}
for i in range(15):
    corte = int(duracion[i])
    serie = np.concatenate([[CAPITAL], equity[i, :corte]])
    serie = np.concatenate([serie, np.full(31 - serie.size, np.nan)])
    ax.plot(np.arange(31), serie, color=colores[int(resultado[i])], linewidth=1.5, alpha=0.85,
            zorder=3)
for dia in range(1, 10):
    ax.axvline(dia * OPS_DIA, color=REJILLA, linewidth=0.7, linestyle=":", zorder=1)
ax.axhline(CAPITAL + OBJETIVO, color=VERDE, linewidth=1.3, linestyle="--", zorder=2)
ax.axhline(CAPITAL, color=TEXTO, linewidth=1.0, linestyle="--", zorder=2)
anotar(ax, "el objetivo: 6.000 € por encima", xy=(20, CAPITAL + OBJETIVO),
       xytext=(0.36, 0.93), color=VERDE, flecha=False)
anotar(ax, "tres pérdidas en el mismo día\nagotan el límite diario", xy=(6.0, 97000.0),
       xytext=(0.03, 0.12), color=ROJO)
titulo(ax, "Quince intentos con un 1 % de riesgo, parados al decidirse",
       "cada línea vertical separa un día de tres operaciones")
ax.set_xlabel("operación dentro de la prueba")
ax.set_ylabel("valor de la cuenta (miles)")
ax.set_xlim(-0.5, 30.5)
finales = [float(equity[i, min(int(duracion[i]), equity.shape[1]) - 1]) for i in range(15)]
ax.set_ylim(min(94000.0, min(finales)) - 1500, CAPITAL + OBJETIVO + 2600)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _p: f"{v / 1000:.0f}"))
rejilla(ax)

guardar(fig, "prueba-fondeo-riesgo-y-muerte")
