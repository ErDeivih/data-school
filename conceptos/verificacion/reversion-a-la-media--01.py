import numpy as np

rng = np.random.default_rng(0)
n = 3000
rho, sigma = 0.9, 0.01
x = np.zeros(n)
for t in range(1, n):
    x[t] = rho * x[t - 1] + rng.normal(0, sigma)

# Estimacion de x_t = a + rho * x_{t-1} por minimos cuadrados
X = np.column_stack([np.ones(n - 1), x[:-1]])
coef, *_ = np.linalg.lstsq(X, x[1:], rcond=None)
rho_hat = coef[1]
vida_media = -np.log(2) / np.log(rho_hat)

print("rho estimado    %.4f" % rho_hat)
print("vida media      %.2f periodos" % vida_media)
print("mitad en 1 paso %.4f" % (1 - rho_hat))
# -> rho estimado    0.8978
# -> vida media      6.43 periodos
# -> mitad en 1 paso 0.1022
