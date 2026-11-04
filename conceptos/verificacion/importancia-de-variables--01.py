import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split

# 8 variables: solo 3 informan. Las otras 5 son ruido puro.
X, y = make_classification(n_samples=700, n_features=8, n_informative=3, n_redundant=0,
                           n_repeated=0, shuffle=False, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)
bosque = RandomForestClassifier(n_estimators=100, random_state=0).fit(X_tr, y_tr)

mdi = bosque.feature_importances_      # atributo con guion bajo final: existe solo tras fit
print("accuracy en test:", round(bosque.score(X_te, y_te), 3))       # -> 0.914
print("importancia por impureza:", mdi.round(3).tolist())
# -> [0.148, 0.37, 0.117, 0.073, 0.069, 0.07, 0.072, 0.081]
# mdi[3:] son las cinco ultimas columnas, que son las de ruido: se cuentan con un booleano
print("variables de ruido con impureza > 0.05:", int((mdi[3:] > 0.05).sum()), "de 5")   # -> 5 de 5

# n_repeats=4 promedia cuatro barajados de cada columna (el objeto trae tambien la desviacion)
perm = permutation_importance(bosque, X_te, y_te, n_repeats=4, random_state=0).importances_mean
print("importancia por permutacion:", perm.round(3).tolist())
# -> [0.163, 0.331, 0.106, -0.001, -0.007, 0.004, 0.005, -0.001]
print("variables de ruido con permutacion > 0.01:", int((perm[3:] > 0.01).sum()), "de 5")  # -> 0 de 5
