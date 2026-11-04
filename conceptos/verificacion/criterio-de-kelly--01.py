import numpy as np

p = 0.55                     # probabilidad de ganar
b = 1.0                      # se gana 1 por cada 1 arriesgado
q = 1 - p
f_kelly = (p * b - q) / b    # fraccion optima del capital

def crecimiento(f):
    """Crecimiento esperado por apuesta: media de log(1 + resultado)."""
    return p * np.log(1 + f * b) + q * np.log(1 - f)

print(f"fraccion de Kelly {f_kelly:.2f}")            # -> fraccion de Kelly 0.10
for f in (0.0, 0.05, 0.10, 0.15, 0.20, 0.30):
    print(f"f={f:.2f}  crecimiento {crecimiento(f):+.4%}")
# El maximo esta en f=0.10 (+0.5008 %), que es f*; en f=0.20 el crecimiento
# ya es negativo (-0.0138 %) aunque cada apuesta tenga esperanza positiva.
