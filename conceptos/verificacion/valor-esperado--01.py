import numpy as np

# X es el resultado de un dado; Y = X, asi que son perfectamente dependientes.
x = np.arange(1, 7, dtype=float)
y = x.copy()

print(f"E[X]     = {x.mean():.4f}")               # -> 3.5000
print(f"E[X*Y]   = {(x * y).mean():.4f}")         # -> 15.1667
print(f"E[X]E[Y] = {x.mean() * y.mean():.4f}")    # -> 12.2500

# La linealidad no necesita independencia: se comprueba valor a valor.
print(f"E[3X + 10] = {(3 * x + 10).mean():.4f}")  # -> 20.5000
print(f"3E[X] + 10 = {3 * x.mean() + 10:.4f}")    # -> 20.5000
