import numpy as np

# La validacion lleva su propio ruido independiente: asi las dos perdidas miden lo mismo
# y el hueco (val - train) significa algo.
def entrena(wd, lr=0.02, epochs=1200):
    rng = np.random.default_rng(0)
    x = np.linspace(-3, 3, 60).reshape(-1, 1)
    y = np.sin(x) + rng.normal(0, 0.3, x.shape)
    xv = np.linspace(-3, 3, 60).reshape(-1, 1)
    yv = np.sin(xv) + rng.normal(0, 0.3, xv.shape)

    W1 = rng.normal(0, 1.0, (1, 16)) / 3; b1 = np.zeros(16)
    W2 = rng.normal(0, 1.0, (16, 1)) / 4; b2 = np.zeros(1)

    for _ in range(epochs):
        h = np.tanh(x @ W1 + b1)
        g = 2 * (h @ W2 + b2 - y) / x.size
        gW2 = h.T @ g + wd * W2                      # wd * W2 es el gradiente de (wd/2) * ||W||^2
        gh = (g @ W2.T) * (1 - h ** 2)
        gW1 = x.T @ gh + wd * W1
        W1 -= lr * gW1; b1 -= lr * gh.sum(0)
        W2 -= lr * gW2; b2 -= lr * g.sum(0)

    htr = np.tanh(x @ W1 + b1); hva = np.tanh(xv @ W1 + b1)
    return float(np.mean((htr @ W2 + b2 - y) ** 2)), float(np.mean((hva @ W2 + b2 - yv) ** 2))

for wd in (0.0, 0.003, 0.01):
    tr, va = entrena(wd)
    print(f"weight decay {wd:.3f}  train {tr:.4f}  val {va:.4f}  hueco {va - tr:+.4f}")
# -> 0.000  train 0.0910  val 0.0990  hueco +0.0080
# -> 0.003  train 0.0916  val 0.0975  hueco +0.0059
# -> 0.010  train 0.0938  val 0.0947  hueco +0.0009
