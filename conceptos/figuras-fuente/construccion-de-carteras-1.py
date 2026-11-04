"""construccion-de-carteras-1.py — la única comida gratis: combinar dos estrategias con
correlación baja mejora la relación entre rentabilidad y riesgo, pero el peso en capital no es
el peso en riesgo y diez estrategias no son diez apuestas. Figura de la página de Construcción
de carteras (fase 9)."""

import numpy as np

from comun import *


def num(x, decimales=2):
    """Número con coma decimal, como se escribe en el portal."""
    return f"{x:.{decimales}f}".replace(".", ",")


estilo()
azar = np.random.default_rng(7)

mu_anual, sigma_anual = 0.10, 0.20
sigma_mensual, mu_mensual = sigma_anual / np.sqrt(12), mu_anual / 12
meses = 180

# Dos estrategias con la MISMA volatilidad (20 % anual) y correlación 0,2 exacta, construidas
# sobre tres series ortogonales: así la figura mide el efecto de la correlación y nada más.
crudo = azar.normal(size=(3, meses))
base = []
for fila in crudo:
    v = fila - fila.mean()
    for u in base:
        v = v - (v @ u) / (u @ u) * u
    base.append(v / np.linalg.norm(v) * np.sqrt(meses - 1))
comun, e1, e2 = base
r1 = mu_mensual + sigma_mensual * (comun + 2 * e1) / np.sqrt(5)
r2 = mu_mensual + sigma_mensual * (comun + 2 * e2) / np.sqrt(5)
cartera = 0.5 * r1 + 0.5 * r2
vol_cartera = 100 * float(cartera.std(ddof=1) * np.sqrt(12))
print(f"volatilidad de cada estrategia {100 * r1.std(ddof=1) * np.sqrt(12):.2f} %")
print(f"correlación muestral {np.corrcoef(r1, r2)[0, 1]:.4f}")
print(f"volatilidad de la cartera al 50 % {vol_cartera:.2f} %")

fig, ejes = plt.subplots(2, 2, figsize=(10.8, 7.4))

# ── Arriba a la izquierda: lo que baja la volatilidad según la correlación ────
eje = ejes[0, 0]
rhos = np.linspace(0, 1, 200)
eje.plot(rhos, 100 * sigma_anual * np.sqrt((1 + rhos) / 2), color=AZUL, linewidth=2.2)
eje.axhline(100 * sigma_anual, color=REJILLA, linewidth=1.4, linestyle="--")
eje.plot([0.2], [vol_cartera], marker="o", markersize=7, color=ROJO, zorder=4)
anotar(eje, f"con correlación 0,2 la cartera baja al {num(vol_cartera)} %",
       xy=(0.2, vol_cartera), xytext=(0.97, 0.12), color=ROJO, align="right")
anotar(eje, "la raya gris es una estrategia sola: el hueco hasta la curva\nes rentabilidad que no has tenido que ganar",
       xy=(0.62, float(100 * sigma_anual * np.sqrt((1 + 0.62) / 2))), xytext=(0.03, 0.92),
       color=TEXTO, align="left", flecha=False)
titulo(eje, "La diversificación se mide por ρ",
       "dos estrategias iguales combinadas al 50 %, cada una con un 20 % de volatilidad")
eje.set_xlabel("correlación entre las dos estrategias")
eje.set_ylabel("volatilidad de la cartera (%)")
eje.set_xlim(0, 1)
eje.set_ylim(13, 21)
rejilla(eje)
numeros(eje)

# ── Arriba a la derecha: el mismo resultado visto en el capital ───────────────
eje = ejes[0, 1]
eje.plot(100 * np.cumprod(1 + r1), color=AZUL, linewidth=1.7, label="estrategia 1")
eje.plot(100 * np.cumprod(1 + r2), color=NARANJA, linewidth=1.7, label="estrategia 2")
eje.plot(100 * np.cumprod(1 + cartera), color=MORADO, linewidth=2.4,
         label="la cartera, mitad y mitad")
anotar(eje, f"misma media muestral, un {num(100 * mu_anual, 0)} % anual:\nlo que cambia es el camino",
       xy=(meses - 1, float(100 * np.cumprod(1 + cartera)[-1])), xytext=(0.97, 0.05),
       color=MORADO, align="right", flecha=False)
titulo(eje, "Misma media, menos sobresaltos",
       "capital de las dos estrategias y de la cartera, con correlación 0,2")
eje.set_xlabel("meses")
eje.set_ylabel("capital (base 100)")
eje.set_ylim(60, 440)
eje.legend(loc="upper left", fontsize=8)
rejilla(eje)
numeros(eje, ejes="y")

# ── Abajo a la izquierda: peso en capital frente a aporte al riesgo ───────────
eje = ejes[1, 0]
pesos = np.array([0.5, 0.5])
sigmas = np.array([sigma_anual, 0.10])
cov = np.outer(sigmas, sigmas) * np.array([[1.0, 0.2], [0.2, 1.0]])
sigma_p = float(np.sqrt(pesos @ cov @ pesos))
aporte = 100 * pesos * (cov @ pesos) / sigma_p ** 2
posiciones = np.arange(2)
eje.bar(posiciones - 0.19, 100 * pesos, width=0.36, color=CIAN, alpha=0.85,
        label="peso en capital", zorder=2)
eje.bar(posiciones + 0.19, aporte, width=0.36, color=MORADO, alpha=0.85,
        label="aporte al riesgo", zorder=2)
for xi, valor in zip(posiciones - 0.19, 100 * pesos):
    eje.text(xi, valor + 2.5, f"{num(valor, 0)} %", ha="center", fontsize=9, color=CIAN)
for xi, valor in zip(posiciones + 0.19, aporte):
    eje.text(xi, valor + 2.5, f"{num(valor, 1)} %", ha="center", fontsize=9, color=MORADO)
eje.set_xticks(posiciones)
eje.set_xticklabels(["estrategia del 20 %", "estrategia del 10 %"])
eje.set_xlim(-0.65, 1.65)
eje.set_ylim(0, 100)
anotar(eje, "mitad del dinero, tres cuartas partes del riesgo",
       xy=(0.19, float(aporte[0])), xytext=(0.97, 0.92), color=MORADO, align="right")
titulo(eje, "Peso en capital no es peso en riesgo",
       "las dos con la mitad del dinero y una correlación de 0,2")
eje.set_ylabel("% del total")
eje.legend(loc="upper left", fontsize=8)
rejilla(eje)
numeros(eje, ejes="y")

# ── Abajo a la derecha: cuántas apuestas independientes hay de verdad ─────────
eje = ejes[1, 1]
n_estrategias = np.arange(1, 21)
eje.plot(n_estrategias, n_estrategias, color=REJILLA, linewidth=1.4, linestyle="--")
for rho, color in zip((0.2, 0.5), [NARANJA, ROJO]):
    autovalores = (((1 + (n_estrategias - 1) * rho) ** 2
                    + (n_estrategias - 1) * (1 - rho) ** 2))
    eje.plot(n_estrategias, n_estrategias ** 2 / autovalores, color=color, linewidth=2.0,
             label=f"correlación media {num(rho, 1)}")
apuestas = 100 / (((1 + 9 * 0.2) ** 2 + 9 * 0.8 ** 2))
eje.plot([10], [apuestas], marker="o", markersize=7, color=NARANJA, zorder=4)
anotar(eje, f"diez estrategias con correlación 0,2\nson {num(apuestas)} apuestas",
       xy=(10, apuestas), xytext=(0.97, 0.93), color=NARANJA, align="right")
titulo(eje, "Diez estrategias no son diez apuestas",
       "número efectivo de apuestas según los autovalores de la correlación")
eje.set_xlabel("número de estrategias")
eje.set_ylabel("apuestas efectivas")
eje.set_xlim(1, 20)
eje.set_ylim(0, 24)
eje.legend(loc="upper left", fontsize=8)
rejilla(eje)
numeros(eje)

guardar(fig, "carteras-diversificacion-riesgo-y-apuestas")
