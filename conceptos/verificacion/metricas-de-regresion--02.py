import numpy as np

# Un unico error grande dispara el RMSE y apenas mueve el MAE
errores = np.array([1.0, 1.0, 1.0, 1.0, 10.0])
print(f"MAE  {np.abs(errores).mean():.3f}")            # -> 2.800
print(f"RMSE {np.sqrt((errores ** 2).mean()):.3f}")    # -> 4.561

# El R2 puede ser negativo: aqui el modelo predice 50 para todo y la serie va de 10 a 50
real = np.array([10.0, 20.0, 30.0, 40.0, 50.0])
# np.full(5, 50.0) es un array de cinco 50.0: el «predictor constante» mas tonto posible.
pred = np.full(5, 50.0)
r2 = 1 - ((real - pred) ** 2).sum() / ((real - real.mean()) ** 2).sum()
print(f"R2 de un predictor constante {r2:.1f}")        # -> -2.0
