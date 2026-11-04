"""evaluacion-de-llms-1.py — por qué un 92 % de acuerdo puede no significar nada: la matriz
de coincidencias, el acuerdo que saldria por azar y el kappa. Figura de la pagina de
evaluación de LLMs (fase 8)."""

import numpy as np

from comun import *

estilo()

# Matriz de coincidencias del ejemplo: 50 respuestas, juez automatico contra anotador humano.
# Filas: etiqueta del humano (1 = correcta). Columnas: etiqueta del juez.
matriz = np.array([[28, 2],
                   [2, 18]])
N = matriz.sum()
po = float(np.trace(matriz) / N)               # acuerdo observado: la diagonal
pj = matriz.sum(axis=0) / N                    # marginales del juez
ph = matriz.sum(axis=1) / N                    # marginales del humano
pe = float(pj @ ph)                            # acuerdo esperado por azar
kappa = (po - pe) / (1 - pe)

fig, (izq, der) = plt.subplots(1, 2, figsize=(10.0, 4.2),
                               gridspec_kw={"width_ratios": [1.05, 1.0]})

# Panel izquierdo: la matriz de coincidencias. El color no aporta informacion nueva, solo
# separa la diagonal (donde coinciden) de las dos esquinas donde no.
izq.imshow(matriz, cmap="Blues", vmin=0, vmax=30)
for i in range(2):
    for j in range(2):
        nota = "coinciden" if i == j else "no"
        izq.annotate(f"{matriz[i, j]}  ({nota})", (j, i), ha="center", va="center",
                     fontsize=11, color="white" if matriz[i, j] > 20 else TEXTO)
izq.set_xticks([0, 1])
izq.set_xticklabels(["juez dice 1", "juez dice 0"])
izq.set_yticks([0, 1])
izq.set_yticklabels(["humano\ndice 1", "humano\ndice 0"])
izq.set_xlim(-0.5, 1.5)
izq.set_ylim(1.5, -0.5)
izq.set_title("Coinciden en 46 de 50: un 92 % que impresiona", fontsize=10)

# Panel derecho: la formula del kappa resuelta para el acuerdo observado. El punto del juez
# esta muy por encima de la linea de azar, y esa distancia es lo que mide el kappa.
kappas = np.array([-0.05, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
observados = kappas * (1 - pe) + pe            # po que corresponde a cada kappa con este pe

der.plot(observados, kappas, color=AZUL, linewidth=1.8)
der.axhline(0.0, color=TEXTO, linewidth=0.8, alpha=0.4)
der.axvline(pe, color=CIAN, linewidth=1.4, linestyle="--")
der.annotate("acuerdo por azar: 0,52\naquí el kappa vale 0", (pe, 0.0),
             textcoords="offset points", xytext=(-8, 14), ha="right", color=CIAN, fontsize=9)
der.plot([po], [kappa], "o", color=ROJO, markersize=7)
etiqueta = "este juez: 92 % de acuerdo\ny kappa " + ("%.2f" % kappa).replace(".", ",")
der.annotate(etiqueta, (po, kappa), textcoords="offset points", xytext=(-16, 6),
             ha="right", color=ROJO, fontsize=9)
der.set_xlim(0, 1.06)
der.set_ylim(-0.12, 1.12)
der.set_title("El kappa descuenta el acuerdo que sale solo", fontsize=10)
der.set_xlabel("acuerdo observado entre juez y humano")
der.set_ylabel("kappa de Cohen")
der.set_xticks([0, pe, po, 1.0])
der.set_xticklabels(["0", "0,52\n(azar)", "0,92", "1"])
der.set_yticks(kappas)
rejilla(der)
numeros(der, "y")

guardar(fig, "evaluacion-acuerdo-y-kappa")
