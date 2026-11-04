import numpy as np

# Barajar solo cambia el orden, no el conjunto: el total no se mueve nunca.
rs = np.array([2.0, 1.0, -1.0, 3.0, -1.0, 1.0, -1.0, 2.0, -1.0, 1.0])
rng = np.random.default_rng(1)

def caida_maxima(curva):
    picos = np.maximum.accumulate(curva)
    return float(((picos - curva) / picos).max())

original = np.cumprod(1 + 0.02 * rs)
dds = [caida_maxima(np.cumprod(1 + 0.02 * rng.permutation(rs))) for _ in range(20_000)]

print(f"total original  {original[-1] - 1:+.4%}")      # -> +12.2218%
print(f"caida real      {caida_maxima(original):.2%}")  # -> 2.04%
print(f"caida mediana   {np.median(dds):.2%}")          # -> 3.96%
print(f"peor de 20.000  {np.max(dds):.2%}")             # -> 7.76%
