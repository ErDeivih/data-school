import numpy as np

lado = np.array([1, 1, -1, 1, -1, -1, 1, 1, -1, 1, -1, -1])
y    = np.array([1, -1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1])
p    = np.array([0.78, 0.72, 0.66, 0.58, 0.55, 0.71, 0.83, 0.33, 0.62, 0.69, 0.44, 0.30])

z = ((lado * y) > 0).astype(int)      # etiqueta del secundario: acerto el primario?
toma = p >= 0.5                       # el secundario decide si se apuesta

print(f"primario: {z.sum()} aciertos de {z.size}  precision {z.mean():.3f}")   # -> 0.667
print(f"secundario: {toma.sum()} apuestas de {z.size}  precision {z[toma].mean():.3f}")  # -> 0.778
print(f"cobertura del filtro: {toma.mean():.3f}")   # -> 0.750
