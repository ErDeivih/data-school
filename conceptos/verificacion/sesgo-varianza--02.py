import numpy as np

# Un solo conjunto: la brecha entre entrenamiento y validacion es la varianza
rng = np.random.default_rng(5)
x = np.linspace(0, 1, 40)
y = np.sin(2 * np.pi * x) + rng.normal(0, 0.3, x.size)

# Validacion entrelazada: uno de cada cinco puntos, repartidos por todo el rango
validacion = np.arange(x.size) % 5 == 4
x_tr, y_tr = x[~validacion], y[~validacion]
x_va, y_va = x[validacion], y[validacion]

print("grado  error train  error validacion")
for g in range(1, 13):
    coef = np.polyfit(x_tr, y_tr, g)
    e_tr = np.sqrt(np.mean((y_tr - np.polyval(coef, x_tr)) ** 2))
    e_va = np.sqrt(np.mean((y_va - np.polyval(coef, x_va)) ** 2))
    print("%5d  %11.3f  %16.3f" % (g, e_tr, e_va))
# ->     5        0.222             0.276
# ->    10        0.198             1.040
# El minimo de validacion esta en los grados 5 y 6; a partir de ahi, la brecha crece
print("desviacion del ruido 0.30")
print("puntos: %d entrenamiento, %d validacion" % (x_tr.size, x_va.size))
# -> puntos: 32 entrenamiento, 8 validacion
