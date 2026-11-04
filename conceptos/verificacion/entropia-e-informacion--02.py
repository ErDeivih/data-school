import numpy as np
from scipy import stats

# Tabla conjunta: filas llueve (si, no), columnas paraguas (si, no).
conjunta = np.array([[0.40, 0.05],
                     [0.10, 0.45]])
px = conjunta.sum(axis=1, keepdims=True)
py = conjunta.sum(axis=0, keepdims=True)
mi = (conjunta * np.log2(conjunta / (px * py))).sum()

print(f"P(llueve) = {px[0, 0]:.2f}  P(paraguas) = {py[0, 0]:.2f}")   # -> P(llueve) = 0.45  P(paraguas) = 0.50
print(f"informacion mutua = {mi:.4f} bits")                          # -> 0.3973 bits

hx = -(conjunta.sum(axis=1) * np.log2(conjunta.sum(axis=1))).sum()
hy = -(conjunta.sum(axis=0) * np.log2(conjunta.sum(axis=0))).sum()
print(f"H(X) = {hx:.4f}  H(Y) = {hy:.4f}")                           # -> H(X) = 0.9928  H(Y) = 1.0000
print(f"H(X) + H(Y) - MI = {hx + hy - mi:.4f}")                      # -> 1.5955

# La entropia maxima con 8 resultados posibles es log2(8) = 3 bits.
print(f"uniforme 8 simbolos = {stats.entropy(np.full(8, 1 / 8), base=2):.4f} bits")  # -> 3.0000 bits
