"""gan-1.py — por qué se entrena el generador con la pérdida no saturada y que es el
colapso de modos. La figura de la pagina de GAN (fase 7)."""

import numpy as np

from comun import *

estilo()


def normal(x, mu, s):
    return np.exp(-0.5 * ((x - mu) / s) ** 2) / (s * np.sqrt(2 * np.pi))


fig, ejes = plt.subplots(1, 2, figsize=(9.4, 3.9))

# --- Panel 1: la senal que llega al generador segun la perdida ---
# D es la probabilidad que el discriminador asigna a que la muestra sea real.
D = np.linspace(0.001, 0.999, 500)
ejes[0].plot(D, D * (1 - D), color=ROJO, linewidth=2.0, label="saturada: D(1 - D)")
ejes[0].plot(D, 1 - D, color=AZUL, linewidth=2.0, label="no saturada: 1 - D")
ejes[0].axvline(0.001, color=REJILLA, linewidth=1.0, linestyle=":")
titulo(ejes[0], "Cuando el rival acierta, el gradiente se apaga",
       "con D = 0,001 la senal cae de 0,999 a 0,001: un factor mil")
ejes[0].set_xlabel("D(G(z)): probabilidad que el discriminador da a lo falso")
ejes[0].set_ylabel("senal que recibe el generador")
ejes[0].legend(loc="upper center")
anotar(ejes[0], "aqui el generador no aprende", xy=(0.02, 0.02), xytext=(0.30, 0.55), color=ROJO)
rejilla(ejes[0])
numeros(ejes[0])

# --- Panel 2: colapso de modos en una mezcla de dos gaussianas ---
x = np.linspace(-7, 7, 600)
datos = 0.5 * normal(x, -2, 0.5) + 0.5 * normal(x, 2, 0.5)   # datos reales: dos modos
un_modo = normal(x, -2, 0.5)                                 # cubre uno solo y no arriesga
ancha = normal(x, 0.0, 1.6)                                  # se reparte por el centro
ejes[1].plot(x, datos, color=TEXTO, linewidth=2.0, label="datos reales")
ejes[1].plot(x, un_modo, color=NARANJA, linewidth=2.0, label="generador de un solo modo")
ejes[1].plot(x, ancha, color=CIAN, linewidth=2.0, linestyle="--", label="generador ancho y centrado")
titulo(ejes[1], "Cubrir un solo modo sale barato en una KL",
       "KL(p_g|p_d) = 0,693 frente a 12,175 al reves: por eso colapsa")
ejes[1].set_xlabel("valor de la muestra")
ejes[1].set_ylabel("densidad")
ejes[1].legend(loc="upper right")
anotar(ejes[1], "cubrir solo este modo no se penaliza", xy=(-2, 0.75), xytext=(0.05, 0.28), color=NARANJA)
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "gan-gradiente-y-colapso")
