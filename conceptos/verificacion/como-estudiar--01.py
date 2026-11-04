import numpy as np

# Curva del olvido: R(t) = exp(-t/S). Cada repaso exitoso multiplica S (la fuerza
# de la huella) y por eso el intervalo que aguanta se puede alargar.
dias_repaso = [0, 1, 3, 7, 16]
factor, S0 = 2.2, 8.0

fuerza_final = S0 * factor ** (len(dias_repaso) - 1)
dias_desde_ultimo = 35 - dias_repaso[-1]

print(f"fuerza tras 5 repasos       {fuerza_final:6.1f}")                     # ->  187.4
print(f"retencion el dia 35         {np.exp(-dias_desde_ultimo / fuerza_final):.2f}")  # -> 0.90
print(f"retencion el dia 35 sin nada {np.exp(-35 / S0):.3f}")                  # -> 0.013
