import numpy as np

# La regularizacion lambda encoge la ganancia: con lambda grande la division no compensa.
g = np.array([-3.0, -1.0, 1.0, 3.0])

def ganancia(gl, hl, gr, hr, lam):
    total = 0.5 * (gl**2 / (hl + lam) + gr**2 / (hr + lam) - g.sum() ** 2 / (4 + lam))
    return total

# El mejor corte separa {1, 2} de {4, 7}: G_L = -4, H_L = 2, G_R = 4, H_R = 2
for lam in (0.0, 4.0, 16.0):
    print(f"lambda {lam:>4.1f}  ganancia del mejor corte  {ganancia(-4.0, 2.0, 4.0, 2.0, lam):.2f}")
# -> lambda  0.0  ganancia del mejor corte  8.00
# -> lambda  4.0  ganancia del mejor corte  2.67
# -> lambda 16.0  ganancia del mejor corte  0.89
