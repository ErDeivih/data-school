import numpy as np

# Horas de estudio (x) y nota (y) de 5 alumnos.
x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
y = np.array([4.0, 5.0, 6.0, 8.0, 9.0])

# Minimos cuadrados en forma cerrada: b1 = Sxy / Sxx
xm, ym = x.mean(), y.mean()
b1 = ((x - xm) * (y - ym)).sum() / ((x - xm) ** 2).sum()
b0 = ym - b1 * xm

residuos = y - (b0 + b1 * x)
r2 = 1 - (residuos ** 2).sum() / ((y - ym) ** 2).sum()

print(f"pendiente  {b1:.3f}")
print(f"intercepto {b0:.3f}")
print(f"R2         {r2:.4f}")
print(f"suma de residuos {residuos.sum():.1e}")
print(f"prediccion para x=6: {b0 + b1 * 6:.1f}")
# -> pendiente  1.300
# -> intercepto 2.500
# -> R2         0.9826
# -> suma de residuos 0.0e+00
# -> prediccion para x=6: 10.3
