import numpy as np

r = np.array([0.03, -0.02, 0.04, -0.05, 0.01, 0.02])
objetivo = 0.0                                   # T: rentabilidad minima aceptable, mensual
exceso = r - objetivo

vol_total = exceso.std(ddof=1)
bajista_n = np.sqrt((np.minimum(exceso, 0) ** 2).sum() / exceso.size)      # divide entre n
bajista_k = np.sqrt((np.minimum(exceso, 0) ** 2).sum() / (exceso < 0).sum())  # entre negativos
raiz = np.sqrt(12)

print(f"volatilidad         {vol_total:.4f}")                       # -> 0.0339
print(f"bajista (n = {exceso.size})    {bajista_n:.4f}")            # -> 0.0220
print(f"bajista (k = {(exceso < 0).sum()})    {bajista_k:.4f}")      # -> 0.0381
print(f"Sharpe anual        {exceso.mean() / vol_total * raiz:.2f}")        # -> 0.51
print(f"Sortino anual / n   {exceso.mean() / bajista_n * raiz:.2f}")         # -> 0.79
print(f"Sortino anual / k   {exceso.mean() / bajista_k * raiz:.2f}")         # -> 0.45
