import numpy as np
from sklearn.ensemble import IsolationForest

# Isolation Forest: no supone ninguna distribucion, aisla con cortes aleatorios.
rng = np.random.default_rng(3)
datos = np.vstack([rng.normal(0.0, 1.0, size=(200, 2)), [[6.0, 6.0], [-7.0, 5.0]]])

bosque = IsolationForest(n_estimators=100, random_state=0).fit(datos)
puntuacion = bosque.score_samples(datos)          # mas negativo = mas raro

print("los 4 mas raros:", np.argsort(puntuacion)[:4].tolist())        # -> [200, 201, 0, 168]
print("puntuacion mediana:", round(float(np.median(puntuacion)), 3))  # -> -0.398
print("marca con contamination=0.02:", int((bosque.set_params(contamination=0.02).fit_predict(datos) == -1).sum()))  # -> 5
print("marca con contamination=0.10:", int((bosque.set_params(contamination=0.10).fit_predict(datos) == -1).sum()))  # -> 21
