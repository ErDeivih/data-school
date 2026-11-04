"""copias-de-seguridad-y-recuperacion-1.py — la línea del tiempo de un incidente, con el
RPO y el RTO marcados, y lo que baja la probabilidad de perderlo todo. La figura de la
página de copias de seguridad y recuperación (fase 11)."""

import numpy as np

from comun import *

estilo()

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 4.2))

# --- Izquierda: lo que se pierde y lo que se tarda en volver ------------------------
COPIA, FALLO, VUELTA = 0.0, 6.0, 14.5

izq.axvspan(COPIA, FALLO, color=ROJO, alpha=0.16, linewidth=0)
izq.axvspan(FALLO, VUELTA, color=AZUL, alpha=0.16, linewidth=0)
izq.plot([COPIA, VUELTA], [0.5, 0.5], color=TEXTO, linewidth=1.4, zorder=3)
for x in (COPIA, FALLO, VUELTA):
    izq.plot([x], [0.5], marker="o", color=TEXTO, markersize=6, zorder=4)

izq.text((COPIA + FALLO) / 2, 0.66, "RPO\n6 h de datos\nque no vuelven", ha="center",
         va="bottom", color=ROJO, fontsize=9)
izq.text((FALLO + VUELTA) / 2, 0.66, "RTO\n8,5 h hasta\nvolver a servir", ha="center",
         va="bottom", color=AZUL, fontsize=9)
izq.text(COPIA + 0.15, 0.40, "última copia\ncompleta", ha="left", va="top",
         color=TEXTO, fontsize=8.5)
izq.text(FALLO, 0.40, "el fallo", ha="center", va="top", color=TEXTO, fontsize=8.5)
izq.text(VUELTA - 0.15, 0.40, "servicio\nrestaurado", ha="right", va="top",
         color=TEXTO, fontsize=8.5)

izq.set_xlim(-0.6, 15.6)
izq.set_ylim(0, 1)
izq.set_yticks([])
izq.set_xlabel("horas desde la última copia completa")
titulo(izq, "Qué se pierde y cuánto se tarda", "el plan de recuperación son estos dos números")
rejilla(izq, eje="x")
numeros(izq, ejes="x")

# --- Derecha: la independencia es lo que de verdad protege ---------------------------
p = 0.01
n = np.arange(1, 5)
independientes = p ** n
misma_cuenta = np.full(len(n), p)

# Lineas y no barras: en escala logaritmica una barra sugiere un cero que no existe.
der.plot(n, independientes, marker="o", markersize=5, color=VERDE, linewidth=1.8,
         label="copias independientes")
der.plot(n, misma_cuenta, marker="s", markersize=5, color=ROJO, linewidth=1.8,
         label="las tres en la misma cuenta")

der.set_yscale("log")
der.set_ylim(1e-9, 1.0)
der.set_xticks(n)
der.set_xticklabels(["1 copia", "2 copias", "3 copias", "4 copias"])
der.set_yticks([1e-8, 1e-6, 1e-4, 1e-2])
der.set_yticklabels(["1 entre 100 millones", "1 entre un millón", "1 entre 10.000",
                     "1 entre 100"], fontsize=8)
anotar(der, "cada copia de verdad independiente\ndivide el riesgo entre cien",
       xy=(2.0, 1e-4), xytext=(0.22, 0.92), color=VERDE)
anotar(der, "el fallo común no se reparte", xy=(3.0, p), xytext=(0.42, 0.58), color=ROJO)
der.set_ylabel("probabilidad de perderlo todo")
der.legend(loc="lower left", fontsize=8.5)
titulo(der, "La independencia es lo que protege", "cada copia con un 1 % de ser inservible")
rejilla(der, eje="y")

guardar(fig, "copias-rpo-rto-y-copias")
