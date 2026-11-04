import numpy as np

# 10 operaciones en multiplos de R (lo que arriesgas en cada una) de un sistema ya probado
rs = np.array([2.0, 1.0, -1.0, 3.0, -1.0, 1.0, -1.0, 2.0, -1.0, 1.0])
riesgo = 0.02                                 # 2 % del capital por operacion

original = np.cumprod(1 + riesgo * rs)
picos = np.maximum.accumulate(original)
print(f"total de la muestra {rs.sum():+.0f}R")                                  # -> +6R
print(f"resultado del orden real {original[-1] - 1:+.2%}")                     # -> +12.22%
print(f"caida del orden real {((picos - original) / picos).max():.2%}")        # -> 2.04%

# Monte Carlo: remuestreamos con reemplazo para ver el abanico de resultados.
rng = np.random.default_rng(0)
muestras = rng.choice(rs, size=(20_000, rs.size), replace=True)
curvas = np.cumprod(1 + riesgo * muestras, axis=1)
picos = np.maximum.accumulate(curvas, axis=1)
dd = ((picos - curvas) / picos).max(axis=1)
final = curvas[:, -1] - 1

print(f"mediana final {np.median(final):+.2%}")            # -> +12.22%
print(f"percentil 5   {np.percentile(final, 5):+.2%}")     # -> -2.38%
print(f"caida mediana {np.median(dd):.2%}")                # -> 3.96%
print(f"caida p95     {np.percentile(dd, 95):.2%}")        # -> 7.87%
print(f"acaba en perdidas {(final < 0).mean():.2%}")       # -> 11.27%
