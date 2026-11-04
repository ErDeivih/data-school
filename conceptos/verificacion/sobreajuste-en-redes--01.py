import numpy as np

# Curvas reales de un entrenamiento pequeno: 60 ejemplos de entrenamiento y 60 de validacion,
# la misma red (1 -> 16 -> 1) y el mismo ruido en los dos conjuntos.
rng = np.random.default_rng(0)
x = np.linspace(-3, 3, 60).reshape(-1, 1)
y = np.sin(x) + rng.normal(0, 0.3, x.shape)
xv = np.linspace(-3, 3, 60).reshape(-1, 1)
yv = np.sin(xv) + rng.normal(0, 0.3, xv.shape)

W1 = rng.normal(0, 1.0, (1, 16)) / 3; b1 = np.zeros(16)
W2 = rng.normal(0, 1.0, (16, 1)) / 4; b2 = np.zeros(1)

def mse(X, Y):
    return float(np.mean((np.tanh(X @ W1 + b1) @ W2 + b2 - Y) ** 2))

curva = []
for epoca in range(1, 3001):
    h = np.tanh(x @ W1 + b1)
    g = 2 * (h @ W2 + b2 - y) / x.size
    gh = (g @ W2.T) * (1 - h ** 2)
    W2 -= 0.02 * h.T @ g; b2 -= 0.02 * g.sum(0)
    W1 -= 0.02 * x.T @ gh; b1 -= 0.02 * gh.sum(0)
    if epoca % 300 == 0:
        curva.append((epoca, mse(x, y), mse(xv, yv)))

for epoca, tr, va in curva:
    print(f"epoca {epoca:>4}  train {tr:.4f}  validacion {va:.4f}")

mejor = min(curva, key=lambda c: c[2])
print(f"mejor validacion en la epoca {mejor[0]}  ({mejor[2]:.4f})")          # -> 600  (0.0936)
print(f"al final, train {curva[-1][1]:.4f}  validacion {curva[-1][2]:.4f}")  # -> 0.0810  0.1011
