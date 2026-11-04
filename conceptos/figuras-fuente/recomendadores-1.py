"""recomendadores-1.py — dos listas con el mismo contenido y el mismo acierto en los dos
primeros puestos: solo el NDCG ve que una coloca antes lo importante. Página de sistemas de
recomendación (fase 6)."""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.6))

# Las dos ordenaciones del ejemplo de la página: relevancia 3 = muy relevante, 0 = nada.
lista_a = np.array([3, 0, 2, 1])
lista_b = np.array([2, 0, 3, 1])


def dcg(relevancias):
    """Ganancia acumulada descontada: lo relevante en el puesto i pesa 1/log2(i+1)."""
    r = np.asarray(relevancias, float)
    return float(((2 ** r - 1) / np.log2(np.arange(2, r.size + 2))).sum())


def ndcg(relevancias, k):
    """NDCG@k: el DCG de los k primeros dividido entre el del mejor orden posible."""
    ideal = np.sort(np.asarray(relevancias, float))[::-1]
    return dcg(np.asarray(relevancias)[:k]) / dcg(ideal[:k])


# --- Izquierda: la relevancia de cada puesto en las dos listas.
posiciones = np.arange(1, lista_a.size + 1)
ancho = 0.36
ejes[0].bar(posiciones - ancho / 2, lista_a, width=ancho, color=AZUL,
            label="lista A: 3, 0, 2, 1")
ejes[0].bar(posiciones + ancho / 2, lista_b, width=ancho, color=NARANJA,
            label="lista B: 2, 0, 3, 1")
for p, (va, vb) in enumerate(zip(lista_a, lista_b), start=1):
    if va:
        ejes[0].text(p - ancho / 2, va + 0.08, str(va), ha="center", color=AZUL, fontsize=9)
    if vb:
        ejes[0].text(p + ancho / 2, vb + 0.08, str(vb), ha="center", color=NARANJA, fontsize=9)
anotar(ejes[0], "las dos tienen un producto relevante\nentre los dos primeros: precisión@2 = 0,50",
       xy=(2, 0.1), xytext=(0.03, 0.92), color=TEXTO, flecha=False)
titulo(ejes[0], "El mismo contenido, en otro orden",
       "relevancia de cada puesto: 3 es muy relevante, 0 no aporta nada")
ejes[0].set_xticks(posiciones, ["1.º", "2.º", "3.º", "4.º"])
ejes[0].set_xlabel("puesto en la lista")
ejes[0].set_ylabel("relevancia")
ejes[0].set_ylim(0, 4.2)
ejes[0].legend(loc="upper right", fontsize=8.5)
rejilla(ejes[0])
numeros(ejes[0], ejes="y")

# --- Derecha: el NDCG acumulado según cuántos puestos se miren.
ks = np.arange(1, lista_a.size + 1)
curva_a = np.array([ndcg(lista_a, int(k)) for k in ks])
curva_b = np.array([ndcg(lista_b, int(k)) for k in ks])
print("NDCG@k lista A:", np.round(curva_a, 4).tolist())
print("NDCG@k lista B:", np.round(curva_b, 4).tolist())

ejes[1].plot(ks, curva_a, color=AZUL, linewidth=2.0, marker="o", markersize=5,
             label="lista A: 3, 0, 2, 1")
ejes[1].plot(ks, curva_b, color=NARANJA, linewidth=2.0, marker="o", markersize=5,
             label="lista B: 2, 0, 3, 1")
for k, va, vb in zip(ks, curva_a, curva_b):
    ejes[1].text(k, va + 0.045, f"{va:.2f}".replace(".", ","), ha="center", color=AZUL,
                 fontsize=8.5)
    ejes[1].text(k, vb - 0.055, f"{vb:.2f}".replace(".", ","), ha="center", color=NARANJA,
                 fontsize=8.5)
anotar(ejes[1], "misma precisión@2 (0,50) en las dos\ny aun así NDCG@4: "
       + f"{curva_a[-1]:.2f}".replace(".", ",") + " frente a " + f"{curva_b[-1]:.2f}".replace(".", ","),
       xy=(4, float(curva_b[-1])), xytext=(0.03, 0.93), color=ROJO, flecha=False)
titulo(ejes[1], "El NDCG sí ve el desorden",
       "ganancia descontada por el puesto, comparada con el mejor orden posible")
ejes[1].set_xticks(ks)
ejes[1].set_xlabel("cuántos puestos se miran (k)")
ejes[1].set_ylabel("NDCG@k")
ejes[1].set_ylim(0.25, 1.25)
ejes[1].legend(loc="lower right", fontsize=8.5)
rejilla(ejes[1])
numeros(ejes[1], ejes="y")

guardar(fig, "recomendadores-ndcg-y-orden")
