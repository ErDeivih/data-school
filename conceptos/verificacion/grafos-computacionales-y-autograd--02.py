import numpy as np

# Acumular gradientes por trozos debe dar el gradiente del lote completo.
X = np.array([[1.0, 0.5], [2.0, -1.0], [3.0, 2.0], [0.5, 1.0]])
yt = np.array([1.0, -1.0, 2.0, 0.0])
w = np.zeros(2)

def gradiente(indices):                       # gradiente de la MSE media del trozo
    error = X[indices] @ w - yt[indices]      # X[indices] es indexado fancy: devuelve una COPIA
    return 2 * X[indices].T @ error / len(indices)   # @ multiplica matrices y .T transpone

g_completo = gradiente(np.arange(4))
g_acumulado = np.zeros(2)
for lote in ([0, 1], [2, 3]):                 # dos trozos de dos ejemplos
    g_acumulado += gradiente(lote) * len(lote) / 4   # ponderado por su tamano
print(f"lote completo {g_completo}")           # -> lote completo [-2.5  -2.75]
print(f"acumulado     {g_acumulado}")          # -> acumulado     [-2.5  -2.75]
