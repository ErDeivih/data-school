import numpy as np

# Variable continua: integramos la densidad para obtener probabilidades.
lam = 0.5                                  # tasa: 0,5 fallos por hora -> media 2 horas
x = np.linspace(0, 2, 20001)
area = np.trapezoid(lam * np.exp(-lam * x), x)

print(f"P(X <= 2) por integral = {area:.4f}")          # -> 0.6321
print(f"1 - exp(-lam * 2)      = {1 - np.exp(-lam * 2):.4f}")   # -> 0.6321
print(f"densidad en x = 2      = {lam * np.exp(-lam * 2):.4f}") # -> 0.1839
print(f"P(X = 2)               = {0.0:.4f}")            # -> 0.0000
