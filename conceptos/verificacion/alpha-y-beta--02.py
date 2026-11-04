import numpy as np

rng = np.random.default_rng(11)
meses = 120
mercado = rng.normal(0.008, 0.04, meses)                 # mercado alcista: +0,8 % mensual
estrategia = 2.0 * mercado + rng.normal(0, 0.02, meses)  # beta 2 y alpha 0 de verdad

beta, alpha = np.polyfit(mercado, estrategia, 1)
acum_mercado = (np.prod(1 + mercado) - 1) * 100
acum_estrategia = (np.prod(1 + estrategia) - 1) * 100

print(f"acumulado del mercado    {acum_mercado:.1f} %")      # -> 185.2 %
print(f"acumulado de la estrategia {acum_estrategia:.1f} %")  # -> 514.6 %
print(f"beta {beta:.2f}  alpha mensual {alpha * 100:+.2f} %")  # -> beta 2.06  alpha mensual -0.11 %
