# Descenso de gradiente sobre f(x) = (x - 3)^2, cuyo minimo esta en x = 3.
x = 0.0
for _ in range(20):
    x = x - 0.1 * 2 * (x - 3)   # 0.1 es la tasa de aprendizaje; 2(x-3) es la derivada

print("x tras 20 pasos:", round(x, 6))            # -> 2.965412
print("valor de f(x)  :", round((x - 3) ** 2, 10))   # -> 0.0011963052
