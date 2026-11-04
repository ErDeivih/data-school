"""colas-y-mensajeria-1.py — la espera creciente con tope y el jitter: por qué no se reintenta
de inmediato contra un servicio caído. La figura de la página de colas y mensajería (fase 11)."""

import numpy as np

from comun import *

estilo()

base, tope = 1.0, 30.0                      # primer reintento a 1 s, tope de 30 s
intentos = np.arange(1, 9)
espera = np.minimum(tope, base * 2 ** (intentos - 1))    # 1, 2, 4, 8, 16, 30, 30, 30

fig, (izq, der) = plt.subplots(1, 2, figsize=(9.8, 3.8))

# --- Izquierda: la curva de espera ---------------------------------------------------
# La banda es el jitter: cada cliente sortea un poco alrededor del valor teórico.
izq.fill_between(intentos, espera * 0.7, np.minimum(tope, espera * 1.3), color=AZUL, alpha=0.15,
                 label="margen de jitter")
izq.plot(intentos, espera, color=AZUL, linewidth=1.8, marker="o", markersize=4,
         label="espera(n) = min(30, 2^(n-1))")
izq.axhline(tope, color=ROJO, linewidth=1.1, linestyle="--")
izq.text(1.1, tope + 1.4, "tope: a partir del sexto reintento ya no crece", fontsize=9, color=ROJO)
izq.set_ylim(-2, 40)
# Rejilla cada 10 s (y no cada 5): con la rejilla tupida, la raya de 0 pasaba por dentro de la
# leyenda y la de 5 no dejaba hueco para las dos filas.
izq.set_yticks([0, 10, 20, 30, 40])
izq.set_xticks(intentos)
izq.set_xlabel("número del reintento")
izq.set_ylabel("espera antes de reintentar (s)")
titulo(izq, "La espera se dobla hasta el tope de 30 s",
       "sin tope, el reintento 20 esperaría 2^19 s: casi seis días")
izq.legend(loc="lower right", bbox_to_anchor=(1.0, 0.09))
rejilla(izq)
numeros(izq)

# --- Derecha: el jitter reparte a los clientes ---------------------------------------
rng = np.random.default_rng(11)
clientes = 500
sincronizados = np.ones(clientes)                    # todos reintentan en el mismo instante
repartidos = rng.uniform(0.5, 1.5, clientes)         # cada uno sortea su momento
bordes = np.arange(0.0, 2.01, 0.1)
der.hist([sincronizados, repartidos], bins=bordes, color=[ROJO, VERDE],
         label=["sin jitter: un pico", "con jitter: repartidos"])
der.set_ylim(0, 620)
der.set_xlabel("segundos desde el fallo del servicio")
der.set_ylabel("clientes que reintentan")
titulo(der, "El jitter cambia un pico de 500 por 50",
       "500 clientes reintentan a la vez: sin azar coinciden todos")
der.legend(loc="upper right")
rejilla(der)
numeros(der)

guardar(fig, "colas-espera-creciente")
