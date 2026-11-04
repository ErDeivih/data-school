"""maxima-verosimilitud-1.py — el máximo de la log-verosimilitud es el MLE, y más datos
afilan ese máximo (información de Fisher). Figura de la página maxima-verosimilitud."""

import numpy as np

from comun import *

estilo()

p = np.linspace(1e-6, 1 - 1e-6, 4000)

fig, ejes = plt.subplots(1, 2, figsize=(7.9, 3.9))

# --- Izquierda: el máximo es el MLE, y lo que vale la pena se mide en diferencias ---
eje = ejes[0]
n, caras = 50, 30
log_ver = caras * np.log(p) + (n - caras) * np.log(1 - p)
p_mle = caras / n
en_medio = (n / 2) * np.log(0.5)                       # ℓ(0,5) con 50 lanzamientos
veces = np.exp(log_ver.max() - en_medio)               # cociente de verosimilitudes

eje.plot(p, log_ver, color=AZUL, linewidth=1.8)
eje.plot([p_mle], [log_ver.max()], marker="o", color=ROJO, markersize=7, zorder=4)
eje.plot([0.5], [en_medio], marker="o", color=MORADO, markersize=6, zorder=4)
eje.axvline(p_mle, color=ROJO, linewidth=1.0, linestyle=":")
eje.axvline(0.5, color=MORADO, linewidth=1.0, linestyle=":")
eje.set_xlim(0.15, 0.95)
eje.set_ylim(-70, -28)
anotar(eje, "aquí el máximo: el MLE es 0,6", xy=(p_mle, log_ver.max()),
       xytext=(0.42, 0.88), color=ROJO)
anotar(eje, "en p = 0,5 la curva baja 1,01:\nlos datos son %.1f veces más probables" % veces,
       xy=(0.5, en_medio), xytext=(0.04, 0.18), color=MORADO)
titulo(eje, "El máximo de la log-verosimilitud es el MLE",
       "50 lanzamientos con 30 caras")
eje.set_xlabel("p, probabilidad de cara")
eje.set_ylabel("log-verosimilitud")
rejilla(eje)
numeros(eje)

# --- Derecha: más datos, máximo más afilado (y estimación menos variable) ----------
eje = ejes[1]
for lanzamientos, color in ((10, VERDE), (50, AZUL), (200, MORADO)):
    exitos = 0.6 * lanzamientos
    curva = exitos * np.log(p) + (lanzamientos - exitos) * np.log(1 - p)
    error_tipico = np.sqrt(0.6 * 0.4 / lanzamientos)
    eje.plot(p, curva - curva.max(), color=color, linewidth=1.7,
             label="n = %d: error típico %.3f" % (lanzamientos, error_tipico))
eje.axvline(0.6, color=ROJO, linewidth=1.0, linestyle=":")
eje.set_xlim(0.3, 0.9)
eje.set_ylim(-8, 0.8)
eje.text(0.03, 0.40, "la curvatura del máximo\nes la información de Fisher",
         transform=eje.transAxes, fontsize=8, va="top")
titulo(eje, "Más datos, máximo más afilado: menos varianza",
       "la misma proporción, 0,6, con tres tamaños")
eje.set_xlabel("p, probabilidad de cara")
eje.set_ylabel("log-verosimilitud menos su máximo")
eje.legend(loc="lower center", fontsize=8)
rejilla(eje)
numeros(eje)

guardar(fig, "verosimilitud-maximo-e-información")
