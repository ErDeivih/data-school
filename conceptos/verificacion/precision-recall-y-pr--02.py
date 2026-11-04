import numpy as np
from sklearn.metrics import average_precision_score, roc_auc_score

# 100 positivos entre 10.000 casos: la clase rara es el 1 %
pos = np.r_[np.linspace(0.80, 0.99, 90), np.linspace(0.10, 0.60, 10)]
neg = np.r_[np.linspace(0.80, 0.99, 495), np.linspace(0.00, 0.79, 9405)]
y = np.r_[np.ones(100), np.zeros(9900)]
score = np.r_[pos, neg]

# La ROC parece redonda; la PR ensena el ruido real de las alertas
print(f"AUC {roc_auc_score(y, score):.3f}")            # -> 0.920
print(f"AP  {average_precision_score(y, score):.4f}")  # -> 0.1483
# y.mean() sobre unos y ceros es la proporcion de positivos: la linea base de la PR.
print(f"azar (prevalencia) {y.mean():.4f}")             # -> 0.0100
