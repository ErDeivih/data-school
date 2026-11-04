import numpy as np

# El factor por capa depende del fan-in: el mismo std no vale para capas de distinto tamano.
for n_in in (64, 256, 1024):
    factor_std_0_01 = np.sqrt(0.5 * n_in * 0.01 ** 2)       # ReLU incluido
    # sqrt porque lo que se compara con 1 es el factor de la DESVIACION, no el de la varianza
    factor_he = np.sqrt(0.5 * n_in * (2 / n_in))
    # :>4 alinea n_in a la derecha en cuatro caracteres, para que las columnas no bailen
    print(f"n_in {n_in:>4}  std 0.01 -> {factor_std_0_01:.4f} por capa   He -> {factor_he:.4f}")
# -> n_in   64  std 0.01 -> 0.0566 por capa   He -> 1.0000
# -> n_in  256  std 0.01 -> 0.1131 por capa   He -> 1.0000
# -> n_in 1024  std 0.01 -> 0.2263 por capa   He -> 1.0000

# Xavier con ReLU: pierde la mitad de la varianza en cada capa
print(f"Xavier con ReLU, 10 capas: {np.sqrt(0.5) ** 10:.4f} de la senal inicial")
# -> Xavier con ReLU, 10 capas: 0.0313 de la senal inicial
