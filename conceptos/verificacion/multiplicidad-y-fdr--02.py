import numpy as np

# Cien metricas que NO dependen de nada: los p-valores son uniformes por construccion.
rng = np.random.default_rng(0)
p = rng.uniform(0, 1, 100)

print(f"p < 0.05 sin corregir: {(p < 0.05).sum()}")        # -> p < 0.05 sin corregir: 6
print(f"p < 0.05/100:          {(p < 0.05 / 100).sum()}")  # -> p < 0.05/100:          0
print(f"p < 0.05/10:           {(p < 0.05 / 10).sum()}")   # -> p < 0.05/10:           1
print(f"FWER con 100 tests:    {1 - 0.95**100:.4f}")       # -> FWER con 100 tests:    0.9941
