import numpy as np

# Error tipico y margen del 95 % para la media de un tiempo de atencion.
sigma, n = 12.0, 100
error_tipico = sigma / np.sqrt(n)
print(f"error tipico   = {error_tipico:.4f}")          # -> 1.2000
print(f"margen 95 %    = {1.96 * error_tipico:.4f}")   # -> 2.3520

# Cuadruplicar n divide el error tipico entre 2.
print(f"con n = 400    = {sigma / np.sqrt(400):.4f}")  # -> 0.6000
