import numpy as np

r = np.array([0.03, -0.02, 0.04, -0.05, 0.01, 0.02])      # retornos mensuales
capital = 100 * np.cumprod(1 + r)

vol_mensual = r.std(ddof=1)
picos = np.maximum.accumulate(capital)
mdd = float(((picos - capital) / picos).max())
anualizado = float((capital[-1] / 100.0) ** (12 / r.size) - 1)   # 100 es el capital inicial

print(f"retorno total       {capital[-1] - 100:+.2f} %")     # -> +2.74 %
print(f"volatilidad mensual {vol_mensual:.4f}")              # -> 0.0339
print(f"volatilidad anual   {vol_mensual * np.sqrt(12):.4f}")  # -> 0.1175
print(f"Sharpe anual        {r.mean() / vol_mensual * np.sqrt(12):.2f}")   # -> 0.51
print(f"caida maxima        {mdd:.2%}")                       # -> 5.00%
print(f"retorno anualizado  {anualizado:.2%}")               # -> 5.56%
print(f"Calmar              {anualizado / mdd:.2f}")          # -> 1.11
