# Dos frases que significan lo contrario y solo se diferencian en un "no".
documentos = ["la pelicula es buena", "la pelicula no es buena"]

def vocabulario(documentos, tam):
    """tam=1 devuelve unigramas; tam=2, unigramas y bigramas."""
    terminos = set()
    for d in documentos:
        palabras = d.split()
        for t in range(1, tam + 1):
            terminos.update(tuple(palabras[i:i + t]) for i in range(len(palabras) - t + 1))
    return sorted(" ".join(t) for t in terminos)     # la tupla se une con espacios: "pelicula no"

unigramas = vocabulario(documentos, 1)
print("unigramas:", unigramas)
# -> unigramas: ['buena', 'es', 'la', 'no', 'pelicula']
print("recuento de cada frase:", [[d.split().count(t) for t in unigramas] for d in documentos])
# -> recuento de cada frase: [[1, 1, 1, 0, 1], [1, 1, 1, 1, 1]]

con_bigramas = vocabulario(documentos, 2)
print("variables con bigramas:", len(con_bigramas))       # -> 10
print("aparece 'pelicula no':", "pelicula no" in con_bigramas)   # -> True
