import numpy as np
from sklearn.metrics import precision_score, recall_score

# 100 casos: 20 positivos (los primeros) y 80 negativos, con puntuaciones que se solapan.
y = np.array([1] * 20 + [0] * 80)
p = np.concatenate([np.linspace(0.95, 0.05, 20), np.linspace(0.6, 0.01, 80)])

# El umbral 0.5 no es sagrado: moverlo reparte de otra forma recall y precision.
for t in (0.9, 0.5, 0.1):
    pred = (p >= t).astype(int)
    print(f"umbral {t:.1f}  positivos {int(pred.sum()):>3}  "
          f"recall {recall_score(y, pred):.2f}  precision {precision_score(y, pred, zero_division=0):.2f}")
# -> umbral 0.9  positivos   2  recall 0.10  precision 1.00
# -> umbral 0.5  positivos  24  recall 0.50  precision 0.42
# -> umbral 0.1  positivos  85  recall 0.90  precision 0.21
