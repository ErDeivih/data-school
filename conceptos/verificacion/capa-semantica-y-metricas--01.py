import numpy as np

visitas = np.array([50, 400, 250])
pedidos = np.array([12, 20, 25])

# Correcto: se agregan las componentes y se divide una sola vez
total = pedidos.sum() / visitas.sum() * 100
# Incorrecto: se promedian ratios ya calculados. Cada dia pesa igual, tenga 50 o 400 visitas
media = (pedidos / visitas).mean() * 100

print(f"ratio del total   {total:.2f} %")    # -> 8.14
print(f"media de ratios   {media:.2f} %")    # -> 13.00
print(f"sobreestima       {media / total:.2f} veces")   # -> 1.60
