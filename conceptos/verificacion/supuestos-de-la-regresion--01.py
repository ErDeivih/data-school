import numpy as np
import statsmodels.api as sm

rng = np.random.default_rng(0)
n = 200
x = rng.uniform(1, 10, size=n)
y = 2 + 0.8 * x + rng.normal(0, 0.02 * x ** 2)   # la varianza del error crece con x^2

X = sm.add_constant(x)                           # columna de unos para el intercepto
clasico = sm.OLS(y, X).fit()
# cov_type se pasa a fit(): el error estandar se calcula con los residuos al cuadrado
# de cada fila en vez de con una varianza comun.
robusto = sm.OLS(y, X).fit(cov_type="HC3")

print(f"beta1   clasico {clasico.params[1]:.4f}  robusto {robusto.params[1]:.4f}")
print(f"SE      clasico {clasico.bse[1]:.4f}  robusto {robusto.bse[1]:.4f}")
print(f"t       clasico {clasico.tvalues[1]:.2f}  robusto {robusto.tvalues[1]:.2f}")
# -> beta1   clasico 0.7435  robusto 0.7435
# -> SE      clasico 0.0288  robusto 0.0316
# -> t       clasico 25.83  robusto 23.50
