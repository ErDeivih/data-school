import numpy as np

horas = np.array([1, 2, 3, 4, 5, 6], dtype=float)
notas = np.array([4.0, 4.5, 5.0, 6.0, 7.0, 8.5])

cov = np.cov(horas, notas, ddof=1)[0, 1]
print(f"covarianza  = {cov:.4f}")                          # -> 3.1000
print(f"correlacion = {np.corrcoef(horas, notas)[0, 1]:.4f}")  # -> 0.9787

# Cambiar de unidades multiplica la covarianza pero deja la correlacion intacta.
notas_nuevas = notas * 100 + 5
print(f"cov * 100   = {np.cov(horas, notas_nuevas, ddof=1)[0, 1]:.2f}")       # -> 310.00
print(f"corr igual  = {np.corrcoef(horas, notas_nuevas)[0, 1]:.4f}")         # -> 0.9787
