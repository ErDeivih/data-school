import numpy as np

# Cinco viviendas: precio real y prediccion, en miles de euros
real = np.array([100.0, 150.0, 200.0, 250.0, 300.0])
pred = np.array([110.0, 140.0, 210.0, 240.0, 320.0])

error = real - pred                      # residuos con signo
# .mean() de un array de NumPy divide entre n (no entre n-1): para un error medio es lo
# que se quiere. np.abs se aplica elemento a elemento antes de promediar.
mae = np.abs(error).mean()
rmse = np.sqrt((error ** 2).mean())      # error ** 2 tambien es elemento a elemento
# Aqui se divide cada error entre SU valor real, y solo despues se promedian los cocientes.
mape = (np.abs(error) / real).mean()
# SS_res = suma de los residuos al cuadrado; SS_tot = variabilidad respecto a la media.
r2 = 1 - (error ** 2).sum() / ((real - real.mean()) ** 2).sum()

print(f"MAE  {mae:.4f}")    # -> 12.0000
print(f"MSE  {(error ** 2).mean():.4f}")   # -> 160.0000
print(f"RMSE {rmse:.4f}")   # -> 12.6491
print(f"MAPE {mape:.4f}")   # -> 0.0647
print(f"R2   {r2:.4f}")     # -> 0.9680
