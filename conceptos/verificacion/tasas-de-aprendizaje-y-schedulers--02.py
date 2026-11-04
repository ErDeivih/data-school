import numpy as np

# En f(theta) = theta^2 con paso theta <- theta - eta*2*theta, el error se multiplica
# por (1 - 2*eta) en cada iteracion: con eta > 1 el factor supera 1 en valor absoluto.
for eta in (0.1, 0.5, 1.1):
    theta = 1.0
    for _ in range(10):
        theta = theta - eta * 2 * theta
    # {eta:<4} alinea a la izquierda y {:+.1f} fuerza el signo: asi se ve el factor 0.0 y el -1.2
    print(f"eta {eta:<4} factor por paso {1 - 2 * eta:+.1f}  theta tras 10 pasos {theta:+.6f}")
# -> eta 0.1  factor por paso +0.8  theta tras 10 pasos +0.107374
# -> eta 0.5  factor por paso +0.0  theta tras 10 pasos +0.000000
# -> eta 1.1  factor por paso -1.2  theta tras 10 pasos +6.191736
