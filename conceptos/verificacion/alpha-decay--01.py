import numpy as np

rng = np.random.default_rng(11)
T, N = 2000, 100
s = np.zeros((T, N))
s[0] = rng.normal(0, 1, N)
for t in range(1, T):
    s[t] = 0.93 * s[t - 1] + rng.normal(0, 0.37, N)     # senal AR(1)

w = s / np.abs(s).sum(axis=1, keepdims=True)            # pesos proporcionales a la senal

rho = np.corrcoef(s[:-1].ravel(), s[1:].ravel())[0, 1]
vida_media = -np.log(2) / np.log(rho)
giro = np.abs(np.diff(w, axis=0)).sum(axis=1).mean()

print("autocorr de la senal %.3f" % rho)
print("vida media           %.2f periodos" % vida_media)
print("giro medio           %.3f del bruto por periodo" % giro)
print("coste con 5 pb       %.2f%% al ano" % (100 * giro * 252 * 0.0005))
# -> autocorr de la senal 0.930
# -> vida media           9.58 periodos
# -> giro medio           0.374 del bruto por periodo
# -> coste con 5 pb       4.72% al ano
