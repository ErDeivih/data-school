"""metricas-de-ranking-1.py — precisión@k, recall@k y NDCG: lo que mide cada familia
de métricas de ranking y por qué el orden cambia el resultado (fase 6)."""

import numpy as np

from comun import *

estilo()

# Dos consultas inventadas con 20 documentos ordenados por el sistema.
# 1 = relevante, 0 = no relevante. La A tiene los aciertos arriba y 8 relevantes
# en todo el catalogo; la B tiene un solo acierto (en la posicion 2) y 18 relevantes.
consulta_a = np.array([1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
consulta_b = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])


def acumuladas(rel, total=None):
    """Precisión@k y recall@k para cada k. Los acumulo uno a uno porque las dos
    métricas dividen entre cosas distintas: la precisión entre k y el recall entre
    el total de relevantes de la consulta, que no tiene por qué caber en la lista."""
    aciertos = np.cumsum(rel)                      # aciertos entre los k primeros
    k = np.arange(1, rel.size + 1)
    total = int(rel.sum()) if total is None else total
    return aciertos, aciertos / k, aciertos / total


def dcg(grados, k=None):
    """Ganancia acumulada descontada: suma (2^rel - 1) / log2(i + 1)."""
    g = np.asarray(grados[:k], dtype=float)
    descuento = 1.0 / np.log2(np.arange(2, g.size + 2))
    return float((((2 ** g) - 1) * descuento).sum())


def ap_binaria(grados):
    """Precisión media con relevancia binaria: cada grado mayor que cero cuenta como
    acierto y el promedio va sobre el total de relevantes de la consulta."""
    aciertos, suma, total = 0, 0.0, int((grados > 0).sum())
    for i, g in enumerate(grados, start=1):
        if g > 0:
            aciertos += 1
            suma += aciertos / i
    return suma / total


grados_bueno = np.array([3, 2, 1, 0, 0, 0, 0, 0])       # casi el orden ideal
grados_mezcla = np.array([0, 1, 2, 3, 0, 0, 0, 0])      # los mejores, hundidos
grados_invertida = np.array([0, 0, 0, 1, 2, 3, 0, 0])   # los relevantes, al final
grados_ideal = np.sort(grados_bueno)[::-1]              # el mejor orden posible
listas = [grados_bueno, grados_mezcla, grados_invertida]

# NDCG@k acumulado: en cada posicion divido lo conseguido entre lo ideal hasta ahi.
dcg_bueno = np.array([dcg(grados_bueno, k) for k in range(1, 9)])
dcg_mezcla = np.array([dcg(grados_mezcla, k) for k in range(1, 9)])
dcg_ideal = np.array([dcg(grados_ideal, k) for k in range(1, 9)])
ndcg_bueno = dcg_bueno / dcg_ideal

# Dos filas y dos columnas: tres paneles en una sola fila se pisan. El hueco se borra.
fig, rejilla_ejes = plt.subplots(2, 2, figsize=(10.4, 7.2))
ejes = [rejilla_ejes[0][0], rejilla_ejes[0][1], rejilla_ejes[1][0]]
fig.delaxes(rejilla_ejes[1][1])

# --- (a) El corte k manda: la precision baja y el recall se estanca -------------
k = np.arange(1, 21)
_, prec_a, rec_a = acumuladas(consulta_a)
_, _, rec_b = acumuladas(consulta_b, total=18)   # 18 relevantes en el catalogo, 1 en la lista
ejes[0].plot(k, prec_a, color=AZUL, linewidth=1.8, label="Precisión@k  consulta A")
ejes[0].plot(k, rec_a, color=AZUL, linewidth=1.8, linestyle="--", label="Recall@k  consulta A")
ejes[0].plot(k, rec_b, color=NARANJA, linewidth=1.8, linestyle="--", label="Recall@k  consulta B")
ejes[0].set_xlabel("k (documentos que se miran)")
ejes[0].set_ylabel("valor de la métrica")
ejes[0].set_ylim(-0.03, 1.12)
ejes[0].legend(loc="lower right", fontsize=8)
titulo(ejes[0], "El corte k decide que se mide",
       "el recall de A solo llega a 1 bajando hasta la posición 8")
rejilla(ejes[0])
numeros(ejes[0])

# --- (b) Las tres familias sobre la misma lista, ordenada de tres maneras -------
etiquetas = ["buena", "mezclada", "invertida"]
# Cada familia con su definicion: la precision media cuenta los grados > 0, el NDCG divide
# el DCG de la lista entre el del orden ideal, y el MRR es 1 partido por la posicion del
# primer acierto. Los tres salen del mismo par de listas, no de numeros escritos a mano.
ap = [round(ap_binaria(g), 3) for g in listas]
mrr = [round(1 / (int(np.argmax(g > 0)) + 1), 3) for g in listas]
ndcg = [round(dcg(g) / dcg(grados_ideal), 3) for g in listas]
x = np.arange(3)
ancho = 0.26
ejes[1].bar(x - ancho, ap, ancho, color=AZUL, label="MAP (precisión media)")
ejes[1].bar(x, mrr, ancho, color=NARANJA, label="MRR")
ejes[1].bar(x + ancho, ndcg, ancho, color=VERDE, label="NDCG")
ejes[1].axhline(1.0, color=TEXTO, linewidth=0.8, linestyle=":", alpha=0.6)
ejes[1].axvline(0.5, color=REJILLA, linewidth=0.8, linestyle="--")
ejes[1].axvline(1.5, color=REJILLA, linewidth=0.8, linestyle="--")
ejes[1].set_xticks(x)
ejes[1].set_xticklabels(etiquetas)
ejes[1].set_ylim(0, 1.25)
ejes[1].set_ylabel("valor de la métrica")
ejes[1].legend(loc="upper right", fontsize=7.5, handlelength=1.3)
anotar(ejes[1], "La lista invertida se queda\ncon el 43 % del NDCG de la buena",
       xy=(2.26, 0.26), xytext=(0.02, 0.90))
titulo(ejes[1], "Mismos aciertos, distinto orden",
       "las tres castigan el hundimiento de los relevantes")
rejilla(ejes[1])
numeros(ejes[1])

# --- (c) Ganancia acumulada: la curva ideal es el liston ------------------------
posiciones = np.arange(1, 9)
# El sombreado va primero para que las tres curvas queden por encima y se lean enteras.
ejes[2].fill_between(posiciones, dcg_mezcla, dcg_ideal, color=ROSA, alpha=0.10)
ejes[2].plot(posiciones, dcg_ideal, color=ROJO, linewidth=2.0, linestyle=":",
             label="IDCG (orden ideal)")
ejes[2].plot(posiciones, dcg_bueno, color=VERDE, linewidth=1.9, label="DCG (orden bueno)")
ejes[2].plot(posiciones, dcg_mezcla, color=ROSA, linewidth=1.9, label="DCG (orden mezclado)")
ejes[2].set_xlabel("posición en la lista")
ejes[2].set_ylabel("ganancia acumulada")
ejes[2].set_ylim(0, 11.4)
ejes[2].legend(loc="lower right", fontsize=8)
anotar(ejes[2], "La distancia entre la curva ideal y la real,\ndividida entre la ideal, es el NDCG en esa\nposición",
       xy=(5.5, 8.0), xytext=(0.04, 0.86))
titulo(ejes[2], "El descuento por posición, acumulado",
       "NDCG = DCG / IDCG, siempre entre 0 y 1")
rejilla(ejes[2])
numeros(ejes[2])

guardar(fig, "metricas-de-ranking-corte-y-orden")
