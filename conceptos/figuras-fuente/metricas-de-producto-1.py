"""metricas-de-producto-1.py — la curva de retención por cohortes y el estado estacionario
de la base de usuarios. La figura de la página de métricas de producto (fase 12)."""

import numpy as np

from comun import *

estilo()

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 4.2))

# --- Izquierda: la cohorte que empieza más alta no es la que retiene -----------------
semanas = np.arange(0, 9)
alta_y_rapida = np.array([100.0, 45, 32, 26, 22, 20, 19, 18.5, 18])
baja_y_estable = np.array([100.0, 38, 30, 26, 24.5, 24, 23.8, 23.7, 23.7])

izq.axhspan(18, 24, color=REJILLA, alpha=0.16, linewidth=0)
izq.plot(semanas, alta_y_rapida, marker="o", markersize=3.5, color=NARANJA, linewidth=1.7,
         label="cohorte de enero")
izq.plot(semanas, baja_y_estable, marker="o", markersize=3.5, color=AZUL, linewidth=1.7,
         label="cohorte de marzo")
anotar(izq, "el suelo es lo que decide:\naquí se queda la gente que vuelve sola",
       xy=(7.5, 21), xytext=(0.30, 0.62), color=MORADO)
anotar(izq, "empieza más alta\ny acaba por debajo", xy=(2.0, 33), xytext=(0.06, 0.92),
       color=NARANJA)
izq.set_xlim(0, 8)
izq.set_ylim(0, 105)
izq.set_xlabel("semanas desde el alta")
izq.set_ylabel("% de la cohorte que sigue activa")
izq.legend(loc="upper right", fontsize=8.5)
titulo(izq, "La retención se lee por cohortes", "nunca en el agregado de todo el producto")
rejilla(izq)
numeros(izq, ejes="both")

# --- Derecha: con altas constantes la base converge a altas entre abandono -----------
altas, inicial = 4000, 10000
meses = np.arange(0, 61)


def base(churn):
    """Recurrencia U(t+1) = U(t) * (1 - churn) + altas."""
    valores = [inicial]
    for _ in meses[1:]:
        valores.append(valores[-1] * (1 - churn) + altas)
    return np.array(valores)


der.plot(meses, base(0.06), color=AZUL, linewidth=1.8, label="abandono del 6 %")
der.plot(meses, base(0.05), color=VERDE, linewidth=1.8, label="abandono del 5 %")
der.axhline(66667, color=AZUL, linestyle="--", linewidth=1.0)
der.axhline(80000, color=VERDE, linestyle="--", linewidth=1.0)
anotar(der, "un punto de abandono vale\n13.333 usuarios estables", xy=(46, 73300),
       xytext=(0.32, 0.24), color=MORADO)
der.set_xlim(0, 60)
der.set_ylim(0, 90000)
der.set_xlabel("meses desde el inicio")
der.set_ylabel("usuarios activos")
der.legend(loc="lower right", fontsize=8.5)
titulo(der, "El estado estacionario", "4.000 altas al mes: la base tiende a ellas entre el abandono")
rejilla(der)
numeros(der, ejes="both")

guardar(fig, "metricas-retencion-y-estado-estacionario")
