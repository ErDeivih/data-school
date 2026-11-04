import numpy as np
from sklearn.model_selection import KFold, StratifiedKFold, GroupKFold

rng = np.random.default_rng(2)
n = 300
y = (rng.random(n) < 0.15).astype(int)          # 15 % de positivos
grupos = np.repeat(np.arange(30), 10)           # 30 clientes, 10 filas cada uno
X = rng.normal(size=(n, 4)) + y[:, None] * 0.8

# Proporcion de positivos que cae en cada pliegue de prueba
for nombre, divisor in (("KFold", KFold(5, shuffle=True, random_state=0)),
                        ("Stratified", StratifiedKFold(5, shuffle=True, random_state=0)),
                        ("GroupKFold", GroupKFold(5))):
    pliegues = (divisor.split(X, y, groups=grupos) if nombre == "GroupKFold"
                else divisor.split(X, y))
    print("%s: positivos por pliegue %s"
          % (nombre, " ".join("%.1f" % (100 * y[te].mean()) for _, te in pliegues)))
# -> KFold: positivos por pliegue 21.7 8.3 10.0 16.7 15.0
# -> Stratified: positivos por pliegue 13.3 13.3 15.0 15.0 15.0
# -> GroupKFold: positivos por pliegue 21.7 20.0 10.0 11.7 8.3

# Cuantos clientes aparecen a la vez en entrenamiento y prueba (sumando los 5 pliegues)
fugas = sum(len(set(grupos[tr]) & set(grupos[te]))
            for tr, te in KFold(5, shuffle=True, random_state=0).split(X))
sin_fugas = sum(len(set(grupos[tr]) & set(grupos[te]))
                for tr, te in GroupKFold(5).split(X, y, groups=grupos))
print("clientes compartidos con KFold: %d" % fugas)          # -> clientes compartidos con KFold: 140
print("clientes compartidos con GroupKFold: %d" % sin_fugas)  # -> clientes compartidos con GroupKFold: 0
