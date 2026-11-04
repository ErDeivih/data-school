import numpy as np
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(0)
y = (rng.random(400) < 0.12).astype(int)      # solo el 12 % son bajas
X = rng.normal(size=(400, 5))

for nombre, est in (("sin estratificar", None), ("estratificada", y)):
    _, resto, _, y_resto = train_test_split(X, y, test_size=0.2, random_state=0, stratify=est)
    # Al estratificar, la segunda particion mantiene tambien la proporcion de clases
    _, _, y_val, y_test = train_test_split(
        resto, y_resto, test_size=0.5, random_state=0, stratify=None if est is None else y_resto)
    print("%s: validacion %d de %d (%.1f %%)  prueba %d de %d (%.1f %%)"
          % (nombre, y_val.sum(), y_val.size, 100 * y_val.mean(),
             y_test.sum(), y_test.size, 100 * y_test.mean()))
# -> sin estratificar: validacion 3 de 40 (7.5 %)  prueba 2 de 40 (5.0 %)
# -> estratificada: validacion 5 de 40 (12.5 %)  prueba 4 de 40 (10.0 %)
