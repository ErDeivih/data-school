import numpy as np

def pesos_fracd(d, umbral=1e-3):
    w, k = [1.0], 1
    while True:
        s = -w[-1] * (d - k + 1) / k
        if abs(s) < umbral:
            break
        w.append(s)
        k += 1
    return np.array(w)

def acf(x, lag):
    x = x - x.mean()
    return float(np.dot(x[:-lag], x[lag:]) / np.dot(x, x))

rng = np.random.default_rng(0)
serie = np.cumsum(rng.normal(0.05, 1.0, size=800))   # paseo con deriva

# Al subir d la serie se vuelve estacionaria (el acf decae) pero pierde memoria (acf lejano).
print("  d   acf(1)  acf(5)  acf(25)  desviacion")
for d in (0.0, 0.2, 0.4, 0.6, 1.0):
    w = pesos_fracd(d)
    y = np.convolve(serie, w, "full")[w.size - 1:][-700:]
    print(f"{d:>4.1f}   {acf(y, 1):>6.3f}  {acf(y, 5):>6.3f}   {acf(y, 25):>6.3f}  "
          f"{y.std():>9.3f}")
# con d=1.0 el acf a 25 rezagos es 0.003; con d=0.4 todavia vale 0.192
