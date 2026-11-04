import numpy as np

# Calendario lineal: beta_t crece de 1e-4 a 0.02 en T pasos.
T = 1000
betas = np.linspace(1e-4, 0.02, T)
abar = np.cumprod(1.0 - betas)      # alpha_bar_t = producto de (1 - beta_s), s <= t

for t in (0, 100, 500, 900, 999):
    print(f"t={t:>4}  alpha_bar={abar[t]:.5f}  sqrt(alpha_bar)={np.sqrt(abar[t]):.4f}"
          f"  sqrt(1-alpha_bar)={np.sqrt(1 - abar[t]):.4f}")
# -> t=   0  alpha_bar=0.99990  sqrt(alpha_bar)=0.9999  sqrt(1-alpha_bar)=0.0100
# -> t= 100  alpha_bar=0.89514  sqrt(alpha_bar)=0.9461  sqrt(1-alpha_bar)=0.3238
# -> t= 500  alpha_bar=0.07780  sqrt(alpha_bar)=0.2789  sqrt(1-alpha_bar)=0.9603
# -> t= 900  alpha_bar=0.00027  sqrt(alpha_bar)=0.0164  sqrt(1-alpha_bar)=0.9999
# -> t= 999  alpha_bar=0.00004  sqrt(alpha_bar)=0.0064  sqrt(1-alpha_bar)=1.0000

# Forma cerrada: x_t = sqrt(alpha_bar) * x0 + sqrt(1 - alpha_bar) * eps
rng = np.random.default_rng(0)
x0, paso = 0.7, 500
eps = rng.normal()                  # un unico numero normal estandar, no un array
xt = np.sqrt(abar[paso]) * x0 + np.sqrt(1 - abar[paso]) * eps
# Al despejar x0 con el mismo eps sale 0.7 exacto: la formula no mete error por si sola.
recuperado = (xt - np.sqrt(1 - abar[paso]) * eps) / np.sqrt(abar[paso])
print(f"x_t={xt:.4f}  x0 original={x0}  x0 recuperado con el eps exacto={recuperado:.6f}")
# -> x_t=0.3160  x0 original=0.7  x0 recuperado con el eps exacto=0.700000
