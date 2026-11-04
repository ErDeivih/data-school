import numpy as np

n = 53                       # el calculo anterior redondeado hacia arriba
abandono = 0.15              # esperamos perder un 15 % de los sujetos

print(f"reclutar por grupo {np.ceil(n / (1 - abandono)):.0f}")   # -> reclutar por grupo 63

# Diseno por conglomerados: 20 usuarios por tienda y correlacion intraclase 0,05.
m, rho = 20, 0.05
deff = 1 + (m - 1) * rho
print(f"efecto de diseno {deff:.2f}  n necesario {n * deff:.0f}")
# -> efecto de diseno 1.95  n necesario 103
