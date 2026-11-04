import numpy as np

# Cuatro valores muy dispares: 1, 10, 100 y 1000. En escala logaritmica ocupan lo mismo.
valores = np.array([1.0, 10.0, 100.0, 1000.0])
logaritmos = np.log10(valores)
print("log10 de cada valor:", logaritmos)
print("media aritmetica  :", round(float(valores.mean()), 2))
print("media geometrica  :", round(float(10.0 ** logaritmos.mean()), 2))
print("log10(100*1000)   :", np.log10(100 * 1000), "=", np.log10(100) + np.log10(1000))
