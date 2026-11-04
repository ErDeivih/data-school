import math

# BM25 de "gato" en tres documentos. k1 controla la saturacion; b, la longitud.
documentos = {
    "d1": "el gato come pescado y el gato duerme",
    "d2": "el perro come pienso",
    "d3": "el gato y el perro duermen",
}
termino, k1, b = "gato", 1.2, 0.75

largos = {doc: len(texto.split()) for doc, texto in documentos.items()}
medio = sum(largos.values()) / len(largos)
N = len(documentos)
df = sum(1 for texto in documentos.values() if termino in texto.split())
idf = math.log(1 + (N - df + 0.5) / (df + 0.5))       # version suavizada del IDF

print("largo medio: {:.2f}  df: {}  idf: {:.4f}".format(medio, df, idf))
for doc, texto in documentos.items():
    f = texto.split().count(termino)
    score = idf * (f * (k1 + 1)) / (f + k1 * (1 - b + b * largos[doc] / medio))
    print("{:<3} f={} largo={}  BM25={:.4f}".format(doc, f, largos[doc], score))
# idf = 0.4700; d1 f=2 largo=8 BM25=0.5909; d2 BM25=0.0000; d3 f=1 BM25=0.4700
