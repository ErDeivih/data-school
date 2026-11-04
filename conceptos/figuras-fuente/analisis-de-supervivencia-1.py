"""analisis-de-supervivencia-1.py — la curva de Kaplan-Meier con censura y por qué una
separación visible entre dos grupos puede no ser concluyente. Página de análisis de
supervivencia (fase 5)."""

import numpy as np

from comun import *

estilo()

# 24 sujetos: 0 = control, 1 = tratamiento (12 en cada grupo), con censura por la derecha
tiempo = np.array([3, 5, 6, 8, 9, 11, 13, 15, 18, 21, 25, 30,
                   7, 10, 12, 16, 19, 22, 24, 27, 29, 33, 36, 40], dtype=float)
evento = np.array([1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0,
                   1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0])
grupo = np.array([0] * 12 + [1] * 12)


def kaplan_meier(g):
    """Escalones de la curva y los tiempos en que alguien se censura, para un grupo."""
    tg, eg = tiempo[grupo == g], evento[grupo == g]
    tiempos, supervivencia, S = [0.0], [1.0], 1.0
    for ti in np.unique(tg[eg == 1]):
        en_riesgo = int((tg >= ti).sum())          # siguen en observación en ti
        casos = int(((tg == ti) & (eg == 1)).sum())
        S *= 1 - casos / en_riesgo
        tiempos.append(float(ti))
        supervivencia.append(S)
    return np.array(tiempos), np.array(supervivencia), tg[(eg == 0)]


t0, S0, cens0 = kaplan_meier(0)
t1, S1, cens1 = kaplan_meier(1)
S_antes = lambda tiempos, supervivencia, x: supervivencia[np.searchsorted(tiempos, x, "right") - 1]

# Log-rank: observados frente a esperados en el grupo 1, tiempo a tiempo
obs = esp = var = 0.0
for ti in np.unique(tiempo[evento == 1]):
    riesgo = tiempo >= ti
    n, n1 = float(riesgo.sum()), float((riesgo & (grupo == 1)).sum())
    d = float(((tiempo == ti) & (evento == 1)).sum())
    d1 = float(((tiempo == ti) & (evento == 1) & (grupo == 1)).sum())
    obs += d1
    esp += d * n1 / n
    var += d * (n1 / n) * (1 - n1 / n) * (n - d) / (n - 1)
chi2 = (obs - esp) ** 2 / var

fig, ejes = plt.subplots(1, 2, figsize=(7.0, 4.4))

# --- Panel izquierdo: la curva y la censura ----------------------------------
izq = ejes[0]
izq.step(t0, S0, where="post", color=AZUL, linewidth=1.9, label="control")
izq.step(t1, S1, where="post", color=VERDE, linewidth=1.9, label="tratamiento")
izq.plot(cens0, S_antes(t0, S0, cens0), "|", color=AZUL, markersize=9, linestyle="none")
izq.plot(cens1, S_antes(t1, S1, cens1), "|", color=VERDE, markersize=9, linestyle="none")
izq.axhline(0.5, color=TEXTO, linewidth=0.9, linestyle="--")
izq.annotate("la censura no baja la curva:\nsolo saca sujetos del denominador",
             xy=(24, S_antes(t1, S1, np.array([24.0]))[0]), xytext=(0.30, 0.80),
             textcoords="axes fraction", fontsize=8.5, color=REJILLA,
             arrowprops=dict(arrowstyle="->", color=REJILLA, linewidth=0.9, shrinkA=2, shrinkB=3))
izq.annotate("mediana del control, 11 meses;\ndel tratamiento, 24: el primer t\ncon S(t) ≤ 0,5",
             xy=(24, 0.476), xytext=(0.03, 0.14), textcoords="axes fraction",
             fontsize=8.5, color=ROJO,
             arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9, shrinkA=2, shrinkB=3))
izq.set_xlabel("meses de seguimiento")
izq.set_ylabel("S(t): probabilidad de seguir sin el evento")
izq.set_ylim(0, 1.05)
izq.set_title("La censura no baja la curva")
izq.legend(loc="upper right")
rejilla(izq)
numeros(izq)

# --- Panel derecho: la separación visible frente a la evidencia --------------
der = ejes[1]
der.step(t0, S0, where="post", color=AZUL, linewidth=1.9)
der.step(t1, S1, where="post", color=VERDE, linewidth=1.9)
der.plot(cens0, S_antes(t0, S0, cens0), "|", color=AZUL, markersize=7, linestyle="none")
der.plot(cens1, S_antes(t1, S1, cens1), "|", color=VERDE, markersize=7, linestyle="none")
der.axhline(0.5, color=TEXTO, linewidth=1.0, linestyle="--")
der.annotate("p = 0,174: con 24 sujetos no se puede\nrechazar que el efecto sea nulo",
             xy=(33, 0.32), xytext=(0.04, 0.72), textcoords="axes fraction",
             fontsize=8.5, color=ROJO,
             arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9, shrinkA=2, shrinkB=3))
der.text(0.04, 0.06, "log-rank: esperados %.1f  ·  observados %.1f  ·  chi² = %.2f"
         % (esp, obs, chi2), transform=der.transAxes, fontsize=8.5, color=TEXTO)
der.set_xlabel("meses de seguimiento")
der.set_ylabel("S(t)")
der.set_ylim(0, 1.05)
der.set_title("Curvas separadas, evidencia corta")
rejilla(der)
numeros(der)

guardar(fig, "supervivencia-kaplan-meier-y-censura")
