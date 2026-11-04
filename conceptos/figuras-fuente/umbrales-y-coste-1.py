"""umbrales-y-coste-1.py — la curva de coste del ejemplo y de dónde sale el umbral
óptimo cuando los dos errores no cuestan lo mismo. Figura de la página de umbrales y
coste del error (fase 6)."""

import numpy as np

from comun import *

estilo()

# --- Panel izquierdo: 2.001 casos con probabilidad conocida y etiqueta generada a partir
# de ella (así el modelo sí está calibrado, que es el supuesto de la fórmula). Se barre
# el umbral y se suma el coste de los dos errores con c_FP = 3 € y c_FN = 200 €.
azar = np.random.default_rng(7)
p = np.linspace(0.0, 1.0, 2001)
y = (azar.random(p.size) < p).astype(float)
c_fp, c_fn = 3.0, 200.0

umbrales = np.linspace(0.0, 0.60, 121)
costes = []
for t in umbrales:
    pred = p >= t
    falsas = int((pred & (y == 0)).sum())
    fugas = int((~pred & (y == 1)).sum())
    costes.append(c_fp * falsas + c_fn * fugas)
costes = np.array(costes)
i_min = int(np.argmin(costes))
t_min, c_min = float(umbrales[i_min]), float(costes[i_min])

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.4))

ejes[0].plot(umbrales, costes, color=AZUL, linewidth=1.9)
ejes[0].plot([t_min], [c_min], "o", color=ROJO, markersize=6, zorder=3)
ejes[0].axvline(c_fp / (c_fp + c_fn), color=VERDE, linewidth=1.2, linestyle="--")
anotar(ejes[0], f"el mínimo: umbral {t_min:.3f}".replace(".", ",") +
       f"\ncon {c_min:,.0f} € de coste".replace(",", "."),
       xy=(t_min, c_min), xytext=(0.45, 0.22), color=ROJO)
anotar(ejes[0], "la línea verde es el umbral teórico\nc_FP / (c_FP + c_FN) = 0,015",
       xy=(0.0148, 20000), xytext=(0.30, 0.90), color=VERDE, flecha=False)
ejes[0].set_yscale("log")
ejes[0].set_xlim(-0.01, 0.61)
ejes[0].set_xlabel("umbral de decisión")
ejes[0].set_ylabel("coste total de los errores (€)")
rejilla(ejes[0])
# En un eje logarítmico el formateador propio ya escribe 10³ y 6 × 10³; si se le pone
# encima el de la coma decimal, las etiquetas mayores salen «1000» y las menores «10³».
numeros(ejes[0], ejes="x")
titulo(ejes[0], "El coste tiene un único mínimo, y no está en 0,5",
       "con el corte de 0,5 por costumbre el coste se multiplica por diecinueve")

# --- Panel derecho: de dónde sale ese umbral. Si el falso negativo cuesta r veces más
# que la falsa alarma, el punto de corte óptimo es 1 / (1 + r).
r = np.logspace(0, 3, 300)
ejes[1].plot(r, 1 / (1 + r), color=MORADO, linewidth=1.9)
ejes[1].plot([200 / 3], [1 / (1 + 200 / 3)], "o", color=ROJO, markersize=6, zorder=3)
anotar(ejes[1], "solo con costes iguales sale 0,5", xy=(1, 0.5), xytext=(0.02, 0.60),
       color=MORADO)
anotar(ejes[1], "el ejemplo: el fraude cuesta 67 veces más\nque una falsa alarma → 0,015",
       xy=(200 / 3, 1 / (1 + 200 / 3)), xytext=(0.30, 0.78), color=ROJO)
ejes[1].set_xscale("log")
ejes[1].set_ylim(-0.02, 1.02)
ejes[1].set_xlabel("cuántas veces cuesta más el falso negativo (c_FN / c_FP)")
ejes[1].set_ylabel("umbral óptimo")
rejilla(ejes[1])
numeros(ejes[1])
titulo(ejes[1], "Cuanto más caro es dejarlo pasar, más bajo el corte",
       "la fórmula vale con probabilidades calibradas; sin calibrar, manda el barrido")

guardar(fig, "umbral-curva-de-coste")
