"""latencia-y-ejecucion-1.py — de qué depende el presupuesto de latencia y qué señales
lo agotan antes. Figura de la página de latencia y ejecución (fase 9)."""

import numpy as np
from matplotlib.lines import Line2D

from comun import *

estilo()

precio = 100.0
deriva_pb_por_ms = 0.005                       # deriva adversa, en pb por milisegundo
deriva_eur_por_ms = precio * deriva_pb_por_ms / 10_000

# ── Panel de arriba: la ventaja se gasta a ritmo constante ─────────────────────
edge_pb = 5.0                                  # ventaja esperada, en puntos básicos
edge_eur = precio * edge_pb / 10_000           # ventaja en EUR por acción
presupuesto_ms = edge_eur / deriva_eur_por_ms

latencia = np.linspace(0, 160, 400)
queda = 100 * (1 - deriva_eur_por_ms * latencia / edge_eur)

# ── Panel de abajo: cada señal tiene su presupuesto ────────────────────────────
ventajas_pb = np.array([0.5, 1.0, 2.0, 5.0, 25.0])
etiquetas = ["un tick (arbitraje)", "reversión intradía", "momentum de días",
             "cartera sistemática", "posición de semanas"]
presupuestos = precio * ventajas_pb / 10_000 / deriva_eur_por_ms

# Lo que tarda en llegar una orden según el montaje, en milisegundos
montajes = [("retail doméstico", 30.0), ("servidor en la ciudad", 3.0),
            ("co-location en la bolsa", 0.15)]

fig, ejes = plt.subplots(2, 1, figsize=(7.0, 6.2))

eje = ejes[0]
eje.plot(latencia, queda, color=AZUL, linewidth=1.9)
eje.axhline(0, color=TEXTO, linewidth=1.0)
eje.fill_between(latencia, queda, 0, where=(queda > 0), color=VERDE, alpha=0.14)
eje.fill_between(latencia, queda, 0, where=(queda <= 0), color=ROJO, alpha=0.14)
eje.axvline(presupuesto_ms, color=ROJO, linewidth=1.1, linestyle=":")
titulo(eje, "La ventaja se gasta a ritmo constante mientras esperas",
       "Con 5 pb de ventaja y 0,005 pb de deriva adversa por milisegundo")
eje.set_xlabel("latencia desde la señal hasta la llegada al libro (ms)")
eje.set_ylabel("% de la ventaja\nque sobrevive")
eje.set_xlim(0, 160)
eje.set_ylim(-20, 118)
rejilla(eje)
anotar(eje, "a los 100 ms se ha gastado toda la ventaja",
       (presupuesto_ms, 0.0), (0.62, 0.72), color=ROJO)
anotar(eje, "por debajo de esta raya la operación aún tiene esperanza",
       (20, 60.0), (0.04, 0.45), color=VERDE, flecha=False)

eje = ejes[1]
eje.barh(np.arange(len(ventajas_pb)), presupuestos, height=0.45, color=MORADO, alpha=0.75)
for fila, (ventaja, nombre) in enumerate(zip(ventajas_pb, etiquetas)):
    eje.text(4.6e-3, fila, f"{nombre}: {ventaja:g} pb de ventaja", fontsize=8,
             color=TEXTO, va="center")
for nombre, latencia_ms in montajes:
    eje.axvline(latencia_ms, color=NARANJA, linewidth=1.0, linestyle="--")
eje.set_xscale("log")
eje.set_yticks([])
eje.set_xlim(4e-3, 6e7)
eje.set_ylim(-0.55, len(ventajas_pb) - 0.35)
titulo(eje, "Cuanto más pequeña es la ventaja, menos latencia admite",
       "Presupuesto de latencia de cada señal; las líneas naranjas son montajes reales")
eje.set_xlabel("presupuesto de latencia (ms, escala logarítmica)")
rejilla(eje, eje="x")
eje.legend(handles=[Line2D([], [], color=NARANJA, linewidth=1.0, linestyle="--",
                           label="retail doméstico: 30 ms  ·  servidor: 3 ms  ·  "
                                 "co-location: 0,15 ms")],
           loc="lower right", fontsize=7.5)

numeros(ejes[0])
numeros(ejes[1], ejes="x")

guardar(fig, "latencia-presupuesto-y-montajes")
