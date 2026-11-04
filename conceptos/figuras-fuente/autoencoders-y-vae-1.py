"""autoencoders-y-vae-1.py — cuantas dimensiones latentes hacen falta y donde corta el
umbral de anomalia. La figura de la pagina de autoencoders y VAE (fase 7)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# Dimension latente de 1 a 20. El error que se tira es la varianza que no se retiene.
k = np.arange(1, 21)
pca = 0.60 * np.exp(-k / 3.3) + 0.015          # proyeccion lineal: subespacio plano
ae = 0.60 * np.exp(-(k / 2.4) ** 1.6) + 0.010  # variedad curva: cae antes y mas abajo

fig, ejes = plt.subplots(1, 2, figsize=(9.4, 3.9))

# --- Panel 1: curva de error frente a la anchura del cuello de botella ---
ejes[0].plot(k, pca, color=AZUL, linewidth=2.0, marker="o", markersize=3.4, label="subespacio lineal (PCA)")
ejes[0].plot(k, ae, color=MORADO, linewidth=2.0, marker="s", markersize=3.4, label="variedad curva (autoencoder)")
# Por debajo de este suelo solo queda ruido: son dimensiones que se memorizan, no que resumen.
ejes[0].axhline(0.045, color=ROJO, linewidth=1.1, linestyle="--")
titulo(ejes[0], "Cuantas dimensiones latentes bastan",
       "el error baja y luego se estanca: ese suelo es el ruido")
ejes[0].set_xlabel("dimensiones del cuello de botella k")
ejes[0].set_ylabel("error de reconstrucción")
ejes[0].legend(loc="upper right")
anotar(ejes[0], "aqui solo se memoriza ruido", xy=(16, 0.045), xytext=(0.40, 0.22), color=ROJO)
anotar(ejes[0], "con 6 basta si la variedad es curva", xy=(6, ae[5]), xytext=(0.34, 0.60), color=MORADO)
rejilla(ejes[0])
numeros(ejes[0])

# --- Panel 2: el error de reconstruccion como puntuacion de anomalia ---
# Se entrena solo con datos normales; lo raro se reconstruye mal.
normal = azar.gamma(2.0, 0.010, 400)
raro = azar.gamma(2.0, 0.010, 40) + azar.gamma(4.0, 0.020, 40)
umbral = float(np.quantile(normal, 0.99) * 1.35)
bins = np.linspace(0.0, 0.30, 40)

ejes[1].hist(normal, bins=bins, color=AZUL, alpha=0.75, label="normales")
ejes[1].hist(raro, bins=bins, color=NARANJA, alpha=0.75, label="anomalias")
ejes[1].axvline(umbral, color=ROJO, linewidth=1.6, linestyle="--")
titulo(ejes[1], "El error separa lo normal de lo raro",
       "el umbral se calibra con datos normales de validación")
ejes[1].set_xlabel("error de reconstrucción")
ejes[1].set_ylabel("observaciones")
ejes[1].legend(loc="upper right")
anotar(ejes[1], "umbral en el p99 de los normales", xy=(umbral, 60), xytext=(0.42, 0.62), color=ROJO)
rejilla(ejes[1])
numeros(ejes[1])

guardar(fig, "autoencoders-y-vae-latente-y-anomalia")
