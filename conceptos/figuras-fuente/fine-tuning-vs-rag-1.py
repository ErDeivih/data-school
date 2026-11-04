"""fine-tuning-vs-rag-1.py — dónde gana cada enfoque: el recuperador elige el fragmento
correcto y poner al día un dato cuesta órdenes de magnitud menos. La figura de la página
de ajuste fino frente a RAG (fase 8)."""

import re

import numpy as np

from comun import *

estilo()

# Los tres fragmentos y la consulta de la página, cada uno con su etiqueta corta.
FRAGMENTOS = [
    ("devoluciones:\n30 días", "El plazo de devolución de un pedido es de 30 dias desde la entrega."),
    ("envíos a Canarias:\n5 a 7 días", "Los envios a Canarias tardan entre 5 y 7 dias laborables."),
    ("garantía:\n2 años", "La garantia de los productos electronicos cubre 2 anos."),
]
CONSULTA = "cuanto tarda un envio a Canarias"


def vectorizar(docs):
    """TF-IDF con las filas normalizadas: el producto escalar es la similitud del coseno."""
    vocabulario = sorted({p for d in docs for p in re.findall(r"[a-z]+", d.lower())})
    indice = {p: i for i, p in enumerate(vocabulario)}
    tf = np.zeros((len(docs), len(vocabulario)))
    for f, d in enumerate(docs):
        for p in re.findall(r"[a-z]+", d.lower()):
            tf[f, indice[p]] += 1
    df = (tf > 0).sum(axis=0)
    idf = np.log((1 + len(docs)) / (1 + df)) + 1
    return (tf * idf) / np.linalg.norm(tf * idf, axis=1, keepdims=True)


matriz = vectorizar([t for _, t in FRAGMENTOS] + [CONSULTA])
similitud = matriz[:-1] @ matriz[-1]                 # un número por fragmento, ya normalizados
mejor = int(np.argmax(similitud))

# Mas ancho que antes: los dos titulos y la nota de cada barra caben en una linea.
fig, ejes = plt.subplots(1, 2, figsize=(11.6, 4.2))

# --- Izquierda: a quién elige el recuperador ---------------------------------
for i, ((etiqueta, _), valor) in enumerate(zip(FRAGMENTOS, similitud)):
    color = VERDE if i == mejor else AZUL
    ejes[0].barh(i, valor, color=color, height=0.55)
    ejes[0].text(max(valor, 0.004) + 0.006, i, ("%.3f" % valor).replace(".", ","),
                 va="center", fontsize=9, color=TEXTO)

ejes[0].set_yticks(range(len(FRAGMENTOS)))
ejes[0].set_yticklabels([e[0] for e in FRAGMENTOS], fontsize=8)
ejes[0].invert_yaxis()
ejes[0].set_xlim(0, 0.27)
ejes[0].set_xlabel("similitud con la pregunta «cuánto tarda un envío a Canarias»")
titulo(ejes[0], "El recuperador elige el fragmento correcto",
       "si el fragmento bueno no entrara en el top_k, ningún prompt lo arregla")
rejilla(ejes[0], "x")
numeros(ejes[0], "x")

# --- Derecha: lo que cuesta poner al día un dato que ha cambiado --------------
actualizar = [
    ("RAG: reindexar\nun documento", 0.014, VERDE, "0,014 $ y sigue citando la fuente"),
    ("Ajuste fino:\nreentrenar", 4.5, ROJO, "4,5 $ por experimento, y harás varios"),
]
for i, (etiqueta, valor, color, nota) in enumerate(actualizar):
    ejes[1].barh(i, valor, color=color, height=0.45)
    ejes[1].text(valor * 1.35, i, nota, va="center", fontsize=8, color=TEXTO)

ejes[1].set_yticks(range(len(actualizar)))
ejes[1].set_yticklabels([a[0] for a in actualizar], fontsize=8)
ejes[1].invert_yaxis()
ejes[1].set_xscale("log")
ejes[1].set_xlim(0.01, 400)
ejes[1].set_xlabel("dólares por poner al día el conocimiento (escala logarítmica)")
titulo(ejes[1], "Poner al día un dato cuesta 300 veces más",
       "reindexar cuesta céntimos; cada reentrenamiento, 4,5 $: la palanca barata es buscar mejor")
rejilla(ejes[1], "x")
numeros(ejes[1], "x")

guardar(fig, "fine-tuning-vs-rag-recuperar-o-entrenar")
