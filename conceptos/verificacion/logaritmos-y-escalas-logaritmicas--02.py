import numpy as np

# Un crecimiento multiplicativo constante es una recta en escala logaritmica: los pasos
# de log10 son todos iguales. La recta no dice "suma", dice "multiplica por lo mismo".
capital = 100.0 * 1.26 ** np.arange(6)
print("capital por paso:", np.round(capital, 1))
print("pasos de log10  :", np.round(np.diff(np.log10(capital)), 3))

# El punto medio VISUAL de un eje logaritmico no es la media de los extremos: es su raiz.
print("mitad de 1 a 1000:", round(float(np.sqrt(1 * 1000)), 1), "y no 500")

# Aviso numerico: log(1+x) se come los incrementos diminutos y log1p no.
print("log(1 + 1e-16)   :", np.log(1 + 1e-16))
print("log1p(1e-16)     :", np.log1p(1e-16))
