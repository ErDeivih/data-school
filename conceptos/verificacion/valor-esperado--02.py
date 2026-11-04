import numpy as np

# Juego: pagas 2 EUR, ganas 5 EUR solo si sale un 6.
# Beneficio neto: +3 con probabilidad 1/6, -2 con probabilidad 5/6.
beneficios = np.array([3.0, -2.0])
probabilidades = np.array([1 / 6, 5 / 6])

esperado = (beneficios * probabilidades).sum()
print(f"E[beneficio] por tirada = {esperado:.4f} EUR")        # -> -1.1667
print(f"perdida esperada en 100 tiradas = {100 * esperado:.2f} EUR")  # -> -116.67

# Linealidad: sumar dos juegos independientes suma sus esperanzas.
otro = np.array([0.0, 8.0])
print(f"E[X1 + X2] = {(beneficios * probabilidades).sum() + (otro * np.array([0.9, 0.1])).sum():.4f}")  # -> -0.3667
