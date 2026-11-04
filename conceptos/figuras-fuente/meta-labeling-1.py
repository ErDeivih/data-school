"""meta-labeling-1.py — el portero del meta-etiquetado: subir el umbral sube la precisión
y baja la cobertura, pero el dinero total tiene un máximo. Figura de la pagina de
meta-etiquetado (fase 9)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# 600 senales de un primario con habilidad moderada. El secundario da su probabilidad p y la
# probabilidad real de acierto crece con p, pero nunca llega a 1: el secundario no es adivino.
n = 600
p = azar.uniform(0.10, 0.95, n)
acierto = azar.random(n) < (0.20 + 0.65 * p)

# Recorremos el umbral de decision y medimos las tres cosas que importan en cada punto.
umbrales = np.linspace(0.10, 0.90, 81)
cobertura, precision, r_total = [], [], []
for u in umbrales:
    toma = p >= u
    cobertura.append(toma.mean())
    precision.append(acierto[toma].mean() if toma.any() else np.nan)
    r_total.append(np.where(acierto[toma], 1.6, -1.0).sum() if toma.any() else np.nan)
cobertura, precision, r_total = np.array(cobertura), np.array(precision), np.array(r_total)

i_mejor = int(np.nanargmax(r_total))
u_mejor = float(umbrales[i_mejor])
u_alta = 0.80
i_alta = int(np.argmin(np.abs(umbrales - u_alta)))
r_alta = float(r_total[i_alta])

fig, ejes = plt.subplots(2, 1, figsize=(7.0, 6.2), sharex=True)

# --- Arriba: precision y cobertura, que se mueven en direcciones opuestas -------------
ejes[0].plot(umbrales, precision, color=VERDE, linewidth=1.8)
ejes[0].plot(umbrales, cobertura, color=AZUL, linewidth=1.8)
ejes[0].axhline(acierto.mean(), color=ROJO, linewidth=1.2, linestyle="--")
ejes[0].axvline(u_mejor, color=MORADO, linewidth=1.3, linestyle=":")
ejes[0].set_ylim(0, 1.12)
titulo(ejes[0], "Subir el umbral sube la precisión y baja la cobertura",
       "las dos métricas que hay que mirar juntas, nunca una sola")
anotar(ejes[0], "sin filtro: la precisión\ncruda del primario", xy=(0.30, acierto.mean()),
       xytext=(0.17, 0.28), color=ROJO)
anotar(ejes[0], "precisión de lo que aceptas",
       xy=(0.55, precision[np.argmin(np.abs(umbrales - 0.55))]),
       xytext=(0.30, 0.72), color=VERDE)
anotar(ejes[0], "cobertura: cuántas señales\ndel primario te quedas",
       xy=(0.70, cobertura[np.argmin(np.abs(umbrales - 0.70))]),
       xytext=(0.98, 0.20), color=AZUL, align="right")
ejes[0].set_ylabel("fracción")
rejilla(ejes[0])
numeros(ejes[0], "y")

# --- Abajo: el dinero total es una colina, no una recta -------------------------------
ejes[1].plot(umbrales, r_total, color=MORADO, linewidth=1.9)
ejes[1].axhline(0, color=TEXTO, linewidth=0.8, alpha=0.4)
ejes[1].axhline(r_total.max(), color=MORADO, linewidth=1.0, linestyle="--", alpha=0.6)
ejes[1].plot([u_mejor], [r_total[i_mejor]], marker="o", markersize=6, color=MORADO)
ejes[1].axvline(u_mejor, color=MORADO, linewidth=1.3, linestyle=":")
ejes[1].plot([u_alta, u_alta], [0, r_alta], color=ROJO, linewidth=1.3, linestyle=":")
ejes[1].plot([u_alta], [r_alta], marker="o", markersize=6, color=ROJO)
ejes[1].set_xlabel("umbral del secundario  (solo se opera si p ≥ u)")
ejes[1].set_ylabel("R sumados")
titulo(ejes[1], "El dinero total tiene un máximo, y no está en la precisión máxima",
       "filtrar de más deja la cartera sin operaciones")
anotar(ejes[1], f"máximo: {r_total[i_mejor]:.0f}R con u = {u_mejor:.2f}".replace(".", ","),
       xy=(u_mejor, r_total[i_mejor]), xytext=(0.28, 0.58), color=MORADO)
anotar(ejes[1], f"con u = {u_alta:.2f} la precisión es alta\ny el total se ha dejado {r_total[i_mejor] - r_alta:.0f}R en el camino".replace(".", ","),
       xy=(u_alta, r_alta), xytext=(0.98, 0.86), color=ROJO, align="right")
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "meta-etiquetado-precision-y-cobertura")
