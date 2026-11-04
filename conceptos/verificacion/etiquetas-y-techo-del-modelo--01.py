import numpy as np

rng = np.random.default_rng(0)
C, n = 10, 200_000
y = rng.integers(0, C, n)                                       # etiqueta verdadera
acierta = rng.random(n) < 0.90                                  # el modelo acierta el 90 %
y_pred = np.where(acierta, y, (y + rng.integers(1, C, n)) % C)  # cuando falla, cae en otra clase

rho = 0.20                                                      # 20 % de etiquetas cambiadas al azar
cambiada = rng.random(n) < rho
y_ruidosa = np.where(cambiada, rng.integers(0, C, n), y)

medida = (y_pred == y_ruidosa).mean()
real = (y_pred == y).mean()
corregida = (medida - rho / C) / (1 - rho)

print(f"exactitud real      {real:.4f}")       # -> 0.9010
print(f"exactitud medida    {medida:.4f}")     # -> 0.7411
print(f"exactitud corregida {corregida:.4f}")  # -> 0.9014
