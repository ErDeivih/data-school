import numpy as np

retornos = np.array([0.02, 0.03, -0.01, 0.04, 0.01, 0.02,
                     -0.02, 0.03, 0.00, 0.02, 0.01, 0.01])
rf_mensual = 0.002

exceso = retornos - rf_mensual
sharpe_mensual = exceso.mean() / exceso.std(ddof=1)   # ddof=1: estimamos la media
sharpe_anual = sharpe_mensual * np.sqrt(12)

print(f"media mensual   {retornos.mean():.4f}")        # -> 0.0133
print(f"volatilidad     {retornos.std(ddof=1):.4f}")   # -> 0.0172
print(f"Sharpe mensual  {sharpe_mensual:.2f}")         # -> 0.66
print(f"Sharpe anual    {sharpe_anual:.2f}")           # -> 2.28
