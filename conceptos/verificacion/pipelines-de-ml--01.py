import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier

# 120 filas con dos columnas en escalas muy distintas: anos e ingresos en euros
rng = np.random.default_rng(0)
X = np.column_stack([rng.normal(40, 10, 120), rng.normal(30000, 8000, 120)])
# La comparacion contra 0 da un booleano; .astype(int) lo convierte en las clases 0 y 1
y = (X[:, 0] - 40 + (X[:, 1] - 30000) / 8000 + rng.normal(0, 1, 120) > 0).astype(int)

# MAL: escalar con la media y la desviacion de todo el conjunto, prueba incluida
print("sin pipeline:", round(cross_val_score(LogisticRegression(),
      StandardScaler().fit_transform(X), y, cv=5).mean(), 3))               # -> 0.967

# BIEN: el escalador se ajusta dentro de cada pliegue, con sus 96 filas
print("con pipeline:", round(cross_val_score(make_pipeline(StandardScaler(),
      LogisticRegression()), X, y, cv=5).mean(), 3))                        # -> 0.975

# Un pipeline con nombre en cada paso se lee y se depura mucho mejor
modelo = Pipeline([
    ("imputar", SimpleImputer(strategy="median")),   # primero los nulos
    ("escalar", StandardScaler()),                   # luego la escala
    ("reducir", PCA(n_components=2)),                # luego la dimension
    ("modelo", RandomForestClassifier(n_estimators=50, random_state=0)),
]).fit(X, y)
# steps es una lista de tuplas (nombre, objeto): se recorre con dos variables, no con una
print("pasos:", [nombre for nombre, _ in modelo.steps])   # -> ['imputar', 'escalar', 'reducir', 'modelo']
print("accuracy en entrenamiento:", round(modelo.score(X, y), 3))   # -> 1.0
