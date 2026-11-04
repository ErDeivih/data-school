from decimal import Decimal, ROUND_HALF_UP

# round() trabaja sobre el binario de debajo y desempata hacia el numero par:
# 2,675 se guarda como 2,67499..., y 0,5 queda justo en medio.
print(f"round(2.675, 2)     {round(2.675, 2)}")      # -> 2.67
print(f"round(0.5) round(1.5)  {round(0.5)} {round(1.5)}")   # -> 0 2

# Decimal respeta los decimales que le escribes y deja elegir el redondeo.
factura = Decimal("2.675").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
print(f"Decimal HALF_UP     {factura}")               # -> 2.68

# Tres lineas de factura tampoco suman exacto en coma flotante.
total = 0.0
for precio in [0.1, 0.2, 0.3]:
    total += precio
print(f"total en float      {total}")                 # -> 0.6000000000000001
print(f"total en Decimal    {sum(Decimal(str(p)) for p in [0.1, 0.2, 0.3])}")   # -> 0.6
