import numpy as np
from sklearn.metrics import roc_auc_score

# Ocho casos: y = 1 si era el caso que buscamos, score = puntuacion del modelo
y = np.array([1, 1, 1, 0, 0, 0, 0, 0])
score = np.array([0.95, 0.60, 0.40, 0.85, 0.55, 0.35, 0.20, 0.10])

# AUC a mano: fraccion de parejas (positivo, negativo) en las que gana el positivo
# score[y == 1] no es un bucle: la comparacion produce una mascara de True y False y NumPy
# devuelve solo las puntuaciones marcadas con True (indexado booleano).
# La doble comprension es el producto cartesiano 3 x 5 = 15 parejas; cada p > n vale True o
# False y sum() los cuenta como 1 y 0, sin construir ninguna lista.
mejores = sum(p > n for p in score[y == 1] for n in score[y == 0])
# (y == 1).sum() cuenta los True: en una suma, True vale 1 y False vale 0.
parejas = (y == 1).sum() * (y == 0).sum()

print(f"parejas ganadas {mejores} de {parejas}")     # -> parejas ganadas 12 de 15
print(f"AUC a mano  {mejores / parejas:.3f}")        # -> 0.800
print(f"AUC sklearn {roc_auc_score(y, score):.3f}")  # -> 0.800
