import numpy as np
from sklearn.model_selection import KFold, cross_val_score
from sklearn.neighbors import KNeighborsRegressor

rng = np.random.default_rng(0)
n = 300
t = np.arange(n).reshape(-1, 1)
y = np.sin(2 * np.pi * np.arange(n) / 50) + rng.normal(0, 0.3, n)

# Con KFold barajado, el vecino mas cercano en el tiempo cae casi siempre en el mismo pliego.
barajado = cross_val_score(KNeighborsRegressor(n_neighbors=5), t, y,
                           cv=KFold(5, shuffle=True, random_state=0)).mean()

# Con cortes consecutivos hay que extrapolar hacia delante, que es lo que pasa de verdad.
bloques = np.array_split(np.arange(n), 5)
temporal = np.mean([
    KNeighborsRegressor(n_neighbors=5).fit(t[:b[0]], y[:b[0]]).score(t[b[0]:], y[b[0]:])
    for b in bloques[1:]
])

print(f"R2 con KFold barajado    {barajado:.2f}")   # -> 0.81
print(f"R2 con cortes temporales {temporal:.2f}")   # -> -1.54
