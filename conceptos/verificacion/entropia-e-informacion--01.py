import numpy as np
from scipy import stats

# Moneda sesgada: la entropia es la sorpresa media, en bits.
for p in (0.5, 0.9, 0.99):
    print(f"moneda p={p:<5} H = {stats.entropy([p, 1 - p], base=2):.4f} bits")

# scipy.stats.entropy(p, q) devuelve la divergencia KL; la cruzada es H(p) + KL(p; q).
p = np.array([0.7, 0.3])     # distribucion real
q = np.array([0.5, 0.5])     # modelo, plano
print(f"H(p)    = {stats.entropy(p, base=2):.4f}")                                # -> 0.8813
print(f"KL(p;q) = {stats.entropy(p, q, base=2):.4f}")                            # -> 0.1187
print(f"CE(p;q) = {stats.entropy(p, base=2) + stats.entropy(p, q, base=2):.4f}")  # -> 1.0000
print(f"KL(q;p) = {stats.entropy(q, p, base=2):.4f}")                            # -> 0.1258
