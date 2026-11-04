import numpy as np

# La d es una estimacion: con pocos datos su intervalo de confianza es enorme.
# Error tipico aproximado de d: raiz(1/n1 + 1/n2 + d^2 / (2*(n1+n2))).
def d_con_intervalo(a, b):
    n1, n2 = a.size, b.size
    sp = np.sqrt(((n1 - 1) * a.var(ddof=1) + (n2 - 1) * b.var(ddof=1)) / (n1 + n2 - 2))
    d = (a.mean() - b.mean()) / sp
    ee = np.sqrt(1 / n1 + 1 / n2 + d**2 / (2 * (n1 + n2)))
    return d, 1.96 * ee

rng = np.random.default_rng(3)                   # el efecto real de la simulacion es d = 0.55
for n in (8, 200):
    a = rng.normal(0.55, 1.0, n)
    b = rng.normal(0.00, 1.0, n)
    d, margen = d_con_intervalo(a, b)
    print(f"n={n:>4}  d={d:+.2f}  IC95% [{d - margen:+.2f}, {d + margen:+.2f}]")
    # -> n=   8  d=+0.08  IC95% [-0.90, +1.06]
    # -> n= 200  d=+0.55  IC95% [+0.35, +0.75]
