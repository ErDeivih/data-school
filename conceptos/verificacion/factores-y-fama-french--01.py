import numpy as np

rng = np.random.default_rng(0)
n = 240
mkt = rng.normal(0.006, 0.04, n)
hml = rng.normal(0.005, 0.03, n)
hml = hml - hml.mean() + 0.005          # fijamos la prima media del factor en la muestra

# Estrategia SIN habilidad: alpha cero, beta de mercado 0,8 y carga de valor 0,5
y = 0.8 * mkt + 0.5 * hml + rng.normal(0, 0.006, n)

coef_con, *_ = np.linalg.lstsq(np.column_stack([np.ones(n), mkt, hml]), y, rcond=None)
coef_sin, *_ = np.linalg.lstsq(np.column_stack([np.ones(n), mkt]), y, rcond=None)

print("con HML  alpha %+.4f  beta_mkt %.3f  beta_hml %.3f" % (coef_con[0], coef_con[1], coef_con[2]))
print("sin HML  alpha %+.4f  beta_mkt %.3f" % (coef_sin[0], coef_sin[1]))
# -> con HML  alpha +0.0000  beta_mkt 0.795  beta_hml 0.485
# -> sin HML  alpha +0.0023  beta_mkt 0.828
