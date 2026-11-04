import numpy as np

# La ganancia de XGBoost, calculada a mano sobre cuatro residuos.
x = np.array([1.0, 2.0, 4.0, 7.0])
g = np.array([-3.0, -1.0, 1.0, 3.0])   # primeras derivadas (gradiente)
h = np.ones(4)                          # hessianas: 1 con perdida cuadratica
lam = 0.0

def ganancia(corte):
    izq, der = x <= corte, x > corte
    gl, hl = g[izq].sum(), h[izq].sum()
    gr, hr = g[der].sum(), h[der].sum()
    padre = g.sum() ** 2 / (h.sum() + lam)
    return 0.5 * (gl**2 / (hl + lam) + gr**2 / (hr + lam) - padre)

for corte in (1.5, 3.0, 5.5):
    print(f"corte x <= {corte:>3.1f}  ganancia {ganancia(corte):.1f}")
# -> corte x <= 1.5  ganancia 6.0
# -> corte x <= 3.0  ganancia 8.0
# -> corte x <= 5.5  ganancia 6.0
