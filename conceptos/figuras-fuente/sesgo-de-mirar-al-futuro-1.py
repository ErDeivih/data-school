"""sesgo-de-mirar-al-futuro-1.py — la misma regla y el mismo dia: lo único que cambia es si la
posición se cobra en su propia barra o en la siguiente. La figura de la pagina del sesgo de
mirar al futuro (fase 9)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)
n = 220
ret = azar.normal(0.0002, 0.012, n)     # retornos diarios, sin ninguna habilidad dentro
precio = 100 * np.cumprod(1 + ret)

# La regla es la misma en las dos versiones: comprado si el retorno de hoy fue positivo.
senal = (ret > 0).astype(float)
tramposo = senal * ret                  # la senal de hoy cobra el retorno de hoy
honesto = senal[:-1] * ret[1:]          # la senal de ayer cobra el retorno de hoy
mantener = ret[1:]                      # comprar y mantener, con las mismas 219 barras

trampa_c = np.cumprod(1 + tramposo) - 1
honesto_c = np.cumprod(1 + honesto) - 1
mantener_c = np.cumprod(1 + mantener) - 1

# Los dos se miden con la misma serie de retornos: solo cambia el signo que les toca.
sharpe_trampa = tramposo.mean() / tramposo.std(ddof=1) * np.sqrt(252)
sharpe_honesto = honesto.mean() / honesto.std(ddof=1) * np.sqrt(252)

fig, ejes = plt.subplots(2, 1, figsize=(7.0, 5.8), sharex=True)

# --- Arriba: el acumulado. La trampa sube en todas las barras ---
ejes[0].plot(trampa_c, color=ROJO, linewidth=1.8)
ejes[0].plot(honesto_c, color=VERDE, linewidth=1.8)
ejes[0].plot(mantener_c, color=REJILLA, linewidth=1.2, linestyle="--")
ejes[0].axhline(0, color=TEXTO, linewidth=0.8, alpha=0.4)
titulo(ejes[0], "El acumulado: la trampa no pierde ni una barra",
       "la señal de hoy se cobra el mismo día que se calcula")
ejes[0].set_ylabel("rentabilidad")
ejes[0].set_ylim(-0.45, 1.50)
# Los tres rótulos van arriba a la izquierda, apilados en el mismo orden que las curvas al
# final del eje, y cada uno cae en la franja entre dos rejillas (0,95 / 0,808 / 0,666 del
# alto). Estaban a la altura de su curva: el cero, las dos curvas y una rejilla los
# atravesaban (medido: 185 px de línea dentro de «honesto…» y 170 px dentro de «comprar y
# mantener…») y además los dos textos se pisaban entre sí (2,7 px de solape). El hueco está
# vacío: la curva roja no pasa de 1,19 y las otras dos van por debajo de cero.
rótulos = [
    ("sin desplazar: +%.0f %%" % (100 * trampa_c[-1]), ROJO, 0.95),
    ("honesto (señal de ayer): %.0f %%" % (100 * honesto_c[-1]), VERDE, 0.808),
    ("comprar y mantener: %.0f %%" % (100 * mantener_c[-1]), REJILLA, 0.666),
]
for texto, color, altura in rótulos:
    anotar(ejes[0], texto, xy=(0, 0), xytext=(0.05, altura), color=color, flecha=False)
rejilla(ejes[0])
numeros(ejes[0], "y")

# --- Abajo: el precio, para ver de dónde sale y a dónde llega la información ---
ejes[1].plot(precio, color=AZUL, linewidth=1.5)
titulo(ejes[1], "De dónde sale y a dónde llega la información",
       "la barra t decide el precio: en la trampa se cobra a la vez")
ejes[1].set_xlabel("barra")
ejes[1].set_ylabel("precio")
objetivo = int(np.argmax(np.abs(tramposo[1:] - honesto))) + 1
ejes[1].axvline(objetivo, color=NARANJA, linewidth=1.0, linestyle=":")
# Rejillas cada 10 y no cada 5: con el paso de 5 la rejilla de 75 partía en dos la nota
# (medido: 124 px de línea dentro del texto). La nota también se centra en el hueco entre las
# rejillas de 70 y 80 (caja de 77 a 128 px) en vez de colgar del borde de abajo.
ejes[1].set_yticks([70, 80, 90, 100])
anotar(ejes[1], "la barra donde las dos versiones\nmás se separan: en la tramposa, este\n"
                "precio decide y se cobra a la vez",
       xy=(objetivo, precio[objetivo]), xytext=(0.03, 0.218), color=NARANJA)
ejes[1].plot([objetivo], [precio[objetivo]], "o", color=NARANJA, markersize=4)
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "sesgo-de-mirar-al-futuro-una-barra")
