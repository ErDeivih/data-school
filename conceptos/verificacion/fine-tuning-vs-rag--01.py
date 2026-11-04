import re
import numpy as np

# Tres fragmentos de un manual interno: lo que un RAG pondria en el prompt.
fragmentos = [
    "El plazo de devolucion de un pedido es de 30 dias desde la entrega.",
    "Los envios a Canarias tardan entre 5 y 7 dias laborables.",
    "La garantia de los productos electronicos cubre 2 anos.",
]
consulta = "cuanto tarda un envio a Canarias"
documentos = fragmentos + [consulta]     # lista nueva: la consulta entra como un documento mas

# TF-IDF calculado a mano: frecuencia de termino por el logaritmo de la
# frecuencia inversa, y luego cada fila normalizada para comparar por coseno.
def vectorizar(docs):
    # un set quita repetidos y sorted fija el orden: la columna de cada palabra no cambia entre ejecuciones
    vocabulario = sorted({p for d in docs for p in re.findall(r"[a-z]+", d.lower())})
    indice = {p: i for i, p in enumerate(vocabulario)}      # palabra -> numero de columna
    tf = np.zeros((len(docs), len(vocabulario)))            # una fila por documento, en float
    for f, d in enumerate(docs):
        for p in re.findall(r"[a-z]+", d.lower()):
            tf[f, indice[p]] += 1                           # cuenta cuantas veces sale cada palabra
    df = (tf > 0).sum(axis=0)                               # axis=0 suma por columnas: en cuantos documentos sale
    idf = np.log((1 + len(docs)) / (1 + df)) + 1            # el +1 evita dividir entre cero
    # keepdims deja la norma con forma (n, 1) para poder dividir fila a fila
    return (tf * idf) / np.linalg.norm(tf * idf, axis=1, keepdims=True)

matriz = vectorizar(documentos)
similitud = matriz[:-1] @ matriz[-1]     # producto matriz-vector: un numero por fragmento (la consulta es la ultima fila)

# El fragmento util tiene que estar arriba: si no, el prompt no salva la respuesta.
for i in np.argsort(-similitud):         # el menos ordena de mayor a menor: argsort ordena ascendente
    print(f"{similitud[i]:.3f}  fragmento {i}")
# -> 0.206  fragmento 1
# -> 0.074  fragmento 0
# -> 0.000  fragmento 2
print("mejor fragmento:", int(np.argmax(similitud)))    # -> 1
