"""tick-data-y-ohlcv-1.py — qué se pierde al pasar de la operación suelta a la vela: el
camino dentro del intervalo y el tamaño de cada operación. Página «Datos de transacción y
velas» (fase 9)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(6)

# Cuarenta minutos de operaciones: ni un tick por segundo ni precios de un céntimo
t = np.arange(0.0, 2400.0, 10.0)                 # una operación cada 10 segundos
precio = 50.0 + np.cumsum(azar.normal(0.0, 0.03, t.size))
volumen = azar.integers(40, 1200, t.size)

# Velas de un minuto: el orden y el tamaño de las operaciones se pierden al resumir
O, H, L, C = [], [], [], []
for k in range(40):
    trozo = precio[k * 6:(k + 1) * 6]
    O.append(trozo[0])
    H.append(trozo.max())
    L.append(trozo.min())
    C.append(trozo[-1])
O, H, L, C = map(np.array, (O, H, L, C))
recorrido = 100 * (H[0] - L[0]) / O[0]

# Los mismos ticks, dos criterios de agregación
cierres_tiempo = precio[5::6]
cierres_volumen = []
acumulado = 0.0
for p, v in zip(precio, volumen):
    acumulado += v
    if acumulado >= 1000:                        # se cierra la barra y se reinicia
        cierres_volumen.append(p)
        acumulado = 0.0
cierres_volumen = np.array(cierres_volumen)
comparables = cierres_tiempo.size                # se comparan los dos criterios en la misma ventana
desv_tiempo = np.diff(cierres_tiempo).std(ddof=1)
desv_volumen = np.diff(cierres_volumen[:comparables]).std(ddof=1)

fig, (izq, der) = plt.subplots(1, 2, figsize=(7.0, 4.4))

# --- Izquierda: el camino que la vela no cuenta ------------------------------
izq.plot(t[:42], precio[:42], color=REJILLA, linewidth=1.1, zorder=2)
tamano = 6 + 34 * (volumen[:42] / volumen.max())
izq.scatter(t[:42], precio[:42], s=tamano, color=AZUL, alpha=0.75, zorder=3)
for k in range(7):
    izq.axvline(k * 60, color=TEXTO, linewidth=0.8, linestyle=":", zorder=1)
for k in range(7):
    centro = k * 60 + 30
    izq.vlines(centro, L[k], H[k], color=NARANJA, linewidth=2.6, zorder=4)
    izq.vlines(centro, min(O[k], C[k]), max(O[k], C[k]), color=VERDE, linewidth=6.0, zorder=4)

izq.annotate("el primer minuto abre y cierra casi al mismo\nprecio, pero dentro se mueve un %.2f %%:" % recorrido,
             xy=(55, H[0]), xytext=(0.42, 0.82), textcoords="axes fraction",
             fontsize=8.5, color=ROJO,
             arrowprops=dict(arrowstyle="->", color=ROJO, linewidth=0.9, shrinkA=2, shrinkB=3))
izq.text(0.42, 0.60, "la vela no dice en qué orden\nni en cuántas operaciones",
         transform=izq.transAxes, fontsize=8.5, color=ROJO)
izq.text(0.03, 0.97, "gris: operaciones\nverde: cuerpo   naranja: máximo y mínimo",
         transform=izq.transAxes, fontsize=8, color=TEXTO, va="top")
izq.set_xlabel("segundos")
izq.set_ylabel("precio (EUR)")
izq.set_xlim(-10, 560)
izq.set_ylim(49.82, 50.34)
izq.set_title("Dentro de la vela hay una secuencia")
rejilla(izq)
numeros(izq)

# --- Derecha: la misma serie agregada con dos criterios ----------------------
der.plot(np.arange(comparables), cierres_tiempo[:comparables], color=AZUL, linewidth=1.3,
         label="barras de tiempo (1 minuto)")
der.plot(np.arange(comparables), cierres_volumen[:comparables], color=NARANJA, linewidth=1.3,
         label="barras de volumen (1.000 títulos)")
der.set_xlabel("número de barra desde el principio")
der.set_ylabel("precio (EUR)")
der.set_title("Dos criterios, dos números distintos")
der.legend(loc="upper left")
der.text(0.30, 0.06, "desviación de las variaciones:\npor tiempo %.4f  ·  por volumen %.4f"
         % (desv_tiempo, desv_volumen), transform=der.transAxes, fontsize=8.5, color=TEXTO)
rejilla(der)
numeros(der)

guardar(fig, "tick-a-vela-que-se-pierde")
