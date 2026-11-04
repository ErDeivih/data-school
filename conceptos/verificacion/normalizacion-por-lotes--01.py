import numpy as np

x = np.array([1.0, 2.0, 3.0, 4.0])          # un canal, un lote de 4
media, var = x.mean(), x.var()               # varianza del lote: divide por m, no por m-1
# El 1e-5 va DENTRO de la raiz, como en la formula: sqrt(sigma^2 + eps), no sqrt(sigma^2) + eps
x_sombrero = (x - media) / np.sqrt(var + 1e-5)

gamma, beta = 2.0, 1.0                       # en una red de verdad, estos dos los aprende la capa
print(f"media {media:.2f}  varianza {var:.2f}  desviacion {np.sqrt(var):.3f}")
# -> media 2.50  varianza 1.25  desviacion 1.118
print(f"normalizado   {np.round(x_sombrero, 3)}")
# -> normalizado   [-1.342 -0.447  0.447  1.342]
print(f"con gamma y beta  {np.round(gamma * x_sombrero + beta, 3)}")
# -> con gamma y beta  [-1.683  0.106  1.894  3.683]
print(f"media de la salida {x_sombrero.mean():.4f}  desviacion {x_sombrero.std():.4f}")
# -> media de la salida 0.0000  desviacion 1.0000
