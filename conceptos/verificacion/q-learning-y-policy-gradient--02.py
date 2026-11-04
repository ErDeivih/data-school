import numpy as np

premios = np.array([2.0, 0.5])    # recompensa esperada de la accion buena y de la mala


def valor(theta):
    p = 1 / (1 + np.exp(-theta))  # probabilidad de elegir la accion buena
    return p * premios[0] + (1 - p) * premios[1]


theta, h = 0.5, 1e-6
p = 1 / (1 + np.exp(-theta))
analitica = p * (1 - p) * (premios[0] - premios[1])
numerica = (valor(theta + h) - valor(theta - h)) / (2 * h)

rng = np.random.default_rng(0)
muestras = 200000
a = np.where(rng.random(muestras) < p, 0, 1)   # 0 = accion buena, con probabilidad p
grad_log = np.where(a == 0, 1 - p, -p)         # d/dtheta log pi(a)
print(f"analitico {analitica:.4f}  numerico {numerica:.4f}"
      f"  REINFORCE {(premios[a] * grad_log).mean():.4f}")
# -> analitico 0.3525  numerico 0.3525  REINFORCE 0.3539
