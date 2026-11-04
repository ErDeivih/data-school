import numpy as np

rng = np.random.default_rng(7)
n = 900
comun = np.cumsum(rng.normal(0, 0.01, n))        # paseo comun: el "mercado"
desv = np.zeros(n)
for t in range(1, n):
    desv[t] = 0.94 * desv[t - 1] + rng.normal(0, 0.008)   # diferencial que revierte
log_a = 4.0 + comun + 0.5 * desv
log_b = 3.5 + 0.8 * comun + rng.normal(0, 0.003, n)

m = n // 2
beta = np.polyfit(log_b[:m], log_a[:m], 1)[0]    # ratio de cobertura, solo con la primera mitad
spread = log_a - beta * log_b
mu, sd = spread[:m].mean(), spread[:m].std(ddof=1)
z = (spread - mu) / sd

print("beta estimada %.3f" % beta)
print("z fuera de muestra: min %+.2f  max %+.2f" % (z[m:].min(), z[m:].max()))
print("dias con z fuera de +-1,5: %d de %d" % (int(np.sum(np.abs(z[m:]) > 1.5)), n - m))
# -> beta estimada 1.271
# -> z fuera de muestra: min -2.27  max +3.38
# -> dias con z fuera de +-1,5: 88 de 450
