import numpy as np

def resumen(y, X):
    X = np.column_stack([np.ones(len(y)), X])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ coef
    n, k = X.shape
    s2 = resid @ resid / (n - k)
    se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
    r2 = 1 - (resid @ resid) / ((y - y.mean()) @ (y - y.mean()))
    return coef, se, r2

rng = np.random.default_rng(0)
n = 240
mkt = rng.normal(0.006, 0.04, n)
hml = rng.normal(0.005, 0.03, n)
hml = hml - hml.mean() + 0.005
y = 0.8 * mkt + 0.5 * hml + rng.normal(0, 0.006, n)

coef_c, se_c, r2_c = resumen(y, np.column_stack([mkt, hml]))
coef_s, se_s, r2_s = resumen(y, mkt.reshape(-1, 1))

print("con HML  alpha %+.4f  t %+.2f  R2 %.3f" % (coef_c[0], coef_c[0] / se_c[0], r2_c))
print("sin HML  alpha %+.4f  t %+.2f  R2 %.3f" % (coef_s[0], coef_s[0] / se_s[0], r2_s))
# -> con HML  alpha +0.0000  t +0.10  R2 0.977
# -> sin HML  alpha +0.0023  t +2.21  R2 0.815
