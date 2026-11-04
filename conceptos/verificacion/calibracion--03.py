from sklearn.calibration import CalibratedClassifierCV
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

# Un arbol sin limite de profundidad deja hojas puras: solo sabe decir 0 y 1.
# flip_y=0.1 cambia el 10 % de las etiquetas a proposito: sin ese ruido el problema seria
# demasiado facil y el arbol acertaria sin despeinarse.
X, y = make_classification(n_samples=2000, n_features=10, n_informative=4,
                           n_redundant=2, flip_y=0.1, random_state=0)
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4, random_state=0)

def brier(p, yv):
    # Media de los cuadrados: (p - yv) ** 2 se calcula elemento a elemento.
    return float(((p - yv) ** 2).mean())

base = DecisionTreeClassifier(random_state=0).fit(X_tr, y_tr)
# cv=5 no es «cinco modelos distintos»: CalibratedClassifierCV parte X_tr en cinco pliegues,
# entrena un arbol con cuatro y ajusta el calibrador con el que dejo fuera. Asi el calibrador
# nunca ve los datos con los que se entreno su arbol.
# El DecisionTreeClassifier se pasa SIN entrenar: la clase lo clona por dentro en cada pliegue.
calibrado = CalibratedClassifierCV(
    DecisionTreeClassifier(random_state=0), method="isotonic", cv=5
).fit(X_tr, y_tr)

# predict_proba devuelve una columna por clase, en el orden de `classes_`; la 1 es la positiva.
p_base = base.predict_proba(X_te)[:, 1]
p_cal = calibrado.predict_proba(X_te)[:, 1]

print(f"Brier sin calibrar {brier(p_base, y_te):.4f}")   # -> 0.2437
print(f"Brier calibrado    {brier(p_cal, y_te):.4f}")    # -> 0.1599
# (a == 0) | (a == 1) es la mascara de las probabilidades extremas y .mean() da su
# proporcion. El formato :.0% multiplica por 100 y anade el simbolo por su cuenta.
print(f"extremos 0 o 1     {((p_base == 0) | (p_base == 1)).mean():.0%}")  # -> 100%
print(f"confianza media    {p_base.mean():.3f}  frecuencia real {y_te.mean():.3f}")
