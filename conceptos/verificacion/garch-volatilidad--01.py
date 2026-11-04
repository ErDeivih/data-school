import numpy as np

omega, alpha, beta = 1e-5, 0.12, 0.86
rng = np.random.default_rng(0)
n = 2000
z = rng.standard_normal(n)
eps = np.zeros(n)
var = np.empty(n)
var[0] = omega / (1 - alpha - beta)
for t in range(1, n):                       # GARCH(1,1) simulado
    var[t] = omega + alpha * eps[t - 1] ** 2 + beta * var[t - 1]
    eps[t] = np.sqrt(var[t]) * z[t]

def neglog(p, eps):
    """Menos el log de la verosimilitud gaussiana condicional."""
    w, a, b = p
    if w <= 0 or a < 0 or b < 0 or a + b >= 0.999:
        return 1e10
    v = w / (1 - a - b)
    s = 0.0
    for t in range(1, eps.size):
        v = w + a * eps[t - 1] ** 2 + b * v
        s += np.log(v) + eps[t] ** 2 / v
    return 0.5 * s

# Rejilla gruesa y refinamiento: no hace falta un optimizador para ver el mecanismo
mejor = min(((neglog((1e-5, a, b), eps), a, b)
             for a in np.arange(0.04, 0.26, 0.02) for b in np.arange(0.70, 0.95, 0.02)),
            key=lambda x: x[0])
mejor = min(((neglog((1e-5, a, b), eps), round(a, 3), round(b, 3))
             for a in np.arange(mejor[1] - 0.02, mejor[1] + 0.021, 0.005)
             for b in np.arange(mejor[2] - 0.02, mejor[2] + 0.021, 0.005)),
            key=lambda x: x[0])
print("estimado alpha %.3f  beta %.3f  (simulado 0.120 y 0.860)" % (mejor[1], mejor[2]))
# -> alpha 0.115 y beta 0.865
print("corr de los retornos con su retardo 1     %.3f" % np.corrcoef(eps[1:], eps[:-1])[0, 1])
print("corr del VALOR ABSOLUTO con su retardo 1   %.3f" % np.corrcoef(np.abs(eps[1:]), np.abs(eps[:-1]))[0, 1])
# -> 0.001 frente a 0.195: la direccion es impredecible, la magnitud no
orden = np.argsort(np.abs(eps[:-1]))
hoy = np.abs(eps[1:])
print("media de |eps| tras 200 dias tranquilos %.4f" % hoy[orden[:200]].mean())
print("media de |eps| tras 200 dias agitados   %.4f" % hoy[orden[-200:]].mean())
# -> 0.0140 frente a 0.0231
