import math

# La misma regla, hacia atrás: retropropagación en una red de dos capas.
# z1 = x*w1, a1 = sigmoide(z1), z2 = a1*w2, L = (y - z2)**2/2  (error cuadrático)
def sigmoide(u):
    return 1 / (1 + math.exp(-u))

x, y = 0.5, 1.0
w1, w2 = 0.8, -0.6

z1, a1, z2 = x * w1, None, None
a1 = sigmoide(z1)
z2 = a1 * w2
L = 0.5 * (y - z2) ** 2

# dL/dz2 -> dL/da1 -> dL/dz1 -> dL/dw1 : cada paso multiplica por la derivada local
dL_dz2 = -(y - z2)
dL_dw2 = dL_dz2 * a1
dL_da1 = dL_dz2 * w2
dL_dz1 = dL_da1 * a1 * (1 - a1)
dL_dw1 = dL_dz1 * x

print("L       ", round(L, 4))          # salida: 0.9237
print("dL/dw2  ", round(dL_dw2, 4))     # salida: -0.8137
print("dL/dw1  ", round(dL_dw1, 4))     # salida: 0.098
