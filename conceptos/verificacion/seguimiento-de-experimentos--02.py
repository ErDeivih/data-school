import numpy as np

a = np.array([0.842, 0.851, 0.838, 0.849, 0.845])   # configuracion A, una fila por semilla
b = np.array([0.851, 0.856, 0.849, 0.858, 0.852])   # configuracion B, las mismas semillas

# Dispersion agrupada: el ruido entre semillas que comparten las dos configuraciones
s = np.sqrt((a.std(ddof=1) ** 2 + b.std(ddof=1) ** 2) / 2)
delta = b.mean() - a.mean()
ee = s * np.sqrt(2 / len(a))                        # error tipico de la diferencia de medias

print(f"medias          {a.mean():.4f}  y  {b.mean():.4f}")   # -> 0.8450  y  0.8532
print(f"dispersion s    {s:.4f}")                             # -> 0.0045
print(f"diferencia      {delta:.4f}")                         # -> 0.0082
print(f"2 x ee(delta)   {2 * ee:.4f}")                        # -> 0.0057
print(f"mejora creible  {bool(abs(delta) > 2 * ee)}")         # -> True
print(f"semillas para detectar delta=0,004 con esa s: {int(np.ceil(8 * (s / 0.004) ** 2))}")   # -> 11
