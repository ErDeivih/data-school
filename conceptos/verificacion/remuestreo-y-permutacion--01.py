import itertools
import numpy as np

a = np.array([12, 14, 16])
b = np.array([20, 22, 24])
todos = np.concatenate([a, b])
observado = a.mean() - b.mean()

# Enumeramos las C(6,3) = 20 formas de repartir los seis valores en grupos de tres
extremos = 0
for indice in itertools.combinations(range(6), 3):
    grupo = todos[list(indice)]
    resto = np.delete(todos, list(indice))
    if abs(grupo.mean() - resto.mean()) >= abs(observado) - 1e-9:
        extremos += 1

print(f"diferencia observada  {observado:.1f}")            # -> -8.0
print(f"repartos extremos     {extremos} de 20")           # -> 2 de 20
print(f"p-valor exacto        {extremos / 20:.2f}")        # -> 0.10
