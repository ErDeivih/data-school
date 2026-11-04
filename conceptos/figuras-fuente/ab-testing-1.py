"""ab-testing-1.py - las dos decisiones que se toman antes de lanzar un A/B y por qué.

Izquierda: cuanta gente hace falta por rama para detectar cada efecto mínimo, con la base del
12 % del ejemplo del portal. Es la curva cuadrática de la formula: partir el efecto por dos
multiplica la muestra por cuatro.
Derecha: lo que se lleva gastado de error de tipo I si en vez de fijar la duración miras el
resultado cada dia y cortas cuando el p baja de 0,05. Contado sobre 20000 experimentos simulados
donde NO hay ningun efecto.
"""

import numpy as np
from scipy import stats

from comun import *

estilo()
azar = np.random.default_rng(7)

p0, alfa, potencia = 0.12, 0.05, 0.80
z_a = stats.norm.ppf(1 - alfa / 2)
z_b = stats.norm.ppf(potencia)


def n_por_rama(mde):
    """Formula del portal para una métrica binaria, vectorizada."""
    return 2 * (z_a + z_b) ** 2 * p0 * (1 - p0) / np.asarray(mde, float) ** 2


fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.4))

# ═══ Izquierda: el efecto que quieres ver decide la muestra ═══
ax = ejes[0]
mde = np.linspace(0.003, 0.05, 400)
ax.plot(mde * 100, n_por_rama(mde), color=AZUL, linewidth=2.0)
ax.set_yscale("log")
elegido = 0.01
n_elegido = float(n_por_rama(elegido))
ax.scatter([elegido * 100], [n_elegido], s=60, color=ROJO, zorder=4)
ax.annotate("el MDE que fijas tú: 1 punto\nporcentual → 16.577 por rama\n(16,6 días a 2.000 visitas)",
            xy=(elegido * 100, n_elegido), xytext=(0.32, 0.70), textcoords="axes fraction",
            fontsize=8.5, color=ROJO,
            arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9))
ax.annotate("doblar el efecto lo ahorra todo;\npartirlo por la mitad, multiplicar\nla muestra por cuatro",
            xy=(1.94, float(n_por_rama(0.019))), xytext=(0.02, 0.03), textcoords="axes fraction",
            va="bottom", fontsize=8.5, color=NARANJA,
            arrowprops=dict(arrowstyle="->", color=NARANJA, linewidth=0.9))
ax.set_xlabel("efecto mínimo detectable (puntos porcentuales)")
ax.set_ylabel("unidades necesarias por rama (escala logarítmica)")
titulo(ax, "Cuanto más pequeño el efecto, más caro el experimento",
       "conversión base del 12 %, α = 0,05 y potencia del 80 %")
rejilla(ax)

# ═══ Derecha: mirar todos los dias y cortar cuando sale bonito ═══
ax = ejes[1]
reps, por_dia, dias = 20000, 2500, 14
control = azar.binomial(por_dia, p0, (reps, dias)).cumsum(axis=1)
variante = azar.binomial(por_dia, p0, (reps, dias)).cumsum(axis=1)
n = np.arange(1, dias + 1) * por_dia
p_control, p_var = control / n, variante / n
diferencia = p_var - p_control
error_tipico = np.sqrt(p_control * (1 - p_control) / n + p_var * (1 - p_var) / n)
z = np.abs(diferencia) / error_tipico
cruza = z > z_a
# Cuantos de los 20000 ya habrian cortado como muy tarde en el dia d.
acumulado = np.array([cruza[:, :d + 1].any(axis=1).mean() for d in range(dias)])

ax.plot(n, acumulado, color=ROJO, linewidth=2.0, marker="o", markersize=4)
ax.axhline(alfa, color=TEXTO, linewidth=1.4, linestyle="--")
ax.text(por_dia * 0.6, alfa + 0.006, "el 5 % que prometiste", color=TEXTO, fontsize=8.5)
ax.annotate(f"mirando cada día y cortando cuando\nsale, el error llega al {acumulado[-1] * 100:.0f} %:\n"
            "más del cuádruple de lo prometido",
            xy=(n[-1] * 0.96, acumulado[-1] * 0.97), xytext=(0.09, 0.80), textcoords="axes fraction",
            fontsize=9, color=ROJO,
            arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=1.0))
ax.set_ylim(0, acumulado[-1] * 1.25)
ax.set_xlabel("acumulado del experimento (unidades por rama)")
ax.set_ylabel("error de tipo I ya gastado")
titulo(ax, "Mirar cada día infla el falso positivo que prometiste",
       "20000 experimentos simulados sin ningún efecto, con la misma conversión en las dos ramas")
rejilla(ax)
numeros(ax, ejes="x")

guardar(fig, "ab-testing-muestra-y-mirar-cada-dia")
