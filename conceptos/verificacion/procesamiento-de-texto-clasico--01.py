import math
from collections import Counter

documentos = ["el gato duerme", "el perro duerme", "el gato come"]
cestas = [d.split() for d in documentos]
n = len(cestas)

# Frecuencia inversa de documento, con el suavizado habitual.
df = Counter(t for c in cestas for t in set(c))     # set(c): cuenta documentos, no repeticiones
idf = {t: math.log((1 + n) / (1 + df[t])) + 1 for t in df}    # math.log es neperiano
print("idf:", {t: round(v, 4) for t, v in sorted(idf.items())})
# -> {'come': 1.6931, 'duerme': 1.2877, 'el': 1.0, 'gato': 1.2877, 'perro': 1.6931}

def vector(documento):
    """Pesos tf-idf del documento, normalizados a norma 1."""
    cuenta = Counter(documento.split())
    v = {t: cuenta[t] * idf[t] for t in cuenta}     # solo las palabras que estan: vector disperso
    norma = math.sqrt(sum(x ** 2 for x in v.values()))   # norma L2, para comparar largos y cortos
    return {t: round(x / norma, 4) for t, x in v.items()}

def coseno(a, b):
    """Con vectores de norma 1, el coseno es el producto escalar."""
    return sum(v * b.get(t, 0.0) for t, v in a.items())   # get: la palabra ausente vale 0

print("tf-idf doc1:", vector(documentos[0]))
# -> {'el': 0.4813, 'gato': 0.6198, 'duerme': 0.6198}

d1, d2, d3 = (vector(d) for d in documentos)
print("coseno doc1-doc2:", round(coseno(d1, d2), 4),
      "doc1-doc3:", round(coseno(d1, d3), 4),
      "doc2-doc3:", round(coseno(d2, d3), 4))
# -> coseno doc1-doc2: 0.5443 doc1-doc3: 0.5443 doc2-doc3: 0.181
