import numpy as np

rng = np.random.default_rng(0)
base = rng.normal(0, 1, size=(2000, 64))
base /= np.linalg.norm(base, axis=1, keepdims=True)      # normalizar = comparar por coseno
consulta = rng.normal(0, 1, size=64)
consulta /= np.linalg.norm(consulta)

# Producto escalar = similitud del coseno cuando los vectores son unitarios
similitudes = base @ consulta
# argsort ordena de menor a mayor: el menos delante lo da la vuelta para quedarse con el top
mejores = np.argsort(-similitudes)[:5]

print("mejores indices:", mejores.tolist())
print("sus similitudes:", np.round(similitudes[mejores], 3).tolist())
print("coste: 1 producto matriz-vector,", base.shape[0] * base.shape[1], "multiplicaciones")
