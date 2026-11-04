import numpy as np
from math import erfc, sqrt

# 24 sujetos: 0 = control, 1 = tratamiento (12 en cada grupo)
tiempo = np.array([3, 5, 6, 8, 9, 11, 13, 15, 18, 21, 25, 30,
                   7, 10, 12, 16, 19, 22, 24, 27, 29, 33, 36, 40], dtype=float)
evento = np.array([1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0,
                   1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0])
grupo = np.array([0] * 12 + [1] * 12, dtype=float)

def log_verosimilitud_parcial(beta):
    """Suma de log(exp(b*x_i) / suma de exp(b*x_j) sobre el conjunto en riesgo)."""
    total = 0.0
    for i in np.where(evento == 1)[0]:
        en_riesgo = tiempo >= tiempo[i]
        total += beta * grupo[i] - np.log(np.exp(beta * grupo[en_riesgo]).sum())
    return total

# El riesgo base no aparece: se maximiza la parcial en una rejilla, sin derivadas
rejilla = np.arange(-3.0, 3.0001, 0.001)
valores = np.array([log_verosimilitud_parcial(b) for b in rejilla])
beta = rejilla[valores.argmax()]
estadistico = 2 * (valores.max() - log_verosimilitud_parcial(0.0))
p = erfc(sqrt(estadistico / 2))     # ji-cuadrado con 1 grado de libertad = cola de una normal

print("beta estimado %.3f" % beta)                        # -> beta estimado -0.708
print("razon de riesgos exp(beta) %.3f" % np.exp(beta))   # -> razon de riesgos exp(beta) 0.493
print("log-verosimilitud nula %.3f" % log_verosimilitud_parcial(0.0))
# -> log-verosimilitud nula -41.559
print("log-verosimilitud max %.3f" % valores.max())       # -> log-verosimilitud max -40.670
print("estadistico LR %.2f  p = %.4f" % (estadistico, p)) # -> estadistico LR 1.78  p = 0.1824

# Log-rank: observados frente a esperados en el grupo 1, tiempo a tiempo
obs = esp = var = 0.0
for t in np.unique(tiempo[evento == 1]):
    riesgo = tiempo >= t
    n, n1 = riesgo.sum(), (riesgo & (grupo == 1)).sum()
    d = ((tiempo == t) & (evento == 1)).sum()
    d1 = ((tiempo == t) & (evento == 1) & (grupo == 1)).sum()
    obs += d1
    esp += d * n1 / n
    var += d * (n1 / n) * (1 - n1 / n) * (n - d) / (n - 1)
chi2 = (obs - esp) ** 2 / var
print("log-rank observados %.1f esperados %.1f chi2 %.2f p = %.4f"
      % (obs, esp, chi2, erfc(sqrt(chi2 / 2))))
# -> log-rank observados 8.0 esperados 10.5 chi2 1.85 p = 0.1740
