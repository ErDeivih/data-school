"""ventanas-y-watermarks-1.py — cuando se cierra una ventana y que pasa con lo que llega tarde.
Figura de la pagina 'ventanas-y-watermarks' (fase 4)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

ANCHO, RETRASO = 5, 2          # ventana fija de 5 minutos y 2 minutos de retraso permitido
N_VENTANAS = 12

# Cada evento trae su tiempo de evento; el retraso es lo que tarda en llegar al sistema.
eventos = []
for w in range(N_VENTANAS):
    for t in w * ANCHO + azar.uniform(0.05, ANCHO - 0.05, int(azar.integers(3, 11))):
        eventos.append((float(t), float(azar.gamma(2.0, 1.5))))
eventos.sort(key=lambda e: e[0] + e[1])          # el sistema los ve por orden de llegada

# El motor: la marca de agua va por detras del ultimo tiempo de evento visto.
max_visto = -1e9
abiertas, publicadas, entran = {}, {}, []
for t_ev, retraso in eventos:
    max_visto = max(max_visto, t_ev)
    marca = max_visto - RETRASO
    for w in sorted(abiertas):                    # cierra lo que la marca de agua ya dejo atras
        if (w + 1) * ANCHO <= marca:
            publicadas[w] = abiertas.pop(w)
    w = int(t_ev // ANCHO)
    if w in publicadas:                           # su ventana ya se publico: llega tarde
        entran.append(False)
    else:
        abiertas[w] = abiertas.get(w, 0) + 1
        entran.append(True)

reales = {}
for t_ev, _ in eventos:
    reales[int(t_ev // ANCHO)] = reales.get(int(t_ev // ANCHO), 0) + 1

tiempos = np.array([e[0] for e in eventos])
retrasos = np.array([e[1] for e in eventos])
entro = np.array(entran)
i_tarde = int(np.argmax(np.where(entro, retrasos, -1)))    # entro con el retraso mas alto
i_fuera = int(np.argmin(np.where(entro, 99, retrasos)))    # se quedo fuera con el mas bajo

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.6, 3.9))

# Izquierda: quien entra en su ventana y quien no, frente al retraso permitido.
izq.scatter(tiempos[entro], retrasos[entro], s=18, color=AZUL,
            label="entró en su ventana antes del cierre")
izq.scatter(tiempos[~entro], retrasos[~entro], s=34, color=ROJO, marker="X",
            label="llegó con la ventana ya cerrada")
izq.axhline(RETRASO, color=NARANJA, linewidth=1.4, linestyle="--")
izq.set_ylim(0, 14.5)
titulo(izq, "La marca de agua decide quién entra",
       "y no el retraso de cada evento por separado")
izq.set_xlabel("tiempo de evento (minutos desde las 8:00)")
izq.set_ylabel("retraso de llegada (min)")
anotar(izq, "Este entró con 8 min de retraso", xy=(tiempos[i_tarde], retrasos[i_tarde]),
       xytext=(0.02, 0.70), color=AZUL)
anotar(izq, "Y este, con 4, se quedó fuera", xy=(tiempos[i_fuera], retrasos[i_fuera]),
       xytext=(0.02, 0.56), color=ROJO)
izq.text(0.98, 0.42, "retraso permitido R = 2 min", ha="right", color=NARANJA, fontsize=9,
         transform=izq.transAxes)
izq.legend(loc="upper center", ncol=1, fontsize=8.5)
numeros(izq)
rejilla(izq)

# Derecha: el recuento que se publica frente a lo que habia de verdad.
ventanas = np.arange(N_VENTANAS)
pub = np.array([publicadas.get(int(w), 0) for w in ventanas], dtype=float)
tarde = np.array([reales[int(w)] - publicadas.get(int(w), 0) if int(w) in publicadas else 0
                  for w in ventanas], dtype=float)
pendiente = np.array([reales[int(w)] if int(w) not in publicadas else 0 for w in ventanas], dtype=float)

der.bar(ventanas, pub, color=AZUL, width=0.72, label="publicado al cerrar la ventana")
der.bar(ventanas, tarde, bottom=pub, color=ROJO, width=0.72, label="llegó después del cierre")
der.bar(ventanas, pendiente, bottom=pub + tarde, color=REJILLA, width=0.72,
        label="ventana aún sin cerrar")
der.set_ylim(0, 16)
etiquetas = ["8:%02d" % int(w * ANCHO % 60) for w in ventanas]
der.set_xticks(ventanas)
der.set_xticklabels(etiquetas, fontsize=8)
titulo(der, "Cerrar pronto pública un recuento corto",
       "la diferencia con la realidad se queda en el olvido")
der.set_xlabel("ventana por su hora de inicio")
der.set_ylabel("eventos")
w_peor = int(max((w for w in publicadas), key=lambda w: reales[w] - publicadas[w]))
anotar(der, "10 eventos de verdad, 9 publicados", xy=(w_peor, reales[w_peor]),
       xytext=(0.24, 0.74), color=ROJO)
der.legend(loc="upper center", ncol=1, fontsize=8.5)
numeros(der, ejes="y")
rejilla(der)

guardar(fig, "ventanas-y-watermarks-cierre")
