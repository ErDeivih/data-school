import numpy as np

# Entropia cruzada de una etiqueta correcta segun la probabilidad que le asigna el modelo.
for q in (0.99, 0.5, 0.01):
    print(f"q(correcta) = {q:<5} coste = {-np.log2(q):.4f} bits")

# Si el modelo da probabilidad cero a algo que ocurre, la KL es infinita.
from scipy import stats
print(f"KL con soporte imposible = {stats.entropy([0.5, 0.5], [1.0, 0.0], base=2)}")  # -> inf
