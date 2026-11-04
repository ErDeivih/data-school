"""reconciliacion-y-pruebas-1.py — cuadrar origen y destino y donde poner la tolerancia.
Figura de la pagina 'reconciliacion-y-pruebas' (fase 4)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(3)

dias = np.arange(1, 15)
origen = np.round(8400 + 420 * np.sin(dias / 1.9) + azar.normal(0, 70, dias.size)).astype(int)
destino = origen.copy()
destino[8] -= 412          # un dia cargo a medias: faltan filas
destino[3] -= 52           # una diferencia pequena, justo fuera del limite
destino[11] += 38          # duplicados de un reintento, dentro de la tolerancia
relativa = 100 * (destino - origen) / origen

tolerancia = 0.5           # en porcentaje

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.6, 3.9))

# Izquierda: los dos recuentos, dia a dia.
izq.bar(dias - 0.19, origen, width=0.36, color=AZUL, label="lo que dice el origen")
izq.bar(dias + 0.19, destino, width=0.36, color=VERDE, label="lo que hay en el destino")
izq.set_ylim(0, 11400)
titulo(izq, "Origen y destino cuadran casi todos los días",
       "las barras se separan justo en los días que hay que investigar")
izq.set_xlabel("día del mes")
izq.set_ylabel("filas cargadas")
izq.legend(loc="upper center", ncol=2, fontsize=8.5)
numeros(izq)
rejilla(izq)

# Derecha: la diferencia relativa frente a la tolerancia pactada.
fuera = np.abs(relativa) > tolerancia
der.axhspan(-tolerancia, tolerancia, color=VERDE, alpha=0.12)
der.axhline(tolerancia, color=VERDE, linewidth=1.2, linestyle="--")
der.axhline(-tolerancia, color=VERDE, linewidth=1.2, linestyle="--")
der.axhline(0, color=TEXTO, linewidth=0.8, alpha=0.4)
der.vlines(dias, 0, relativa, color=REJILLA, linewidth=1.0, zorder=1)
der.scatter(dias[~fuera], relativa[~fuera], s=30, color=AZUL, zorder=3)
der.scatter(dias[fuera], relativa[fuera], s=45, color=ROJO, marker="D", zorder=3)
der.set_ylim(-1.6, 1.6)
titulo(der, "La tolerancia marca qué días hay que mirar",
       "dentro de la banda, la diferencia se acepta y se documenta")
der.set_xlabel("día del mes")
der.set_ylabel("diferencia destino − origen (%)")
anotar(der, "El día 9 se sale de la escala: −5,2 %", xy=(9, -1.45), xytext=(0.40, 0.10),
       color=ROJO)
anotar(der, "El día 12 se queda a 0,05 puntos del límite", xy=(12, relativa[11]),
       xytext=(0.30, 0.90), color=VERDE)
der.text(0.03, 0.62, "tolerancia de ±0,5 %", color=VERDE, fontsize=8.5, transform=der.transAxes)
numeros(der)
rejilla(der)

guardar(fig, "reconciliacion-tolerancia-y-dias")
