import numpy as np

r = np.array([0.03, -0.02, 0.04, -0.05, 0.01, 0.02])
nivel = 0.05
umbral = np.quantile(r, nivel)

var = -umbral
cola = r[r <= umbral]
cvar = -cola.mean()

print(f"cuantil 5 %         {umbral:.4f}")        # -> -0.0425
print(f"VaR 95 % historico  {var:.2%}")          # -> 4.25%
print(f"CVaR 95 %           {cvar:.2%}")         # -> 5.00%
print(f"observaciones en la cola: {cola.size} de {r.size}")   # -> 1 de 6
