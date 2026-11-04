import numpy as np

# Misma media y misma desviacion tipica, dos formas distintas
dos_extremos = np.array([-1.0, 1.0])
dos_grupos = np.array([-1.224744871391589, -1.224744871391589,
                       1.224744871391589, 1.224744871391589])

print("media", round(float(dos_extremos.mean()), 4),
      round(float(dos_grupos.mean()), 4))                            # -> 0.0 0.0
print("sd   ", round(float(dos_extremos.std(ddof=1)), 4),
      round(float(dos_grupos.std(ddof=1)), 4))                       # -> 1.4142 1.4142
print("IQR  ", round(float(np.percentile(dos_extremos, 75) - np.percentile(dos_extremos, 25)), 4),
      round(float(np.percentile(dos_grupos, 75) - np.percentile(dos_grupos, 25)), 4))  # -> 1.0 2.4495
