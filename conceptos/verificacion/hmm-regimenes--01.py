import numpy as np

rng = np.random.default_rng(7)
n = 600
P = np.array([[0.95, 0.05], [0.10, 0.90]])        # matriz de transicion real
s = np.zeros(n, int)
for t in range(1, n):
    s[t] = rng.choice(2, p=P[s[t - 1]])
y = rng.normal(np.where(s == 0, 0.0, 2.0), np.where(s == 0, 1.0, 3.0))

def gauss(y, mu, var):
    return np.exp(-0.5 * (y - mu) ** 2 / var) / np.sqrt(2 * np.pi * var)

# Arranque por cuantiles: separa los periodos tranquilos de los agitados
mu = np.quantile(y, [0.25, 0.8])
var = np.array([y.var() / 4, y.var() * 2])
A = np.array([[0.9, 0.1], [0.1, 0.9]])
for _ in range(30):                                # Baum-Welch: con 30 iteraciones de EM basta
    B = np.column_stack([gauss(y, mu[k], var[k]) for k in range(2)])
    al = np.zeros((n, 2)); al[0] = 0.5 * B[0]
    for t in range(1, n):                          # paso forward (filtrado)
        al[t] = (al[t - 1] @ A) * B[t]
        al[t] /= al[t].sum()
    be = np.ones((n, 2))
    for t in range(n - 2, -1, -1):                 # paso backward
        be[t] = A @ (B[t + 1] * be[t + 1])
        be[t] /= be[t].sum()
    g = al * be; g /= g.sum(1, keepdims=True)      # gamma: probabilidad suavizada
    xi = np.array([al[t][:, None] * A * (B[t + 1] * be[t + 1])[None, :] for t in range(n - 1)])
    xi /= xi.sum((1, 2), keepdims=True)
    A = xi.sum(0) / g[:-1].sum(0)[:, None]         # paso M: transiciones, medias y varianzas
    mu = (g * y[:, None]).sum(0) / g.sum(0)
    var = (g * (y[:, None] - mu) ** 2).sum(0) / g.sum(0)

print("medias     ", np.round(mu, 2), " (simuladas: 0.00 y 2.00)")     # -> [-0.    1.98]
print("varianzas  ", np.round(var, 2), " (simuladas: 1.00 y 9.00)")    # -> [0.95 9.63]
print("transicion ", np.round(A, 3).tolist())                          # -> [[0.951, 0.049], [0.124, 0.876]]
print("filas suman 1:", np.allclose(A.sum(1), 1))                      # -> True
print("duracion esperada", np.round(1 / (1 - np.diag(A)), 1))          # -> [20.4  8.1]
print("acuerdo con el estado simulado", round((g.argmax(1) == s).mean(), 3))   # -> 0.933
