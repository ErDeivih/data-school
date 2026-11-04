import numpy as np

mercado = np.array([0.02, -0.01, 0.03, 0.00, 0.01])   # ya en exceso del activo sin riesgo
cartera = np.array([0.03, -0.02, 0.04, 0.01, 0.02])

beta, alpha = np.polyfit(mercado, cartera, 1)          # pendiente y ordenada en el origen
residuo = cartera - (alpha + beta * mercado)
n = mercado.size

s = np.sqrt((residuo ** 2).sum() / (n - 2))            # error tipico de la regresion
se_alpha = s * np.sqrt(1 / n + mercado.mean() ** 2 / ((mercado - mercado.mean()) ** 2).sum())
r2 = 1 - (residuo ** 2).sum() / ((cartera - cartera.mean()) ** 2).sum()

print(f"beta       {beta:.2f}")                 # -> 1.40
print(f"alpha      {alpha * 100:+.2f} %/mes")   # -> +0.20 %/mes
print(f"R2         {r2:.3f}")                   # -> 0.925
print(f"t de alpha {alpha / se_alpha:.2f}")     # -> 0.50
