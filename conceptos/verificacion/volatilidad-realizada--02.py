import numpy as np

# El ruido de microestructura (rebote bid-ask) infla la varianza realizada al afinar el muestreo
rng = np.random.default_rng(1)
n = 780                                    # barras de 1 minuto en una sesion
verdadero = rng.normal(0, 0.0005, n)       # volatilidad real: 5 pb por minuto
rebote = 0.0002 * rng.choice([-1.0, 1.0], n)   # ruido puro, sin informacion

for factor in (1, 5, 15):
    corte = n - n % factor
    limpio = verdadero[:corte].reshape(-1, factor).sum(axis=1)
    observado = (verdadero + rebote)[:corte].reshape(-1, factor).sum(axis=1)
    print(f"cada {factor:>2} min: RV limpia {np.sum(limpio ** 2):.3e}  "
          f"RV con rebote {np.sum(observado ** 2):.3e}  inflado x{np.sum(observado ** 2) / np.sum(limpio ** 2):.2f}")
