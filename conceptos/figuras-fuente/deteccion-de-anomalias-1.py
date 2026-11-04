"""deteccion-de-anomalias-1.py — las dos caras del problema: unos pocos puntos raros que el
ojo separa sin esfuerzo, y una puntuación clásica que no llega a marcarlos porque el propio
outlier la deja sin fuerza. Página de detección de anomalías (fase 6)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.6))

# --- Izquierda: 315 observaciones, 15 de ellas en un anillo lejano.
normal = azar.normal(0, 1, size=(300, 2))
angulos = np.linspace(0, 2 * np.pi, 15, endpoint=False)   # 15 puntos repartidos por el anillo
anomalos = 7 * np.column_stack([np.cos(angulos), np.sin(angulos)])
ejes[0].scatter(normal[:, 0], normal[:, 1], s=11, color=AZUL, alpha=0.55,
                label="300 normales")
ejes[0].scatter(anomalos[:, 0], anomalos[:, 1], s=34, color=ROJO, label="15 anómalos")
radio = np.linspace(0, 2 * np.pi, 200)
ejes[0].plot(7 * np.cos(radio), 7 * np.sin(radio), color=REJILLA, linewidth=1.0,
             linestyle="--")
anotar(ejes[0], "15 de 315: el 4,8 %\nson los que el negocio revisa",
       xy=(float(anomalos[6, 0]), float(anomalos[6, 1])), xytext=(0.02, 0.94), color=ROJO)
anotar(ejes[0], "en dos dimensiones el ojo basta;\ncon 40 variables, ya no",
       xy=(0.0, 0.0), xytext=(0.03, 0.06), color=TEXTO, flecha=False)
titulo(ejes[0], "Un anillo de puntos raros",
       "sin etiquetas no hay nada que aprender: solo hay rareza que ordenar")
ejes[0].set_xlabel("variable 1")
ejes[0].set_ylabel("variable 2")
ejes[0].set_aspect("equal")                   # el anillo solo parece un anillo si los ejes miden igual
ejes[0].set_xlim(-9.5, 9.5)
ejes[0].set_ylim(-9.5, 9.5)
ejes[0].legend(loc="upper right", fontsize=8.5)
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="both")

# --- Derecha: qué le pasa al z-score clásico cuando el valor extremo crece.
base = np.array([10.0, 11, 12, 12, 13, 13, 14, 15])
extremos = np.linspace(16, 45, 200)
z_clasico, z_mod = [], []
for X in extremos:
    muestra = np.r_[base, X]
    z_clasico.append((X - muestra.mean()) / muestra.std(ddof=1))
    mediana = np.median(muestra)
    mad = np.median(np.abs(muestra - mediana))     # MAD: mediana de las distancias a la mediana
    z_mod.append(0.6745 * (X - mediana) / mad)     # 0,6745 hace comparables las dos escalas
techo = (base.size) / np.sqrt(base.size + 1)       # máximo que puede alcanzar el z clásico
print("techo teórico:", round(float(techo), 3),
      "z clasico en 45:", round(z_clasico[-1], 3), "z mod en 45:", round(z_mod[-1], 2))

ejes[1].plot(extremos, z_clasico, color=AZUL, linewidth=2.0, label="z clásico (media y desviación)")
ejes[1].plot(extremos, z_mod, color=ROJO, linewidth=2.0, label="z modificado (mediana y MAD)")
ejes[1].axhline(techo, color=AZUL, linewidth=1.1, linestyle="--")
ejes[1].axhline(3.0, color=NARANJA, linewidth=1.1, linestyle=":", label="umbral clásico (3)")
ejes[1].axhline(3.5, color=VERDE, linewidth=1.1, linestyle=":", label="umbral robusto (3,5)")
anotar(ejes[1], "el z clásico se queda pegado a su techo: nunca llega a 3",
       xy=(30, float(z_clasico[-1])), xytext=(0.26, 0.21), color=AZUL, flecha=False)
anotar(ejes[1], "el robusto ya pasó el umbral\ncon un valor de 18,2",
       xy=(18.2, 3.5), xytext=(0.03, 0.03), color=ROJO)
titulo(ejes[1], "El z clásico se queda sin fuerza",
       "la media y la desviación se calculan con el outlier dentro, y él mismo las infla")
ejes[1].set_xlabel("valor del punto extremo (el resto son 10 … 15)")
ejes[1].set_ylabel("puntuación de rareza")
ejes[1].set_ylim(0, 23)
ejes[1].legend(loc="upper left", fontsize=8.5)
rejilla(ejes[1], eje="both")
numeros(ejes[1], ejes="both")

guardar(fig, "anomalias-anillo-y-z-robusto")
