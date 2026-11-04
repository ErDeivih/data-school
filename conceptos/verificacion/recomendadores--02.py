import numpy as np

def ndcg(relevancia):
    """Ganancia acumulada descontada, normalizada por el orden ideal."""
    r = np.asarray(relevancia, float)
    dcg = ((2 ** r - 1) / np.log2(np.arange(2, r.size + 2))).sum()   # descuento log2(2), log2(3)...
    ideal = np.sort(r)[::-1]                                        # el mejor orden posible
    idcg = ((2 ** ideal - 1) / np.log2(np.arange(2, ideal.size + 2))).sum()
    return dcg / idcg

# Dos ordenaciones de los mismos cuatro articulos. La relevancia va de 3 (perfecto) a 0.
for lista in ([3, 0, 2, 1], [2, 0, 3, 1]):
    precision2 = sum(1 for r in lista[:2] if r > 0) / 2
    print(lista, "precision@2", round(precision2, 2), "NDCG@4", round(float(ndcg(lista)), 4))
# -> [3, 0, 2, 1] precision@2 0.5 NDCG@4 0.9508
# -> [2, 0, 3, 1] precision@2 0.5 NDCG@4 0.7379
