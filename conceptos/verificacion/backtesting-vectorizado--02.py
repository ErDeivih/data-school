import numpy as np

# El NaN del shift no da error: envenena la serie entera y la curva sale vacia.
# Aqui la posicion es larga-corta (+1 / -1), asi que la rotacion es el doble que en 0/1.
ret = np.array([0.02, -0.0098, 0.0396, -0.019, 0.0291, 0.0189])
posicion = np.array([np.nan, 1.0, -1.0, 1.0, -1.0, 1.0])

print("con NaN    ", np.round(np.cumsum(posicion * ret), 4).tolist())
# -> [nan, nan, nan, nan, nan, nan]

limpia = np.nan_to_num(posicion)      # NaN -> 0: el primer dia no estabas dentro
bruto = float((limpia * ret).sum())
rotacion = float(np.abs(np.diff(limpia)).sum())
coste = rotacion * 0.001

print(f"bruto      {bruto:+.2%}")                       # -> -7.86%
print(f"rotacion   {rotacion:.0f}  coste {coste:.2%}")  # -> rotacion 9  coste 0.90%
print(f"neto       {bruto - coste:+.2%}")               # -> -8.76%
