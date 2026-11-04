import numpy as np

# Termino KL de un VAE gaussiano: 0.5 * (mu^2 + sigma^2 - 1 - log sigma^2), sumado por dimension.
def kl(mu, log_var):
    # El codificador devuelve log_var, no sigma: exp() lo convierte en la varianza. Se guarda
    # en logaritmo porque asi nunca puede salir negativa y el gradiente no se dispara.
    return float(0.5 * np.sum(mu ** 2 + np.exp(log_var) - 1.0 - log_var))

print("mu=0, log_var= 0:", round(kl(np.array([0.0]), np.array([0.0])), 4))    # -> 0.0
print("mu=1, log_var= 0:", round(kl(np.array([1.0]), np.array([0.0])), 4))    # -> 0.5
print("mu=2, log_var= 0:", round(kl(np.array([2.0]), np.array([0.0])), 4))    # -> 2.0
print("mu=0, log_var=-3:", round(kl(np.array([0.0]), np.array([-3.0])), 4))   # -> 1.0249
print("mu=0, log_var= 3:", round(kl(np.array([0.0]), np.array([3.0])), 4))    # -> 8.0428
print("sigma:", round(float(np.exp(-3.0 / 2)), 3), round(float(np.exp(3.0 / 2)), 3))  # -> 0.223 4.482
