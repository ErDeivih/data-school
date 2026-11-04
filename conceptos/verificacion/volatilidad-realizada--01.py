import numpy as np

# Seis retornos logaritmicos de 5 minutos dentro de una sesion
r = np.array([0.0010, -0.0020, 0.0015, -0.0005, 0.0020, -0.0010])

rv = np.sum(r ** 2)                 # varianza realizada del dia
vol_dia = np.sqrt(rv)
vol_anual = vol_dia * np.sqrt(252)

print(f"varianza realizada  {rv:.3e}")            # -> 1.250e-05
print(f"volatilidad diaria  {vol_dia:.6f}")       # -> 0.003536
print(f"volatilidad anual   {vol_anual:.4f}")     # -> 0.0561
print(f"retorno del dia     {r.sum():+.4f}")      # -> +0.0010
print(f"ese retorno al cuadrado {r.sum() ** 2:.3e}")  # -> 1.000e-06
