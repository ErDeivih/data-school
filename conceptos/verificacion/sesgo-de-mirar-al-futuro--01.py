import numpy as np

precios = np.array([100.0, 102.0, 101.0, 105.0, 103.0])
ret = np.diff(precios) / precios[:-1]

pnl_trampa = np.sign(ret) * ret            # la senal de hoy opera el retorno de hoy
pnl_honesto = np.sign(ret[:-1]) * ret[1:]  # la senal de ayer opera el retorno de hoy

print("retornos:", np.round(ret * 100, 2).tolist())         # -> [2.0, -0.98, 3.96, -1.9]
print(f"acumulado con la trampa: {pnl_trampa.sum():+.2%}")  # -> +8.85%
print(f"acumulado honesto      : {pnl_honesto.sum():+.2%}") # -> -6.85%
print(f"comprar y mantener     : {precios[-1] / precios[0] - 1:+.2%}")   # -> +3.00%
