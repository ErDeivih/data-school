import numpy as np
from sklearn.metrics import brier_score_loss, roc_auc_score

# Probabilidades calibradas por construccion: de cada 100 casos con p = 0,30
# exactamente 30 son positivos.
valores = np.arange(5, 100, 5) / 100.0        # 0,05 ... 0,95
# np.repeat repite CADA valor 100 veces (1.900 casos); np.tile repetiria la lista entera.
p = np.repeat(valores, 100)
# La comprension construye 19 bloques de 100 etiquetas: los `int(v * 100)` primeros son 1
# y el resto 0, asi que la frecuencia real coincide con la probabilidad declarada.
y = np.concatenate([np.r_[np.ones(int(v * 100)), np.zeros(100 - int(v * 100))]
                    for v in valores])

# Una transformacion creciente (elevar al cuadrado) conserva el orden y rompe la escala
distorsionada = p ** 2

print(f"casos {p.size}  prevalencia {y.mean():.2f}")            # -> casos 1900  prevalencia 0.50
print(f"AUC   original {roc_auc_score(y, p):.3f}")             # -> 0.816
print(f"AUC   distorsionada {roc_auc_score(y, distorsionada):.3f}")  # -> 0.816
print(f"Brier original {brier_score_loss(y, p):.4f}")          # -> 0.1750
print(f"Brier distorsionada {brier_score_loss(y, distorsionada):.4f}")  # -> 0.2101
