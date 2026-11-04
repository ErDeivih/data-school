import numpy as np

rng = np.random.default_rng(0)
grupo_a = rng.normal(0.30, 1.0, size=120)     # efecto real pequeno
grupo_b = rng.normal(0.00, 1.0, size=120)
todos = np.concatenate([grupo_a, grupo_b])
etiquetas = np.array([1] * 120 + [0] * 120)
observado = grupo_a.mean() - grupo_b.mean()

# Barajamos las etiquetas B veces: asi se genera la distribucion nula
B = 5000
extremos = 0
for _ in range(B):
    rng.shuffle(etiquetas)
    diferencia = todos[etiquetas == 1].mean() - todos[etiquetas == 0].mean()
    extremos += abs(diferencia) >= abs(observado)

# El +1 en numerador y denominador incluye el reparto observado: nunca da cero
print(f"diferencia observada  {observado:.4f}")              # -> 0.5073
print(f"permutaciones extremas {extremos} de {B}")          # -> 0 de 5000
print(f"p-valor Monte Carlo   {(extremos + 1) / (B + 1):.4f}")  # -> 0.0002
