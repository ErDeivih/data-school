import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score

# 10.000 casos con un 1 % de positivos: el modelo "todo negativo" triunfa en accuracy.
y = np.zeros(10000, dtype=int)
y[:100] = 1
pred = np.zeros(10000, dtype=int)   # prediccion perezosa: nunca senala un positivo

print(f"accuracy  {accuracy_score(y, pred):.4f}")   # -> 0.9900
print(f"recall    {recall_score(y, pred):.4f}")     # -> 0.0000
print(f"precision {precision_score(y, pred, zero_division=0):.4f}")  # -> 0.0000
