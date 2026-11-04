import numpy as np

# Varianza de la media de n modelos con varianza 1 y correlacion rho entre ellos:
# Var = rho + (1 - rho) / n
for rho in (0.0, 0.3, 0.8):
    v = [rho + (1 - rho) / n for n in (1, 10, 100)]
    print(f"rho={rho:.1f}  n=1 {v[0]:.3f}  n=10 {v[1]:.3f}  n=100 {v[2]:.3f}")
# -> rho=0.0  n=1 1.000  n=10 0.100  n=100 0.010
# -> rho=0.3  n=1 1.000  n=10 0.370  n=100 0.307
# -> rho=0.8  n=1 1.000  n=10 0.820  n=100 0.802
