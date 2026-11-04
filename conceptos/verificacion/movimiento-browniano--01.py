import numpy as np

# 20.000 trayectorias de un ano, 252 pasos: el mismo ruido para el ABM y para el GBM
rng = np.random.default_rng(7)
trayectorias, pasos = 20_000, 252
dt = 1 / pasos
w = np.cumsum(rng.standard_normal((trayectorias, pasos)) * np.sqrt(dt), axis=1)[:, -1]

abm = 100 + 0.05 * 100 + 0.20 * 100 * w
gbm = 100 * np.exp((0.05 - 0.5 * 0.20 ** 2) + 0.20 * w)

print(f"ABM media {abm.mean():.2f} desviacion {abm.std():.2f}")      # -> ABM media 104.96 desviacion 19.87
print(f"GBM media {gbm.mean():.2f} desviacion {gbm.std():.2f}")      # -> GBM media 105.06 desviacion 21.05
print(f"ABM negativo {(abm < 0).mean():.2%}")                        # -> ABM negativo 0.00%
print(f"log GBM desviacion {np.log(gbm / 100).std():.4f}")           # -> log GBM desviacion 0.1987