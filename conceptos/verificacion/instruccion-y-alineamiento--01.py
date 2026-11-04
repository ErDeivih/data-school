import numpy as np

# Modelo de recompensa de Bradley-Terry: sigma(r_ganadora - r_perdedora)
sigma = lambda z: 1 / (1 + np.exp(-z))   # funcion logistica: lleva cualquier diferencia a [0, 1]

pares = [(1.2, 0.3), (0.4, 0.5), (2.0, -0.5)]
for rw, rl in pares:                     # desempaqueta cada tupla en las dos puntuaciones
    print(f"r ganadora {rw:+.1f}  r perdedora {rl:+.1f}  P(preferir) = {sigma(rw - rl):.3f}")
# -> 0.711, 0.475 y 0.924 en las tres lineas

# En RLHF el objetivo es recompensa menos una penalizacion por alejarse del modelo base
recompensa, kl, beta = 1.2, 2.0, 0.05
print(f"objetivo {recompensa - beta * kl:.3f}  (recompensa {recompensa} menos {beta * kl:.2f} de KL)")
# -> objetivo 1.100  (recompensa 1.2 menos 0.10 de KL)
