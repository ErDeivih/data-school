import numpy as np

# Relevancia graduada: 0 = nada, 1 = util, 2 = bueno, 3 = perfecto
def dcg(grados, k=None):
    g = np.asarray(grados[:k], dtype=float)
    # np.arange(2, ...) porque el descuento de la posicion i es log2(i + 1): la
    # primera posicion se divide entre log2(2) = 1, o sea que no se descuenta.
    descuento = 1.0 / np.log2(np.arange(2, g.size + 2))
    return float((((2 ** g) - 1) * descuento).sum())

bueno = [3, 2, 0, 1]
malo = [0, 1, 3, 2]
ideal = sorted(bueno, reverse=True)   # el mejor orden posible con esos mismos grados

print(f"DCG bueno {dcg(bueno):.4f}")                 # -> 9.3235
print(f"IDCG      {dcg(ideal):.4f}")                 # -> 9.3928
print(f"NDCG bueno {dcg(bueno) / dcg(ideal):.4f}")   # -> 0.9926
print(f"NDCG malo  {dcg(malo) / dcg(ideal):.4f}")    # -> 0.5774
print(f"DCG@2 bueno {dcg(bueno, k=2):.4f}")          # -> 8.8928
