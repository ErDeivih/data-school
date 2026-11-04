import numpy as np

# La derivada decide si la senal sobrevive: es el factor que multiplica al gradiente
z = np.array([-6.0, -2.0, 0.0, 2.0, 6.0])
s = 1.0 / (1.0 + np.exp(-z))
print("derivada sigmoide:", np.round(s * (1 - s), 4))
# -> [0.0025 0.105  0.25   0.105  0.0025]

print("derivada tanh    :", np.round(1 - np.tanh(z) ** 2, 4))
# -> [0.     0.0707 1.     0.0707 0.    ]

# ReLU no satura por arriba: pendiente 1 en toda la zona positiva
# (z > 0) da booleanos y astype(float) los convierte en 0.0 y 1.0
print("derivada relu    :", (z > 0).astype(float))
# -> [0. 0. 0. 1. 1.]

# El producto de las derivadas mide cuanto sobrevive el gradiente al atravesar la pila
# De 0,0025 a 0,105 hay un factor 42: la sigmoide cerca de 0 deja pasar mucho mas
print("minimo de la derivada sigmoide:", round(float((s * (1 - s)).min()), 4))   # -> 0.0025
print("maximo de la derivada sigmoide:", round(float((s * (1 - s)).max()), 4))   # -> 0.25
