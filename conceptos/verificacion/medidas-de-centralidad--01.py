import numpy as np

salarios = np.array([1800, 1900, 2000, 2100, 2200, 2400, 9000])

print(f"media   {salarios.mean():>8.0f}")     # -> 3057
print(f"mediana {np.median(salarios):>8.0f}")  # -> 2100

# Cuántas personas ganan menos que la media: la media no representa a la mayoría
print("por debajo de la media:", int((salarios < salarios.mean()).sum()), "de", salarios.size)  # -> 6 de 7
