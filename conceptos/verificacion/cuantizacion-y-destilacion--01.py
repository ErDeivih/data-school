import numpy as np

rng = np.random.default_rng(0)
w = rng.normal(0, 0.05, size=1024)      # los pesos de una capa, en float32


def cuantiza(w, bits):
    qmax = 2 ** (bits - 1) - 1
    escala = np.abs(w).max() / qmax     # escala simetrica respecto a cero
    return np.clip(np.round(w / escala), -qmax - 1, qmax) * escala


for bits in (8, 4, 3):
    error = np.sqrt(((w - cuantiza(w, bits)) ** 2).mean())
    print(f"{bits} bits  error cuadratico medio={error:.5f}"
          f"  relativo a la desviacion={error / w.std():.2%}")
# -> 8 bits  error cuadratico medio=0.00045  relativo a la desviacion=0.92%
# -> 4 bits  error cuadratico medio=0.00816  relativo a la desviacion=16.79%
# -> 3 bits  error cuadratico medio=0.01860  relativo a la desviacion=38.27%

# La misma cuantizacion de 4 bits, pero con una escala por canal de 256 pesos.
por_canal = np.concatenate([cuantiza(c, 4) for c in w.reshape(4, -1)])
print(f"4 bits por tensor={np.sqrt(((w - cuantiza(w, 4)) ** 2).mean()):.5f}"
      f"  4 bits por canal={np.sqrt(((w - por_canal) ** 2).mean()):.5f}")
# -> 4 bits por tensor=0.00816  4 bits por canal=0.00662
