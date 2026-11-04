import numpy as np
from scipy import stats

rng = np.random.default_rng(0)

# La exponencial es muy asimetrica; la media de 30 ya se comporta como una normal.
muestras = rng.exponential(scale=1.0, size=(4000, 30))
medias = muestras.mean(axis=1)

print(f"media de las medias = {medias.mean():.4f}")                        # -> 0.9967
print(f"error tipico        = {medias.std(ddof=1):.4f}")                  # -> 0.1851
print(f"teorico 1/sqrt(30)  = {1 / np.sqrt(30):.4f}")                      # -> 0.1826
print(f"dentro de 1 error   = {(np.abs(medias - 1) < 1 / np.sqrt(30)).mean():.4f}")   # -> 0.6825
print(f"dentro de 2 errores = {(np.abs(medias - 1) < 2 / np.sqrt(30)).mean():.4f}")   # -> 0.9527
print(f"asimetria restante  = {stats.skew(medias, bias=False):.4f}")       # -> 0.4041
