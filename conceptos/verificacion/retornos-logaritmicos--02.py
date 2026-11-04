import numpy as np

# La aproximacion ln(1+r) ~ r - r^2/2 solo vale para retornos pequenos:
# al 50 % el error es de tres centesimas, no de una millonesima.
for r in (0.001, 0.01, 0.10, 0.50):
    error = r - r * r / 2 - np.log1p(r)
    print(f"r={r:>5.1%}  ln(1+r)={np.log1p(r):+.6f}  error de la aproximacion {error:+.2e}")

# En el tiempo los logs se suman; entre activos NO: la cartera promedia simples.
pesos = np.array([0.5, 0.5])
simples = np.array([0.10, -0.10])
print(f"cartera con simples {(pesos * simples).sum():+.4f}")              # -> +0.0000
print(f"media de los logs   {(pesos * np.log1p(simples)).sum():+.4f}")   # -> -0.0050
