"""agentes-y-herramientas-1.py — el presupuesto de pasos es lo que decide si un bucle de
agente termina: el que acierta, el que gasta pasos en errores y el que repite sin avanzar.
Figura de la pagina de agentes y uso de herramientas (fase 8)."""

import numpy as np

from comun import *

estilo()

# La misma politica del ejemplo, con el estado de cada paso: (agente, numero de paso, estado)
# ok = la herramienta se ejecuto; rechazada = el validador no la dejo pasar.
PASOS = [
    ("A", 1, "multiplicar", "ok"),
    ("A", 2, "sumar", "ok"),
    ("B", 1, "multiplicar", "ok"),
    ("B", 2, "sumar", "rechazada"),
    ("B", 3, "multiplicar", "ok"),
    ("B", 4, "sumar", "ok"),
    ("C", 1, "sumar", "repetida"),
    ("C", 2, "sumar", "repetida"),
    ("C", 3, "sumar", "repetida"),
    ("C", 4, "sumar", "repetida"),
]
PRESUPUESTO = 4

COLOR = {"ok": VERDE, "rechazada": ROJO, "repetida": NARANJA}
ETIQUETA = {
    "ok": "la herramienta se ejecuta y el resultado vuelve al historial",
    "rechazada": "el validador la para: no se ejecuta nada y el error se le devuelve",
    "repetida": "misma llamada, mismo resultado: gasta presupuesto sin avanzar",
}

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 3.9))

# Panel 1: la rejilla de pasos de los tres agentes
agentes = ["A", "B", "C"]
for indice, agente in enumerate(agentes):
    for nombre, paso, herramienta, estado in PASOS:
        if nombre != agente:
            continue
        ejes[0].barh(indice, 1, left=paso - 1, height=0.62, color=COLOR[estado])
        ejes[0].annotate(herramienta, (paso - 0.5, indice), ha="center", va="center",
                         color="white", fontsize=8.5)
    # la linea del presupuesto corta el bucle a partir del paso siguiente
    ejes[0].plot([PRESUPUESTO, PRESUPUESTO], [indice - 0.45, indice + 0.45], color=TEXTO,
                 linewidth=1.6)
ejes[0].set_xlim(0, 4.9)
ejes[0].set_ylim(2.6, -0.6)
ejes[0].set_yticks(range(3))
ejes[0].set_yticklabels(["agente A\nacierta", "agente B\nun error", "agente C\nrepite"])
ejes[0].set_xticks(range(6))
titulo(ejes[0], "La línea negra es el presupuesto",
       "cuatro pasos concedidos: a partir de ahí el bucle se corta")
ejes[0].set_xlabel("paso del bucle")
rejilla(ejes[0], "x")
numeros(ejes[0], "x")
ejes[0].legend(handles=[plt.Rectangle((0, 0), 1, 1, color=VERDE),
                        plt.Rectangle((0, 0), 1, 1, color=ROJO),
                        plt.Rectangle((0, 0), 1, 1, color=NARANJA)],
               labels=[ETIQUETA["ok"], ETIQUETA["rechazada"], ETIQUETA["repetida"]],
               loc="upper center", bbox_to_anchor=(0.5, -0.28), fontsize=8.5,
               handlelength=1.1)

# Panel 2: lo que cambia el presupuesto, con y sin condicion de estancamiento
presupuestos = np.arange(1, 9)
# El agente C arranca con 4 pasos (los suyos del ejemplo): sin estancamiento gasta todo lo que
# le des; con la condicion de parada se queda en esos 4 y no sube.
arranque_c = 4
con_estancamiento = np.minimum(presupuestos, arranque_c)
sin_estancamiento = presupuestos.copy()

ejes[1].plot(presupuestos, sin_estancamiento, color=ROJO, linewidth=1.9, marker="o",
             markersize=4, label="sin detectar el estancamiento")
ejes[1].plot(presupuestos, con_estancamiento, color=VERDE, linewidth=1.9, marker="o",
             markersize=4, label="con parada por estancamiento")
anotar(ejes[1], "misma llamada cuatro veces: aquí se corta",
       xy=(arranque_c, arranque_c), xytext=(0.32, 0.17), color=VERDE)
titulo(ejes[1], "Sin parada, el bucle gasta todo lo que le des",
       "la condición de estancamiento es lo que lo frena")
ejes[1].set_xlabel("presupuesto de pasos concedido")
ejes[1].set_ylabel("pasos que llega a gastar")
rejilla(ejes[1])
numeros(ejes[1])
# La esquina de arriba a la izquierda está libre: la diagonal roja pasa muy por debajo.
ejes[1].legend(fontsize=8.5, loc="upper left")

guardar(fig, "agentes-presupuesto-de-pasos")
