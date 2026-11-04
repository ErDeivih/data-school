import numpy as np
from sklearn.metrics import roc_auc_score

# 100 positivos entre 10.000 casos: la clase rara es el 1 %
# np.linspace(a, b, n) da n valores equiespaciados entre a y b: 90 + 10 = 100 positivos
# y 495 + 9405 = 9.900 negativos.
pos = np.r_[np.linspace(0.80, 0.99, 90), np.linspace(0.10, 0.60, 10)]
neg = np.r_[np.linspace(0.80, 0.99, 495), np.linspace(0.00, 0.79, 9405)]
y = np.r_[np.ones(100), np.zeros(9900)]
score = np.r_[pos, neg]

pred = score >= 0.80
vp = int(((pred == 1) & (y == 1)).sum())
fp = int(((pred == 1) & (y == 0)).sum())

print(f"AUC       {roc_auc_score(y, score):.3f}")  # -> 0.920
print(f"TPR       {vp / (y == 1).sum():.3f}")      # -> 0.900
print(f"FPR       {fp / (y == 0).sum():.3f}")      # -> 0.050
print(f"precision {vp / (vp + fp):.4f}")           # -> 0.1538
