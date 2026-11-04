import math

# La suma mas famosa de la informatica: 0,1 y 0,2 no se guardan exactos, y el
# resultado se redondea al flotante mas cercano.
print(f"0.1 + 0.2          {0.1 + 0.2}")            # -> 0.30000000000000004
print(f"igual que 0.3      {0.1 + 0.2 == 0.3}")     # -> False
print(f"diferencia         {0.1 + 0.2 - 0.3:.2e}")  # -> 5.55e-17
print(f"con tolerancia     {math.isclose(0.1 + 0.2, 0.3)}")   # -> True
print(f"epsilon maquina    {2.0 ** -52:.2e}")       # -> 2.22e-16
