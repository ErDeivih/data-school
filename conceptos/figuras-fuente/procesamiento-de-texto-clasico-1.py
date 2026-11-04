"""procesamiento-de-texto-clasico-1.py — por qué hay que pesar las palabras: la idf hunde lo
que aparece en todas partes y el tf-idf deja mandar a las palabras que distinguen. Página de
procesamiento de texto clásico (fase 6)."""

import numpy as np

from comun import *

estilo()

fig, ejes = plt.subplots(1, 2, figsize=(10.8, 4.6))

# --- Izquierda: cuánto vale un término según en cuántos documentos aparezca.
n = 1000
df = np.geomspace(1, n, 300)                 # de 1 documento a todos, en escala logarítmica
idf = np.log((1 + n) / (1 + df)) + 1         # la versión suavizada: nunca llega a 0
print("idf en df=1:", round(float(np.log((1 + n) / 2) + 1), 2),
      "en df=1000:", round(float(np.log(1) + 1), 2))

ejes[0].plot(df, idf, color=AZUL, linewidth=2.2)
ejes[0].axhline(1.0, color=REJILLA, linewidth=1.1, linestyle="--")
for marcado, color in ((1, ROJO), (n, ROJO)):
    valor = float(np.log((1 + n) / (1 + marcado)) + 1)
    ejes[0].plot([marcado], [valor], "o", color=color, markersize=6, zorder=4)
    if marcado == n:                         # el valor de df = 1 ya lo dice la anotación
        ejes[0].text(marcado * 0.55, valor + 0.05, coma(round(valor, 2)), color=ROJO,
                     fontsize=8.5)
anotar(ejes[0], "en un solo documento\nvale 7,22: es la señal",
       xy=(1, 7.21), xytext=(0.05, 0.86), color=ROJO, flecha=False)
anotar(ejes[0], "en todos los documentos\nsigue valiendo 1, no 0",
       xy=(1000, 1.0), xytext=(0.98, 0.78), color=REJILLA, flecha=False, align="right")
titulo(ejes[0], "La idf hunde lo que sale en todas partes",
       "1 000 documentos; ln((1 + n)/(1 + df)) + 1, la versión suavizada de scikit-learn")
ejes[0].set_xlabel("documentos en los que aparece el término (df)")
ejes[0].set_ylabel("idf del término")
ejes[0].set_xscale("log")
ejes[0].set_ylim(0, 8.6)
rejilla(ejes[0], eje="both")
numeros(ejes[0], ejes="both")

# --- Derecha: el mismo documento con recuento bruto y con tf-idf.
palabras = ["el", "devolución", "roto", "tarde"]
cuenta = np.array([5.0, 2, 1, 1])            # veces que aparece cada palabra en el documento
documentos = np.array([1000.0, 40, 120, 300])   # en cuántos de los 1 000 documentos sale
idf_palabra = np.log((1 + n) / (1 + documentos)) + 1
solo_contar = cuenta / cuenta.sum()          # lo que haría un modelo que solo cuenta
tfidf = cuenta * idf_palabra
tfidf = tfidf / np.sqrt((tfidf ** 2).sum())  # normalizado a norma 1, como en la página
print("solo contar:", np.round(solo_contar, 3).tolist())
print("tf-idf:", np.round(tfidf, 3).tolist())

posiciones = np.arange(len(palabras))
ancho = 0.36
ejes[1].bar(posiciones - ancho / 2, solo_contar, width=ancho, color=NARANJA,
            label="solo contar palabras (tf)")
ejes[1].bar(posiciones + ancho / 2, tfidf, width=ancho, color=AZUL,
            label="tf-idf normalizado")
anotar(ejes[1], "«el» manda en el recuento\ny no distingue nada",
       xy=(-ancho / 2, float(solo_contar[0])), xytext=(0.03, 0.90), color=NARANJA)
anotar(ejes[1], "«devolución» es la que separa\nuna queja de una felicitación",
       xy=(1 + ancho / 2, float(tfidf[1])), xytext=(0.55, 0.50), color=AZUL)
titulo(ejes[1], "Contar palabras no basta",
       "el mismo documento: recuento bruto frente a tf-idf normalizado a norma 1")
ejes[1].set_xticks(posiciones, palabras)
ejes[1].set_ylabel("peso de la palabra")
ejes[1].set_ylim(0, 1.12)
ejes[1].legend(loc="upper right", fontsize=8.5)
rejilla(ejes[1])
numeros(ejes[1], ejes="y")

guardar(fig, "texto-idf-y-pesos")
