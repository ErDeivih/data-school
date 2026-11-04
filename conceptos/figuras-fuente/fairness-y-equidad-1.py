"""fairness-y-equidad-1.py — con un modelo igual de bueno en los dos grupos, la diferencia de
prevalencia impide cumplir a la vez paridad demográfica e igualdad de oportunidades. Figura de
la página de equidad y métricas de fairness (fase 6)."""

from math import sqrt

import numpy as np
from scipy.special import erf

from comun import *

estilo()


def phi(z):
    """Función de distribución de la normal estándar, vectorizada."""
    return 0.5 * (1.0 + erf(np.asarray(z, dtype=float) / sqrt(2.0)))


# El modelo puntúa igual de bien a los dos grupos: mismas curvas de exhaustividad y de falsas
# alarmas. Lo único que cambia entre ellos es la prevalencia real (30 % frente a 12 %).
mu_pos, mu_neg, sd = 0.75, 0.35, 0.15
prev_a, prev_b = 0.30, 0.12

tau = np.linspace(0.0, 1.0, 601)
tpr = 1.0 - phi((tau - mu_pos) / sd)
fpr = 1.0 - phi((tau - mu_neg) / sd)
sel_a = prev_a * tpr + (1.0 - prev_a) * fpr
sel_b = prev_b * tpr + (1.0 - prev_b) * fpr
prev_total = 0.5 * (prev_a + prev_b)
sel_total = prev_total * tpr + (1.0 - prev_total) * fpr

# Objetivo de paridad demográfica: la tasa de selección que da el corte único de 0,50.
objetivo = float(np.interp(0.50, tau, sel_total))


def umbral_para(sel):
    """La tasa de selección decrece con tau, así que se invierte el eje para interpolar."""
    return float(np.interp(objetivo, sel[::-1], tau[::-1]))


tau_a, tau_b = umbral_para(sel_a), umbral_para(sel_b)
tpr_a = 1.0 - phi((tau_a - mu_pos) / sd)
tpr_b = 1.0 - phi((tau_b - mu_pos) / sd)
fpr_a = 1.0 - phi((tau_a - mu_neg) / sd)
fpr_b = 1.0 - phi((tau_b - mu_neg) / sd)

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.2))

# --- Panel izquierdo: dos curvas que no se cruzan en ningún umbral útil.
ejes[0].plot(tau, sel_a, color=AZUL, linewidth=1.9, label=f"grupo A (prevalencia {prev_a:.0%})")
ejes[0].plot(tau, sel_b, color=NARANJA, linewidth=1.9, label=f"grupo B (prevalencia {prev_b:.0%})")
ejes[0].axhline(objetivo, color=TEXTO, linewidth=1.1, linestyle="--")
ejes[0].axvline(tau_a, color=AZUL, linewidth=1.1, linestyle=":")
ejes[0].axvline(tau_b, color=NARANJA, linewidth=1.1, linestyle=":")
anotar(ejes[0], f"para seleccionar al mismo {objetivo:.0%}\ncada grupo necesita su umbral",
       xy=(tau_b, objetivo), xytext=(0.36, 0.80), color=TEXTO)
anotar(ejes[0], "con un único corte de 0,50\nel grupo A entra mucho más",
       xy=(0.50, float(np.interp(0.50, tau, sel_a))), xytext=(0.03, 0.14), color=AZUL)
ejes[0].set_xlabel("umbral de decisión")
ejes[0].set_ylabel("tasa de selección\n(proporción de positivos predichos)")
ejes[0].set_xlim(0.0, 1.0)
ejes[0].set_ylim(0.0, 1.02)
ejes[0].legend(loc="upper right")
rejilla(ejes[0])
numeros(ejes[0])
titulo(ejes[0], "La paridad demográfica pide dos umbrales",
       "las dos curvas no se tocan en ningún corte útil")

# --- Panel derecho: lo que cuesta cumplirla. El modelo es el mismo; la disparidad, no.
x = np.arange(4)
alto = [tpr_a, tpr_b, fpr_a, fpr_b]
colores = [AZUL, NARANJA, AZUL, NARANJA]
ejes[1].bar(x, alto, width=0.6, color=colores)
for xi, v in zip(x, alto):
    ejes[1].text(xi, v + 0.03, f"{v:.2f}".replace(".", ","), ha="center", fontsize=9, color=TEXTO)
anotar(ejes[1], f"la exhaustividad se separa:\n{tpr_b:.0%} frente a {tpr_a:.0%}",
       xy=(1.0, tpr_b), xytext=(0.05, 0.90), color=NARANJA)
ejes[1].set_xticks(x)
ejes[1].set_xticklabels(["exhaustividad\nA", "exhaustividad\nB", "falsas alarmas\nA",
                         "falsas alarmas\nB"])
ejes[1].set_ylim(0.0, 1.32)
ejes[1].set_ylabel("tasa dentro del grupo")
rejilla(ejes[1])
numeros(ejes[1], "y")
titulo(ejes[1], "Cumplirla rompe la igualdad de oportunidades",
       f"mismo modelo en los dos grupos: umbral {tau_a:.2f} para A y {tau_b:.2f} para B")

guardar(fig, "fairness-y-equidad-paridad-frente-a-oportunidad")
