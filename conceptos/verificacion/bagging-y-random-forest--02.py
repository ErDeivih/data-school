import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = make_classification(n_samples=300, n_features=6, n_informative=3,
                           flip_y=0.15, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4, random_state=0)

arbol = DecisionTreeClassifier(random_state=0).fit(X_tr, y_tr)
bosque = RandomForestClassifier(n_estimators=60, oob_score=True,
                                random_state=0, n_jobs=1).fit(X_tr, y_tr)

print(f"un arbol train {arbol.score(X_tr, y_tr):.3f}  test {arbol.score(X_te, y_te):.3f}")
print(f"bosque   train {bosque.score(X_tr, y_tr):.3f}  test {bosque.score(X_te, y_te):.3f}")
print(f"OOB del bosque {bosque.oob_score_:.3f}")
# -> un arbol train 1.000  test 0.792
# -> bosque   train 1.000  test 0.833
# -> OOB del bosque 0.844
