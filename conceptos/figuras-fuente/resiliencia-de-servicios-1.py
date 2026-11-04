"""resiliencia-de-servicios-1.py — la carga que recibe una dependencia con y sin
cortacircuitos, y la ley de Little agotando el grupo de conexiones. La figura de la
página de resiliencia de servicios (fase 11)."""

import numpy as np

from comun import *

estilo()

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 4.3))

# --- Izquierda: el cortacircuitos corta la carga justo cuando hace falta ------------
NORMAL = 100             # peticiones por segundo en regimen normal
REINTENTOS = 300         # el mismo trafico con 3 intentos por peticion
CAPACIDAD = 150          # lo que aguanta de verdad la dependencia

t = np.arange(0, 61)
# Sin cortacircuitos: los reintentos martillean la dependencia desde el fallo y nunca se recupera.
sin_cb = np.where(t < 12, NORMAL, REINTENTOS)
# Con cortacircuitos: abre en t=15, deja pasar unas pruebas en t=35 y vuelve en t=40.
con_cb = np.where(t < 12, NORMAL,
                  np.where(t < 15, REINTENTOS,
                           np.where(t < 35, 0,
                                    np.where(t < 40, 5, NORMAL))))

izq.step(t, sin_cb, where="post", color=ROJO, linewidth=1.8, label="sin cortacircuitos")
izq.step(t, con_cb, where="post", color=AZUL, linewidth=1.8, label="con cortacircuitos")
izq.axhline(CAPACIDAD, color=REJILLA, linestyle="--", linewidth=1.2)
izq.text(59, CAPACIDAD + 10, "capacidad real de la dependencia: 150/s", ha="right",
         color=REJILLA, fontsize=8.5)
izq.axvspan(15, 35, color=VERDE, alpha=0.10, linewidth=0)
anotar(izq, "abierto: cero llamadas durante 20 s", xy=(25, 15), xytext=(0.30, 0.60),
       color=VERDE)
anotar(izq, "los reintentos triplican la carga\njusto cuando la dependencia falla",
       xy=(26, REINTENTOS), xytext=(0.26, 0.90), color=ROJO)
izq.set_xlim(0, 60)
izq.set_ylim(0, 380)
izq.set_xlabel("segundos desde el fallo de la dependencia")
izq.set_ylabel("peticiones por segundo")
izq.legend(loc="lower right", fontsize=8.5)
titulo(izq, "El cortacircuitos deja respirar", "carga que recibe una dependencia lenta")
rejilla(izq)
numeros(izq, ejes="both")

# --- Derecha: la ley de Little decide cuando se agota el grupo de conexiones ---------
llegadas, pool = 200, 50
latencia = np.linspace(0.01, 3.0, 400)
en_vuelo = llegadas * latencia

der.plot(latencia, en_vuelo, color=AZUL, linewidth=1.8)
der.axhline(pool, color=ROJO, linestyle="--", linewidth=1.4)
der.axhspan(pool, 700, color=ROJO, alpha=0.08, linewidth=0)
anotar(der, "con 250 ms el grupo ya está lleno", xy=(0.25, pool), xytext=(0.36, 0.34),
       color=ROJO)
anotar(der, "a partir de aquí se encola todo:\nla espera y el timeout se comen el trabajo",
       xy=(2.0, 400), xytext=(0.04, 0.88), color=TEXTO)
der.set_xlim(0, 3)
der.set_ylim(0, 650)
der.set_xlabel("latencia de la dependencia (segundos)")
der.set_ylabel("conexiones en vuelo")
titulo(der, "La ley de Little: el pool se agota", "200 peticiones por segundo y 50 conexiones")
rejilla(der)
numeros(der, ejes="both")

guardar(fig, "resiliencia-cortacircuitos-y-pool")
