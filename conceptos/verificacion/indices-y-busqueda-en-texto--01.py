import re
from collections import defaultdict

documentos = {
    "d1": "el gato come pescado y el gato duerme",
    "d2": "el perro come pienso",
    "d3": "el gato y el perro duermen",
}


def analizar(texto):
    """Tokeniza a minusculas. Aqui no se quitan stopwords, a proposito."""
    return re.findall(r"[a-z]+", texto.lower())


indice = defaultdict(set)
for doc, texto in documentos.items():
    for termino in analizar(texto):
        indice[termino].add(doc)

print("postings de 'gato':", sorted(indice["gato"]))   # -> ['d1', 'd3']
print("postings de 'come':", sorted(indice["come"]))   # -> ['d1', 'd2']
print("terminos distintos:", len(indice))              # -> 9

# Una consulta AND es la interseccion de las listas de postings.
consulta = ["gato", "perro"]
resultado = set.intersection(*(indice[t] for t in consulta))
print("documentos con", consulta, ":", sorted(resultado))   # -> ['d3']
