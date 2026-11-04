import numpy as np

# Cuanto se contamina un K-fold normal: la comprobacion que justifica la purga.
n = 100
t0 = np.arange(n)
t1 = t0 + 10
prueba = np.arange(40, 60)                      # tercer pliegue de 5
inicio, fin = t0[prueba].min(), t1[prueba].max()

train_normal = np.setdiff1d(np.arange(n), prueba)          # K-fold clasico
contaminado = train_normal[(t1[train_normal] >= inicio) & (t0[train_normal] <= fin)]

print(f"ventana de prueba      [{inicio}, {fin})")
print(f"train clasico          {train_normal.size} observaciones")
print(f"de ellas contaminadas  {contaminado.size}  ({contaminado.size / train_normal.size:.0%})")
print(f"primera y ultima       {contaminado.min()} .. {contaminado.max()}")
