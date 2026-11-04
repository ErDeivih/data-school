"""outliers-y-deteccion-1.py — el enmascaramiento: el extremo se esconde de si mismo
al inflar la desviación típica. La figura de la pagina de valores atipicos (fase 5)."""

import numpy as np

from comun import *

estilo()

base = np.array([8.0, 9.0, 10.0, 10.0, 11.0, 12.0, 12.0, 13.0, 14.0, 15.0, 16.0])
extremos = np.array([45.0, 60.0, 100.0, 200.0, 400.0, 1000.0])

z_clasico, z_robusto, desviaciones = [], [], []
for extremo in extremos:
    v = np.append(base, extremo)
    mediana = float(np.median(v))
    mad = float(np.median(np.abs(v - mediana)))
    desviaciones.append(float(v.std(ddof=1)))
    z_clasico.append((extremo - float(v.mean())) / float(v.std(ddof=1)))
    z_robusto.append(0.6745 * (extremo - mediana) / mad)

z_clasico = np.array(z_clasico)
z_robusto = np.array(z_robusto)

fig, ejes = plt.subplots(1, 2, figsize=(7.8, 3.9))

# --- Panel izquierdo: uno se queda clavado y el otro crece --------------------
ax = ejes[0]
ax.plot(extremos, z_clasico, "o-", color=AZUL, markersize=5, linewidth=1.4,
        label="z-score (media y desviación)")
ax.plot(extremos, z_robusto, "s-", color=ROJO, markersize=5, linewidth=1.4,
        label="z modificado (mediana y MAD)")
ax.axhline(3.5, color=REJILLA, linewidth=1.1, linestyle=":")
ax.set_xscale("log")
ax.set_ylim(-14, 348)
ax.set_xlabel("valor del extremo (escala logaritmica)")
ax.set_ylabel("puntuación de rareza")
anotar(ax, "el umbral habitual, 3,5", (60.0, 3.5), (0.04, 0.42), color=TEXTO, flecha=False)
anotar(ax, f"de 3,08 a {z_clasico[-1]:.2f}: no se entera", (1000.0, z_clasico[-1]), (0.66, 0.14), color=AZUL)
ax.legend(loc="upper left")
titulo(ax, "El clasico se enmascara, el robusto no")
rejilla(ax)
numeros(ax)

# --- Panel derecho: que se infla cuando el extremo crece ---------------------
ax = ejes[1]
ax.plot(extremos, desviaciones, "o-", color=NARANJA, markersize=5, linewidth=1.4)
ax.set_xscale("log")
ax.set_ylim(-14, 318)
ax.set_xlabel("valor del extremo (escala logaritmica)")
ax.set_ylabel("desviación típica muestral")
anotar(ax, "la desviación crece con el extremo", (45.0, desviaciones[0]), (0.04, 0.92), color=NARANJA)
anotar(ax, "es el número que el z-score lleva en el denominador",
       (200.0, 54.38), (0.06, 0.55), color=TEXTO)
titulo(ax, "La desviación se infla sola", "el orden de magnitud cambia el denominador")
rejilla(ax)
numeros(ax)

guardar(fig, "outliers-enmascaramiento-z-frente-a-mad")
