import numpy as np

def normaliza(x):
    x -= x.mean()        # -= modifica el array del que llama, no una copia
    return x / x.std()

datos = np.array([1.0, 2.0, 3.0, 4.0])
salida = normaliza(datos)

print(datos.tolist())              # -> [-1.5, -0.5, 0.5, 1.5]  (el original ya no son los datos)
print(np.round(salida, 3).tolist())   # -> [-1.342, -0.447, 0.447, 1.342]

# La rebanada de un array grande mantiene vivo todo el buffer: 8 bytes utiles, 80 MB retenidos
grande = np.zeros(10_000_000)
trocito = grande[:1]               # vista, no copia
print(trocito.nbytes, grande.nbytes)   # -> 8 80000000
print(np.shares_memory(grande, trocito))   # -> True
