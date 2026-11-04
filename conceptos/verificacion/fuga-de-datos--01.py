import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(0)
n = 500
y = rng.integers(0, 2, n)                     # etiqueta binaria
senal = rng.normal(0, 1, n)                   # variable legitima, sin relacion con y
fuga = y + rng.normal(0, 0.1, n)              # calculada DESPUES de conocer y

X = np.column_stack([senal, fuga])
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=0)

con_fuga = LogisticRegression().fit(X_tr, y_tr)
sin_fuga = LogisticRegression().fit(X_tr[:, :1], y_tr)

print(f"accuracy con la variable con fuga   {accuracy_score(y_te, con_fuga.predict(X_te)):.2f}")   # -> 1.00
print(f"accuracy con la senal legitima sola {accuracy_score(y_te, sin_fuga.predict(X_te[:, :1])):.2f}")   # -> 0.53
