"""priorizar-y-planificar-1.py — la espera según la ocupación del equipo y las tres formas
de coste del retraso. La figura de la página de priorizar y planificar (fase 12)."""

import numpy as np

from comun import *

estilo()

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 4.2))

# --- Izquierda: la espera crece como la ocupación entre lo que le falta -------------
rho = np.linspace(0.05, 0.95, 300)
espera = rho / (1 - rho)

izq.plot(100 * rho, espera, color=AZUL, linewidth=1.8)
for r in (0.7, 0.9, 0.95):
    izq.plot([100 * r], [r / (1 - r)], marker="o", color=ROJO, markersize=5, zorder=4)
anotar(izq, "al 70 % se espera 2,3 veces\nel tiempo de servicio", xy=(70, 2.33),
       xytext=(0.05, 0.74), color=NARANJA)
anotar(izq, "al 95 %, 19 veces", xy=(95, 19), xytext=(0.46, 0.42), color=ROJO)
izq.set_xlim(0, 100)
izq.set_ylim(0, 20)
izq.set_xlabel("ocupación del equipo (%)")
izq.set_ylabel("espera (veces el tiempo de servicio)")
titulo(izq, "La espera se dispara antes del 100 %", "un plan sin aire convierte cada imprevisto en una cola")
rejilla(izq)
numeros(izq, ejes="both")

# --- Derecha: no todos los retrasos cuestan lo mismo --------------------------------
semanas = np.arange(0, 12.01, 0.25)
lineal = 1.0 * semanas
se_enfria = 6 * (1 - np.exp(-semanas / 3))
fecha_limite = np.where(semanas < 8, 0.0, 10.0)

der.plot(semanas, lineal, color=AZUL, linewidth=1.7, label="lineal: cada semana cuesta igual")
der.plot(semanas, se_enfria, color=NARANJA, linewidth=1.7,
         label="se enfría: cada semana cuesta menos")
der.step(semanas, fecha_limite, where="post", color=ROJO, linewidth=1.7,
         label="con fecha límite: se pierde de golpe")
anotar(der, "el acantilado: pasar la fecha\ncuesta todo el valor a la vez", xy=(8.05, 10.05),
       xytext=(0.44, 0.14), color=ROJO)
der.set_xlim(0, 12)
der.set_ylim(0, 14)
der.set_xlabel("semanas de retraso")
der.set_ylabel("coste acumulado del retraso")
der.legend(loc="upper left", fontsize=8.5)
titulo(der, "No todos los retrasos cuestan igual", "la pendiente decide el orden, no el valor total")
rejilla(der)
numeros(der, ejes="both")

guardar(fig, "priorizar-cola-y-coste-del-retraso")
