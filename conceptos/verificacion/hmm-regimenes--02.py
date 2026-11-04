import numpy as np

P = np.array([[0.90, 0.10], [0.20, 0.80]])
print("duracion esperada", np.round(1 / (1 - np.diag(P)), 1), "periodos")   # -> [10.  5.]
val, vec = np.linalg.eig(P.T)                   # vector propio izquierdo de valor propio 1
pi = np.real(vec[:, np.argmin(np.abs(val - 1))])
print("proporcion del tiempo en cada regimen", np.round(pi / pi.sum(), 3))  # -> [0.667 0.333]

y = np.array([0.1, -0.3, 2.4, 1.9, 0.2, 3.1, -0.4])
def logver(mu, var, A):
    """Log-verosimilitud de la serie integrando todos los caminos de estados."""
    def f(v, m, s2):
        return np.exp(-0.5 * (v - m) ** 2 / s2) / np.sqrt(2 * np.pi * s2)
    al = 0.5 * np.array([f(y[0], mu[k], var[k]) for k in range(2)])
    for t in range(1, y.size):
        al = (al @ A) * np.array([f(y[t], mu[k], var[k]) for k in range(2)])
    return np.log(al.sum())

mu, var = np.array([0.0, 2.5]), np.array([1.0, 1.0])
print("log-verosimilitud original            %.4f" % logver(mu, var, P))          # -> -14.0878
print("log-verosimilitud con etiquetas al reves %.4f" % logver(mu[::-1], var[::-1], P[::-1, ::-1]))
# -> tambien -14.0878: los nombres de los estados son arbitrarios
