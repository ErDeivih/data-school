import numpy as np

# Las mismas 500 personas: salario en euros y edad en anyos.
rng = np.random.default_rng(0)
salario = rng.normal(30000, 8000, 500)
edad = rng.normal(40, 10, 500)
M = np.column_stack([salario, edad])
Mc = M - M.mean(axis=0)

valores = np.linalg.eigvalsh(Mc.T @ Mc / (M.shape[0] - 1))[::-1]
print("sin escalar:", np.round(valores / valores.sum(), 4).tolist())    # -> [1.0, 0.0]

Z = Mc / Mc.std(axis=0, ddof=1)             # varianza 1 por columna, con la misma ddof que S
valores_z = np.linalg.eigvalsh(Z.T @ Z / (Z.shape[0] - 1))[::-1]
print("estandarizado:", np.round(valores_z / valores_z.sum(), 4).tolist())
# -> [0.5026, 0.4974]
