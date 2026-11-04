import numpy as np

p = np.array([0.0001, 0.0008, 0.0021, 0.0043, 0.0067, 0.0091, 0.0122, 0.0180,
              0.0245, 0.0301, 0.0410, 0.0520, 0.0680, 0.0900, 0.1200, 0.1800,
              0.2400, 0.3100, 0.4500, 0.6200])
alfa, m = 0.05, p.size

# Bonferroni: umbral por contraste alfa/m. Benjamini-Hochberg: se compara el
# p-valor ordenado i con alfa*i/m y se rechazan los i primeros que cumplen.
orden = np.argsort(p)
pasa = p[orden] <= alfa * np.arange(1, m + 1) / m
k_max = (np.max(np.where(pasa)[0]) + 1) if pasa.any() else 0

print(f"m={m} contrastes, alfa={alfa}")                          # -> 20 y 0.05
print(f"sin ajustar: {int((p <= alfa).sum())}")                  # -> 11
print(f"Bonferroni : {int((p <= alfa / m).sum())}")              # -> 3
print(f"Benjamini-Hochberg: {k_max}")                            # -> 8
