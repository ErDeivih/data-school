import math

# Dos variantes de una pagina: 50 y 56 conversiones sobre 1.000 visitas cada una.
n_a, x_a = 1000, 50
n_b, x_b = 1000, 56
p_a, p_b = x_a / n_a, x_b / n_b
diferencia = p_b - p_a

# Error tipico de la diferencia de dos proporciones independientes.
se = math.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)
z = diferencia / se
p_valor = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / math.sqrt(2))))

print(f"conversion A {p_a:.3%}  B {p_b:.3%}")   # -> conversion A 5.000%  B 5.600%
print(f"diferencia {diferencia:.4f} = {diferencia * 100:.2f} puntos")  # -> diferencia 0.0060 = 0.60 puntos
print(f"error tipico {se:.4f}")                # -> error tipico 0.0100
print(f"z {z:.2f}  p {p_valor:.3f}")           # -> z 0.60  p 0.549
print(f"IC 95%  [{diferencia - 1.96 * se:+.4f}, {diferencia + 1.96 * se:+.4f}]")
