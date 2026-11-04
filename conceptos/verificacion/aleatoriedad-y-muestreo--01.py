# Generador congruencial lineal: x_{n+1} = (a * x_n + c) mod m
a, c, m = 5, 3, 16
x = 1
secuencia = []
for _ in range(16):
    x = (a * x + c) % m
    secuencia.append(x)

print("secuencia:", secuencia)
print("valores distintos:", len(set(secuencia)))          # -> 16
print("el ultimo vuelve a la semilla:", secuencia[-1] == 1)  # -> True
