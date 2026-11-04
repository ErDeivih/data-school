"""cuantizacion-y-destilacion-1.py — dónde aparece el error al cuantizar y cuánto pesa cada
bit. La figura de la página de cuantización y destilación (fase 7)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# Pesos verosímiles de una capa: casi todos pequeños, alguno de más.
pesos = azar.normal(0.0, 0.05, 4000)


def cuantiza(w, bits):
    """Redondea w a los niveles de `bits` bits simétricos: la escala la fija el más extremo."""
    qmax = 2 ** (bits - 1) - 1                  # 127 con 8 bits, 7 con 4, 3 con 2
    escala = np.abs(w).max() / qmax
    return np.clip(np.round(w / escala), -qmax - 1, qmax) * escala


fig, ejes = plt.subplots(2, 1, figsize=(7.0, 6.0))

# --- Arriba: la escalera de niveles frente a la recta que se quería guardar ---
ax = ejes[0]
limite = 0.012
x = np.linspace(-limite, limite, 600)
ax.plot(x, x, color=REJILLA, linewidth=1.6, label="float32: sin tocar")
for bits, color in ((8, AZUL), (4, NARANJA)):
    ax.plot(x, cuantiza(x, bits), color=color, linewidth=1.7, label=f"{bits} bits")
ax.axhline(0, color=TEXTO, linewidth=0.8, alpha=0.35)
ax.set_xlim(-limite, limite)
ax.set_ylim(-limite * 1.3, limite * 1.3)
ax.set_xlabel("peso original")
ax.set_ylabel("peso guardado")
ax.legend(loc="upper left", fontsize=8.5)
anotar(ax, "con 4 bits la escala vale 0,0017: son 18 veces\nmenos niveles que con 8 bits",
       (0.0, 0.0), (0.98, 0.07), color=NARANJA, flecha=False, align="right")
titulo(ax, "Guardar un peso es redondearlo a un escalón",
       "la escala la fija el peso más extremo del grupo")
rejilla(ax)
numeros(ax)

# --- Abajo: cómo quedan los 4.000 pesos de la capa ---
ax = ejes[1]
centros = np.linspace(-0.22, 0.22, 500)
ancho = centros[1] - centros[0]


def densidad(w):
    """Reparte los pesos en cajas y suaviza, para ver la forma sin histograma de barras."""
    cajas = np.histogram(w, bins=np.append(centros - ancho / 2, centros[-1] + ancho / 2))[0]
    suave = np.convolve(cajas, np.ones(9) / 9, mode="same")
    return suave / (suave.sum() * ancho)


ax.fill_between(centros, densidad(pesos), color=REJILLA, alpha=0.35)
ax.plot(centros, densidad(pesos), color=TEXTO, linewidth=1.3, label="float32")
for bits, color in ((8, AZUL), (4, NARANJA)):
    ax.plot(centros, densidad(cuantiza(pesos, bits)), color=color, linewidth=1.5,
            label=f"{bits} bits")
# Los niveles reales de 4 bits para estos pesos: la escala la fija max|w| = 0,183, asi que
# la rejilla va de -7 a +7 escalones (0,0262 cada uno) y los pesos ocupan catorce de ellos.
escala4 = np.abs(pesos).max() / (2 ** (4 - 1) - 1)
for nivel in np.arange(-7, 8) * escala4:
    ax.axvline(nivel, color=NARANJA, linewidth=0.6, linestyle=":", alpha=0.7)
ax.set_xlim(-0.22, 0.22)
ax.set_xlabel("valor del peso")
ax.set_ylabel("densidad")
ax.legend(loc="upper right", fontsize=8.5)
anotar(ax, "cada línea vertical es un nivel de 4 bits:\nla forma se rompe en barrotes",
       (0.15, 0.2), (0.02, 0.95), color=NARANJA, flecha=False)
titulo(ax, "Los pesos se apelotonan en catorce escalones",
       "el error no se reparte: se concentra en el redondeo")
rejilla(ax)
numeros(ax)

guardar(fig, "cuantizacion-escalones-y-densidad")
