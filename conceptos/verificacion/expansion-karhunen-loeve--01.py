import numpy as np

t = np.linspace(0, 1, 2000, endpoint=False)

def e(k):
    return np.sqrt(2) * np.sin(k * np.pi * t)

total = 1 / 6
for k in (3, 10, 50):
    lam = sum(1 / (j * np.pi) ** 2 for j in range(1, k + 1))
    print(f"{k} terminos varianza {lam:.6f} fraccion {lam / total:.2%}")

print(f"producto 1,2 {(e(1) * e(2)).mean():+.6f}")   # -> producto 1,2 +0.000000
print(f"norma 1 {(e(1) ** 2).mean():.6f}")           # -> norma 1 1.000000