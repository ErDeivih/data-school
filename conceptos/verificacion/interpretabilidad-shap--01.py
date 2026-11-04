import itertools
from math import factorial
import numpy as np

# Juego cooperativo de 3 variables: v(S) es lo que predice el modelo usando solo S.
# Con 3 variables hay 8 coaliciones, asi que el valor de Shapley se calcula exacto.
v = {(): 0.0, ("a",): 1.0, ("b",): 2.0, ("c",): 3.0,
     ("a", "b"): 4.0, ("a", "c"): 5.5, ("b", "c"): 6.0, ("a", "b", "c"): 8.0}
todos = ("a", "b", "c")

def shapley(j, v, todos):
    total = 0.0
    for r in range(len(todos)):
        for S in itertools.combinations([k for k in todos if k != j], r):
            peso = factorial(r) * factorial(len(todos) - r - 1) / factorial(len(todos))
            total += peso * (v[tuple(sorted(S + (j,)))] - v[tuple(sorted(S))])
    return total

phi = {j: shapley(j, v, todos) for j in todos}
for j in todos:
    print(f"phi_{j} = {phi[j]:+.3f}")
print("suma =", round(sum(phi.values()), 3), " v(todos) =", v[todos])
# -> phi_a = +1.750
# -> phi_b = +2.500
# -> phi_c = +3.750
# -> suma = 8.0  v(todos) = 8.0
