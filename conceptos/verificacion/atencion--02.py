import numpy as np

# La varianza del producto punto crece con d_k: de ahi sale el 1/sqrt(d_k).
rng = np.random.default_rng(0)                 # semilla fija: siempre los mismos numeros
for d in (4, 16, 64, 256):
    q = rng.normal(0, 1, (2000, d))            # 2000 consultas de d dimensiones
    k = rng.normal(0, 1, (2000, d))
    # (q * k) es elemento a elemento; .sum(axis=1) es el producto punto de cada fila.
    print(f"d_k={d:>4}  desviacion tipica {float((q * k).sum(axis=1).std()):>5.2f}"
          f"  sqrt(d_k) {np.sqrt(d):>5.2f}")
    # -> 2.04 y 2.00 ; 3.95 y 4.00 ; 8.10 y 8.00 ; 15.80 y 16.00
