import numpy as np

rng = np.random.default_rng(0)
x = rng.normal(0, 1, size=40)
y = 0.5 * x + rng.normal(0, 1, size=40)

# Verosimilitud de una Bernoulli: n = 50 lanzamientos con 30 caras
n, exitos = 50, 30
p_mle = exitos / n
log_ver = exitos * np.log(p_mle) + (n - exitos) * np.log(1 - p_mle)
print(f"p MLE                  {p_mle:.4f}")        # -> 0.6000
print(f"log-verosimilitud      {log_ver:.3f}")      # -> -33.651

# La derivada de la log-verosimilitud en el maximo debe ser cero
h = 1e-6
def lv(p):
    return exitos * np.log(p) + (n - exitos) * np.log(1 - p)
print(f"derivada en el maximo  {(lv(p_mle + h) - lv(p_mle - h)) / (2 * h):.6f}")  # -> 0.000000

# Error tipico asintotico a partir de la informacion de Fisher: I(p) = n / (p(1-p))
error_tipico = np.sqrt(p_mle * (1 - p_mle) / n)
print(f"error tipico asintotico {error_tipico:.4f}")  # -> 0.0693

# Comprobacion por simulacion: el MLE de una moneda con p = 0,6 y n = 50
ps = rng.binomial(n, 0.6, size=20000) / n
print(f"desviacion simulada del MLE {ps.std(ddof=1):.4f}")  # -> 0.0691
print(f"media simulada del MLE      {ps.mean():.4f}")       # -> 0.5995
