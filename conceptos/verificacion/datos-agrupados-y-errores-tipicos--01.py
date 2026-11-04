import numpy as np

# Tabla de frecuencias: punto medio de cada intervalo y cuantas observaciones caen dentro.
x = np.array([10.0, 30.0, 50.0, 70.0, 90.0])       # marcas de clase
f = np.array([8, 14, 42, 38, 18])                  # frecuencias
n = f.sum()
k = f.size

media = (f * x).sum() / n
var_entre = (f * (x - media) ** 2).sum() / (n - 1)
s = np.sqrt(var_entre)

print(f"n {n}  k {k}  media {media:.2f}  s {s:.2f}  s2 {var_entre:.1f}")
# -> n 120  k 5  media 57.33  s 21.68  s2 470.1
print(f"EE correcto (raiz de n) {s / np.sqrt(n):.2f}   EE con raiz de k {s / np.sqrt(k):.2f}")
# -> EE correcto (raiz de n) 1.98   EE con raiz de k 9.70
print(f"factor del error {np.sqrt(n / k):.2f}  Sheppard suma {20.0 ** 2 / 12:.1f}")
# -> factor del error 4.90  Sheppard suma 33.3
