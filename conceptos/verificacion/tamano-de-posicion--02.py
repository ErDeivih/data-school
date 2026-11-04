import numpy as np

# Volatilidad de una cartera con N posiciones iguales, volatilidad sigma y
# correlacion media rho entre todos los pares.
sigma = 0.25
print("  N     rho=0.0    rho=0.3    rho=0.7")
for n in (1, 5, 10, 20):
    fila = [sigma * np.sqrt(1 / n + rho * (n - 1) / n) for rho in (0.0, 0.3, 0.7)]
    print(f"{n:>3}  " + "  ".join(f"{v:>9.2%}" for v in fila))
# ->   1     25.00%     25.00%     25.00%
# ->  10      7.91%     15.21%     21.36%
