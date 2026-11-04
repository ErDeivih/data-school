import numpy as np

# El mismo modelo aplicado a tres planes hasta un examen el dia 30. Es un modelo,
# no una medida: compara planes, no predice tu nota.
def retencion(dia_examen, repasos, S0=8.0, factor=2.2):
    fuerza = S0 * factor ** (len(repasos) - 1)      # cada repaso multiplica la fuerza
    return np.exp(-(dia_examen - repasos[-1]) / fuerza)

print(f"plan A (solo el dia 1)         {retencion(30, [1]):.3f}")                  # -> 0.027
print(f"plan B (dias 1, 2, 4 y 8)      {retencion(30, [1, 2, 4, 8]):.3f}")          # -> 0.772
print(f"plan C (dias 1, 2, 4, 8, 16, 30) {retencion(30, [1, 2, 4, 8, 16, 30]):.3f}")  # -> 1.000
