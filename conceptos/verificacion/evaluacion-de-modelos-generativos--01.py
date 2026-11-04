import numpy as np


def fid(mu_r, S_r, mu_g, S_g):
    # Tr((S_r S_g)^(1/2)) sale de los autovalores de S_r^(1/2) S_g S_r^(1/2), que si es simetrica
    vals, vecs = np.linalg.eigh(S_r)
    raiz = vecs @ np.diag(np.sqrt(vals)) @ vecs.T
    A = raiz @ S_g @ raiz
    return float(((mu_r - mu_g) ** 2).sum() + np.trace(S_r) + np.trace(S_g)
                 - 2 * np.sqrt(np.linalg.eigvalsh(A)).sum())


I = np.eye(2)
print(f"desplazado 0,5 en un eje     {fid(np.zeros(2), I, np.array([0.5, 0.0]), I):.4f}")   # -> 0.2500
print(f"con un 50 % mas de varianza  {fid(np.zeros(2), I, np.zeros(2), 1.5 * I):.4f}")     # -> 0.1010
print(f"las dos cosas a la vez       {fid(np.zeros(2), I, np.array([0.5, 0.0]), 1.5 * I):.4f}")  # -> 0.3510
