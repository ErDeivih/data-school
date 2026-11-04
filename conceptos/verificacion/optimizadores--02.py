import numpy as np

# Correccion de sesgo de Adam: sin ella el primer paso es 3.16 veces eta, porque las
# medias arrancan en cero (0.1 / sqrt(0.001) = 3.16).
g = 2.0
m, v = 0.1 * g, 0.001 * g ** 2
print(f"sin corregir  {m / np.sqrt(v):.4f}")            # -> sin corregir  3.1623
mh, vh = m / (1 - 0.9), v / (1 - 0.999)                 # 1 - beta**t con t = 1
print(f"corregido     {mh / np.sqrt(vh):.4f}")          # -> corregido     1.0000

# Con la correccion, el primer paso mide eta en cualquier direccion: el gradiente
# se normaliza y solo importa su signo.
print(f"paso en x  {0.05 * mh / (np.sqrt(vh) + 1e-8):.4f}")   # -> paso en x  0.0500
