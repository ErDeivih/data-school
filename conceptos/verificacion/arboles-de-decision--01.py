import numpy as np

def gini(conteos):
    p = np.asarray(conteos, dtype=float)
    p = p / p.sum()
    return 1 - (p ** 2).sum()

def entropia(conteos):
    c = np.asarray(conteos, dtype=float)
    p = c[c > 0] / c.sum()
    return -(p * np.log2(p)).sum() + 0.0

for conteos in ([6, 6], [2, 4], [1, 5], [0, 6]):
    print(f"nodo {str(conteos):<9} gini {gini(conteos):.4f}  entropia {entropia(conteos):.4f}")
# -> nodo [6, 6]    gini 0.5000  entropia 1.0000
# -> nodo [2, 4]    gini 0.4444  entropia 0.9183
# -> nodo [1, 5]    gini 0.2778  entropia 0.6500
# -> nodo [0, 6]    gini 0.0000  entropia 0.0000
