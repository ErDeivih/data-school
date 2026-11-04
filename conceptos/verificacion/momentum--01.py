import numpy as np

# 5 activos, 13 retornos mensuales en tanto por uno; el ultimo es el mes en curso
r = np.array([
    [0.02, 0.01, 0.03, 0.02, 0.01, 0.02, 0.01, 0.02, 0.03, 0.01, 0.02, 0.01,  0.01],
    [0.01, 0.02, 0.00, 0.01, 0.02, 0.01, 0.02, 0.00, 0.01, 0.02, 0.01, 0.02, -0.06],
    [-0.01, 0.00, 0.01, -0.02, 0.00, 0.01, -0.01, 0.00, 0.01, -0.01, 0.00, 0.01, 0.04],
    [0.03, 0.02, 0.01, 0.02, 0.03, 0.01, 0.02, 0.03, 0.01, 0.02, 0.03, 0.02, 0.00],
    [0.00, 0.01, 0.02, 0.01, 0.00, 0.01, 0.02, 0.01, 0.00, 0.01, 0.02, 0.01,  0.00],
])

mom_12_1 = np.prod(1 + r[:, :12], axis=1) - 1     # 12 meses, saltando el ultimo
mom_total = np.prod(1 + r, axis=1) - 1            # incluyendo el mes en curso

print("momentum 12-1   ", np.round(mom_12_1, 4))
print("con el ultimo   ", np.round(mom_total, 4))
print("orden 12-1  (mejor a peor)", np.argsort(-mom_12_1))
print("orden total (mejor a peor)", np.argsort(-mom_total))
# -> momentum 12-1    [ 0.2311  0.1604 -0.0105  0.2803  0.1265]
# -> con el ultimo    [0.2434 0.0908 0.0291 0.2803 0.1265]
# -> orden 12-1  (mejor a peor) [3 0 1 4 2]
# -> orden total (mejor a peor) [3 0 4 1 2]
