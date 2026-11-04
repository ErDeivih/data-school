"""tsne-y-umap-1.py — los mismos tres grupos dibujados con dos perplejidades: las islas se
separan igual, pero las distancias entre ellas cambian por completo. Página de t-SNE y UMAP
(fase 6)."""

import numpy as np
from sklearn.manifold import TSNE

from comun import *

estilo()
azar = np.random.default_rng(7)

# Tres grupos de 60 puntos en 10 dimensiones: centros a 4, 4 y 5,66 de distancia real.
centros = np.array([[0.0] * 10, [4.0] + [0.0] * 9, [0.0, 4.0] + [0.0] * 8])
X = np.vstack([azar.normal(c, 0.7, size=(60, 10)) for c in centros])
etiquetas = np.repeat([0, 1, 2], 60)
colores = [AZUL, NARANJA, VERDE]                 # un color por grupo en los dos paneles
# Distancias entre los centros de verdad: 4, 4 y 4·√2. Son las que el dibujo no respeta.
reales = [np.linalg.norm(centros[0] - centros[1]), np.linalg.norm(centros[0] - centros[2]),
          np.linalg.norm(centros[1] - centros[2])]
print("distancias reales:", np.round(reales, 2).tolist())

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.9))

for eje, perplejidad in zip(ejes, (5, 30)):
    # t-SNE solo dibuja: no hay transformación que puedas reutilizar en datos nuevos.
    mapa = TSNE(n_components=2, perplexity=perplejidad, random_state=0,
                init="random", max_iter=500).fit_transform(X)
    centros_mapa = np.array([mapa[etiquetas == k].mean(axis=0) for k in range(3)])
    distancias = np.array([np.linalg.norm(centros_mapa[0] - centros_mapa[1]),
                           np.linalg.norm(centros_mapa[0] - centros_mapa[2]),
                           np.linalg.norm(centros_mapa[1] - centros_mapa[2])])
    print(f"perplejidad {perplejidad}:", np.round(distancias, 1).tolist(),
          "cociente", round(float(distancias.max() / distancias.min()), 2))

    for k in range(3):
        eje.scatter(mapa[etiquetas == k, 0], mapa[etiquetas == k, 1], s=11,
                    color=colores[k], alpha=0.75,
                    label=f"grupo {k + 1}" if perplejidad == 5 else None)
    # Las coordenadas de un mapa t-SNE no tienen unidades ni origen: solo importa el orden.
    ancho = np.ptp(mapa[:, 0])                   # máximo menos mínimo, para dejar margen
    alto = np.ptp(mapa[:, 1])
    eje.set_xlim(mapa[:, 0].min() - 0.28 * ancho, mapa[:, 0].max() + 0.28 * ancho)
    eje.set_ylim(mapa[:, 1].min() - 0.28 * alto, mapa[:, 1].max() + 0.28 * alto)
    anotar(eje, "en el mapa, pares 1-2 / 1-3 / 2-3:\n" +
           " · ".join(coma(round(d, 1)) for d in distancias) +
           "   (cociente " + coma(round(float(distancias.max() / distancias.min()), 2)) + ")",
           xy=(float(centros_mapa[1, 0]), float(centros_mapa[1, 1])), xytext=(0.02, 0.96),
           color=TEXTO, flecha=False)
    eje.set_xlabel("eje 1 del mapa (sin unidades)")
    eje.set_ylabel("eje 2 del mapa")
    rejilla(eje, eje="both")
    numeros(eje, ejes="both")

titulo(ejes[0], "Perplejidad 5: las islas se igualan",
       "en los datos, los tres centros distan 4,00, 4,00 y 5,66 (cociente 1,41)")
titulo(ejes[1], "Perplejidad 30: otras distancias",
       "los mismos datos y los mismos grupos, con el vecindario más ancho")
ejes[0].legend(loc="lower right", fontsize=8.5)

guardar(fig, "tsne-perplejidad-y-distancias")
