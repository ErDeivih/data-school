"""prediccion-con-incertidumbre-1.py — el error crece con el nivel y qué intervalo lo refleja.
La figura de la página de predicción con incertidumbre (fase 5)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# 60 días de calibración: el error crece en proporción al nivel de la predicción
pred = np.linspace(60.0, 260.0, 60)
real = pred + azar.normal(0.0, 0.11, 60) * pred
resid = np.abs(real - pred)

q_abs = np.quantile(resid, 0.80, method="higher")            # anchura fija
q_rel = np.quantile(resid / pred, 0.80, method="higher")     # anchura proporcional

fig, ejes = plt.subplots(1, 2, figsize=(7.4, 3.8))

# --- Panel izquierdo: dos formas de medir el mismo error ----------------------
ax = ejes[0]
ax.scatter(pred, real, s=14, color=AZUL, alpha=0.75, zorder=3)
eje = np.array([40.0, 280.0])
ax.fill_between(eje, eje - q_abs, eje + q_abs, color=REJILLA, alpha=0.55, zorder=1)
ax.fill_between(eje, eje * (1 - q_rel), eje * (1 + q_rel), color=VERDE, alpha=0.22, zorder=1)
ax.set_xlabel("predicción del modelo")
ax.set_ylabel("valor real")
anotar(ax, f"anchura fija +-{q_abs:.0f}", (110.0, 110.0 - q_abs), (0.02, 0.30), color=TEXTO)
anotar(ax, f"anchura proporcional, +-{100 * q_rel:.0f} %", (250.0, 250.0 * (1 + q_rel)), (0.04, 0.92), color=VERDE)
titulo(ax, "El error crece con el nivel", "los residuos se abren en abanico")
rejilla(ax)
numeros(ax)

# --- Panel derecho: el mismo modelo, dos intervalos distintos -----------------
ax = ejes[1]
niveles = np.array([80.0, 160.0, 240.0])
ancho = 26.0
ax.errorbar(niveles - ancho / 2, niveles, yerr=q_abs, fmt="o", color=REJILLA,
            capsize=5, markersize=5, label="anchura fija")
ax.errorbar(niveles + ancho / 2, niveles, yerr=q_rel * niveles, fmt="o", color=VERDE,
            capsize=5, markersize=5, label="anchura proporcional")
ax.set_xlabel("tamaño de la predicción")
ax.set_ylabel("predicción e intervalo")
anotar(ax, "aquí la fija se queda corta", (240.0 - ancho / 2, 240.0 + q_abs), (0.34, 0.09), color=ROJO)
ax.legend(loc="upper left")
titulo(ax, "Ninguna anchura única vale para todo", "la proporcional se adapta al tamaño")
rejilla(ax)
numeros(ax, ejes="y")
ax.set_xticks(niveles, ["pequeño", "mediano", "grande"])   # numeros() no toca este eje

guardar(fig, "prediccion-incertidumbre-intervalo-fijo-o-proporcional")
