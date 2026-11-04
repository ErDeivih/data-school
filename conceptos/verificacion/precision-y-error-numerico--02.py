import math

# Acumular en un float: cada suma vuelve a redondear sobre un total que crece.
acumulado = 0.0
for _ in range(10):
    acumulado += 0.1
print(f"diez veces 0,1     {acumulado}")            # -> 0.9999999999999999
print(f"error absoluto     {acumulado - 1.0:.2e}")  # -> -1.11e-16

# Con magnitudes muy distintas, el sumando pequeno desaparece sin avisar.
ingenuo = 0.0
for valor in [1e16] + [1.0] * 10:
    ingenuo += valor
print(f"suma ingenua       {ingenuo:.0f}")          # -> 10000000000000000
print(f"math.fsum          {math.fsum([1e16] + [1.0] * 10):.0f}")   # -> 10000000000000010
