import numpy as np

# Decaimiento de pesos: sin gradiente, solo el factor (1 - eta*lambda) por paso.
eta = 0.1
for lam in (0.01, 0.1):
    # {lam:<5} alinea a la izquierda en 5 caracteres: sin eso las dos lineas salen desalineadas
    print(f"lambda {lam:<5} factor por paso {1 - eta * lam:.4f}  tras 1000 pasos {(1 - eta * lam) ** 1000:.3f}")
# -> lambda 0.01  factor por paso 0.9990  tras 1000 pasos 0.368
# -> lambda 0.1   factor por paso 0.9900  tras 1000 pasos 0.000
